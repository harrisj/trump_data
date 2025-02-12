from bs4 import BeautifulSoup
from bs4.element import Tag
import re
import canonicaljson
import dateparser
import requests
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, AnyHttpUrl

JUST_SECURITY_URL = "https://www.justsecurity.org/107087/tracker-litigation-legal-challenges-trump-administration/"


class Link(BaseModel):
    url: AnyHttpUrl
    title: str


# for the future, I might break out Case Updates as a separate type
# class CaseUpdate(BaseModel):
#    title: str = None
#    text: str
#    links: List[Link]


class Case(BaseModel):
    case_name: str
    case_link: Link
    complaint_link_text: Optional[str] = None
    complaint_link: Optional[Link] = None
    date_filed: date
    case_summary: str
    case_summary_html: str
    last_update: date


class ExecutiveAction(BaseModel):
    title: str
    links: List[Link]
    cases: List[Case]


class Category(BaseModel):
    title: str
    exec_actions: List[ExecutiveAction]


class LitigationTracker(BaseModel):
    last_updated: date
    categories: List[Category]


class LitigationParser:
    def parse_link(tag: Tag) -> Link:
        assert tag.name == "a", f"Tag Name {tag.name} unexpected for a link parser"
        return Link(url=tag["href"], title=tag.string)

    def parse_category(tag: Tag) -> Category:
        col = tag.find("td", class_="column-1")
        assert col is not None, "No category found"

        return Category(title=col.text, exec_actions=[])

    def parse_exec_action(tag: Tag) -> ExecutiveAction:
        col = tag.find("td", class_="column-2")
        assert col is not None, "No exec action found"

        links = [Link(url=a["href"], title=a.string) for a in col.find_all("a")]
        title = col.text.replace("Executive Action: ", "").strip()
        return ExecutiveAction(title=title, links=links, cases=[])

    def parse_case(tag: Tag) -> Case:
        col = tag.find("td", class_="column-3")
        assert col is not None

        case_name = re.sub(r"\n+", " ", col.text).strip()
        case_link = Link(url=col.a["href"], title=col.a.text)

        complaint_link_text = None
        complaint_link = None
        col = tag.find("td", class_="column-4")
        if col is not None:
            complaint_link_text = col.text
            a = col.find("a")
            if a is not None:
                complaint_link = Link(url=a["href"], title=a.string)

        date_filed = None
        col = tag.find("td", class_="column-5")
        if col is not None:
            date_filed = dateparser.parse(col.string)

        case_summary = None
        case_summary_html = None
        col = tag.find("td", class_="column-6")
        if col is not None:
            case_summary = col.text
            case_summary_html = col.decode_contents()

        last_update = None
        col = tag.find("td", class_="column-7")
        if col is not None:
            last_update = dateparser.parse(col.string)

        return Case(
            case_name=case_name,
            case_link=case_link,
            complaint_link=complaint_link,
            complaint_link_text=complaint_link_text,
            date_filed=date_filed,
            case_summary=case_summary,
            case_summary_html=case_summary_html,
            last_update=last_update,
        )

    def parse_litigation_tracker(html: str) -> LitigationTracker:
        doc = BeautifulSoup(html, "html.parser")

        last_updated_span = doc.find("span", string="Last updated")
        last_updated_el = last_updated_span.next_sibling
        last_updated = dateparser.parse(last_updated_el.text)

        categories = []
        last_category = None
        last_exec_action = None

        tbody = doc.find("tbody")
        assert tbody is not None, "No tbody found"

        for tr in tbody.find_all("tr"):
            category = LitigationParser.parse_category(tr)

            if category != last_category:
                categories.append(category)
                last_category = category

            exec_action = LitigationParser.parse_exec_action(tr)
            if exec_action != last_exec_action:
                last_category.exec_actions.append(exec_action)
                last_exec_action = exec_action

            case = LitigationParser.parse_case(tr)
            last_exec_action.cases.append(case)

        return LitigationTracker(last_updated=last_updated, categories=categories)


if __name__ == "__main__":
    response = requests.get(JUST_SECURITY_URL)
    tracker = LitigationParser.parse_litigation_tracker(response.text)
    canonical_json = canonicaljson.encode_pretty_printed_json(tracker.model_dump(mode="json"))
    print(str(canonical_json, "utf-8"))

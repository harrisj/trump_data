import pytest
from bs4 import BeautifulSoup
from scrape_eo_lawsuits import LitigationParser

TEST_HTML_ROW = """<tr class="row-4">
	<td class="column-1">Immigration and Citizenship</td><td class="column-2"><strong>Executive Action: Birthright Citizenship (<a href="https://www.federalregister.gov/documents/2025/01/29/2025-02007/protecting-the-meaning-and-value-of-american-citizenship"><u>Executive Order 14160</u></a>)</strong></td><td class="column-3"><a href="https://www.courtlistener.com/docket/69561497/state-of-new-jersey-v-trump/"><em><u>State of New Jersey et al v. Donald J. Trump et al</u></em></a> (D. Mass.)<br />
<br />
Case No. 1:25-cv-10139</td><td class="column-4"><a href="https://storage.courtlistener.com/recap/gov.uscourts.mad.279895/gov.uscourts.mad.279895.1.0_1.pdf"><u>Complaint</u></a></td><td class="column-5">Jan. 21, 2025</td><td class="column-6">Trump’s executive order seeks to revoke birthright citizenship for the children of undocumented immigrants on the basis that people in the United States illegally are not “subject to the jurisdiction thereof.” The attorneys general of 22 states, the District of Columbia, and the City of San Francisco sued to protect residents who would lose their citizenship under the executive order. The suit argues that the plain text of the 14th Amendment, as confirmed in U.S. v. Wong Kim Ark (1898), explicitly grants birthright citizenship for all people born in the United States.</td><td class="column-7">2025-01-31</td>
</tr>"""


class TestParsing:
    def test_parse_link_normal(self):
        doc = BeautifulSoup(
            '<a href="https://www.courtlistener.com/docket/69560542/new-hampshire-indonesian-community-support-v-trump/"><em><u>New Hampshire Indonesian Community Support v. Donald J. Trump</u></em></a>',
            "html.parser",
        )
        link = LitigationParser.parse_link(doc.a)

        assert (
            str(link.url)
            == "https://www.courtlistener.com/docket/69560542/new-hampshire-indonesian-community-support-v-trump/"
        )
        assert (
            str(link.title)
            == "New Hampshire Indonesian Community Support v. Donald J. Trump"
        )

    def test_parse_category(self):
        doc = BeautifulSoup(TEST_HTML_ROW, "html.parser")
        category = LitigationParser.parse_category(doc.tr)

        assert category.title == "Immigration and Citizenship"
        assert category.exec_actions == []

    def test_parse_exec_action(self):
        doc = BeautifulSoup(TEST_HTML_ROW, "html.parser")
        exec_action = LitigationParser.parse_exec_action(doc.tr)

        assert exec_action.title == "Birthright Citizenship (Executive Order 14160)"
        assert len(exec_action.links) == 1
        assert (
            str(exec_action.links[0].url)
            == "https://www.federalregister.gov/documents/2025/01/29/2025-02007/protecting-the-meaning-and-value-of-american-citizenship"
        )
        assert exec_action.links[0].title == "Executive Order 14160"
        assert exec_action.cases == []

    def test_parse_case(self):
        doc = BeautifulSoup(TEST_HTML_ROW, "html.parser")
        case = LitigationParser.parse_case(doc.tr)

        # <td class="column-3"><a href="https://www.courtlistener.com/docket/69561497/state-of-new-jersey-v-trump/"><em><u>State of New Jersey et al v. Donald J. Trump et al</u></em></a> (D. Mass.)<br />
        # <br />
        # Case No. 1:25-cv-10139</td><td class="column-4"><a href="https://storage.courtlistener.com/recap/gov.uscourts.mad.279895/gov.uscourts.mad.279895.1.0_1.pdf"><u>Complaint</u></a></td><td class="column-5">Jan. 21, 2025</td><td class="column-6">Trump’s executive order seeks to revoke birthright citizenship for the children of undocumented immigrants on the basis that people in the United States illegally are not “subject to the jurisdiction thereof.” The attorneys general of 22 states, the District of Columbia, and the City of San Francisco sued to protect residents who would lose their citizenship under the executive order. The suit argues that the plain text of the 14th Amendment, as confirmed in U.S. v. Wong Kim Ark (1898), explicitly grants birthright citizenship for all people born in the United States.</td><td class="column-7">2025-01-31</td>
        # </tr>"""

        assert (
            case.case_name
            == "State of New Jersey et al v. Donald J. Trump et al (D. Mass.) Case No. 1:25-cv-10139"
        )
        assert (
            str(case.case_link.url)
            == "https://www.courtlistener.com/docket/69561497/state-of-new-jersey-v-trump/"
        )
        assert (
            case.case_link.title == "State of New Jersey et al v. Donald J. Trump et al"
        )
        assert (
            str(case.complaint_link.url)
            == "https://storage.courtlistener.com/recap/gov.uscourts.mad.279895/gov.uscourts.mad.279895.1.0_1.pdf"
        )
        assert case.complaint_link.title == "Complaint"
        assert case.complaint_link_text == 'Complaint'
        assert case.date_filed.isoformat() == "2025-01-21"
        assert (
            case.case_summary
            == """Trump’s executive order seeks to revoke birthright citizenship for the children of undocumented immigrants on the basis that people in the United States illegally are not “subject to the jurisdiction thereof.” The attorneys general of 22 states, the District of Columbia, and the City of San Francisco sued to protect residents who would lose their citizenship under the executive order. The suit argues that the plain text of the 14th Amendment, as confirmed in U.S. v. Wong Kim Ark (1898), explicitly grants birthright citizenship for all people born in the United States."""
        )
        assert (
            case.case_summary_html
            == """Trump’s executive order seeks to revoke birthright citizenship for the children of undocumented immigrants on the basis that people in the United States illegally are not “subject to the jurisdiction thereof.” The attorneys general of 22 states, the District of Columbia, and the City of San Francisco sued to protect residents who would lose their citizenship under the executive order. The suit argues that the plain text of the 14th Amendment, as confirmed in U.S. v. Wong Kim Ark (1898), explicitly grants birthright citizenship for all people born in the United States."""
        )
        assert case.last_update.isoformat() == "2025-01-31"

    def test_parse_litigation_tracker(self):
        with open("./jt_sample_page.html", "r") as f:
            html = f.read()

        tracker = LitigationParser.parse_litigation_tracker(html)
        assert tracker.last_updated.isoformat() == "2025-02-11"
        assert len(tracker.categories) == 7

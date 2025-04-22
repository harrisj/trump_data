"""Utility methods"""

import re
import yaml
from typing import Any, List, Union, Dict
from edtf import parse_edtf
from edtf.parser.parser_classes import EDTFObject, UncertainOrApproximate


def edtf_representer(dumper, data):
    return dumper.represent_scalar("!edtf", "%s" % data)


yaml.add_representer(UncertainOrApproximate, edtf_representer)


def edtf_constructor(loader, node):
    value = loader.construct_scalar(node)
    return parse_edtf(str(value))


yaml.add_constructor("!edtf", edtf_constructor)

pattern = re.compile(r"^(2024|2025)-\d{2}-\d{2}(~?)$")
yaml.add_implicit_resolver("!edtf", pattern)


def read_yaml(file_path: str) -> Any:
    with open(file_path, "r") as file:
        return yaml.full_load(file)


def read_yaml_as_dict(file_path: str, key_field: str) -> Dict[str, Any]:
    raw_yaml = read_yaml(file_path)
    assert isinstance(raw_yaml, list)

    out = {}
    for item in raw_yaml:
        key = item[key_field]
        out[key] = item

    return out


def as_list(l: Union[str, List[str]]) -> List[str]:
    if isinstance(l, str):
        return [l]
    else:
        return l


def sorted_by_last_name(l: Any) -> List:
    out = list(l)

    return sorted(out, key=lambda x: x.split()[-1])


# Probably a smarter way to do this, but I don't care
def create_dumper(line_break_indent: int) -> yaml.SafeDumper:
    class MyYamlDumper(yaml.Dumper):
        def ignore_aliases(self, data):
            return True

        # HACK: insert blank lines between top-level objects
        # inspired by https://stackoverflow.com/a/44284819/3786245
        def write_line_break(self, data=None):
            super().write_line_break(data)

            if len(self.indents) == line_break_indent:
                super().write_line_break()

    return MyYamlDumper


class MyYamlDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True

    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def read_raw_events(path="./it_modernization/raw_data/events.yaml"):
    return read_yaml(path)


def read_processed_events():
    yaml = read_yaml("./it_modernization/events.yaml")
    return yaml["events"]


def read_raw_cases(path="./it_modernization/raw_data/cases.yaml"):
    return read_yaml(path)


def read_raw_systems(path="./it_modernization/raw_data/systems.yaml"):
    return read_yaml(path)


def read_raw_cases_dict(path="./it_modernization/raw_data/cases.yaml"):
    return read_yaml_as_dict(path, "case_no")


def read_raw_systems_dict(path="./it_modernization/raw_data/systems.yaml"):
    return read_yaml_as_dict(path, "id")


def read_raw_agencies(path="./it_modernization/raw_data/agencies.yaml"):
    return read_yaml(path)


def read_raw_agencies_dict(path="./it_modernization/raw_data/agencies.yaml"):
    return read_yaml_as_dict(path, "id")


def read_raw_aliases_dict(path="./it_modernization/raw_data/aliases.yaml"):
    return read_yaml_as_dict(path, "id")


def read_raw_details(path="./it_modernization/raw_data/details.yaml"):
    return read_yaml(path)


def read_raw_details_dict(path="./it_modernization/raw_data/details.yaml"):
    return read_yaml_as_dict(path, "id")


def read_raw_roundups(path="./it_modernization/raw_data/roundups.yaml"):
    return read_yaml(path)


def read_postings(path="./it_modernization/postings.yaml"):
    out = read_yaml(path)
    return out["postings"]


def dump_generated_file(meta, data, path, schema=None, line_break_indent=100):
    with open(path, "w") as file:
        if schema is not None:
            file.write(f"# yaml-language-server: $schema={schema}\n")

        file.write(yaml.dump({"meta": meta}, indent=2, width=120, sort_keys=False))
        file.write("\n")
        file.write(
            yaml.dump(
                data,
                Dumper=create_dumper(line_break_indent),
                indent=2,
                width=120,
                sort_keys=False,
                default_flow_style=False,
            )
        )

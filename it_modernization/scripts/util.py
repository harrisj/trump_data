'''Utility methods'''
import yaml
from typing import Any, List, Union, Dict

def read_yaml(file_path:str) -> Any:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def read_yaml_as_dict(file_path:str, key_field: str) -> Dict[str, Any]:
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

    return sorted(out, key=lambda x: x.split()[-1] )

# Probably a smarter way to do this, but I don't care
def create_dumper(line_break_indent: int) -> yaml.SafeDumper:
    class MyYamlDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

        # HACK: insert blank lines between top-level objects
        # inspired by https://stackoverflow.com/a/44284819/3786245
        def write_line_break(self, data=None):
            super().write_line_break(data)

            if len(self.indents) == line_break_indent:
                super().write_line_break()
    
    return MyYamlDumper

class MyYamlDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


def read_raw_events(path = './raw_data/events.yaml'):
    return read_yaml(path)

def read_processed_events():
    yaml = read_yaml("./events.yaml")
    return yaml["events"]

def read_raw_cases_dict(path = './raw_data/cases.yaml'):
    return read_yaml_as_dict(path, "case_no")

def read_raw_agencies_dict(path = './raw_data/agencies.yaml'):
    return read_yaml_as_dict(path, "id")

def read_raw_aliases_dict(path = './raw_data/aliases.yaml'):
    return read_yaml_as_dict(path, "id")

def read_raw_details(path = './raw_data/details.yaml'):
    return read_yaml(path)

def read_raw_details_dict(path = './raw_data/details.yaml'):
    return read_yaml_as_dict(path, 'id')

def read_raw_roundups(path = './raw_data/roundups.yaml'):
    return read_yaml(path)

def dump_generated_file(meta, data, path, schema=None):
    with open(path, 'w') as file:
        if schema is not None:
            file.write(f"# yaml-language-server: $schema={schema}\n")

        file.write(yaml.dump({"meta": meta}, indent=2, width=1000, sort_keys=False))
        file.write("\n")
        file.write(yaml.dump(data, Dumper=create_dumper(2), indent=2, width=1000, sort_keys=False))            

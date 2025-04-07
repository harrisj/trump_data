'''Utility methods'''
import yaml
from typing import Any, List, Union

def read_yaml(file_path:str) -> Any:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
def as_list(l: Union[str, List[str]]) -> List[str]:
    if isinstance(l, str):
        return [l]
    else:
        return l
    
def sorted_by_last_name(l: Any) -> List:
    out = list(l)

    return sorted(out, key=lambda x: x.split()[-1] )

class MyYamlDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


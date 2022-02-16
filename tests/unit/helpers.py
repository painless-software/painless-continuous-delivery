"""
Common helper functions and values for running tests with py.test.
"""

from difflib import context_diff
from pathlib import Path
from textwrap import dedent, indent


def pytest_generate_tests(metafunc):
    """
    A test scenarios implementation for py.test, as found at
    https://docs.pytest.org/en/latest/example/parametrize.html
    #a-quick-port-of-testscenarios.  Picks up a ``scenarios`` class variable
    to parametrize all test function calls.
    """
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


def indent2(text):
    """Remove common indentation and ensure a specific indentation"""
    return indent(dedent(text), 2 * ' ')


def get_lines_for(identifier, module_lines, block_type):
    """
    Extract a Python value definition (list, tuple, dict) in Python code
    (such as the settings file), and return its content as a list of strings.
    Return an empty list if not found.
    """
    delimiters_for = {
        str: ('', '\n'),
        list: ('[', ']'),
        tuple: ('(', ')'),
        dict: ('{', '}'),
    }
    start_symbol, stop_symbol = delimiters_for[block_type]

    try:
        start = module_lines.index(f'{identifier} = {start_symbol}')
        stop = module_lines.index(stop_symbol, start)
        value_lines = module_lines[start:stop + 1]
        return [line.strip() for line in value_lines]
    except ValueError:
        return []


def not_found_pretty(needle, lines):
    """
    Returns a pretty-print assert message.
    """
    return 'Not found in settings: %(needle)s\n' \
           '---------------\n' \
           '%(lines)s' % {
               'needle': needle,
               'lines': '\n'.join(lines)
           }


class FunctionCall:
    """Mimics a class method call for testing settings"""
    def __init__(self, name, end=''):
        self.func = name
        self.end = end
        self.body = ''

    def __call__(self, *body_text):
        new = FunctionCall(self.func, self.end)

        new.body = '\n'
        for line in body_text:
            new.body += f'{line}\n'
        return new

    def __str__(self):
        return '%(func)s(%(body)s)%(end)s' % self.__dict__


def verify_required_settings(required_settings, settings):
    """
    Assert that the required settings are included in the generated ones.
    """
    for key, value in required_settings.items():
        if isinstance(value, (str, FunctionCall)):
            key_value_pair = f'{key} = {value}'
            assert key_value_pair in settings, \
                not_found_pretty(key_value_pair, settings)
        else:
            lines = get_lines_for(key, settings, block_type=type(value))
            if isinstance(value, dict):
                for dict_key, dict_value in value.items():
                    key_value_pair = f"'{dict_key}': {dict_value},"
                    key_val_lines = key_value_pair.splitlines()
                    intersection = [_ for _ in key_val_lines if _ in lines]
                    assert intersection == key_val_lines, \
                        not_found_pretty(key_value_pair, lines)
            else:  # list or tuple
                for item in value:
                    assert item in lines, \
                        not_found_pretty(item, lines)


def verify_file_matches_repo_root(result, *file, max_compare_bytes=-1):
    """
    Assert that a generated file matches the one with the identical name in
    the project repository root.
    """
    repo_root_path = Path(__file__).parent.parent.parent
    mother_file = repo_root_path.joinpath(*file)
    mother_content = mother_file.read_text()[:max_compare_bytes]

    generated_file = result.project_path.joinpath(*file)
    generated_content = generated_file.read_text()[:max_compare_bytes]

    diff = ''.join(
        context_diff(
            mother_content.splitlines(),
            generated_content.splitlines(),
            fromfile=str(mother_file),
            tofile=str(generated_file),
        )
    )
    assert not diff, \
        f"Mother project '{Path(*file)}' not matching template.\n" \
        f"{diff}"

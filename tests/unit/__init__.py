"""Common helper functions and values for running tests with py.test."""
from os.path import dirname
from py._path.local import LocalPath

REPO_ROOT_PATH = LocalPath(dirname(dirname(dirname(__file__))))


def pytest_generate_tests(metafunc):
    """
    A test scenarios implementation for py.test, as found at
    http://docs.pytest.org/en/latest/example/parametrize.html
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
        start = module_lines.index('%s = %s' % (identifier, start_symbol))
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


def verify_required_settings(required_settings, settings):
    """
    Assert that the required settings are included in the generated ones.
    """
    for key, value in required_settings.items():
        if isinstance(value, str):
            key_value_pair = '%s = %s' % (key, value)
            assert key_value_pair in settings, \
                not_found_pretty(key_value_pair, settings)
        else:
            lines = get_lines_for(key, settings, block_type=type(value))
            if isinstance(value, dict):
                for dict_key, dict_value in value.items():
                    key_value_pair = "'%s': %s," % (dict_key, dict_value)
                    assert key_value_pair in lines, \
                        not_found_pretty(key_value_pair, lines)
            else:  # list or tuple
                for item in value:
                    assert item in lines, \
                        not_found_pretty(item, lines)

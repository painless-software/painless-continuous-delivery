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


def slice_dict_from(dict_name, thelist):
    """
    Extract a Python dict definition in Python code such as the settings file
    read as a list of strings.  Return an empty list if not found.
    """
    try:
        start = thelist.index('%s = {' % dict_name)
        stop = thelist.index('}', start)
        dict_lines = thelist[start:stop + 1]
        return [line.strip() for line in dict_lines]
    except ValueError:
        return []

import pytest
from tempfile import NamedTemporaryFile
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError
from jinja2_workarounds import MultiLineInclude


@pytest.fixture
def environment():
    yield Environment(loader=FileSystemLoader('./tests/templates'), extensions=[MultiLineInclude])


def test_include_with_whitespace(environment):
    template = environment.get_template("002.j2")
    assert template.render() == "example:\n    hello:\n        world"


def test_trim_blocks(environment):
    template = environment.get_template("003.j2")
    assert template.render() == "example:\n    hello: world"


def test_include_no_leadin(environment):
    template = environment.get_template("no-whitespace.j2")
    assert template.render() == "hello:\n    world"


def test_include_tabbed_leadin(environment):
    template = environment.get_template("tabbed-leadin.j2")
    assert template.render() == "example:\n\t    hello:\n\t        world"


def test_include_bad_leadin(environment):
    with pytest.raises(TemplateSyntaxError) as excinfo:
            template = environment.get_template("bad-leadin.j2")

    assert "line contains non-whitespace characters before include statement" in str(excinfo.value)

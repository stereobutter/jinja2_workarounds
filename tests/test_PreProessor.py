import pytest
from tempfile import NamedTemporaryFile
from jinja2 import Environment, FileSystemLoader
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
import pytest
from tempfile import NamedTemporaryFile
from jinja2 import Environment, FileSystemLoader
from jinja2_better_includes import PreProcessor


@pytest.fixture
def environment():
    yield Environment(loader=FileSystemLoader('./tests/templates'), extensions=[PreProcessor])


def test_include_with_whitespace(environment):
    template = environment.get_template("002.j2")
    assert template.render() == "example:\n    hello:\n        world"

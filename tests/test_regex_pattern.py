import pytest
import re
from jinja2_workarounds import _improved_include_statement


@pytest.mark.parametrize("tags", [("{%", "%}"), ("<<", ">>"), ("|$", "$|")])
@pytest.mark.parametrize("statement",
    [
        '{start} include "foo.txt" indent content {end}', 
        "{start} include 'foo.txt' indent content {end}",
        "{start}include'foo.txt'indent content{end}"
        "{start}  include  ['foo.txt', 'bar.txt'] ignore missing indent content {end}",
        "{start}  include  ['foo.txt', 'bar.txt'] ignore missing indent content with context {end}",
        "     {start}  include  'foo.txt' indent contentn {end}",
        "  ...   {start}  include  'foo.txt' indent content {end} .. ",
        "{start}- include 'foo.txt' indent content +{end}"
    ]
)
def test_regex_matches(tags, statement):
    start, end = tags
    string = statement.format(start=start, end=end)
    assert _improved_include_statement(start, end).search(string)


@pytest.mark.parametrize("tags", [("{%", "%}"), ("<<", ">>"), ("|$", "$|")])
@pytest.mark.parametrize("statement",
    [
        '{start} include "foo.txt" {end}', 
        "{start} include 'foo.txt' {end}",
        "{start} include 'foo.txt' with context{end}"
    ]
)
def test_regex_doesnt_matches(tags, statement):
    start, end = tags
    string = statement.format(start=start, end=end)
    assert not _improved_include_statement(start, end).search(string)

import pytest
import re
from jinja2_better_includes import _include_statement


@pytest.mark.parametrize("tags", [("{%", "%}"), ("<<", ">>"), ("|$", "$|")])
@pytest.mark.parametrize("statement",
    [
        '{start} include "foo.txt" {end}', 
        "{start} include 'foo.txt' {end}",
        "{start}include'foo.txt'{end}"
        "{start}  include  ['foo.txt', 'bar.txt'] ignore missing  {end}",
        "     {start}  include  'foo.txt'  {end}"
        "  foo:   {start}  include  'foo.txt'  {end} bar "
    ]
)
def test_regex_matches(tags, statement):
    start, end = tags
    string = statement.format(start=start, end=end)
    assert _include_statement(start, end).search(string)

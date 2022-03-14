# 🦸‍♂️ Not the solution `jinja2` deserves, but the workaround it needs right now.
`jinja2_workarounds` offers an extension for jinja2 that works around a long standing issue[^1]
where `include` does not preserve correct indentation for multi-line includes. Simply add the
`jinja2_workarounds.MultiLineInclude` [extension to your environment](https://jinja.palletsprojects.com/en/3.0.x/extensions/) and use the `indent content` directive to
correctly indent your multi-line includes.

## Installation
```pip install jinja2_workarounds```


## Usage example
```jinja2
# text.j2
this
is 
some 
text
```

```jinja2
# example.j2
example:
    {% include 'text.j2' indent content %}
```

is then rendered as 

```
example:
    this
    is 
    some 
    text
```

compared to `jinja2`'s default `include` which would result in 

```
example:
    this
is 
some 
text
```

## Advanced features
`MultiLineInclude` is compatible with custom `block_start_string` and `block_end_string`. It also works with 
the advanced features of `jinja2'`s `include` statement. The following variants are all supported and work as
expected

```jinja2
{% include 'missing.j2' ignore missing indent content %}  # handle missing templates
{% include ['foo.j2', 'bar.j2'] indent content %}  # multiple alternative templates
{% include 'child.j2' without context %}  # include child with/without content
{%- include 'child.j2' +%}  # include with custom whitespace control
```

[^1]: https://github.com/pallets/jinja/issues/178
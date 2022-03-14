from jinja2 import Environment, TemplateSyntaxError
from jinja2.ext import Extension
import re


def _improved_include_statement(block_start, block_end):
    return re.compile(fr"""
        (^ .*)  # first group: greedy tokens at the beginning of the line
        (?= # second group: positive lookahead of pattern
            (
                {re.escape(block_start)}
                (?P<block_start_modifier> [\+|-]?)
                (?P<statement>
                    \s* include \b   # include keyword
                    \s*? .*?  # fluff
                    indent \s content  # new 'with indentation' option
                    \s*? .*? # fluff
                )
                (?P<block_end_modifier> [\+|-]?)
                {re.escape(block_end)}
            )
        )
        .* $ # rest of the line, required to also include the lookahead in the match
        """,
        flags=re.MULTILINE|re.VERBOSE)


class MultiLineInclude(Extension):

    def preprocess(self, source, name, filename=None):
        env: Environment = self.environment

        block_start: str = env.block_start_string
        block_end: str = env.block_end_string
        pattern = _improved_include_statement(block_start=block_start, block_end=block_end)
        re_newline = re.compile('\n')

        def add_indentation_filter(match):
            line_content_before_statement = match.group(1)
            statement = match.group('statement').replace('indent content', '')  # strip 'with indentation' directive

            # guard against invalid use of improved include statement
            if line_content_before_statement is not None:
                # line before include statement must be indentation only
                if not line_content_before_statement.isspace():
                    start_position = match.start(0)
                    lineno = len(re_newline.findall(source, 0, start_position)) + 1
                    raise TemplateSyntaxError(
                        "line contains non-whitespace characters before include statement",
                        lineno,
                        name,
                        filename,
                    )

            indentation = line_content_before_statement or ''
            block_start_modifier = match.group('block_start_modifier') or ''
            block_end_modifier = match.group('block_end_modifier') or ''

            start_filter = indentation + f'{block_start + block_start_modifier} filter indent({len(indentation)}) -{block_end}'
            include_statement = indentation + f'{block_start} {statement} {block_end}'
            end_filter = indentation + f'{block_start}- endfilter {block_end_modifier + block_end}'

            return'\n'.join([start_filter, include_statement, end_filter])

        return pattern.sub(add_indentation_filter, source)

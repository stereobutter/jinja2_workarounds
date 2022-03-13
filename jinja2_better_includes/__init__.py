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
                    with \s indentation  # new 'with indentation' option
                    \s*? .*? # fluff
                )
                (?P<block_end_modifier> [\+|-]?)
                {re.escape(block_end)}
            )
        )
        .* $ # rest of the line, required to also include the lookahead in the match
        """,
        flags=re.MULTILINE|re.VERBOSE)


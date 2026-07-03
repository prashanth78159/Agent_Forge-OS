
import re

def tokenize(text):

    tokens = []

    patterns = [

        ("ARROW", r"->"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("COLON", r":"),
        ("COMMA", r","),
        ("STRING", r'"[^"]*"'),
        ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("SKIP", r"[ \t\n]+")
    ]

    combined = "|".join(
        f"(?P<{name}>{pattern})"
        for name, pattern in patterns
    )

    for match in re.finditer(
        combined,
        text
    ):

        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP":
            continue

        tokens.append(
            {
                "type": kind,
                "value": value
            }
        )

    return tokens

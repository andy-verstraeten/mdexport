from ..mdexport.templates import extract_variables


def test_extract_variables():
    DUMMY_HTML_TEMPLATE = """<html>
    <header>{{var1}}</header>
    <body>
    {{body}}
    </body>
    </html>
"""
    assert set(extract_variables(DUMMY_HTML_TEMPLATE)) == {"var1", "body"}

#!/usr/bin/env python

import sys
import difflib
import webbrowser
import functools

PYTHON_DOCS = "https://docs.python.org/3/"
STDLIB_DOCS = "library/"
TYPE_DOCS = STDLIB_DOCS + "stdtypes#"
FUNCTION_DOCS = "library/functions#"
DATA_MODEL_DOCS = "reference/datamodel.html#"
DATA_MODEL_MAIN_DOCS = DATA_MODEL_DOCS + "objects-values-and-types"
GEN_DOCS = "reference/expressions.html#"
GEN_MAIN_DOCS = GEN_DOCS + "asynchronous-generator-iterator-methods"

GEN = type((_ for _ in ()))
async def f(): yield
AGEN = type(f())
del f


def matches(query, pool, default=None):
    matched = difflib.get_close_matches(query, pool, n=1, cutoff=0.8)
    return matched.pop() if matched else default


def parse(head: str, tail: str, possibilities: list, url: str, fallback: str):
    if tail:
        method = matches(tail, possibilities, default=tail)
        return url + head + '.' + method
    else:
        return fallback


def a_type(t):
    """checks if a string represents a built in type, if so, returns the type"""
    builtin = vars(__builtins__).get(t) # maybe None
    # None is not a built in type (NoneType is) so it will fail the following isinstance check
    if isinstance(builtin, type):
        return builtin


def docc(query: str):
    """if a match was found, jumps to the the docs pinned on the match,
    else open up to the site's search with the query.
    Note that if the module's name if either are slightly incorrect,
    you probably will still be redirected to the correct page and tag."""

    base = ["iterator", "container", "generator", "agen", "object", "class", "frame"] + dir(__builtins__)
    modules = sys.stdlib_module_names
    head, _, tail = query.partition('.')
    path = PYTHON_DOCS

    # some form of a builtin
    if res := matches(head, base):
        parse_unique = functools.partial(parse, head=res, tail=tail)

        # most likely an implementable dunder method shit
        if res in ("object", "class", "frame"):
            return PYTHON_DOCS + parse_unique(
                possibilities=dir(object),
                url=DATA_MODEL_DOCS,
                fallback=DATA_MODEL_MAIN_DOCS
            )

        # it's a type
        if builtin := a_type(res) or res in ("iterator", "container"):
            return PYTHON_DOCS + parse_unique(
                possibilities = dir(builtin) if builtin else ["__iter__", "__next__"],
                url=TYPE_DOCS,
                fallback=TYPE_DOCS + res
            )

        # generator or async generator coroutine
        if res in ("generator", "agen"):
            return PYTHON_DOCS + parse_unique(
                possibilities=dir(AGEN) if res == "agen" else dir(GEN),
                url=GEN_DOCS,
                fallback=GEN_MAIN_DOCS
            )

        # just a builtin function
        return PYTHON_DOCS + FUNCTION_DOCS + res

    # stdlib module
    if module := matches(head, modules):
        return PYTHON_DOCS + parse(
            head=module,
            tail=tail,
            possibilities=dir(__import__(module)),
            url=STDLIB_DOCS + module + "#",
            fallback=STDLIB_DOCS + module
        )

    # couldn't find anything
    return PYTHON_DOCS + "search.html?q=" + query


def visit(query):
    url = docc(query)
    print("Opening", url, "in broswer")
    webbrowser.open(url)


if __name__ == '__main__':
    visit(sys.argv[1])

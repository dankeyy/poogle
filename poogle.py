#!/usr/bin/env python

import argparse
import sys
import difflib
import webbrowser
import functools
from typing import Optional, Iterable

PYTHON_DOCS = "https://docs.python.org/3/"
TERM_DOCS = "glossary.html#term-"
STDLIB_DOCS = "library/"
TYPE_DOCS = STDLIB_DOCS + "stdtypes#"
FUNCTION_DOCS = "library/functions#"
DATA_MODEL_DOCS = "reference/datamodel.html#"
DATA_MODEL_MAIN_DOCS = DATA_MODEL_DOCS + "objects-values-and-types"
GEN_DOCS = "reference/expressions.html#"
GEN_MAIN_DOCS = GEN_DOCS + "asynchronous-generator-iterator-methods"

g = (_ for _ in ())
GEN = type(g)
del g

async def ag(): yield
AGEN = type(ag())
del ag


def matches(query: str, pool: Iterable[str], default:str=''):
    matched = difflib.get_close_matches(query, pool, n=1, cutoff=0.7)
    return matched.pop() if matched else default


def parse(head: str, tail: str, possibilities: list, url: str, fallback: str) -> str:
    if tail:
        method = matches(tail, possibilities)

        if method:
            return url + head + '.' + method

    return fallback


def a_type(t: str) -> Optional[list[str]]:
    """checks if a string represents a built in type (or at least an `abstract` one like iterator), if so, returns the type"""

    if t in ("iterator", "container"):
        return ["__iter__", "__next__"]

    builtin = vars(__builtins__).get(t) # maybe None
    # None is not a built in type (NoneType is) so it will fail the following isinstance check
    if isinstance(builtin, type):
        return dir(builtin)


def url_from(query: str) -> str:
    """if a match was found, return url of docs pinned on the match,
    else return url of the site's search with the query in place.
    Note that if the module's name if either are slightly incorrect,
    you probably will still be redirected to the correct page and tag."""

    base = ["iterator", "container", "generator", "agen", "object", "class", "frame"] + dir(__builtins__)
    modules = sys.stdlib_module_names
    head, _, tail = query.partition('.')

    if head == "term":
        return PYTHON_DOCS + TERM_DOCS + tail

    # some form of a builtin
    if res := matches(head, base):
        parse_unique = functools.partial(parse, head=res, tail=tail)

        # most likely an implementable dunder method shit
        if res in ("object", "class", "frame"):
            return PYTHON_DOCS + parse_unique(
                possibilities=dir(object) + ['clear', "__del__", "__bytes__", "__getattr__",
                                             "__get__", "__set__", "__instancecheck__",
                                             "__subclasscheck__", "__set_name__", "__slots__", "__class_getitem__"],
                url=DATA_MODEL_DOCS,
                fallback=DATA_MODEL_MAIN_DOCS
            )

        # it's a type
        if (typemethods := a_type(res)) is not None:
            return PYTHON_DOCS + parse_unique(
                possibilities=typemethods,
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
    """take query, transform it to an actual url via the url_from function,
    then opens a new browser tab with said url"""

    url = url_from(query)
    print("Opening", url, "in broswer")
    webbrowser.open(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Jump to docs.'
                                        'Enter <function/module/whatever>.<method> (e.g `str.split`)'
                                        'or <function/module> (e.g. `getattr`).'
                                        'To look up a term, prefix term as the module- term.<some-python-jargon>, (e.g. `term.garbage-collection`)')
    parser.add_argument('lookup')
    query = parser.parse_args().lookup
    visit(query)

#!/usr/bin/env python

import sys
import difflib
import webbrowser

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



def docc(query: str):
    """if a match was found, jumps to the the docs pinned on the match,
    else open up to the site's search with the query.
    Note that if the module's name if either are slightly incorrect,
    you probably will still be redirected to the correct page and tag."""

    base = ["iterator", "container", "generator", "agen", "object"] + dir(__builtins__)
    modules = sys.stdlib_module_names
    head, _, tail = query.partition('.')
    path = ""

    if res := matches(head, base):
        if res == "object":
            if tail:
                possibilities = dir(object)
                method = matches(tail, possibilities, tail)
                path = DATA_MODEL_DOCS + res + '.' + method
            else:
                path = DATA_MODEL_MAIN_DOCS

        elif isinstance(builtin := vars(__builtins__).get(res), type) or res in ("iterator", "container"):
            if tail:
                possibilities = dir(builtin) if builtin else ("__iter__", "__next__")
                method = matches(tail, possibilities, default=tail)
                path = TYPE_DOCS + res + '.' + method

            else: # no tail, looking for just a built in type (e.g frozenset)
                path = TYPE_DOCS + res


        elif res  == "generator":
            if tail:
                possibilities = dir(GEN)
                method = matches(tail, possibilities, default=tail)
                path = GEN_DOCS + res + '.' + method
            else:
                path = GEN_MAIN_DOCS

        elif res == "agen":
            if tail:
                possibilities = dir(AGEN)
                method = matches(tail, possibilities, default=tail)
                path = GEN_DOCS + res + '.' + method
            else:
                path = GEN_MAIN_DOCS


        else:
            path = FUNCTION_DOCS + res

    elif res := matches(head, modules):
        path = STDLIB_DOCS + res
        if tail:
            function = matches(tail, dir(__import__(res)), default='')
            path = STDLIB_DOCS + res + "#" + res + '.' + function


    # couldn't find anything, just search
    if not path:
        path = "search.html?q=" + query

    return PYTHON_DOCS + path

# path = "library/functions#" + res if not tail else "library/stdtypes#" + query
# path = "library/" + res if not tail else "library/" + res + "#" + res + '.' + matches(tail, dir(__import__(res)), default='')

def visit(query):
    url = docc(query)
    webbrowser.open(url)


if __name__ == '__main__':
    visit(sys.argv[1])

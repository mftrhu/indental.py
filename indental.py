#!/usr/bin/env python3
# -*- coding: utf-8; -*-
"""
indental.py -- parses Indental data

A more-or less straightforward port of the :ref:`Indental` :ref:`JS
parser` to Python, which still manages to be under 50 lines.

It exports the :function:`indental` function, and it wraps it
minimally, as to make calling this script from the command-line
parse its input as Indental to print it back out as JSON.

.. Indental: https://wiki.xxiivv.com/indental
.. JS parser: https://github.com/XXIIVV/Oscean/blob/master/scripts/lib/indental.js
"""
import re

__author__ = "mftrhu"
__version__ = "0.1"
__license__ = "MIT"

def indental(data: str) -> dict:
    """
    Parses the given Indental data.

    Examples
    --------
    >>> import pprint
    >>> h = indental(\"\"\"
    ... NAME
    ...   KEY : VALUE
    ...   LIST
    ...     ITEM 1
    ...     ITEM 2
    ... \"\"\")
    >>> pprint.pprint(h)
    {'NAME': {'KEY': 'VALUE', 'LIST': ['ITEM 1', 'ITEM 2']}}
    """
    def format_line(line: dict) -> list or dict:
        """
        "Formats" each line: goes through its children and returns
        either an array of them, or an hash.

        **Warning:** hashes apparently can't be nested within arrays.
        I am not sure whether this is a bug of this implementation, or
        part of the Indental spec itself.

        """
        a, h = [], {}
        for child_id, child in line["children"].items():
            if child["key"]:
                h[child["key"].upper()] = child["value"]
            elif len(child["children"]) == 0 and child["content"]:
                a.append(child["content"])
            else:
                h[child["content"].upper()] = format_line(child)
        return a if len(a) > 0 else h

    def make_line(line: str) -> dict:
        """
        Parses each line in the file to extract information to be used
        in the parsing of the file as a whole.  Lines can be commented
        out by starting them with ``;``.
        """
        return {
            "indent": re.search(r"\S|$", line).span(0)[0],
            "content": line.strip(),
            "skip": line.strip() == "" or line[0] == ";",
            "key": line.split(" : ")[0].strip() if line.find(" : ") > - 1 else None,
            "value": line.split(" : ")[1].strip() if line.find(" : ") > - 1 else None,
            "children": {}
        }

    # Do not remove `map`, we need to iterate through `lines` twice.
    lines = list(map(make_line, data.split("\n")))

    # Nota bene: no matter what `stack` is called, it is not actually a
    # stack, but it's defined as a JS object (which can be approximated
    # with a Python dictionary).
    stack = {}
    for line in lines:
        if line["skip"]:
            continue
        target = stack.get(line["indent"] - 2)
        if target:
            target["children"][len(target["children"])] = line
        stack[line["indent"]] = line

    # We build the dictionary to be returned.
    h = {}
    for line in lines:
        if line["skip"] or line["indent"] > 0:
            continue
        key = line["content"].upper()
        # This apparently only gets triggered when an upper-level key
        # is redefined, *not* any arbitrary key within some hash.
        if h.get(key):
            print("Warning: Redefined {}".format(key))
        h[key] = format_line(line)

    return h

if __name__ == "__main__":
    import fileinput, json
    data = ""
    for line in fileinput.FileInput():
        data += line
    print(json.dumps(indental(data)))

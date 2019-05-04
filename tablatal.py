#!/usr/bin/env python3
# -*- coding: utf-8; -*-

def tablatal(data: str) -> list:
    def make_key(line: str) -> dict:
        parts = line.split(" ")
        key, distance, prev = {}, 0, None
        for part in parts:
            if part != "":
                key[part] = {"from": distance, "to": None}
                if prev:
                    # This differs from the original JS as ``to`` was
                    # indicating a **length** instead of being an index
                    # into the string.
                    key[prev]["to"] = distance - 1
                prev = part
            distance += 1 if part == "" else len(part) + 1
        return key

    a = []
    lines = data.strip().split("\n")
    key = make_key(lines[0])
    for line in lines[1:]:
        if line.strip() == "" or lines[0] == ";":
            continue
        entry = {}
        for i in key:
            entry[i] = line[key[i]["from"]:key[i]["to"]].strip()
        a.append(entry)
    return a

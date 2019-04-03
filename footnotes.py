#!/usr/bin/env python3


def get_footnote_indices(text):
    footnote_indices = dict()
    open_footnotes = list()

    search_from = 0
    while True:
        opens_at = text.find("@footnote{", search_from)

        if opens_at == -1:
            break

        search_from = opens_at + 10
        # Our footnote text begins 10 chars after the "@"
        open_footnotes.append(search_from)

    # Starting with the last open footnote, look for a closing bracket
    for opens_at in reversed(open_footnotes):
        search_from = opens_at
        while True:
            # print("looking from {}".format(search_from))
            closes_at = text.find("}", search_from)

            if closes_at == -1:
                raise Exception("No closing bracket found for footnote starting at char " + opens_at)

            # If footnotes can be nested, this "}" may already be taken
            if closes_at not in footnote_indices.values():
                footnote_indices[opens_at] = closes_at
                break

            else:
                search_from = closes_at + 1

    return footnote_indices


def extract_footnotes():
    pass

#!/usr/bin/env python3
import sys
import re
import os


def get_tex_tags(text):
    """Returns a dict of {idx_start: (tag_type, idx_end), ...} for tex tags in text."""
    tex_tags = dict()
    open_footnotes = list()
    pattern = re.compile(r"@[a-z]+{")

    for match in pattern.finditer(text):
        open_footnotes.append((match.end(), match.group(0)))

    # Starting with the last open footnote, look for a closing bracket
    for opens_at, tag_type in reversed(open_footnotes):
        search_from = opens_at
        while True:
            # print("looking from {}".format(search_from))
            closes_at = text.find("}", search_from)

            if closes_at == -1:
                raise Exception("No closing bracket found for footnote starting at char " + opens_at)

            # If footnotes can be nested, this "}" may already be taken
            if closes_at not in [x[1] for x in tex_tags.values()]:
                tex_tags[opens_at] = (tag_type, closes_at)
                break

            else:
                search_from = closes_at + 1
    return tex_tags


def get_footnote_indices(text):
    """Returns the start and end indices for all @footnote{}s in the text."""
    return {x: y[1] for x, y in get_tex_tags(text).items() if y[0] == "@footnote{"}


def check_for_nesting(text):
    """Takes the output of get_footnote_indices and checks for nesting."""
    indices = get_footnote_indices(text)
    for key1, value1 in indices.items():
        for key2, value2 in indices.items():
            if key1 == key2 and value1 == value2:
                continue

            elif key1 < key2 and value1 > value2:
                print("nesting found between {} and {}".format(key1, value1))
                return True

    return False


def extract_footnotes(text, footnote_linker):
    """Takes the main text and a function, footnote_linker(link_number), which supplies the link text."""
    if text.find("¡") > -1:
        raise Exception("Need to choose another escape char")

    modified_text = text
    footnotes = dict()
    index = 1

    tex_tags = get_tex_tags(text)

    for dict_key in sorted(tex_tags.keys()):
        tag_type = tex_tags[dict_key][0]
        opens_at = dict_key
        closes_at = tex_tags[dict_key][1]

        if tag_type == "@footnote{":
            footnotes[index] = (tag_type, text[opens_at:closes_at])

            # We want to put a link for the footnote and also some padding so that len(modified_text) is constant
            footnote_link = footnote_linker(index)
            padding = ((closes_at-opens_at)+11) - len(footnote_link)

            if padding < 0:
                raise Exception("links must be shorter than the footnote they replace")

            index += 1

            modified_text = modified_text[:opens_at-10] + footnote_link + "¡" * padding + modified_text[closes_at+1:]
  
    modified_text = modified_text.replace("¡", "")
    return modified_text, footnotes


def move_footnotes_to_end(text, chapter, first_footnote_number):
    if not text.endswith("{{footnotes}}\n@@\n"):
        raise Exception("Cannot find footnote section: " + text[-20:])

    def foonote_linker(link_number):
        this_link = link_number - 1 + first_footnote_number

        return '<a id="footnote_link_{0}-{1}" class="footnote_link" href="#footnote_{0}-{1}">{1}</a>'.\
            format(chapter, this_link)

    modified_text, footnotes = extract_footnotes(text, foonote_linker)

    def footnote_maker(link_number, link_text):
        this_link = link_number - 1 + first_footnote_number
        return '<div id="footnote_{0}-{1}" class="footnote">' \
               '<p> <a href="#footnote_link_{0}-{1}" class="footnote_backlink">{1}</a>'.format(chapter, this_link) + \
               link_text + "</p></div>"

    for dict_key in sorted(footnotes.keys()):
        modified_text = modified_text[:-3] + footnote_maker(dict_key, footnotes[dict_key][1]) + "\n@@\n"

    return modified_text


if __name__ == "__main__":
    if sys.argv[1] == "checknesting":
        for input_filename in os.listdir(path="content"):
            with open(os.path.join("content", input_filename), "r", encoding="utf8") as input_file:
                print("Checking {}".format(os.path.join("content", input_filename)))
                print("nesting found: {}".format(check_for_nesting(input_file.read())))
                print(" ")
                # There doesn't appear to be any nesting so that's one less thing to think about.

    elif sys.argv[1] == "extract":
        with open(sys.argv[2], "r", encoding="utf-8") as input_file:
            data = input_file.read().replace('\n', '')

            for key, value in extract_footnotes(data)[1].items():
                print("{} : {}".format(key, value[1]))
                # assert value[1][-1] in (".", ")")

    elif sys.argv[1] == "move":
        with open(sys.argv[2], "r", encoding="utf-8") as input_file:
            data = input_file.read()

            with open(sys.argv[2][:-12]+"footnote.content.html", "w", encoding="utf-8") as output_file:
                modified_data = move_footnotes_to_end(data, 3, 34)
                output_file.write(modified_data)

    else:
        print("command not recognised")

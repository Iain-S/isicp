#!/usr/bin/env python
from __future__ import print_function
import sys
import re

tag_re = re.compile(
    r"^({{[\w@]+}})$"  # ()Capture {{Tag}} word,
    r"(.*?)"  # then ()capture characters until
    r"^@@$",  # terminating "@@" line.
    flags=re.DOTALL | re.MULTILINE)  # '.' includes '\n' | '^' and '$' are per line.


def get_tagged_content(file_path):
    with open(file_path, mode="r", encoding="utf8") as content:
        tag_content = dict(re.findall(tag_re, ''.join(content.readlines())))
        return tag_content


def write_output(tagged_content, output_function):
    with open("template.html", mode="r", encoding="utf8") as template:
        for line in template.readlines():
            output_function(tagged_content.get(line.strip(), line))


if __name__ == "__main__":
    write_output(get_tagged_content(sys.argv[1]), print)

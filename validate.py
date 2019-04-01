#!/usr/bin/env python3
""" This is taken from the w3c_validator package, which would not install for some reason. """
import requests
import logging
import tempfile
import os

LOGGER = logging.getLogger(__name__)
HTML_VALIDATOR_URL = "http://validator.w3.org/nu/?out=json"


def validate(filename, verbose=False):
    """
    Validate file and return JSON result as dictionary.
    "filename" can be a file name or an HTTP URL.
    Return "" if the validator does not return valid JSON.
    Raise OSError if curl command returns an error status.
    """
    # is_css = filename.endswith(".css")

    is_remote = filename.startswith("http://") or filename.startswith(
        "https://")
    with tempfile.TemporaryFile() if is_remote else open(
            filename, "rb") as f:

        if is_remote:
            r = requests.get(filename, verify=False)
            f.write(r.content)
            f.seek(0)

        # if is_css:
        #     cmd = (
        #         "curl -sF \"file=@%s;type=text/css\" -F output=json -F warning=0 %s"
        #         % (quoted_filename, CSS_VALIDATOR_URL))
        #     _ = cmd
        # else:
        r = requests.post(
            HTML_VALIDATOR_URL,
            files={"file": (filename, f, "text/html")},
            data={
                "out": "json",
                "showsource": "yes",
            },
            verify=False)

    return r.json()


all_messages = dict()
for file_name in os.listdir("."):
    if file_name.endswith(".html") and file_name[0] in ["4"]:
        print("Processing " + file_name)
        messages = validate(file_name)["messages"]
        for m in messages:
            if not (m["message"].startswith("An “img” element must have an “alt” attribute") or
                    m["message"].startswith("The “name” attribute is obsolete")):
                # print("Type: %(type)s, Line: %(lastLine)d, Description: %(message)s" % m)
                if m["message"] in all_messages:
                    all_messages[m["message"]] = all_messages[m["message"]] + 1
                else:
                    all_messages[m["message"]] = 1

for tup in sorted(all_messages.items(), key=lambda k: k[1], reverse=True):
    print("{}: {}".format(tup[0], tup[1]))

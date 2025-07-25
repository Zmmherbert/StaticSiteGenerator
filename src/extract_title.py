import re

def extract_title(markdown):
    for line in markdown.split("\n"):
        if re.match(r"^# .*", line):
            return line[1:].strip()
    raise Exception("No title header found")
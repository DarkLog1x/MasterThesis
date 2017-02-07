#!/usr/bin/python

import subprocess
import sys
thesis = "thesis"
commands = [
    ['pdflatex', thesis + '.tex'],
    ['bibtex', thesis + '.aux'],
    ['pdflatex', thesis + '.tex'],
    ['pdflatex', thesis + '.tex']
]

for c in commands:
    subprocess.call(c)

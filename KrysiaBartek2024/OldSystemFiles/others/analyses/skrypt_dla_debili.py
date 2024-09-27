"""
This script modifies a .tex file so that after conversion to .pdf and .docx,
bridge symbols can be easily inserted.
The input file is provided as an argument.
Output files:
  - to_docx.tex
  - to_docx.pdf (created using lualatex)
"""

import sys
import subprocess

if len(sys.argv) != 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('to_docx.tex', 'w', encoding='utf-8') as f:
    i = 0
    while i < len(lines):
        line = lines[i]

        # Comment out lines starting with '\vspace{-'
        if line.startswith('\\vspace{-'):
            f.write(f'% {line}')
            i += 1
            continue

        # Replace bridge symbols with their full representations
        line = line.replace('\\spades\\', '!s!')
        line = line.replace('\\clubs\\', '!c!')
        line = line.replace('\\hearts\\', '!h!')
        line = line.replace('\\diams\\', '!d!')
        line = line.replace('\\major\\', 'M')
        line = line.replace('\\minor\\', 'm')
        line = line.replace('\\nt\\', 'NT')
        line = line.replace('\\ntx\\', 'NT')

        line = line.replace('\\xspades', '!s!')
        line = line.replace('\\xclubs', '!c!')
        line = line.replace('\\xhearts', '!h!')
        line = line.replace('\\xdiams', '!d!')

        line = line.replace('\\spades', '!s!')
        line = line.replace('\\clubs', '!c!')
        line = line.replace('\\hearts', '!h!')
        line = line.replace('\\diams', '!d!')
        line = line.replace('\\major', 'M')
        line = line.replace('\\minor', 'm')
        line = line.replace('\\nt', 'NT')
        line = line.replace('\\ntx', 'NT')

        # Remove section headers
        if line.startswith('\\section*'):
            line = line.replace('\\section*', '\\textbf{')
            # add '}' at the end of the line
            line = line + '}'


        # If a line starts with \handdiagramv, comment out that line and the next 4
        if line.startswith('\\handdiagramv'):
            f.write(f'% {line}')
            for j in range(1, 6):
                f.write(f'% {lines[i + j]}')
            i += 6
        else:
            f.write(line)
            i += 1

subprocess.run(['lualatex', 'to_docx.tex'], check=True)

print("Conversion complete.")

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

        if line.startswith('\\title{'):
            f.write('\\usepackage{fancyhdr}\n')
            f.write('\\pagestyle{fancy}\n')
            f.write('\\rhead{Żaczek 25.09.24, Krysia \\& Bartek\\\\}\n')

        # Skip lines starting with '\vspace{-'
        if line.startswith('\\vspace{-'):
            i += 1
            continue

        # Replace bridge symbols with their full representations
        line = line.replace('\\spades\\', '{\\color{blue}!s!}')
        line = line.replace('\\clubs\\', '{\\color{OliveGreen}!c!}')
        line = line.replace('\\hearts\\', '{\\color{Maroon}!h!}')
        line = line.replace('\\diams\\', '{\\color{BurntOrange}!d!}')
        line = line.replace('\\major\\', 'M')
        line = line.replace('\\minor\\', 'm')
        line = line.replace('\\ntx\\', '{\\footnotesize{NT}}')
        line = line.replace('\\nt\\', '{\\footnotesize{NT}}')

        line = line.replace('\\xspades', '{\\color{blue}!s!}')
        line = line.replace('\\xclubs', '{\\color{OliveGreen}!c!}')
        line = line.replace('\\xhearts', '{\\color{Maroon}!h!}')
        line = line.replace('\\xdiams', '{\\color{BurntOrange}!d!}')

        line = line.replace('\\spades', '{\\color{blue}!s!}')
        line = line.replace('\\clubs', '{\\color{OliveGreen}!c!}')
        line = line.replace('\\hearts', '{\\color{Maroon}!h!}')
        line = line.replace('\\diams', '{\\color{BurntOrange}!d!}')
        line = line.replace('\\major', 'M')
        line = line.replace('\\minor', 'm')
        line = line.replace('\\ntx', '{\\footnotesize{NT}}')
        line = line.replace('\\nt', '{\\footnotesize{NT}}')

        line = line.replace('\\pagebreak', '\\newpage\n')

        # Remove section headers
        if line.startswith('\\section*'):
            line = line.replace('\\section*{', '\n\n')
            line = line[:-2] + '\n\n'

        # Skip \handdiagramv and the next 4 lines
        if line.startswith('\\handdiagramv'):
            i += 6
            continue

        # Write the modified line
        f.write(line)
        i += 1

subprocess.run(['lualatex', 'to_docx.tex'], check=True)
subprocess.run(['rm', 'to_docx.aux', 'to_docx.log'], check=True)

print("Conversion complete.")

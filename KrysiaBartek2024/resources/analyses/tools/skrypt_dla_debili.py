"""
This script is used to convert a .tex file to a .pdf file, with some modifications.
"""

import sys
import subprocess
import os

if len(sys.argv) != 2:
    print("Usage: python skrypt_dla_debili.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

OUTPUT_DIR = './tmp'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Full paths for input and output files
input_file = filename
output_tex_file = os.path.join(OUTPUT_DIR, 'to_docx.tex')
output_pdf_file = os.path.join(OUTPUT_DIR, 'to_docx.pdf')

# Read the input file
with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Write the modified content to the output .tex file
with open(output_tex_file, 'w', encoding='utf-8') as f:
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith('\\import{../../lib/}{bridge.sty}'):
            f.write('\\import{../../../lib/}{bridge.sty}\n')
            i += 1
            continue

        if line.startswith('\\title{'):
            f.write('\\usepackage{fancyhdr}\n')
            f.write('\\pagestyle{fancy}\n')
            f.write('\\rhead{Żaczek 30.09.24, Krysia \\& Bartek\\\\}\n\n')

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

        line = line.replace('\\xspades ', '{\\color{blue}!s!}')
        line = line.replace('\\xclubs ', '{\\color{OliveGreen}!c!}')
        line = line.replace('\\xhearts ', '{\\color{Maroon}!h!}')
        line = line.replace('\\xdiams ', '{\\color{BurntOrange}!d!}')

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

        f.write(line)
        i += 1

# Run lualatex to convert the .tex file to .pdf in the specified directory
subprocess.run(['lualatex', '-output-directory=' + OUTPUT_DIR, output_tex_file]) # , check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Clean up auxiliary files
aux_file = os.path.join(OUTPUT_DIR, 'to_docx.aux')
log_file = os.path.join(OUTPUT_DIR, 'to_docx.log')
subprocess.run(['rm', aux_file, log_file], check=True)

print("Conversion complete. Files saved in", OUTPUT_DIR)

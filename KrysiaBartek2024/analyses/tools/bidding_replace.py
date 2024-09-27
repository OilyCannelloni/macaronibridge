"""
TODO
NOT WORKING YET
"""

import re

def process_table(content):
    """
    Process the content of a tabular section and convert it to the simplified bidding format.
    """
    # Split the rows into lines
    lines = content.strip().splitlines()

    # Extract the bids from each row
    bids = []
    for line in lines[1:]:  # Skip the header (first row)
        # Clean the line, removing extra spaces
        line = line.strip()

        # Match table row bids
        if '&' in line:
            row_bids = [item.strip() for item in line.split('&')]

            if 'all \\pass' in line:
                bids.append('ap')
                break

            row_bids = ['P' if item == '--' or item == '\\pass' else item for item in row_bids]

            # Format bids with parentheses for every second bid except (B) and (K)
            formatted_bids = []
            for i, bid in enumerate(row_bids):
                if '(B)' in bid or '(K)' in bid:
                    formatted_bids.append(bid.replace('(B)', '').replace('(K)', ''))
                elif i % 2 == 0:
                    formatted_bids.append(f"({bid})")
                else:
                    formatted_bids.append(bid)

            # Join formatted bids with a dash
            bids.append(' - '.join(formatted_bids))

    # Return the processed bids as a formatted string
    return '\n'.join(bids)

def process_tex_file(input_filename, output_filename):
    """
    Reads a .tex file, processes the tabular sections, and writes the updated content to a new file.
    """
    with open(input_filename, 'r') as file:
        content = file.read()

    # Regular expression to find the table environments
    table_pattern = re.compile(
        r'\\begin\{table\}\[.*?\].*?\\begin\{tabular\}\{.*?\}(.*?)\\end\{tabular\}.*?\\end\{table\}',
        re.DOTALL
    )

    # Find all tables and process them
    modified_content = content
    for match in table_pattern.finditer(content):
        original_table = match.group(0)
        table_content = match.group(1)

        # Process the tabular content to create the simplified version
        simplified_table = process_table(table_content)

        # Replace the original table with the simplified version
        modified_content = modified_content.replace(original_table, simplified_table)

    # Write the modified content to the output file
    with open(output_filename, 'w') as file:
        file.write(modified_content)

# Define input and output file names
input_file = 'tmp.tex'
output_file = 'tmp2.tex'

# Process the input .tex file
process_tex_file(input_file, output_file)

print(f"Processed {input_file} and saved the result to {output_file}.")

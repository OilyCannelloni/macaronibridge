from models import *





def bidding_header(board_n):
    vul = get_vul(board_n)
    ss = ""
    for letter in "WNES":
        if letter in vul:
            ss += f"\\vul{{{letter}}}"
        else:
            ss += f"\\nvul{{{letter}}}"

        if letter != "S":
            ss += " & "
        else:
            ss += "\\\\\n"
    return ss


def build_analysis_page(board: BoardData):
    ss = ""
    ss += "\n\\pagebreak\n"
    ss += f"\\section*{{Rozdanie {board.sequence_number or board.number}}}\n"
    ss += board.to_handdiagramv()
    ss += r"""
\begin{table}[h!]
    \centering
    \begin{tabular}{cccc}
        """
    ss += bidding_header(board.number)

    ss += r"""
    \end{tabular}
\end{table}
"""
    return ss


def build_analysis_template(boards, target_file, verbose=False):
    with open(target_file, "w") as file:
        header = r"""
\documentclass[12pt, a4paper]{article}
\usepackage{import}

\import{../lib/}{bridge.sty}

\title{Board Set Analysis}
\author{... using MacaroniBridge/TCResultsParser}

\begin{document}
\maketitle

    
    """
        if verbose:
            print(header)
        file.write(header)

        for board in boards:
            page = build_analysis_page(board)
            if verbose:
                print(page)
            file.write(page)

        footer = r"""
\end{document}        
"""
        if verbose:
            print(footer)
        file.write(footer)


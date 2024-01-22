# Bridge bidding system

The directory contains the notes for the bidding arrangements.

## Project structure

The root directory contains main system file (SYSTEM.pdf) and 
scripts used to generate SYSTEM files.

The *./source* directory contains .tex files.

The *./docs* directory contains .pdf files with bidding system.
Each file refers to a different convention and contains bidding
arrangements with explanations and examples.

## SYSTEM creation

The system file (SYSTEM.pdf) is being created automatically from
separate system files placed in docs. To produce the SYSTEM run:
```
./makeSystem.sh
```
in the terminal.

## How the SYSTEM is being created?

Each file in *./docs* contains bidding explanations and examples
regarding discussed topic. The explanations are preceded by bare 
arrangements. The `makeSystem.sh` script extracts those arrangements
from each .tex file and puts it all together in SYSTEM file.

## How to change the order or titles in the SYSTEM.pdf?

The arrangements from the .tex file that are being placed in 
the SYSTEM file are bordered with comments:
```
%%% PRIORITY: 42
%%% TITLE: Jebać multi
%%% SYSTEM BEGIN %%%

Content

%%% SYSTEM END %%%
```

To change the title appearing in the SYSTEM or the order of contents,
change the TITLE or PRIORITY in those comments. The higher priority (smaller number)
the earlier given content will appear in the SYSTEM.

## How to produce the separate doc file?

Run:
```
./toPdf.sh filename
```
in the terminal. Write *filename* without extension. The LaTeX build files will
be placed in *./build* directory. The output file will be placed in *./docs* directory.
If you want to make pdfs from all the source files, run:
```
./toPdf.sh
```

## Current docs content

- 1m opening
- 1nt opening
- 2nt opening
- 1nt - dealing with interference
- Overcalling 1nt
- Reverses, jump shifts and jump reverses
- 2nt overcall after major preempt
- Rebid with 3-card support
- Responding to partner's preempt
- Dealing with Multi/Wilkosz
- Dealing with preempts
- Acol 2c
- Gazilli
- Drury
- Asking for shortness (LSF)
- Mini Splinters
- Transfers after 1M (X)
- Overcalling 2nt
- Other bids and rules

## Roadmap

- add generating list of contents in the SYSTEM
- complete system
- add explanations and examples
- 1M opening
- non-serious 3nt

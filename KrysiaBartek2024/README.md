### Bridge bidding system

The directory contains the notes for the bidding arrangements.

## Project structure

The root directory contains main system file (SYSTEM.pdf) and 
scripts used to generate system files.

The *./source* directory contains `.tex` files.

The *./docs* directory contains `.pdf` files with bidding system.
Each file refers to a different convention and contains bidding
arrangements with explanations and examples.

## System creation

The system file (SYSTEM.pdf) is being created automatically from
separate system files placed in docs. To produce the system run:
```
./makeSystem.sh
```
in the terminal.

## How the system is being created?

Each file in *./docs* contains bidding explanations and examples
regarding discussed topic. The explanations are preceded by bare 
arrangements. The `makeSystem.sh` script extracts those arrangements
from each `.tex` file and puts it all together in SYSTEM file.

## How to change the order or titles in the SYSTEM.pdf?

The arrangements from the `.tex` file that are being placed in 
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
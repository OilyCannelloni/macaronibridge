### How to use bridge tools?

To parse hands from website go to `tc-results-parser` dir and type:

```
python3 main.py -d https://mzbs.pl/files/2021/wyniki/zs/tmb2024/gppp/
```

usage:

-d  website with results

-n  number of boards to retrieve (if not specified, all hands will be parsed)

-b  number of board to be retrieved (if only one needed)

Arguments -n and -b cannot be used together.

To generate .pdf suitable for .docx generation, type:

```
python3 skrypt_dla_debili.py ../zaczek_30_09_24.tex
```

The .pdf will be placed in `tmp` dir.

Then, you can use this site to generate .docx:

https://www.ilovepdf.com/pdf_to_word

Next, you can replace appropriate card-suit codes with characters with:

```
python3 docx_replace.py
```

Input file for this script is: `/tmp/to_docx_docx` and output is: `/tmp/ZACZEK.docx`.


### TODO

Replace bidding with simpler form, so it doesn't skew while .docx generation.

Put it all together into one script.

Make tc-results-parser.py Generate '-' for players before the dealer,
note the lead card, and note, where the given players pair sit (which line).
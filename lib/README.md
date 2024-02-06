## Handling spaces

The `\xspace` package is used to handle spaces at the end of macros. `\xspace` after popular
macros are already added (like `\spades`, `\nt`, `\dbl`, etc.). To handle spaces after any other macro add `\xspace` after the command. Example:

```
\newcommand{\spades}{\color{Blue}\ding{171}\color{black}\xspace}
```

If the `xspace` is not behaving as expected, for example between the macro and some unusual character, a new command without the `xspace` can be added and the space can be handled manually at one time, using this command.

## Handling section types

How to modify the library to handle the new secion type (ex. 'subsubsection')? Add following lines between `\makeatletter` and `\makeatother` lines (at the end of file):

```
\let\oldSECTION\SECTION

\renewcommand{\SECTION}{%
  \@ifstar{\mySECTIONStar}{\mySECTIONNoStar}%
}

\newcommand{\mySECTIONNoStar}[1]{%
  \directlua{setSectionTitleFlag()}%
  \oldSECTION{#1}%
  \directlua{resetSectionTitleFlag()}%
}

\newcommand{\mySECTIONStar}[1]{%
  \directlua{setSectionTitleFlag()}%
  \oldSECTION*{#1}%
  \directlua{resetSectionTitleFlag()}%
}
```

Replace 'SECTION' with the appropriate section name (ex. 'subsubsection').
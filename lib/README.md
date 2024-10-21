# How to use LaTeX bridge library?

## Windows

1. Get MikTex from here:

https://miktex.org/download

You can use default configuration during installation.

2. Get Git from here:

https://gitforwindows.org/

You can use default settings during installation.

3. Open Git Console (git bash). Navigate to desired directory, for example (type this in Git Console):

```
cd Desktop
```

Clone our repository:

```
 git clone https://github.com/OilyCannelloni/macaronibridge.git
```

You should see cloned repository in the chosen directory (for example on your Desktop).

Navigate to this directory:

```
cd macaronibridge
```

Create .tex file, you can do it using command:

```
touch file.tex
```

![Zrzut ekranu 2024-10-21 222048](https://github.com/user-attachments/assets/068c0815-0e82-47d7-93ce-3944aaa18ba1)

Note that file.tex appeared in ./macaronibridge directory.

Open this file using TeXworks. This editor should be installed with MikTex.

![Zrzut ekranu 2024-10-21 214728](https://github.com/user-attachments/assets/de1522b5-7129-4478-bad6-fe188218cdb9)

4. Write your TeX file, for example copy & paste this:

```
\documentclass[12pt, a4paper]{report}
\usepackage{import}

\import{./lib/}{bridge.sty}
\setmainlanguage{english}

\title{Example LaTeX file}
\author{Krysia \& Bartek}
\begin{document}
\maketitle

This file is an example LaTeX file, using bridge.sty library.

\sequence{{1\diams}{1\hearts}{2\nt}}
\begin{options}[2]
    \item[\pass]
    \item[3\clubs] ask
    \item[3\diams/3\hearts] to play
    \item[3\spades] ask clubs
\end{options}

\end{document}
```

5. Choose LuaLaTeX as compiler and press 'run' (green arrow).

![Zrzut ekranu 2024-10-21 215220](https://github.com/user-attachments/assets/82e958e8-cd0b-4008-95c3-5ec4ccd61280)

On the first time it may take a while to compile (see screenshot below). If the application asks you if you want to install dependencies; agree (you can choose not to be ased every time).

![Zrzut ekranu 2024-10-21 213716](https://github.com/user-attachments/assets/61f9b604-892c-4354-aa66-b4bdc742c017)

You should see the pdf on the right side of your page. The file.pdf file has been created in the same directory as file.tex.

### remarks

1. Note, that the file.tex created directly in macaronibridge directory imports bridge library like this:

```
\import{./lib/}{bridge.sty}
```

If you decide to put your file somewhere else, you have to edit this line. For example, if you put your file in macaronibridge/myfiles directory, you have to change import line to:

```
\import{../lib/}{bridge.sty}
```

2. Investigate other files in macaronibridge repo to see other examples of what else you can do using bridge LaTeX library.

## Linux

Clone repo and compile your .tex files using LuaLaTeX.

# Some advanced remarks 

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

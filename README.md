# Multi2Diamonds -- Bridge notes in LaTeX!

<img width="300" height="461" alt="image" src="https://github.com/user-attachments/assets/5352b214-d2d4-4a9b-921f-4e8bab035499" />
<img width="300" height="800" alt="image" src="https://github.com/user-attachments/assets/933d7d09-e34f-4fa9-a18a-85c5550a61a4" />

## How to use?
### 1. Configure Overleaf

1. Register on [overleaf.com](overleaf.com) and create a blank project.
2. Download [the bridgetex files](https://github.com/OilyCannelloni/macaronibridge/releases/download/0.2.1/lib.zip), unpack them, and upload to your project.

<img width="400" height="599" alt="image" src="https://github.com/user-attachments/assets/67f1da0b-fcc8-4cee-b32b-a9d50d29538a" />

3. Paste the following code replacing the default content:

```
\documentclass[12pt, a4paper]{article}
\usepackage{import}
\import{./lib/}{bridge.sty}

\title{My first system}
\author{By Me}
\date{\today}

\begin{document}

\maketitle

\sequence{{1\diams}{1\spades}{2\hearts}}
\begin{options}[2]
    \item[2\spades\alrt] Slowdown - any hand with 4-8PC \vimp
    \item[2\nt] \gf asking for shape
    \item[3\clubs] 4th suit
    \item[3\diams] A rather balanced hand with \diams fit
\end{options}

\end{document}
```

4. Compilation should **fail** - we need to use LuaLatex! Change it under Menu in top-left corner

<img width="400" height="593" alt="image" src="https://github.com/user-attachments/assets/1323ce2c-33ab-4f41-a887-dadf3ff2c1eb" />

5. Now you should be able to compile the project.
<img width="400" height="587" alt="image" src="https://github.com/user-attachments/assets/b0fb987b-f335-4b73-8674-591cc9c696ad" />

## [Library Documentation](https://github.com/OilyCannelloni/macaronibridge/blob/master/first_steps_with_bridgetex.pdf)

## Downloading board sets from TournamentCalculator

Navigate to [Multi2Diamonds.com](https://multi2diamonds.com). Paste a link to the base site of a tournament (just like in the example). Pick some interesting boards and submit.

A download should start shortly. Upload it to Overleaf and compile. Time to start making notes!

## Sharing the project with your partner

The free version enables you to collaborate with just one person. Use the 'Share' button in the upper right. You can edit the documents simultanously and log all changes.




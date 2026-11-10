---
title: "getparams.lsp"
weight: 10
ShowToc: true
hiddenInHomeList: true
summary: "user prompts for the pouring parameters"
---

getparams.lsp -- user prompts for the pouring parameters

Source: original program listing, pages 19-20.

NOTE: this is the tail of the GETPARAMS function. The opening of the
function (and the prompts for volume flow rate and spout diameter) were
on pages 1-18, which are not part of this transcription. The final ")"
below closes that missing (defun getparams ...).

Each prompt shows the previous value as the default when one exists.

## In plain English

This is the tail of the routine that interviews the operator. For each setting it checks for a value left over from the last run: if there is one, it is shown in angle brackets as the default and kept when the operator just presses Enter; if not, an answer is required. After the prompts it works out the area of one spout circle and asks the operator to pick the pockets.

*76 lines of code and comments, 9 of them comments.*

## The pieces

| Piece | What it is | Calls | Called by |
| --- | --- | --- | --- |
| [The prompts (tail of getparams)](#getparams) | Asks for the spout pitch, the increment distance, the number of spouts and increments, the accuracy and the output file name. | – | `GO` (missing pages, inferred) |

## The prompts (tail of getparams) {#getparams}

Asks for the spout pitch, the increment distance, the number of spouts and increments, the accuracy and the output file name. Then it calculates the valid area, switches to the graphics screen and calls SSGET so the operator can select the pockets.

**76 lines.** Shared state it touches: `accuracy`, `dia`, `filename`, `inc`, `incs`, `pitch`, `pockset`, `spouts`.

```lisp
;GET THE DISTANCE BETWEEN SPOUTS
(if pitch
    (progn
        (initget (+ 2 4))
        (setq val(getdist (strcat "\n spout pitch <" (rtos pitch) ">: ")))
        (if (/= val nil)(setq pitch val))
    )
    (progn
        (initget (+ 1 2 4))
        (setq pitch(getdist "\n spout pitch: "))
    )
)
;GET THE INCREMENT DISTANCE
(if inc
    (progn
        (initget (+ 2 4))
        (setq val(getdist (strcat "\n increment distance <" (rtos inc) ">: ")))
        (if (/= val nil)(setq inc val))
    )
    (progn
        (initget (+ 1 2 4))
        (setq inc(getdist "\n increment distance: "))
    )
)
;GET THE NUMBER OF SPOUTS
(if spouts
    (progn
        (initget (+ 2 4))
        (setq val(getint (strcat "\n number of spouts <" (rtos spouts) ">: ")))
        (if (/= val nil)(setq spouts val))
    )
    (progn
        (initget (+ 1 2 4))
        (setq spouts(getint "\n number of spouts: "))
    )
)
;GET THE NUMBER OF INCREMENTS
(if incs
    (progn
        (initget (+ 2 4))
        (setq val(getint (strcat "\n number of increments <" (rtos incs) ">: ")))
        (if (/= val nil)(setq incs val))
    )
    (progn
        (initget (+ 1 2 4))
        (setq incs(getint "\n number of increments: "))
    )
)
;GET THE ACCURACY PERCENTAGE FOR VALID CELL DETERMINATION
(if accuracy
    (progn
        (initget (+ 2 4))
        (setq val(getreal (strcat "\n spout accuracy <" (rtos accuracy) "> %: ")))
        (if (/= val nil)(setq accuracy val))
    )
    (progn
        (initget (+ 1 2 4))
        (setq accuracy (getreal "\n spout accuracy %: "))
    )
)
;GET THE OUTPUT FILENAME
(if filename
    (progn
        (setq val(getstring(strcat "\n name of output file <" filename ">: ")))
        (if (/= val "")(setq filename val))
    )
    (setq filename(getstring "\n name of output file: "))
)
;CALCULATE VALID AREA
(setq validarea(/(* 3.14159(* dia dia)) 4))
;SWITCH TO GRAPHICS SCREEN
(graphscr)
;GET THE SELECTION SET OF POCKETS FROM THE USER
(princ "Please Select Pockets")
(setq pockset(ssget))
)
```

> **Look closely.** The numbers passed to INITGET are added bit flags: 1 means an answer is required, 2 forbids zero and 4 forbids negatives, so (+ 1 2 4) demands a positive number. Pi is typed in as 3.14159. Remembering the last values works because they live in global variables that survive between runs.

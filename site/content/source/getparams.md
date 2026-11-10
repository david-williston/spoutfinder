---
title: "getparams.lsp"
weight: 10
summary: "user prompts for the pouring parameters"
---

getparams.lsp -- user prompts for the pouring parameters
Source: original program listing, pages 19-20.
NOTE: this is the tail of the GETPARAMS function. The opening of the
function (and the prompts for volume flow rate and spout diameter) were
on pages 1-18, which are not part of this transcription. The final ")"
below closes that missing (defun getparams ...).

Each prompt shows the previous value as the default when one exists.

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
;--------------------------------------------------------
```

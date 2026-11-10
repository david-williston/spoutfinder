---
title: "output.lsp"
weight: 40
summary: "write the combined location list to the .sdf data file"
---

output.lsp -- write the combined location list to the .sdf data file
Source: original program listing, page 26.

```lisp
;OUTPUT WRITES THE CONTENTS OF THE COMBINED LIST TO A FILE
(defun output( / fd returncount )
    ;SWITCH TO A CLEAR TEXT SCREEN FOR FILE OUTPUT
    (textscr)(textpage)
    (princ (strcat "\n Opening output file" filename))
    ;OPEN THE OUTPUT FILE FOR WRITING
    (setq fd(open filename "w"))
    (princ "\n Writing data to disk")
    (princ "SpoutFinder V0.1 beta DATA FILE\n" fd)
    ;SETUP A COUNTER EXTRACTING ITEMS ONE BY ONE FROM THE LIST AND
    ;OUTPUTTING THEM TO THE FILE.
    (setq returncount 0)
    ;REPEAT FOR THE NUMBER OF INCREMENTS.
    (repeat incs
        ;PRINT A NEWLINE IN THE OUTPUT FILE AFTER EACH ROW OF SPOUTS.
        (princ "\n" fd)
        ;REPEAT FOR THE NUMBER OF SPOUTS.
        (repeat spouts
            ;PRINT A . TO THE SCREEN FOR THE USER TO SEE THAT THE
            ;PROGRAM IS PROCESSING.
            (princ ".")
            ;PRINT THE CURRENT ITEM FROM THE LIST TO THE FILE.
            (princ (nth returncount combinedlist) fd)
            ;PRINT A SPACE AS THIS IS A SPACE DELIMITED FILE.
            (princ " " fd)
            ;INCREMENT THE COUNTER.
            (setq returncount(+ returncount 1))
        )
    )
    (princ "\n Closing output file")
    (princ "\n\nEnd of File" fd)
    ;CLOSE THE OUTPUT FILE.
    (close fd)
    ;END OF PROCESSING
    (princ "\n\n Program Complete")
    (princ)
)
;--------------------------------------------------------
;PRINT AN INTRO SCREEN TO THE USER.
(textscr)(textpage)
(princ "\n\n\n\n\n\n\n\n\n\t\t\t SPOUTFINDER is loaded\n\n\t\t\t    Type GO to run")
;END OF PROGRAM LISTING.
(princ)
;--------------------------------------------------------
```

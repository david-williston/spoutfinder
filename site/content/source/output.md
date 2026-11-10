---
title: "output.lsp"
weight: 40
ShowToc: true
hiddenInHomeList: true
summary: "write the combined location list to the .sdf data file"
---

output.lsp -- write the combined location list to the .sdf data file

Source: original program listing, page 26.

## In plain English

Writes the answer to disk and says hello. Once every pocket has been processed, the merged list becomes a plain text file the pouring machine can read.

*42 lines of code and comments, 17 of them comments.*

## The pieces

| Piece | What it is | Calls | Called by |
| --- | --- | --- | --- |
| [`output`](#output) | Opens the file, writes a header line, then writes one line per increment with one space-separated entry per spout. | – | `GO` (missing pages, inferred) |
| [The startup banner](#banner) | Runs when the file is loaded: clears to the text screen and tells the operator SpoutFinder is loaded and to type GO to run. | – | when the file loads |

## output {#output}

Opens the file, writes a header line, then writes one line per increment with one space-separated entry per spout. It prints a dot to the screen for each spout so the operator can see it is working, then closes the file.

**37 lines.** Shared state it touches: `combinedlist`, `filename`, `incs`, `spouts`.

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
```

> **Look closely.** Everything is written with PRINC to a file handle. The header still says V0.1 beta, even though the program is called V1.0.


## The startup banner {#banner}

Runs when the file is loaded: clears to the text screen and tells the operator SpoutFinder is loaded and to type GO to run.

**5 lines.**

```lisp
;PRINT AN INTRO SCREEN TO THE USER.
(textscr)(textpage)
(princ "\n\n\n\n\n\n\n\n\n\t\t\t SPOUTFINDER is loaded\n\n\t\t\t    Type GO to run")
;END OF PROGRAM LISTING.
(princ)
```

> **Look closely.** GO is defined on the missing pages, so the banner promises a command this transcription cannot yet deliver.

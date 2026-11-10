---
title: "session.lsp"
weight: 60
ShowToc: true
hiddenInHomeList: true
summary: "environment restore, error handling and default values"
---

session.lsp -- environment restore, error handling and default values

Source: original program listing, page 25.

## In plain English

Housekeeping. It restores AutoCAD to how the operator left it, handles errors politely, and supplies the default settings.

*46 lines of code and comments, 11 of them comments.*

## The pieces

| Piece | What it is | Calls | Called by |
| --- | --- | --- | --- |
| [`my_reset`](#my_reset) | Ends the undo group, then restores object snap, command echo and blip mode, and puts AutoCAD's own error handler back. | – | [`my_error`](../session/#my_error) |
| [`my_error`](#my_error) | Replaces AutoCAD's error handler. For a user cancel it just says the program was terminated. | [`my_reset`](../session/#my_reset) | `GO` (missing pages, inferred) |
| [`setdefaults`](#setdefaults) | Sets the values the prompts offer on the first run: flow rate 1, spout diameter 1, pitch 1, increment 1, 8 increments, 8 spouts, accuracy 0.02 and the file name output.sdf. | – | `GO` (missing pages, inferred) |

## my_reset {#my_reset}

Ends the undo group, then restores object snap, command echo and blip mode, and puts AutoCAD's own error handler back.

**16 lines.**

```lisp
;MY_RESET FUNCTION IS CALLED FROM THE ERROR FUNCTION AND AT THE END OF THE
;MAIN. IT RESETS THE SETTINGS SETUP BY MYSETUP.
(defun my_reset( / )
    ;UNDOES EVERYTHING TO THE PRESET UNDO MARKER
    (command "_.undo" "end")
    ;RESTORE OTHER SYSTEM VARIABLES
    (setvar "osmode" os_mode)
    ;RESTORE THE COMMAND ECHO
    (setvar "cmdecho" 1)
    ;RESTORE THE BLIPMODE
    (setvar "blipmode" b_mode)
    ;RESTORE AUTOCAD *ERROR* FUNCTION
    (setq *error* old_err)
    ;CLEAN EXIT PRINC CALL
    (princ)
)
```

> **Look closely.** It is called both at the end of a run and from the error handler, so the drawing environment is put right whichever way the program ends.


## my_error {#my_error}

Replaces AutoCAD's error handler. For a user cancel it just says the program was terminated. For a real error it shows the error number in an alert and tells the operator to type U to undo everything the program did.

**18 lines.**

```lisp
;STANDARD ERROR HANDLING FUNCTION
(defun my_error( msg / err_no message )
    (command)
    (command)
    (if (and(/= msg "Function cancelled")(/= msg "console break"))
        (progn
            (princ "\nProgram error - ")
            (princ msg)
            (setq err_no (getvar "ERRNO"))
            (setq message(strcat "\nProgram Error\nERROR # " (itoa err_no) "\nType <u> to Undo
            all operations done by program"))
            (alert message)
            (princ)
        )
        (princ "\n\n Program Terminated By User\n\n")
    )
    (my_reset)
)
```

> **Look closely.** Undoing a whole run with one command is possible because the work happens inside a single undo group; the group is opened by a setup routine on the missing pages.


## setdefaults {#setdefaults}

Sets the values the prompts offer on the first run: flow rate 1, spout diameter 1, pitch 1, increment 1, 8 increments, 8 spouts, accuracy 0.02 and the file name output.sdf.

**12 lines.** Shared state it touches: `accuracy`, `dia`, `filename`, `inc`, `incs`, `pitch`, `spouts`, `volumeflowrate`.

```lisp
(defun setdefaults ( / )
    ;THESE ARE THE DEFAULT VALUES PRESENTED TO THE USER IN
    ;THE GETPARAMS FUNCTION
    (setq volumeflowrate 1)
    (setq dia 1)
    (setq pitch 1)
    (setq inc 1)
    (setq incs 8)
    (setq spouts 8)
    (setq accuracy 0.02)
    (setq filename "output.sdf")
)
```

---
title: "session.lsp"
weight: 60
summary: "environment restore, error handling and default values"
---

session.lsp -- environment restore, error handling and default values
Source: original program listing, page 25.

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
;--------------------------------------------------------
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
;--------------------------------------------------------
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
;--------------------------------------------------------
```

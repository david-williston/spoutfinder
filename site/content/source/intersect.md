---
title: "intersect.lsp"
weight: 20
ShowToc: true
hiddenInHomeList: true
summary: "spout/pocket intersection and validity test"
---

intersect.lsp -- spout/pocket intersection and validity test

Source: original program listing, pages 21-22.

## In plain English

The heart of the program. For one spout position it builds a circle, intersects it with the pocket surface, and decides whether the spout fits.

*83 lines of code and comments, 32 of them comments.*

## The pieces

| Piece | What it is | Calls | Called by |
| --- | --- | --- | --- |
| [`doint`](#doint) | Draws a circle at the current point on the cell layer, turns it into a region (SOLIDIFY), copies the pocket surface, and intersects the two with SOLINT. | – | `GO` (missing pages, inferred) |
| [`check`](#check) | Judges the overlap. No result means the spout is outside the pocket, so the circle and the copied surface are erased. | – | `GO` (missing pages, inferred) |

## doint {#doint}

Draws a circle at the current point on the cell layer, turns it into a region (SOLIDIFY), copies the pocket surface, and intersects the two with SOLINT. It returns the selection set holding the overlap.

**32 lines.** Shared state it touches: `dia`, `pocksurfname`, `pocksurfset`, `stp`.

```lisp
(defun doint ( / cellname newpocksurfname cell pock cellset resultset )
    ;CHANGE TO THE CELL LAYER
    (command "layer" "set" "cell" "")
    ;CREATE A CIRCLE FOR USE AS A CELL
    (command "circle" stp "D" dia)
    ;GET THE NAME OF THE CIRCLE
    (setq cellname(entlast))
    ;CLEAR THE SELECTION SET CELLSET SO AUTOLISP DOES NOT RUN OUT OF
    ;SELECTION SETS
    (setq cellset nil)
    ;CREATE SELECTION SET OF CELLNAME FOR AME
    (setq cellnameset(ssadd cellname))
    ;SOLIDIFY THE CIRCLE
    (setq cellset(solidify cellnameset))
    ;RELEASE SELECTION SET PASSED TO SOLIDIFY
    (setq cellnameset nil)
    ;COPY THE POCKET SURFACE
    (setq pocksurfname(ssname pocksurfset 0))
    (command "copy" pocksurfname "" '(0 0 0) "")
    ;GET THE COPIED POCKET SURFACE NAME
    (setq newpocksurfname(entlast))
    ;ADD THE COPIED POCKET SURFACE TO THE CELL SELECTION SET
    (ssadd newpocksurfname cellset)
    ;SAVE CELL AND POCKET SURFACE NAMES AS SOLINT EMPTIES PASSED SET
    (setq cell(ssname cellset 0))
    (setq pock(ssname cellset 1))
    ;RESET SELECTION SET TO MAKE AUTOLISP HAPPY
    (setq resultset nil)
    ;CREATE THE INTERFERENCE AREA
    (setq resultset(solint cellset "xy"))
    resultset
)
```

> **Look closely.** A fresh circle and a fresh copy are made every time because SOLINT empties the set it is given, so the code saves the entity names first. Selection sets are set to nil as soon as they are used so AutoLISP does not run out of them.


## check {#check}

Judges the overlap. No result means the spout is outside the pocket, so the circle and the copied surface are erased. Otherwise it measures the overlap with SOLAREA and calls the spout valid if the shortfall from a full circle is under the accuracy tolerance, drawing a circle there.

**51 lines.** Shared state it touches: `accuracy`, `dia`, `stp`, `validity`.

```lisp
;CHECK LOOKS AT THE RESULT OF DOINT TO SEE IF THE LOCATION IS
;A POSSIBLE POURING LOCATION
(defun check ( resultset accuracy / resultname actualarea diff accu )
    (if (= resultset nil)
        ;NIL RESULT SET MEANS SPOUT IS OUTSIDE POCKET AND IS NOT VALID
        (progn
            ;ERASE LAST 2 ENTITIES CREATED; THE CELL AND THE POCKET
            ;SURFACE.
            (command "erase" "l" "")
            (command "erase" "l" "")
        )
        (progn
            ;TRUE RESULTSET MEANS LOCATION MAY BE VALID
            ;AND THE INTERSECTION SHOULD BE FURTHER TESTED
            (setq resultname(ssname resultset 0))
            ;PUT RESULTNAME INTO A SELECTION SET FOR AME SOLAREA
            (setq resultnameset(ssadd resultname))
            ;GET THE AREA OF THE CURRENT RESULT OF SOLINT
            (setq actualarea(solarea resultnameset))
            ;CALC THE DIFFERENCE BETWEEN VALID AND INVALID AREAS
            (setq diff(- validarea actualarea))
            (setq accu(* validarea accuracy))
            ;TEST VALIDITY OF LOCATION BY VIRTUE OF IT'S AREA AS
            ;COMPARED TO THE VALID AREA
            (if (< diff accu)
                (progn
                    ;DRAW A CIRCLE ON THE VALID LOCATION
                    (command "circle" stp "D" dia)
                    (setq validity T)
                )
                (progn
                    (setq validity nil)
                )
            )
        )
    )
    ;ERASE THE RESULTING REGION
    (command "erase" resultset "")
    ;INCREMENT THE CYCLENUMBER FOR SOLPURGE
    (setq cyclenumber(+ cyclenumber 1))
    ;PURGE ERASED REGIONS
    (if (= purgeflag cyclenumber)
        (progn
            ;PURGE ERASED REGIONS FROM DRAWING FILE
            (solpurge)
            ;RESET THE CYCLENUMBER
            (setq cyclenumber 0)
        )
    )
    validity
)
```

> **Look closely.** Every purgeflag cycles it calls SOLPURGE to clear erased solids out of the drawing file; the value of purgeflag is set on the missing pages. The result is the global validity flag, which the next step reads.

---
title: "pocket.lsp"
weight: 50
ShowToc: true
hiddenInHomeList: true
summary: "pocket geometry: surface region, volume, bounding-box test"
---

pocket.lsp -- pocket geometry: surface region, volume, bounding-box test

Source: original program listing, page 20.

## In plain English

Three small helpers that ask AutoCAD's solid modeler about the pocket being worked on: its flat surface, its volume, and its bounding box.

*37 lines of code and comments, 14 of them comments.*

## The pieces

| Piece | What it is | Calls | Called by |
| --- | --- | --- | --- |
| [`pocketsurf`](#pocketsurf) | Slices the current pocket with the XY plane (SOLSECT) to get its flat surface region, then asks AME for that region's mass properties (SOLMASSP). | – | `GO` (missing pages, inferred) |
| [`pocketvolume`](#pocketvolume) | Asks AME for the current pocket's mass properties and keeps item 1 of the returned list, its volume. | – | `GO` (missing pages, inferred) |
| [`seeiflocal`](#seeiflocal) | A cheap pre-check. It reads two corner points of the pocket surface's bounding box out of the SOLMASSP list and tests whether the current spout position lies inside that box. | – | `GO` (missing pages, inferred) |

## pocketsurf {#pocketsurf}

Slices the current pocket with the XY plane (SOLSECT) to get its flat surface region, then asks AME for that region's mass properties (SOLMASSP). The slice and the property list are kept for the later steps.

**10 lines.** Shared state it touches: `pockset`, `pocksurfdatalist`, `pocksurfset`.

```lisp
(defun pocketsurf ( / )
    ;CREATE SURFACE REGION OF EACH POCKET
    (command "layer" "s" "pocketsurf" "")
    ;EXTRACT CURRENT POCKET NAME
    (setq currentpocket(ssname pockset pocketnumber))
    ;SOLSECT THE CURRENT POCKET
    (setq pocksurfset(solsect currentpocket "xy"))
    ;GET SOLMASSPROPERTIES DATA FOR CURRENT POCKET REGION
    (setq pocksurfdatalist(solmassp pocksurfset))
)
```

> **Look closely.** It switches to a layer called pocketsurf first, so the working slices stay apart from the model.


## pocketvolume {#pocketvolume}

Asks AME for the current pocket's mass properties and keeps item 1 of the returned list, its volume.

**8 lines.** Shared state it touches: `pockset`.

```lisp
;POCKETVOLUME GETS THE VOLUME OF THE CURRENT POCKET IN THE SELECTION SET
(defun pocketvolume ( / massinfolist )
    ;MASSINFOLIST IS THE LIST OF PROPERTIES RETURNED FROM THE AME SOLMASP
    ;FUNCTION.
    (setq massinfolist(solmassp (ssname pockset pocketnumber) "n"))
    ;EXTRACT THE VOLUME VALUE FROM THE LIST
    (setq currentpocketvolume(nth 1 massinfolist))
)
```

> **Look closely.** The "n" given to SOLMASSP presumably answers its prompt about writing a report file.


## seeiflocal {#seeiflocal}

A cheap pre-check. It reads two corner points of the pocket surface's bounding box out of the SOLMASSP list and tests whether the current spout position lies inside that box.

**19 lines.** Shared state it touches: `pocksurfdatalist`, `stp`.

```lisp
;SEEIFLOCAL CHECKS THE CURRENT LOCATION STP AGAINST THE BOUNDING
;BOX OF THE CURRENT POCKET SURFACE
(defun seeiflocal ( / islocal xc yx x1 y1 x2 y2 )
    (setq xc(nth 0 stp))
    (setq yc(nth 1 stp))
    ;GET THE X Y RANGE OF THE CURRENT POCKET SURFACE BOUNDING BOX
    (setq x1(nth 0 (nth 2 pocksurfdatalist)))
    (setq y1(nth 1 (nth 2 pocksurfdatalist)))
    (setq x2(nth 0 (nth 3 pocksurfdatalist)))
    (setq y2(nth 1 (nth 3 pocksurfdatalist)))
    ;CHECK TO SEE IF POINT IN BOX
    (if (and (and(< xc x2)(> xc x1)) (and(< yc y2)(> yc y1)) )
        ;TRUE IF STP IS IN BOX
        (setq islocal T)
        ;NIL IF STP IS OUTSIDE BOX
        (setq islocal nil)
    )
    islocal
)
```

> **Look closely.** The local-variable list names yx where the body uses yc, so yc quietly becomes a global. In a language with no compiler warnings, a typo like that was easy to make and hard to see.

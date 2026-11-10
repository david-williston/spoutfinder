---
title: "pocket.lsp"
weight: 150
---

pocket.lsp -- pocket geometry: surface region, volume, bounding-box test

Source: original program listing, page 20.

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
;--------------------------------------------------------
;POCKETVOLUME GETS THE VOLUME OF THE CURRENT POCKET IN THE SELECTION SET
(defun pocketvolume ( / massinfolist )
    ;MASSINFOLIST IS THE LIST OF PROPERTIES RETURNED FROM THE AME SOLMASP
    ;FUNCTION.
    (setq massinfolist(solmassp (ssname pockset pocketnumber) "n"))
    ;EXTRACT THE VOLUME VALUE FROM THE LIST
    (setq currentpocketvolume(nth 1 massinfolist))
)
;--------------------------------------------------------
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
;--------------------------------------------------------
```

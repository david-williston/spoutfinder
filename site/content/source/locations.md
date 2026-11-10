---
title: "locations.lsp"
weight: 30
summary: "spout grid stepping and the pouring-location lists"
---

locations.lsp -- spout grid stepping and the pouring-location lists

Source: original program listing, pages 23-24.

```lisp
;BUILDLIST BUILDS THE TEMPORARY PROGRAM OUTPUT BY RECORDING IN A LIST THE
;VALID AND INVALID POURING LOCATIONS. VALID LOCATIONS ARE MARKED BY THE
;ENTITY NAME OF THE CURRENT POCKET. THE ENTITY NAME IS THEN REPLACED BY A TIME
;VALUE ONCE THE VALUE HAS BEEN CALCULATED. INVALID LOCATIONS ARE MARKED BY
;ZEROS.
(defun buildlist ( / x y )
    ;EXTRACT CURRENT COORDINATES
    (setq x(nth 0 stp))
    (setq y(nth 1 stp))
    ;CHECK TO SEE IF A NEW LIST IS BEING STARTED
    (if (and (= x 0)(= y 0))
        ;A NEW TEMP LIST IS BEING STARTED
        (progn
            (if (= validity T)
                (progn
                    ;A VALID LOCATION WILL HAVE THE ENTITY
                    ;NAME OF THE CURRENT POCKET
                    (setq templist(list (ssname pockset pocketnumber)))
                    ;INCREMENT THE LOCATION COUNT FOR THE
                    ;CURRENT POCKET
                    (setq locationcount(+ locationcount 1))
                )
                ;OTHERWISE A ZERO IS PLACED IN THE LIST
                (setq templist(list 0))
            )
        )
        ;THE TEMP LIST IS BEING APPENDED TO
        (progn
            (if (= validity T)
                (progn
                    ;A VALID LOCATION WILL HAVE THE ENTITY
                    ;NAME OF THE CURRENT POCKET
                    (setq templist(append templist (list (ssname pockset
                    pocketnumber))))
                    ;INCREMENT THE LOCATION COUNT FOR THE
                    ;CURRENT POCKET
                    (setq locationcount(+ locationcount 1))
                )
                ;OTHERWISE A ZERO IS PLACED IN THE LIST
                (setq templist(append templist (list 0)))
            )
        )
    )
)
;--------------------------------------------------------
;NEXTSPOUT MOVES STP TO THE NEXT SPOUT LOCATION
(defun nextspout ( / x y )
    (setq x(nth 0 stp))
    (setq y(nth 1 stp))
    (setq y(+ y pitch))
    (setq stp(list x y 0))
)
;--------------------------------------------------------
;NEXTROW MOVES STP TO THE NEXT ROW
(defun nextrow ( / x y )
    (setq x(nth 0 stp))
    (setq y 0)
    (setq x(+ x inc))
    (setq stp(list x y 0))
);--------------------------------------------------------
;COMBINE COMBINES THE PREVIOUS AND CURRENT TEMPLISTS OF POURING LOCATIONS
(defun combine ( / e1 e2 listlength newcombinedlist )
    ;THE LENGTH OF THE LISTS IS ALWAYS SPOUTS TIMES INCREMENTS
    (setq listlength (* incs spouts))
    ;CHECK TO SEE IF THIS IS THE FIRST LIST TO BE CREATED
    ;IF SO THEN THE LIST CANNOT BE COMBINED WITH A PREVIOUS ONE
    (if (= pocketnumber 0)
        ;THE NEWLIST BECOMES THE TEMPLIST
        (setq newcombinedlist templist)
        ;OTHERWISE ...
        (progn
            ;COUNT IS FOR REPEAT LOOP
            (setq count 0)
            ;REPEAT FOR EACH ITEM IN THE LIST(S)
            (repeat listlength
                ;EXTRACT THE CURRENT ITEM FROM THE PREVIOUSLY
                ;COMBINED LIST.
                (setq e1(nth count combinedlist))
                ;EXTRACT THE CURRENT ITEM FROM THE TEMPLIST
                (setq e2(nth count templist))
                ;CHECK IF THIS IS THE FIRST CELL IN THE CURRENT
                ;POCKET. IE COUNT IS ZERO.
                (if (and(and (= e1 0)(= e2 0))(= count 0))
                    ;THE FIRST CELL WILL BE A ZERO
                    (setq newcombinedlist(list 0))
                    ;OTHERWISE THE ITEM WILL BE AN ENTITY NAME
                    (progn
                        ;CHECK AGAIN TO SEE IF THE CELL IS NOT A
                        ;ZERO.
                        (if (/= e1 0)
                            ;THE CELL IS NOT A ZERO.
                            (setq newcombinedlist(append
                            newcombinedlist (list e1)))
                            ;THE CELL IS A ZERO
                            (setq newcombinedlist(append
                            newcombinedlist (list e2)))
                        )
                    )
                )
                ;INCREMENT THE COUNT OF LOCATIONS.
                (setq count(+ count 1))
            )
        )
    )
    ;SET THE NEW COMBINED LIST TO THE COMBINED LIST
    (setq combinedlist newcombinedlist)
)
;--------------------------------------------------------
```

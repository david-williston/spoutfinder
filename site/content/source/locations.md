---
title: "locations.lsp"
weight: 30
ShowToc: true
hiddenInHomeList: true
summary: "spout grid stepping and the pouring-location lists"
---

locations.lsp -- spout grid stepping and the pouring-location lists

Source: original program listing, pages 23-24.

## In plain English

Walks the grid of spout positions and keeps the results: one list per pocket, merged into a single list for the whole job.

*105 lines of code and comments, 42 of them comments.*

## The pieces

| Piece | What it is | Calls | Called by |
| --- | --- | --- | --- |
| [`buildlist`](#buildlist) | Adds one entry to the temporary list for the current position: the pocket's entity name where a spout is valid, 0 where it is not. | – | `GO` (missing pages, inferred) |
| [`nextspout`](#nextspout) | Moves the current point one spout pitch along y. | – | `GO` (missing pages, inferred) |
| [`nextrow`](#nextrow) | Resets y to 0 and moves x over by the increment distance, starting the next row. | – | `GO` (missing pages, inferred) |
| [`combine`](#combine) | Merges the list for the current pocket into the running list for all pockets. | – | `GO` (missing pages, inferred) |

## buildlist {#buildlist}

Adds one entry to the temporary list for the current position: the pocket's entity name where a spout is valid, 0 where it is not. A position of (0, 0) starts a new list.

**44 lines.** Shared state it touches: `pockset`, `stp`, `templist`, `validity`.

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
```

> **Look closely.** The comment explains the entity name is a stand-in; it was meant to be replaced by a time value once the pour volume was calculated.


## nextspout {#nextspout}

Moves the current point one spout pitch along y.

**7 lines.** Shared state it touches: `pitch`, `stp`.

```lisp
;NEXTSPOUT MOVES STP TO THE NEXT SPOUT LOCATION
(defun nextspout ( / x y )
    (setq x(nth 0 stp))
    (setq y(nth 1 stp))
    (setq y(+ y pitch))
    (setq stp(list x y 0))
)
```


## nextrow {#nextrow}

Resets y to 0 and moves x over by the increment distance, starting the next row.

**7 lines.** Shared state it touches: `inc`, `stp`.

```lisp
;NEXTROW MOVES STP TO THE NEXT ROW
(defun nextrow ( / x y )
    (setq x(nth 0 stp))
    (setq y 0)
    (setq x(+ x inc))
    (setq stp(list x y 0))
)
```


## combine {#combine}

Merges the list for the current pocket into the running list for all pockets. Position by position it keeps an entity name from the earlier list if there is one, otherwise takes the new list's entry.

**47 lines.** Shared state it touches: `combinedlist`, `incs`, `spouts`, `templist`.

```lisp
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
```

> **Look closely.** The list length is always spouts times increments, so the two lists line up exactly and can be merged with a simple counter.

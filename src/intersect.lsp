;;; intersect.lsp -- spout/pocket intersection and validity test
;;; Source: original program listing, pages 21-22.

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
;--------------------------------------------------------
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
;--------------------------------------------------------

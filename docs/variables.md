# SpoutFinder variable listing

From page 27 of the 1994 program listing. Type codes: `ENAME` entity name,
`SS` selection set, `L` local, `G` global. Names are shown as printed (one
name, `CURRENTPOCKETVOLUM`, is cut off in the original; a photo of the page
was partly blocked, so a few descriptions are inferred).

| Name | Type | L/G | Local to | Description |
| --- | --- | --- | --- | --- |
| CELLNAME | ENAME | L | DOINT | Entity name of the current spout profile region |
| POCKSURFNAME | ENAME | G | N/A | Entity name of the current pocket's surface region |
| NEWPOCKSURFNAME | ENAME | L | DOINT | Holds copy of the above item |
| CELL | ENAME | L | DOINT | Name of circle used to generate spout region |
| POCK | ENAME | L | DOINT | Name of current pocket |
| RESULTNAME | ENAME | L | CHECK | Entity name of the intersection of CELLNAME and NEWPOCKSURFNAME |
| E1 | ENAME | L | COMBINE | Temporary storage |
| E2 | ENAME | L | COMBINE | Temporary storage |
| FD | FILEPOINTER | L | OUTPUT | Output file pointer |
| SPOUTS | INT | G | N/A | Number of spouts in the array |
| INCS | INT | G | N/A | Number of increments in the array |
| VOLUMEFLOWRATE | INT | G | N/A | Volume flow rate of spouts |
| LOCATIONCOUNT | INT | L | MAIN | Increment of locations processed |
| LISTLENGTH | INT | L | COMBINE | Length of TEMPLIST, COMBINEDLIST and NEWCOMBINEDLIST |
| RETURNCOUNT | INT | L | OUTPUT | Counter for newlines in OUTPUT function |
| STP | LIST | G | N/A | XY point for current location being checked |
| POCKSURFDATALIST | LIST | G | N/A | List returned from SOLMASSP on POCKSURFNAME |
| MASSINFOLIST | LIST | L | POCKETVOLUME | List returned from SOLMASSP on POCK |
| NEWCOMBINEDLIST | LIST | L | COMBINE | Temporary storage of locations |
| COUNT | LIST | L | COMBINE | Counter for combining lists |
| COMBINEDLIST | LIST | G | N/A | Last combined list of locations |
| ISLOCAL | LOGICAL | L | SEEIFLOCAL, MAIN | True or false flag for bounding box test |
| VALIDITY | LOGICAL | G | N/A | True or false flag for SOLAREA test |
| ACCURACY | REAL | G | N/A | Percent value used for determining validity in area test |
| DIA | REAL | G | N/A | Diameter of spouts |
| PITCH | REAL | G | N/A | Distance between spouts |
| INC | REAL | G | N/A | Distance between increments |
| CURRENTPOCKETVOLUM | REAL | G | N/A | The current pocket's volume |
| XC | REAL | L | SEEIFLOCAL | Coordinates |
| YC | REAL | L | SEEIFLOCAL | Coordinates |
| X1 | REAL | L | SEEIFLOCAL | Coordinates |
| Y1 | REAL | L | SEEIFLOCAL | Coordinates |
| X2 | REAL | L | SEEIFLOCAL | Coordinates |
| Y2 | REAL | L | SEEIFLOCAL | Coordinates |
| ACTUALAREA | REAL | L | CHECK | Area of intersected region |
| DIFF | REAL | L | CHECK | Difference between ACTUAL and VALIDAREA |
| ACCU | REAL | L | CHECK | Temporary storage |
| X | REAL | L | BUILDLIST, NEXTSPOUT, NEXTROW | Coordinate |
| Y | REAL | L | BUILDLIST, NEXTSPOUT, NEXTROW | Coordinate |
| TEMPLIST | REAL | G | N/A | Temporary list of locations |
| TIME | REAL | L | MAIN | Time value to be assigned to spouts |
| POCKSET | SS | G | N/A | Selection set of pockets as entered by user |
| POCKSURFSET | SS | G | N/A | Selection set containing current pocket's surface entity |
| CELLSET | SS | L | DOINT | Selection set containing current spout's profile region |
| RESULTSET | SS | L | MAIN, DOINT | Selection set returned by SOLINT with intersected region |
| FILENAME | STRING | G | N/A | The output filename entered by user |
| MESSAGE | STRING | L | MY_ERROR | Message to the user when an error occurs... |

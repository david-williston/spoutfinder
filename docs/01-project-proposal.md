# Part 1: Project Proposal

**CAD/CAM Proposal for Final Project: Data File Definition and Creation for Shoe Sole Manufacturing System**

**Prepared for:**

- Mr. Phil Dollan, Project Advisor
- Mr. Don Steele, Communications Instructor
- Mr. Tim Peachey, Internal Sponsor, BCIT Technology Centre
- Wetless Aqua Gear, Industry Client

**By:** David J. Williston, set MECH 4A, Student of BCIT CAD/CAM Technology

**Date:** January 23 1994

## Background

Wetless Aqua Gear would like to convert a manual process into an automatic one. The product they are making is a PVC plastic shoe sole. The soles are created by pouring a special formulation of liquid PVC plastic into various reservoirs of open flat molds, then curing or cross-linking them in an oven.

Currently, the different colors and densities of plastic are poured into the pockets to fill the molds by hand. This manual process is time consuming and not cost effective. An automated pouring process would increase the production of the PVC plastic shoe soles and ensure a consistent, high-quality product.

The specifications for this automated pouring machine have been roughly sketched. If the pouring machine were built, what information would it require to perform its task? What would be the content and format of the data files it would use? And how can we extract this information from 3D computer representations of the soles/molds to be created? These problems will be resolved within the scope of this project.

## Benefits

This project has many direct and indirect benefits, namely:

- Increased product supply to meet demand.
- Decreased losses due to human error.
- Increased data integrity by using a single AutoCAD datafile for:
    - Creation of pouring machine data files
    - CNC milling of molds
    - Materials accounting
    - Product evaluation & testing
    - Decreased design cycle time

## Project Details

There will be six phases to this project:

1. Determine the information required to perform the pouring process.
2. Determine how the information will be extracted from a 3D design file.
3. Determine the output format (ie. structure of data) of the extracted data file.
4. Write an Autolisp routine to output the data in the determined format.
5. Test the validity of the output data file via simulation.
6. Document the algorithms and methods used to extract the data file. (concurrent)

*Figure 1: Proposed production line shows mold plates moving under spouts and into an oven. (Drawing not reproduced here.)*

*Figure 2: Typical molding showing the front portion of shoe sole. (Drawing not reproduced here.)*

*Figure 3: Mold plate moving under pouring spouts (third spout is active). (Drawing not reproduced here.)*

## Resources / Equipment / Budget

**Software:**

- AutoCAD R12
- AutoCAD AME (Advanced Modeling Extension)
- AutoLISP

**Hardware:**

- 486DX25 computer system

All software and hardware will be provided by BCIT.

## Project Schedule

| Weeks | Tasks / Goals | Dates |
|---|---|---|
| 2 | Study AME model creation & Prepare representative solid models. | Jan 20 - Feb 3 |
| 2 | Study AutoCAD solids data structure and AutoLISP access. | Feb 3 - Feb 17 |
| 2 | Determine data output requirements. | Feb 17 - Mar 3 |
| 1 | Define output file format. | Mar 3 - Mar 10 |
| 1 | Pseudocode data extraction algorithm. | Mar 10 - Mar 17 |
| 5 | Code data extraction program. | Mar 17 - Apr 21 |
| 2 | Test and Debug. | Apr 21 - May 5 |
| 1 | Prepare final project report. | May 5 - May 9 |
| 1 | Final Project Presentation and Oral Report. | May 9 - May 16 |
| 16 total |  |  |

Intermediate project goals include:

- Weekly meetings with Tim Peachey at Technology Center to discuss progress.
- Documentation of progress in Journal format.
- Five status reports to BCIT and Tim Peachey.
- Final project report.

## Project Timeline

| Task & Dates | Jan20 | Feb03 | Feb17 | Mar03 | Mar10 | Mar17 | Apr21 | May05 | May09 | May16 |
|---|---|---|---|---|---|---|---|---|---|---|
| Documentation | X | X | X | X | X | X | X | X | X |  |
| Study Acad Solid Modelling Techniques | X | X |  |  |  |  |  |  |  |  |
| Study Acad Solid Modelling Data Structure |  | X | X |  |  |  |  |  |  |  |
| Determine Data Requirements |  |  | X | X |  |  |  |  |  |  |
| Define Output File Format |  |  |  | X | X |  |  |  |  |  |
| Pseudo Code Algorithm |  |  |  |  | X | X |  |  |  |  |
| Code Program |  |  |  |  |  | X | X |  |  |  |
| Test & Debug |  |  |  |  |  |  | X | X |  |  |
| Prepare Final Report |  |  |  |  |  |  |  | X | X |  |
| Final Presentation |  |  |  |  |  |  |  |  | X | X |

# Part 2: Progress Report #1

**Progress Report #1: Datafile Definition & Creation for Mold Pouring Machine**

**For:**

- Phil Dollan, Faculty Supervisor
- Tim Peachey, Sponsor
- Wetless Aqua Gear, Industry Client

**By:** David Suggitt, BCIT CAD/CAM Student MECH4A

**Report Period:** Jan 20 - Feb 24 1994

**Date:** February 21 1994

## Project Description

This project involves the creation of an AutoLISP program to output a data file for the control of a shoe sole mold pouring machine. A more complete description is listed in the project proposal.

## Report Content

In this report I will discuss:

- Work completed
- Current Activities
- Progress
- Work to be completed

## Work Completed

I have successfully completed the:

- Study of AME solid modeling techniques
- Preparation of a Representative Solid Model

Through my study of AME solid modeling techniques I have created a good representative model from which to work. It contains most of the geometry which may be encountered in other moldings. I have also become skilled in the creation of solid models, and have documented guidelines for creating solids for the application I am to develop.

## Current Activities

I am in the process of completing and/or am currently working on:

- Modifications to Representative Model
- Study of AME data structure
- AutoLISP access to AME data
- Determination of Data Requirements

In examination of the problem, it was apparent that the solid model must be modified to aid the extraction of required information. This does not change the shape of the model, rather it will break the model into discrete square columns. These columns will allow us to determine valid and invalid pouring regions. Those regions which may be poured into are classified by the material they intersect. If they intersect the outer edges of a region they are classified as Orphan Cells. Otherwise, they are Parent Cells. Parent Cells are distinguished by a completely square top view. It is this geometry which allows us to safely locate and activate a pouring spout above. Orphan Cells, on the other hand, do not have a square appearance from the top view, and therefore are not good sites to pour from. Rather, they must be 'Adopted' by an adjacent Parent Cell in order for their volume to be accounted for. Once the model has been modified then I can efficiently study the way AutoCAD stores these column blocks. Direct comparison of Parent and Orphan Cells data will also enable me to master the functions I will need to use later.

A list of data requirements has been roughly sketched and I will be discussing it with Tim Peachey, my Sponsor, at our weekly meeting this Thursday. The data requirements will include such things as:

- x,y centroid location of Parent Cells
- Combined Volume of Parent & associated Adopted Cells
- Valve Cycle Times

## Progress

Upon initial inspection the project is approximately 1 week behind schedule. However, some of the future steps have been worked on before their scheduled start. For example, the Pseudo Coding of a Programming Algorithm will be completed via work currently being done, and I predict that actual coding may begin ahead of schedule as well.

## Work to be done

In addition to the work to be completed from this report period, I will have finalized the Data Requirements Determination, and will have outlined the format of the data file to be generated later by an AutoLISP program.

## Summary

The project is more or less on schedule and no major difficulties have been encountered.

---
title: "About this archive"
ShowToc: false
---

This site is a small museum exhibit. It preserves a student engineering
project from 1994: the paperwork, the program and the reasoning behind both.
The original pages were printed on paper and have been transcribed from
photographs, so a few lines are inferred where a thumb covered the page.

## The problem the project set out to solve

A company, Wetless Aqua Gear, made PVC plastic shoe soles by pouring liquid
PVC of different colors and densities into the pockets of open, flat molds,
then curing them in an oven. The pouring was done by hand. It was slow and
costly, and it depended on people getting every pocket right.

A pouring machine could do it, if it knew **where each spout should go**. That
meant getting the answer out of the 3D design of the sole itself, so the
design file, and not a person with a ruler, drove the machine.

## What the student built

SpoutFinder is an AutoLISP program that ran inside AutoCAD Release 12 with
the Advanced Modeling Extension (AME). You selected the mold pockets. The
program stepped a grid of spouts across each pocket and, at each position,
drew a circle the size of a spout and intersected it with the pocket's
surface. If the overlap was nearly a full circle, the spout fit. The valid
positions were written to a plain text file, separated by spaces, for the
machine to read.

## Why it still makes a good story

- One drawing was meant to serve everything: the pouring machine, the CNC
  milling of the molds, the materials accounting and the product testing.
- The whole thing ran on a single desktop PC that the college provided.
- The code carries the marks of its time: comments about running out of
  selection sets, and a routine that purges erased solids so the drawing
  file does not swell. These were the limits the author worked inside.

## Where to look next

- [Context](../context/): what computing looked like in 1994
- [Documents](../docs/): the proposal, progress report, final report and variable listing
- [Source](../source/): the AutoLISP listing, pages 19 to 26 of the original
- [Architecture](../architecture/): how the functions fit together, drawn today

## What is missing

Pages 1 to 18 of the program listing, which include the `GO` command that
started it all, have not been transcribed. For now the code is a fragment: it
can be read and studied, but not loaded and run.

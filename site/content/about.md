---
title: "About"
ShowToc: false
---

## The problem

Wetless Aqua Gear makes PVC plastic shoe soles by pouring liquid PVC of
different colors and densities into the pockets of open flat molds, then
curing them in an oven. Filling the pockets by hand is slow and costly. An
automatic pouring machine needs to know **where to place its spouts**, and
that information has to come from the 3D design of the sole.

## The solution

SpoutFinder is an AutoLISP program running inside AutoCAD R12 with the
Advanced Modeling Extension (AME). The user selects the mold pockets; the
program steps a grid of spouts across each pocket, intersects a spout-sized
circle with the pocket's surface region, and accepts a location when the
intersection area is within a tolerance of a full circle. Valid locations
are written to a space-delimited `.sdf` data file for the machine.

## Why it was worth doing

- Increased product supply to meet demand
- Fewer losses from human error
- One AutoCAD data file drives pouring-machine data, CNC milling, materials
  accounting and product testing

## What is here

- [Documents](../docs/): the proposal, progress report, final report and variable listing
- [Source](../source/): the AutoLISP listing, pages 19 to 26 of the original
- [Architecture](../architecture/): how the functions fit together

The listing here is partial: pages 1 to 18 (including the `GO` entry point)
are not yet transcribed, so the program cannot be loaded as it stands.

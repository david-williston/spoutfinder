---
title: "Context: computing in 1994"
ShowToc: false
---

To read this project well, it helps to picture the machine it ran on.

## The workstation

The proposal lists the whole kit: **AutoCAD R12**, its **AME** solid-modeling
extension, **AutoLISP**, and one **486DX25** computer. The 25 stands for
megahertz. Today a phone is thousands of times faster. AutoCAD R12 shipped in
a DOS version driven by typing commands, with a menu down the right side of
the screen and a command line at the bottom. This site borrows that look.

## Slow and scarce

Solid modeling was heavy work for a machine of that class. Each boolean
operation on solids took real time, and the program does hundreds of them: a
circle against a pocket for every spout position. The listing shows the author
managing the machine's limits by hand:

- clearing selection sets so AutoLISP "does not run out" of them;
- erasing each temporary region and purging the erased solids from the drawing
  every few cycles;
- testing a cheap bounding box before doing the costly intersection.

Those are the habits of programming when every resource was counted.

## Paper, not pixels

The proposal, progress report and final report were typed and printed on
paper and handed to a supervisor, a sponsor and the client. There was
no cloud and no shared document. The program was likewise a printed listing,
which is why only eight pages of it survive here, as photographs.

## Before "printing" meant 3D

Making a physical part from a computer model was industrial and rare. The word
"printing" still meant ink on paper, and the idea of a desktop machine that
builds objects was not yet in everyday talk. The project sits at the other end
of that story: it does not make a part, it works out where a machine should
pour, from a design held in a file.

## The point of the exercise

Reading the project today, the striking thing is how much thinking went into a
few hundred lines of code, because there was no room to be careless. A
sponsor, a deadline and a 486 were enough to get a useful tool built.

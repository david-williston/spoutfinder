---
title: "Run SpoutFinder"
ShowToc: false
summary: "Watch the algorithm work through the prototype's pockets"
---

This is the program's method running live, on the shape of the real prototype
sole. Each colored region is a mold pocket. For every pocket the program walks
a grid of candidate spout positions. At each one it draws a circle the size of
a spout, intersects it with the pocket, and accepts the spout if the overlap
comes within the accuracy tolerance of a full circle. The settings are fixed,
as in the program's default run. Press **RUN** and watch.

{{< runner >}}

## What you are seeing

- **Yellow circle:** the position being tested. The filled part is the
  overlap with the pocket, the same quantity `check` measures with `SOLAREA`.
- **Green circle with a cross:** a valid location. A spout can go here.
- **Dashed red circle:** rejected. It overlaps the pocket, but by less than a
  full circle.
- **Positions with no overlap at all** are skipped without a mark, like the
  empty result `SOLINT` returns when the circle is outside the pocket.
- **The bounding-box skip** is the cheap pre-check in
  [`seeiflocal`](../source/pocket/#seeiflocal): positions far from a pocket
  are never tested.
- **The text file** at the end has the shape `output` writes: one line per
  increment, one entry per spout, a pocket number where a spout fits and `0`
  where it does not. In the original, the pocket's entity name stood in for
  the number.

The logic mirrors the transcribed code in [`intersect.lsp`](../source/intersect/)
and [`locations.lsp`](../source/locations/). The areas are measured by sampling
points rather than by AME's solid modeler, and the shapes are traced from a
photograph, so treat the numbers as an illustration.

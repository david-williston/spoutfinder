# spoutfinder

SpoutFinder V1.0: an AutoLISP program for AutoCAD with AME (Advanced Modeling
Extension), written as a 1994 BCIT CAD/CAM final project. For a selected set of
mold pockets, it steps a grid of pouring spouts across each pocket, tests each
location by intersecting a spout-sized circle with the pocket's surface region,
and writes the valid locations to a space-delimited `.sdf` data file.

## Layout

| Path | Contents | Original pages |
| --- | --- | --- |
| `src/getparams.lsp` | Parameter prompts (tail of `getparams`) | 19-20 |
| `src/pocket.lsp` | `pocketsurf`, `pocketvolume`, `seeiflocal` | 20 |
| `src/intersect.lsp` | `doint`, `check` (the area-based validity test) | 21-22 |
| `src/locations.lsp` | `buildlist`, `nextspout`, `nextrow`, `combine` | 23-24 |
| `src/session.lsp` | `my_reset`, `my_error`, `setdefaults` | 25 |
| `src/output.lsp` | `output`, startup banner | 26 |
| `docs/` | Proposal, progress report, final report, variable listing (see `docs/README.md`) | 27 |

See [docs/architecture.md](docs/architecture.md) for a diagram of how the pieces fit together.

## Website

The `site/` directory is a Hugo site using the PaperMod theme (a git submodule).
Run `python3 site/sync.py` to regenerate its content from `docs/` and `src/`, then
`hugo server --source site`. Clone with `--recurse-submodules` to get the theme.

## Status

This is a transcription of printed pages 19-26 of the listing. Pages 1-18 are
not included, so the `GO` entry point (`main`), the setup routine, and the
first part of `getparams` are missing and the files cannot be loaded as a
working program yet. Code is transcribed as printed, original quirks included
(for example `yx` in the local list of `seeiflocal`, where `yc` is used).

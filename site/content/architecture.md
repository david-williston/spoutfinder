---
title: "Architecture"
weight: 0
---

Boxes are grouped by file in `src/`. The `GO` entry point (`main`) is on the
missing pages 1-18, so its calls (dashed arrows) are inferred from the variable
listing and the function comments; solid arrows are calls visible in the code.

```mermaid
flowchart TD
    subgraph missing["pages 1-18 (not transcribed)"]
        main["main / GO"]
        setup["mysetup"]
    end

    subgraph session["session.lsp"]
        setdefaults
        my_error
        my_reset
    end

    subgraph getparams["getparams.lsp"]
        gp["getparams<br/>(prompts, valid area, select pockets)"]
    end

    subgraph pocket["pocket.lsp"]
        pocketsurf
        pocketvolume
        seeiflocal
    end

    subgraph intersect["intersect.lsp"]
        doint
        check
    end

    subgraph locations["locations.lsp"]
        nextspout
        nextrow
        buildlist
        combine
    end

    subgraph output["output.lsp"]
        out["output<br/>(writes .sdf file)"]
    end

    main -.-> setup
    main -.-> setdefaults
    main -.-> gp
    main -.->|"per pocket"| pocketsurf
    main -.-> pocketvolume
    main -.->|"per spout location"| seeiflocal
    seeiflocal -.->|"inside bounding box"| doint
    main -.-> doint
    doint -->|"resultset"| check
    check -->|"validity"| buildlist
    main -.-> nextspout
    main -.-> nextrow
    main -.->|"after each pocket"| combine
    main -.-> out
    main -.-> my_reset
    my_error --> my_reset
```

## Data flow

```mermaid
flowchart LR
    P["pockets selected<br/>(pockset)"] --> S["pocket surface region<br/>(pocksurfset)"]
    S --> G["step spout grid<br/>(stp: nextspout / nextrow)"]
    G --> I["circle ∩ surface<br/>(doint)"]
    I --> V["area test<br/>(check, accuracy)"]
    V --> T["per-pocket list<br/>(templist)"]
    T --> C["merge pockets<br/>(combinedlist)"]
    C --> F[".sdf file<br/>(output)"]
```

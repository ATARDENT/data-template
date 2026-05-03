# Dataset Template

A standardised template for managing ML datasets — from raw source through validation, compilation, and storage. Clone this repo to create a new dataset store that plugs directly into the research pipeline.

---

## Repository structure

```
.
├── dataset/                  # Raw dataset (source layer)
│   ├── source.yaml           # Declares storage location: GitHub or remote URL
│   ├── download.py           # Script to fetch the dataset if stored remotely
│   └── <data files>          # Raw files, if small enough to store on GitHub
│
├── pre-rules/                # Pre-compilation validation
│   ├── metadata.yaml         # Dataset schema: types, expected shape, field definitions
│   └── validate.py           # Runs checks on the raw dataset; exits non-zero on failure
│
├── script/                   # Compilation logic
│   └── compile.py            # Transforms raw data → trainable dataset format
│
├── post-rules/               # Post-compilation validation
│   ├── metadata.yaml         # Expected schema of the compiled output
│   └── validate.py           # Validates the compiled dataset; exits non-zero on failure
│
└── configuration.yaml        # Pipeline control (see below)
```

---

## Configuration

`configuration.yaml` controls the pipeline behaviour for each dataset version.

```yaml
version: "1.0.0"

compile: true                  # Set false to skip Steps 3–5 entirely

output:
  name: "my-dataset-train"     # Name of the compiled dataset artifact
  destination: github          # github | gdrive
  branch: datasets             # GitHub branch to push to (if destination: github)
  folder_id: ""                # Google Drive folder ID (if destination: gdrive)

tag:
  enabled: true                # Create a Git tag after a successful store
  prefix: "dataset"            # Tag format: <prefix>-v<version>  e.g. dataset-v1.0.0
```

---

## Pipeline

```
Step 1 — Clone        Fetch the raw dataset (via download.py if remote)
Step 2 — Pre-validate Run pre-rules/validate.py on the raw data
Step 3 — Compile      Run script/compile.py  [only if compile: true]
          └─ Post-validate  Run post-rules/validate.py on the compiled output
Step 4 — Store        Push the compiled dataset to the configured destination
Step 5 — Tag          Create a Git tag  <prefix>-v<version>  on the target branch
```

**Steps 3–5 are gated on merge.** To avoid abusing CI resources, compilation, storage, and tagging only run when a pull request is merged into the main branch. On regular pushes and open PRs, the pipeline runs Steps 1–2 only (clone + validate), giving fast feedback without triggering expensive operations.

**Validation gates compilation.** Step 3 will not start unless Step 2 exits successfully. Similarly, Step 4 will not run unless post-validation passes. A failed validation in either gate aborts the pipeline and surfaces the error in CI.

**Tagging creates a reproducible reference.** Step 5 writes a Git tag in the format `<prefix>-v<version>` (e.g. `dataset-v1.0.0`) on the storage branch after a successful store. This ties the compiled artifact permanently to the `version` field in `configuration.yaml`, making any past dataset version fully reproducible from CI history.

---

## Implementing this template

1. **Declare your source** — Edit `dataset/source.yaml` to point at a GitHub path or a remote download URL. Add raw files directly to `dataset/` if they are small enough to store on GitHub.

2. **Define your schema** — Fill in `pre-rules/metadata.yaml` with the expected structure of the raw data (column names, types, row count bounds, etc.). Do the same for `post-rules/metadata.yaml` for the compiled output.

3. **Write your validators** — Implement `pre-rules/validate.py` and `post-rules/validate.py`. Both scripts should exit with code `0` on success and a non-zero code with a descriptive error message on failure.

4. **Write your compilation script** — Implement `script/compile.py` to transform the raw dataset into the format your training pipeline expects.

5. **Configure the pipeline** — Set `compile`, `version`, `output`, and `tag` fields in `configuration.yaml` for your dataset.

---

## CI behaviour summary

| Event | Steps run |
|---|---|
| Push / pull request | Clone → Pre-validate |
| Merge to main | Clone → Pre-validate → Compile → Post-validate → Store → Tag |
---
name: ml-cv
description: Defaults for ML and computer-vision work - project scope, layout, data splits, seeding, model outputs and losses, pretrained models, checkpoints, run records, checks, evaluation. Use in projects whose CLAUDE.md says "Project type: ml-cv", when planning or building data pipelines, models, training, fine-tuning or evaluation.
---

# ML/CV defaults

Defaults with reasons, not absolute rules. The project's decisions file overrides them. Every decision here was
walked with the owner (`<brain>/_harness/decisions.md`, 2026-11-27).

## At project setup: ask, then record in the decisions file

1. **Scope.** What does the brief ask for: an off-the-shelf model only, a fine-tuning *proposal* only, fine-tuning,
   or training from scratch? Don't assume (a take-home may ask for off-the-shelf + a proposal only).
2. **Split unit.** What counts as a new, unseen case where the model will be used: an image, scene, video, patient,
   site, time period? Suggest an answer with its reason; the owner decides. Neighbouring video frames or one
   patient's scans in both train and test inflate the score.
3. **Check tier.** Propose which check tiers apply (below), with the reason and the cost; the owner agrees or
   changes it. Re-propose at milestones (before a long run series, before reporting results) if the stakes changed.
4. **Learning areas** and **licences**: see the global CLAUDE.md and `/harness:licence-check`.

## Layout

- One package per stage: `config`, `data`, `models`, `train`, `evaluate`. Each stage has a thin wiring function
  (`setup_*`) that builds objects, and a worker module (`*_proc`) that does the work, so the work can be tested with
  tiny inputs.
- A single script or notebook keeps the same split as functions in one file.

## Variants and ablations

- Compare variants from one class with feature switches (`UNet(residual=False)`), named by an Enum and built
  through a dict: `MODEL_MAP[choice]()`. The same for losses, backbones and pretrained weights.
- CLI choices come from the Enum: `choices=[m.name for m in ModelSelection]`.
- Guard test: `assert set(MODEL_MAP) == set(ModelSelection)`, so a variant added to only one of the two fails fast.

## Data

- **Seeding.** One seed constant. Seed `torch`, `numpy` and `random` from it. Give the split and the train loader
  their own `torch.Generator()` and a `seed_worker` `worker_init_fn` (PyTorch reproducibility note).
  `torch.manual_seed()` returns the *global* generator, so passing it shares one stream with model init.
  Full determinism (`torch.use_deterministic_algorithms(True)`, `cudnn.benchmark = False`) is an opt-in switch: slower.
- **Sorted file lists** before any seeded split (`sorted(os.listdir(...))`).
- **Bad files.** A pre-flight scan opens every file once, writes a manifest of good files and a report of bad ones;
  the dataset is built from the manifest. Never substitute another sample silently.
- **Augmentation.** Training split only. Joint transforms, so image and mask get the same random operation. Choose
  each augmentation from what the task is invariant to, and record why. Look at a page of augmented samples first.

## Models, losses, metrics: check the contract

At each connection from a model's output to a loss, a metric or a pretrained head, run `/harness:library-check` for
the installed version: logits or probabilities, channel layout, argument order, what happens with one channel or
an empty mask. Write the answer as a comment at the wiring line.

Worked example (MONAI source): `DiceCELoss` with one channel uses `BCEWithLogitsLoss`, so it expects logits;
`FocalLoss` says "The input should be the original logits". In MONAI 1.3.2–1.5.0, `SoftclDiceLoss` sums over
`[:, 1:, ...]` (one channel → constant loss) and takes `forward(y_true, y_pred)`. A model ending in `sigmoid` fed
into these trains badly with no error.

## Pretrained models

- When an off-the-shelf model exists for the task, evaluate it as a baseline, even if the project trains its own.
- Load weights through the library's current API (torchvision `weights=`, not the deprecated `pretrained=True`)
  and use the transforms bundled with them (`weights.transforms()`). torchvision: "Using the correct preprocessing
  method is critical and failing to do so may lead to decreased accuracy or incorrect outputs."
- Record the weights' name, version, source and licence. Record freeze vs fine-tune (which layers) and why:
  dataset size and how close it is to the pretraining data.

## Hyperparameters

Every hyperparameter carries a source tag: `# paper (cite)`, `# library default`, `# tuned: <how>`, or
`# guess`. Guesses are reported to the owner as proposals. In ML, these are not "small details".

## Checks, in tiers (agreed with the owner per project)

| Tier | What | Cost |
|---|---|---|
| 1 · Basics | lint, types, imports, one forward pass with shape checks, the guard test, finite loss | seconds |
| 2 · Can it learn | before any run over ~10 min: one batch through every variant; every loss finite, non-constant, nonzero gradients; the model can overfit one batch. Kept as a pytest test | ~1 min GPU |
| 3 · Does it look right | log input \| target \| prediction grids for a **fixed** batch at each validation; view them and name one failure the metric misses | tokens + minutes |

## Training and runs

- **Checkpoints.** Always save the best validation epoch (`deepcopy(model.state_dict())`: `state_dict()` returns
  references). Long runs also save a resumable checkpoint: model, optimizer state, epoch. Every reported result
  names the checkpoint it came from.
- **Run record.** Run identity in file and log names: `{model}_{loss}_{data}-{size}_{epochs}`. Each run folder holds
  a `run.json`: all settings (defaults included), git commit hash, library versions, GPU name.
- **Logging.** Text events through `logging` into a log file in the run folder (see `python-conventions`); metrics
  and image grids in TensorBoard.

## Evaluation

How far to go is agreed in the tier conversation.
- A trivial baseline (constant or dummy) and a strong standard one (classical algorithm, stock or pretrained model).
- The main metric next to one that covers its blind spot (for thin structures, a topology score next to Dice).
- In-domain, and on a shifted set when one exists. A cross-domain test can change which model wins.

## Estimates

A card's estimate covers build time. GPU run time is estimated separately and logged with kind `experiment`:
`py -3 <harness>/tools/log_estimate.py <project> <plan> <card> experiment <model> <estimate_min> <actual_min>`.

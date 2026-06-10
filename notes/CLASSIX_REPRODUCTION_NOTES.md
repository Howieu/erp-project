# CLASSIX Minimal Reproduction Notes

This is a small reproducible benchmark for learning and verifying CLASSIX before moving to RetailRocket.

## What the Script Does

- Builds three standard synthetic datasets: 2D blobs, 10D blobs, and two moons.
- Standardises every dataset before clustering.
- Compares CLASSIX, K-Means++, and DBSCAN using ARI, NMI, Silhouette, Davies-Bouldin, Calinski-Harabasz, runtime, cluster count, and noise count.
- Runs a small CLASSIX radius grid to show parameter sensitivity.
- Saves one `CLASSIX.explain()` output as text.

## How to Run

Using the project `.venv` that currently has CLASSIX installed:

```bash
.venv/bin/python reproduce_classix_minimal.py
```

Using your own `myenv`, replace the Python path:

```bash
/path/to/myenv/bin/python -m pip install classixclustering
/path/to/myenv/bin/python reproduce_classix_minimal.py
```

## Outputs

- `results/classix_minimal/benchmark_metrics.csv`
- `results/classix_minimal/classix_explain_blobs_2d.txt`
- `results/official_classix_shape_subset/shape_subset_compare_with_official.csv`
- `results/official_classix_shape_subset/shape_subset_reproduced_ari.csv`
- `results/official_classix_shape_subset/shape_subset_reproduced_ami.csv`

## Official Repository Reproduction

The official repository has been cloned to:

```text
official_classix/
```

The full official experiment runner is:

```bash
cd official_classix/exps
python3 run_exp_main.py
```

However, the full runner requires `hdbscan` and a compiled `Quickshift++` implementation, and it runs seven experiment groups. For the dissertation timeline, the practical reproduction is the official shape benchmark subset:

```bash
.venv/bin/python reproduce_official_classix_shape_subset.py
```

This script uses the official `exps/data/Shape sets` datasets and the official parameters from `exps/run_shape_bk.py`, then compares the reproduced ARI/AMI values with the official CSV files in `exps/results/exp4`.

Result of the current run:

- CLASSIX distance/density matches the official ARI/AMI values up to floating-point precision.
- DBSCAN also matches up to floating-point precision.
- K-Means++ has small differences under the current scikit-learn version; the largest absolute ARI/AMI difference is about `0.0169`.

## How to Use This in the Dissertation

- Treat this as the first reproducibility check, not the full project experiment.
- Use the CLASSIX radius grid results to motivate the later parameter sensitivity section.
- Use `classix_explain_blobs_2d.txt` as an example of the type of explanation CLASSIX provides.
- Use the official shape subset comparison as evidence that the CLASSIX benchmark behaviour was reproduced locally.
- Next step: replace the synthetic datasets with the RetailRocket user-level feature matrix and keep the same evaluation table format.

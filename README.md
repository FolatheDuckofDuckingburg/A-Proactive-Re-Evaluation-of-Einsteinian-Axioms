# A Provocative Re-Evaluation of Einsteinian Axioms
### An Assumption-Stress-Testing Framework for Speculative Foundations of Physics

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0007--2148--5675-green.svg)](https://orcid.org/0009-0007-2148-5675)

This repository explores **Assumption Stress Testing (AST)** as a method for making assumptions explicit, tracing their consequences, and separating mathematical consistency from empirical support. It is an independent research project; the code here is exploratory and does not establish a new physical theory.

## Core principles

Successful empirical predictions do not by themselves prove that a theory is fundamental. Likewise, an incomplete theory is not automatically wrong. These are methodological reminders, not claims that General Relativity is invalid. Any proposed successor model should recover established results in regimes where those results have been tested.

## Computational toy model: synthetic graph recovery

The script `ast_metric_induction.py` runs a controlled synthetic benchmark:

1. A circular correlation structure is **planted in a Gaussian covariance matrix**.
2. Synthetic observations are sampled from that covariance.
3. Pairwise mutual information is estimated under a bivariate-Gaussian assumption.
4. A graph is inferred from each node's two highest mutual-information scores.
5. Edge precision, recall, and F1 are reported against the known planted ring.

This is a graph-recovery toy model—not a demonstration that spacetime emerges from information. See `docs/MODEL_LIMITATIONS.md` for assumptions and limits.

## Install and run

Python 3.8+ is recommended. Install dependencies:

```bash
python -m pip install numpy matplotlib networkx
```

Run with a plot:

```bash
python ast_metric_induction.py
```

Run without a plot:

```bash
python ast_metric_induction.py --no-plot --nodes 24 --samples 4000 --seed 42
```

Run unit tests:

```bash
python -m unittest discover -s tests -v
```

## Research status

The current script tests a software pipeline on synthetic data only. It does not validate a physical spacetime model, establish emergence, or show that AST is a novel research contribution. Those require explicit comparison with existing literature and a physical model with testable consequences.

## Author

- **Author:** Folarera Kassim
- **ORCID:** [0009-0007-2148-5675](https://orcid.org/0009-0007-2148-5675)

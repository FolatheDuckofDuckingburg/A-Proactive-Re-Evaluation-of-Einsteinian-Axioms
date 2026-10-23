# Scope and limitations of the AST graph-recovery toy model

## What the code does

1. Plants a circular correlation structure by setting a Gaussian covariance matrix to
   Sigma[i,j] = exp(-d[i,j]/ell), where d is shortest circular distance and ell > 0.
2. Samples multivariate Gaussian observations from that covariance.
3. Estimates pairwise mutual information under a bivariate-Gaussian assumption:
   I(X;Y) = -0.5 log(1-r^2), where r is sample correlation.
4. Connects each node to its two highest-scoring mutual-information neighbours.
5. Reports edge precision, recall, and F1 against the known planted ring.

## What this does not establish

- It does not calculate mutual information from neural, cosmological, or other physical data.
- It does not derive a metric tensor, spacetime dynamics, causal structure, or Einstein field equations.
- It does not demonstrate that spacetime emerges from information.
- The target ring is encoded in the covariance used to generate the data. This is recovery of
  a known synthetic structure, not spontaneous emergence of an unknown one.
- The Gaussian MI formula assumes a bivariate-Gaussian model; it is not a universal estimator.
- The spring-layout picture in the previous version was a visualization algorithm, not a
  physical derivation of geometry.

## Appropriate interpretation

This is a reproducible software sanity-check for a narrow graph-recovery pipeline. Robustness
should be assessed across multiple seeds, sample sizes, and length scales. Physical claims
would require a separately specified physical model, observables, derivation, and comparison
with empirical constraints.

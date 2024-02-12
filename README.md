# DynaMITE_FasterMeanEstimation

## Introduction

We introduce a novel statistical measure for MCMC-mean estimation, the inter-trace variance ${\rm trv}^{(\tau{\rm rel})}({\cal M},f)$, which  depends on a Markov chain ${\cal M}$ and a function $f:S \to [a,b]$. We show that the inter-trace variance 
can be efficiently estimated from observed data, and that it leads to a more efficient MCMC-mean estimator, with complexity competitive with a lower-bound obtained from the central limit theorem of Markov chains. 
Most efficient MCMC mean-estimators receive, as input, upper-bounds on chain-dependent terms like mixing time $\tau_{\rm mix}$ or relaxation time $\tau_{\rm rel}$, and often also function-dependent terms such as the stationary variance $v_{\pi}$, and their performance is highly dependent to the sharpness of these bounds.
 In contrast, we introduce DynaMITE, which dynamically adjusts the sample size using the observed data, and 
therefore is less sensitive to the looseness of input upper-bounds on $\tau_{\rm rel}$, 
and requires no bound on $v_{\pi}$.


## Reproduce the experiments

- All the code is available in the directory `src/`
- Required packages and dependencies are in `requirements.txt`
- run `python3 ./src/main.py` to get experimental results 
- run `python3 ./src/process_log.py` to process the logging info
- run `python3 ./src/visualize.py` to obtain the corresponding plots
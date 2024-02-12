import numpy as np
# import numpy.random as rng
from abc import ABC, abstractmethod 
# from copy import deepcopy
import os
import logging
import math
from dynamite import *
from mcmcChain import *

def run_dynamite_on_hypercube(n, k, eps, delta):
    Lambda = 1-1/n
    R = k-1
    modValue = lambda x: sum(x)%k
    print(f"n={n}, k={k}, func = sum(x)%k, eps = {eps}, delta = {delta}")
    chain1 = HcubeChain(np.random.randint(0,2,n), n)
    chain2 = HcubeChain(np.random.randint(0,2,n), n)
    dynamiteHcube = Dynamite(chain1 = chain1, chain2 = chain2, Lambda = Lambda, func = modValue, R = R, eps = eps, delta = delta)
    return dynamiteHcube.mean_estimate(), dynamiteHcube.T

if __name__=="__main__":

    log_filename = "../data/output_20240210_01.log"
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    file_handler = logging.FileHandler(log_filename, mode="a", encoding=None, delay=False)
    logging.basicConfig(handlers=[file_handler], level=logging.DEBUG)

    n_list = [5, 8, 10, 15, 20, 30]
    k_list = [2, 3, 4, 5, 10]
    eps_list = [0.1, 0.05, 0.025, 0.0125, 0.00625]
    delta_list = [0.05]

    for eps in eps_list:
        for delta in delta_list:
            for n in n_list:
                for k in k_list:
                    logging.info("----- This is a new run -----")
                    logging.info("parameters: eps = %.6f, delta = %.3f, n = %d, k = %d", eps, delta, n, k)
                    print(f"parameters: eps = {eps}, delta = {delta}, n = {n}, k = {k}")
                    (mu, var, I, b, clen), T = run_dynamite_on_hypercube(n, k, eps, delta)
                    logging.info("outcomes: mu = %.4f, var = %.4f, I = %d, chainlen = %d, T = %d", mu, var, I, clen, T)
                    print(f"outcomes: mu = {mu}, var = {var}, I = {I}, chainlen = {clen}, T = {T}")

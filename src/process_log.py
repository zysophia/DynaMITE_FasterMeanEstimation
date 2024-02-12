import pandas as pd 
import numpy as np 
from collections import Counter

if __name__ == "__main__":

    log_files = ["data/output_20240210_01.log", "data/output_20240210_02.log"]
    output_csv = "data/output_20240210_01.csv"
    
    datalist = []
    for log_file in log_files:
        f = open(log_file, 'r')
        for line in f.readlines():
            ss = line.split(",")
            if ss[0].startswith("INFO:root:parameters: "):
                eps = float(ss[0][ss[0].find("= ")+2:])
                delta = float(ss[1][ss[1].find("= ")+2:])
                n = int(ss[2][ss[2].find("= ")+2:])
                k = int(ss[3][ss[3].find("= ")+2:])
            elif ss[0].startswith("INFO:root:outcomes: "):
                mu = float(ss[0][ss[0].find("= ")+2:])
                var = float(ss[1][ss[1].find("= ")+2:])
                I = int(ss[2][ss[2].find("= ")+2:])
                chainlen = int(ss[3][ss[3].find("= ")+2:])
                T = int(ss[4][ss[4].find("= ")+2:])
            elif ss[0].startswith("INFO:root:timer: "):
                seconds = float(ss[0][ss[0].find("in ")+3:ss[0].find("seconds")])
                datalist.append([n, k, eps, delta, mu, var, I, chainlen, T, seconds])


    df = pd.DataFrame(datalist, columns=["n", "k", "eps", "delta", "mu", "var", "I", "chainlen", "T", "seconds"])
    print(df)  
    df.to_csv(output_csv, index=False)
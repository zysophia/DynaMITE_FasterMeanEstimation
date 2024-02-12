import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
# import matplotlib.patches as patches

palette ={"sum(x) % 2": "darkblue", "sum(x) % 5": "darkgreen", "sum(x) % 10": "darkred"}

sns.set(font_scale = 5)

def lineplot_complexity_vs_eps_HCube():
    df = pd.read_csv("data/output_20240210_01.csv")

    fix_delta = 0.05
    fix_n = 5
    df_sub = df[(df['delta']==fix_delta)&(df['n']==fix_n)]

    fix_eps_list = [0.1, 0.05, 0.025, 0.0125, 0.00625]
    df_sub = df_sub[df_sub["eps"].isin(fix_eps_list)]

    fix_k_list = [2, 5, 10]
    df_sub = df_sub[df_sub["k"].isin(fix_k_list)]

    df_sub["1/$\epsilon$"] = 1/df_sub["eps"]
    df_sub["complexity"] = df_sub["chainlen"] * df_sub["T"] * 2
    df_sub["function"] = df_sub["k"].apply(lambda k: f"sum(x) % {k}")

    plt.figure(figsize=(6,5))
    sns.set_theme(style="darkgrid")
    g = sns.lineplot(x="1/$\epsilon$", y="complexity", hue="function", style = "function", \
        ci=95 ,data=df_sub, markers=True, markersize = 8, dashes=False, linewidth=2, palette=palette)

    g.set_yscale('log')
    g.set_xscale('log')
    plt.grid(True,which="both",ls="--",c='gray', alpha=0.5) 
    
    g.set_xlabel("1/$\epsilon$",fontsize=15)
    g.set_ylabel("complexity",fontsize=15)
    plt.setp(g.get_legend().get_texts(), fontsize='16') # for legend text
    plt.setp(g.get_legend().get_title(), fontsize='19') # for legend title

    plt.show()
    g.figure.savefig(f"figures/lineplot_complexity_vs_eps_HCube_n{fix_n}_delta{fix_delta}.png", dpi=200)

if __name__=="__main__":
    lineplot_complexity_vs_eps_HCube()


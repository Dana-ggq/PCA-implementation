import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd

#cercul corelatiilor
def plot_corelatii(t, var1, var2, titlu="Corelatii factoriale - cercul corelatiilor", aspect='auto'):
    fig = plt.figure(titlu, figsize=(13, 8))
    assert isinstance(fig, plt.Figure)
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": "b"})
    ax.set_xlabel(var1, fontdict={"fontsize": 12, "color": "b"})
    ax.set_ylabel(var2, fontdict={"fontsize": 12, "color": "b"})
    ax.set_aspect(aspect)
    tetha = np.arange(0,np.pi*2,0.01)
    ax.plot( np.cos(tetha),np.sin(tetha),color='b')
    ax.axhline(0)
    ax.axvline(0)
    ax.scatter(t[var1], t[var2], c="r")
    for i in range(len(t)):
        ax.text(t[var1].iloc[i], t[var2].iloc[i], t.index[i])
    # plt.show()

#Corelograma
def corelograma(t, vmin=-1, vmax=1, titlu="Corelatii factoriale - corelograma"):
    fig = plt.figure(titlu, figsize=(11, 10))
    assert isinstance(fig, plt.Figure)
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontsize=16, color='b')
    # rotunjire date la 3 zecimale pentru vizualizare mai usoara
    ax_ = sb.heatmap(t.round(3), vmin=vmin, vmax=vmax, cmap="bwr", annot=True)
    ax_.set_xticklabels(t.columns, rotation=30, ha="right")
    # plt.show()


def plot_instante(t, var1, var2, titlu="Plot instante", aspect='auto'):
    fig = plt.figure(titlu, figsize=(13, 8))
    assert isinstance(fig, plt.Figure)
    ax = fig.add_subplot(1, 1, 1)
    assert isinstance(ax, plt.Axes)
    ax.set_title(titlu, fontdict={"fontsize": 16, "color": "b"})
    ax.set_xlabel(var1, fontdict={"fontsize": 12, "color": "b"})
    ax.set_ylabel(var2, fontdict={"fontsize": 12, "color": "b"})
    ax.set_aspect(aspect)
    ax.scatter(t[var1], t[var2], c="r")
    for i in range(len(t)):
        ax.text(t[var1].iloc[i], t[var2].iloc[i], t.index[i])


#harta componente
def harta(shp, S, camp_legatura, nume_instante, titlu="Harta componente"):
    m = np.shape(S)[1]
    t = pd.DataFrame(data={"coduri": nume_instante})
    for i in range(m):
        t["v" + str(i + 1)] = S[:, i]
    shp1 = pd.merge(shp, t, left_on=camp_legatura, right_on="coduri")
    for i in range(m):
        f = plt.figure(titlu + "-" + str(i + 1), figsize=(10, 7))
        ax = f.add_subplot(1, 1, 1)
        ax.set_title(titlu + "-" + str(i + 1))
        shp1.plot("v" + str(i + 1), cmap="Reds", ax=ax, legend=True)
    #plt.show()
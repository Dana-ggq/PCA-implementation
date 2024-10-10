import numpy as np
from geopandas import GeoDataFrame
from pandas import *
from acp import acp
from func import nan_replace, tabelare_matrice
from grafice import plot_corelatii, corelograma, plot_instante, harta

#Citire fisier de date
t = read_csv("CSV_women_status.csv", index_col=1)
# print(t)
if any(t.isna()):
    nan_replace(t)
t.to_csv("ACP_Output_nongui\\inlocuireNAN.csv")
print(t)
corrMatrix = t.corr()
corelograma(corrMatrix, titlu="Matricea de corelatie")


#Creare lista de variabile observate (variabilele numerice din csv)
variabile = list(t)[2:]
print(variabile)

#Instantiere obiect model ACP
model_acp = acp(t, variabile)
model_acp.creare_model()
#model_acp.creare_model(std=False)
print(model_acp.alfa)

#Variante explicata de fiecare componenta - explicata de valorile proprii pt fiecare componenta
tabel_varianta = model_acp.tabelare_varianta()
tabel_varianta.to_csv("ACP_Output_nongui\\Varianta.csv")
print(tabel_varianta)
#graficul variantei
model_acp.plot_varianta()

#Factorii de corelatie(loadings)
r_xc = model_acp.r_xc
# print(r_xc)
r_xc_t = tabelare_matrice(r_xc, variabile,
                          model_acp.etichete_componente, "ACP_Output_nongui\\r_xc.csv")
#cercul corelatiilor intre var initiale si CP C1 si C2
plot_corelatii(r_xc_t, "comp1", "comp2", aspect=1)
#corelograma factori de corelatie
corelograma(r_xc_t) #Corelatii intre variabilele observate si componentele principale

#Componente principale
c = model_acp.c
c_t = tabelare_matrice(c, t.index, model_acp.etichete_componente, "ACP_Output_nongui\\componente_principale.csv")
#print(model_acp.nrcomp_c, model_acp.nrcomp_k, model_acp.nrcomp_p)

#Numar componente semnif.
nrcomp = model_acp.nrcomp_p
if model_acp.nrcomp_c is not None:
    if model_acp.nrcomp_c<nrcomp:
        nrcomp=model_acp.nrcomp_c
if model_acp.nrcomp_k is not None:
    if model_acp.nrcomp_k<nrcomp:
        nrcomp=model_acp.nrcomp_k
#plot componente
for i in range(1, nrcomp):
    plot_instante(c_t, "comp1", model_acp.etichete_componente[i], aspect=1)

# Calculul scorurilor
# (componentele principale standardizate)
s = c / np.sqrt(model_acp.alfa)
# Tabelare si desenare plot pentru scoruri
t_scoruri = tabelare_matrice(s,t.index,model_acp.etichete_componente,"ACP_Output_nongui\\s.csv")
plot_instante(t_scoruri,"comp1","comp2",titlu="Plot scoruri",aspect=1)

# Calcul cosinusuri
# calitatea reprezentarii observatiilor pe axele de coordonate ale CP
c2 = c * c
cosin = np.transpose(c2.T / np.sum(c2, axis=1))
cosin_t = tabelare_matrice(cosin, t.index,
                           model_acp.etichete_componente, "ACP_Output_nongui\\cosin.csv")

# Calcul contributii -> procente
# contributia observatiilor la varianta axelor componentelor principale
beta = c2 * 100 / np.sum(c2, axis=0)
beta_t = tabelare_matrice(beta, t.index,
                          model_acp.etichete_componente,
                          "ACP_Output_nongui\\contrib.csv")

# Calcul comunalitati (regasirea componentelor principale in variabilele intiale/observate)
#cate componente principale contribuie in mod relevant la fiecare variabila initiala
r_xc2 = r_xc * r_xc
comm = np.cumsum(r_xc2, axis=1)
comm_t = tabelare_matrice(comm, variabile, model_acp.etichete_componente, "ACP_Output_nongui\\comm.csv")
#corelograma comunalitati
corelograma(comm_t, vmin=0, titlu="Comunalitati")

#HARTA WORLD
shp = GeoDataFrame.from_file("World_Simplificat/World.shp")
#print(list(shp),shp["iso_a3"],sep="\n")
harta(shp,c[:,:nrcomp],"iso_a3",c_t.index)

model_acp.show_grafice()

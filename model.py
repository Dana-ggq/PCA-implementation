from PyQt5.QtWidgets import QMainWindow
import PyQt5.QtWidgets as qw
from ACPui import *
import controller
import numpy as np
from geopandas import GeoDataFrame
from pandas import *
from acp import acp
from func import *
from grafice import *


class Frame(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.model_creat = False
        self.t = None
        self.setupUi(self)

        #gestiune click butoane
        #tabele
        self.buton_citire.clicked.connect(self.citire)
        self.buton_selectie.clicked.connect(lambda x: controller.selectie_generala(self.list_variabile))
        self.buton_distributia_variantei.clicked.connect(self.distributia_variantei)
        self.buton_componente_principale.clicked.connect(self.componente_principale)
        self.buton_scoruri.clicked.connect(self.scoruri)
        self.buton_factori_de_corelatie.clicked.connect(self.factori_de_corelatie)
        self.buton_contributiile.clicked.connect(self.contributiile)
        self.buton_cosinusurile.clicked.connect(self.cosinusurile)
        self.buton_comunalitatile.clicked.connect(self.comunalitatile)
        #grafice
        self.buton_plot_varianta.clicked.connect(self.plot_varianta)
        self.buton_plot_scoruri.clicked.connect(self.plot_scoruri)
        self.buton_cercul_corelatiilor.clicked.connect(self.cercul_corelatiilor)
        self.buton_corelatii_factoriale.clicked.connect(self.corelatii_factoriale)
        self.buton_corelograma_comunalitati.clicked.connect(self.corelograma_comunalitati)
        self.buton_harta_componente.clicked.connect(self.harta_componente)

    def harta_componente(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        # PENTRU TARI
        shp = GeoDataFrame.from_file("World_Simplificat/World.shp")
        print("here")
        # print(list(shp),shp["iso_a3"],sep="\n")
        #Afisare harta componente semnificative
        print(self.c[:, :self.nrcomp])
        print(self.c_t.index)
        harta(shp, self.c[:, :self.nrcomp], "iso_a3", self.c_t.index)
        self.model_acp.show_grafice()

    # corelograma_comunalitati
    def corelograma_comunalitati(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        corelograma(self.comm_t, vmin=0, titlu="Comunalitati")
        self.model_acp.show_grafice()

    #corelograma corelatii factoriale
    def corelatii_factoriale(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        # Corelatii intre variabilele observate si componentele principale
        corelograma(self.r_xc_t)
        self.model_acp.show_grafice()

    #cercul_corelatiilor
    def cercul_corelatiilor(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        print("comp" +self.combo_index_AXA1.currentText())
        plot_corelatii(self.r_xc_t, "comp" +self.combo_index_AXA1.currentText(), "comp"+self.combo_index_AXA2.currentText(), aspect=1)
        print("here")
        self.model_acp.show_grafice()

   #plot_scoruri
    def plot_scoruri(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        plot_instante(self.t_scoruri, "comp" +self.combo_index_AXA1.currentText() , "comp"+self.combo_index_AXA2.currentText(), titlu="Plot scoruri", aspect=1)
        self.model_acp.show_grafice()

    #plot varianta
    def plot_varianta(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        #varianta explicata de fiecare componeneta
        self.model_acp.plot_varianta()
        self.model_acp.show_grafice()

    #Comunalitatile
    def comunalitatile(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        # tabelare, salvare csv
        self.comm_t = tabelare_matrice(self.comm, self.variabile, self.model_acp.etichete_componente, "ACP_Output\\comm.csv")
        # afisare tabel
        dialog = controller.DialogNonModal(self, self.comm_t, titlu="Comunalitatile")
        dialog.show()

    #Cosinusurile
    def cosinusurile(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        #tabelare si salvare csv
        cosin_t = tabelare_matrice(self.cosin, self.t.index, self.model_acp.etichete_componente, "ACP_Output\\cosin.csv")

        #afisare tabel
        dialog = controller.DialogNonModal(self, cosin_t, titlu="Cosinusurile")
        dialog.show()

    #Contributiile
    def contributiile(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        # tabelare si salvare csv
        beta_t = tabelare_matrice(self.beta, self.t.index, self.model_acp.etichete_componente, "ACP_Output\\contributii.csv")

        #afisare tabel
        dialog = controller.DialogNonModal(self, beta_t, titlu="Contributiile")
        dialog.show()

    #Factori de corelatie
    def factori_de_corelatie(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        #tabelare si salvare factori csv
        self.r_xc_t = tabelare_matrice(self.r_xc, self.variabile, self.model_acp.etichete_componente, "ACP_Output\\r_xc.csv")

        #afisare tabel
        dialog = controller.DialogNonModal(self, self.r_xc_t, titlu="Factorii de corelatie")
        dialog.show()

    #Scoruri
    def scoruri(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        # tabelare si salvare scoruri csv
        self.t_scoruri = tabelare_matrice(self.s, self.t.index, self.model_acp.etichete_componente,
                                          "ACP_Output\\scoruri.csv")
        #afisare tabel
        dialog = controller.DialogNonModal(self, self.t_scoruri, titlu="Scorurile")
        dialog.show()

    # componente
    def componente_principale(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        #salvare componente in csv
        self.c_t = tabelare_matrice(self.c, self.t.index, self.model_acp.etichete_componente,
                                    "ACP_Output\\componetele_principale.csv")
        # afisare tabel
        dialog = controller.DialogNonModal(self, self.c_t, titlu="Componentele principale")
        dialog.show()

    #tabel varianta
    def distributia_variantei(self):
        if self.model_creat is False:
            if not self.creare_model():
                return
        # Varianta explicata de fiecare componenta
        tabel_varianta = self.model_acp.tabelare_varianta()
        tabel_varianta.to_csv("ACP_Output\\varianta.csv")
        #print(tabel_varianta)

        #afisare tabel
        dialog =controller.DialogNonModal(self, tabel_varianta, titlu="Varianta componentelor")
        dialog.show()

    # Citire fisier de date
    def citire(self):
        rezultat = controller.citire_fisier_variabile(self.list_variabile)
        if rezultat is not None:
            self.t = rezultat
            #inlocuire nan
            if any(self.t.isna()):
                nan_replace(self.t)
            self.schimbare_selectie()

    def schimbare_selectie(self):
        for i in range(self.list_variabile.count()):
            item = self.list_variabile.item(i)
            check = self.list_variabile.itemWidget(item)
            #recreare model var select
            check.stateChanged.connect(self.reset)

    def reset(self):
        self.model_creat = False

    #Creare model ACP
    def creare_model(self):
        #nu s-a citit fisierul
        if self.t is None:
            msgBox = qw.QMessageBox()
            msgBox.setText("Nu au fost citite datele!")
            msgBox.exec()
            return

        #preluare variabile checked
        self.variabile = controller.selectii_lista(self.list_variabile)
        #print(self.variabile)
        self.m = len(self.variabile)
        if self.m < 2:
            msgBox = qw.QMessageBox()
            msgBox.setText("Prea putine variabile selectate!")
            msgBox.exec()
            return

        #populare combo axe
        controller.init_combo(self.combo_index_AXA1, [str(i) for i in range(1, self.m+1)])
        controller.init_combo(self.combo_index_AXA2, [str(i) for i in range(1, self.m+1)])
        self.combo_index_AXA2.setCurrentIndex(1)

        #creare model
        self.model_acp = acp(self.t, self.variabile)
        self.model_acp.creare_model()
        self.model_creat = True

        # Componentele principale
        self.c = self.model_acp.c
        self.c2 = self.c * self.c
        self.c_t = tabelare_matrice(self.c, self.t.index, self.model_acp.etichete_componente)

        # Numar componente semnificative
        self.nrcomp = self.model_acp.nrcomp_p
        if self.model_acp.nrcomp_c is not None:
            if self.model_acp.nrcomp_c < self.nrcomp:
                self.nrcomp = self.model_acp.nrcomp_c
        if self.model_acp.nrcomp_k is not None:
            if self.model_acp.nrcomp_k < self.nrcomp:
                self.nrcomp = self.model_acp.nrcomp_k

        # Scoruri
        # (componentele principale standardizate)
        self.s = self.c / np.sqrt(self.model_acp.alfa)
        self.t_scoruri = tabelare_matrice(self.s, self.t.index, self.model_acp.etichete_componente)

        #Factori de corelatie
        self.r_xc = self.model_acp.r_xc
        self.r_xc_t = tabelare_matrice(self.r_xc, self.variabile, self.model_acp.etichete_componente)

        # Calcul contributii -> procente
        # contributia observatiilor la varianta axelor componentelor principale
        self.beta = self.c2 * 100 / np.sum(self.c2, axis=0)

        # Cosinusuri
        # calitatea reprezentarii observatiilor pe axele de coordonate ale CP
        self.cosin = np.transpose(self.c2.T / np.sum(self.c2, axis=1))

        # Calcul comunalitati (regasirea componentelor principale in variabilele intiale/observate)
        # cate componente principale contribuie in mod relevant la fiecare variabila initiala
        self.r_xc2 = self.r_xc * self.r_xc
        self.comm = np.cumsum(self.r_xc2, axis=1)
        self.comm_t = tabelare_matrice(self.comm, self.variabile, self.model_acp.etichete_componente)

        return True














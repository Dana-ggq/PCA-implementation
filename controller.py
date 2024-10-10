from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd

# Selectie generala intr-o lista de obiecte QCheckBox
# lista - lista QListWidget de obiecte QCheckBox
def selectie_generala(lista):
    for i in range(lista.count()):
        item = lista.item(i)
        check = lista.itemWidget(item)
        assert isinstance(check, QCheckBox)
        check.setChecked(not check.checkState())


# Initializare combo
# combo - QComboBox
# items - lista de siruri
def init_combo(combo, items):
    combo.clear()
    combo.addItems(items)
    combo.setCurrentIndex(0)


# Citire fisier si variabile
# lista - obiect QListWidget
# combo - obiect QComboBox
# Este intors tabelul
def citire_fisier_variabile(lista=None):
        t = pd.read_csv("CSV_women_status.csv", index_col=1)
        #variabilele numerice
        variabile = list(t)[2:]
        if lista is not None:
            lista.clear()
            for v in variabile:
                item = QListWidgetItem(lista)
                cb = QCheckBox(v)
                lista.setItemWidget(item, cb)
        return t


class ModelTabel(QAbstractTableModel):
    def __init__(self, data):
        super(ModelTabel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            coloana = index.column()
            linia = index.row()
            valoare = self._data.iloc[linia, coloana]
            return str(valoare)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data.columns)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class DialogNonModal(QDialog):
    def __init__(self, parent, t, w=900, h=500, titlu="Tabel"):
        QDialog.__init__(self, parent)
        self.setModal(0)

        tabel = QTableView()
        model = ModelTabel(data=t)
        tabel.setModel(model)
        tabel.setFixedSize(w, h)
        layout1 = QHBoxLayout() #lines up w horizontally
        layout1.addWidget(tabel)
        self.setLayout(layout1)

        self.setWindowTitle(titlu)

# Preluare selectii dintr-o lista QListWidget de obiecte QCheckBox
def selectii_lista(lista):
    variabile_selectate = []
    for i in range(lista.count()):
        item = lista.item(i)
        check = lista.itemWidget(item)
        assert isinstance(check, QCheckBox)
        if check.isChecked():
            variabile_selectate.append(check.text())
    return variabile_selectate



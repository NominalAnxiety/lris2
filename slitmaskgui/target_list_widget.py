
#from inputTargets import TargetList
from slitmaskgui.menu_bar import MenuBar
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSlot
from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QVBoxLayout,
    QLabel,


)
class TableModel(QAbstractTableModel):
    def __init__(self, data=[]):

        super().__init__()
        self._data = data
        self.header = ["Name","Priority","Magnitude","Ra","Dec","Center Distance"]
        #MAGMA header is #,target name,priority,magnitude,ra,dec,center distance
    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            #should add something about whether its vertical or horizontal
            if orientation == Qt.Orientation.Horizontal:
                return self.header[section]
        return super().headerData(section, orientation, role)


    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:

            return self._data[index.row()][index.column()]

    def rowCount(self, index):

        return len(self._data)

    def columnCount(self, index):
        
        return len(self._data[0])
    

class TargetDisplayWidget(QWidget):
    def __init__(self,data=[]):
        super().__init__()
        #self.setGeometry(600,600,100,500)
        self.setFixedSize(700,200)
        #self.setStyleSheet("border: 2px solid black;")
        self.data = data

        self.table = QTableView()
        
        self.model = TableModel(self.data)
        
        self.table.setModel(self.model)

        self.table.verticalHeader().setDefaultSectionSize(0)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows) #makes it so when you select anything you select the entire row
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        main_layout = QVBoxLayout()
        title = QLabel("MASK GENERATION")
        main_layout.addWidget(title)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)
        #self.table.setModel(self.table)
    @pyqtSlot(list,name="target list")
    def change_data(self,data):
        self.model.beginResetModel()
        self.model._data = data
        self.model.endResetModel()







"""
this will display all the slit positions as well as the bar number and then width
additionally, when you click on the slits, it will highlight the corresponding bar in the 
interactive image and highlight the corresponding star in the target list table
"""

from slitmaskgui.menu_bar import MenuBar
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSlot, pyqtSignal, QSize
from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QVBoxLayout,
    QTableWidget


)

class TableModel(QAbstractTableModel):
    def __init__(self, data=[]):

        super().__init__()
        self._data = data
    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            #should add something about whether its vertical or horizontal
            if orientation == Qt.Orientation.Horizontal:
                return ["Row","Center","Width"][section]
            if orientation == Qt.Orientation.Vertical:
                
                return None
        return super().headerData(section, orientation, role)


    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:

            return self._data[index.row()][index.column()]

    def rowCount(self, index):

        return len(self._data)

    def columnCount(self, index):

        return len(self._data[0])


width = .7
default_slit_display_list = [[i+1,0.00,width] for i in range(72)]


class SlitDisplay(QWidget):
    highlight_other = pyqtSignal(int,name="row selected") #change name to match that in the interactive slit mask
    def __init__(self,data=default_slit_display_list):
        super().__init__()

        self.setFixedSize(200,500)

        self.data = data #will look like [[row,center,width],...]

        self.table = QTableView()
        
        self.model = TableModel(self.data)
        
        self.table.setModel(self.model)
        
        self.table.setColumnWidth(0, 32)
        self.table.setColumnWidth(1,90)
        self.table.setColumnWidth(2,50)

        self.table.verticalHeader().setDefaultSectionSize(0)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.selectRow(1)

        self.table.selectionModel().selectionChanged.connect(self.row_selected)

        layout = QVBoxLayout()

        layout.addWidget(self.table)
        self.setLayout(layout)
        #self.table.setModel(self.table)
    
    @pyqtSlot(list,name="input slit positions")
    def change_data(self,data):
        self.data = data
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
    
    def row_selected(self):
        #I have to emit a list of x,y positions [[x,y],...]
        #if there is no star in a row then we have to make it so that there is not change in position
        #I probably need to find the row
        selected_row = self.table.selectionModel().currentIndex().row()
        self.highlight_other.emit(selected_row)

    @pyqtSlot(int,name="other row selected")
    def select_corresponding(self,row):
        self.row = row
        self.table.selectRow(self.row)
 

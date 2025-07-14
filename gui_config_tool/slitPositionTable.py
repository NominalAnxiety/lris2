"""
this will display all the slit positions as well as the bar number and then width
additionally, when you click on the slits, it will highlight the corresponding bar in the 
interactive image and highlight the corresponding star in the target list table
"""

from menuBar import MenuBar
from PyQt6.QtCore import Qt, QAbstractTableModel, pyqtSlot, pyqtSignal
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
        return super().headerData(section, orientation, role)


    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:

            return self._data[index.row()][index.column()]

    def rowCount(self, index):

        return len(self._data)

    def columnCount(self, index):

        return len(self._data[0])

class SlitDispaly(QWidget):
    change_slit_position = pyqtSignal(list,name="slit positions") #change name to match that in the interactive slit mask
    def __init__(self,data=[]):
        super().__init__()

        self.setFixedSize(200,500)

        self.data = data #will look like [[row,center,width],...]

        self.table = QTableView()
        
        self.model = TableModel(self.data)
        
        self.table.setModel(self.model)

        layout = QVBoxLayout()

        layout.addWidget(self.table)
        self.setLayout(layout)
        #self.table.setModel(self.table)
    
    @pyqtSlot(list,name="input slit positions")
    def change_data(self,data):
        self.data = data
        self.model = TableModel(self.data)
        self.table.setModel(self.model)
    
    def change_slits_in_image(self):
        #I have to emit a list of x,y positions [[x,y],...]
        #if there is no star in a row then we have to make it so that there is not change in position
        emitted_list = []
        for x in self.data: #this does not account for any unused bars
            emitted_list.append([x[1],x[0]*7-7])
            #perhaps if there is no star in a position we will just make its x coordinate what the middle would be
            #this is so I don't have to worry about that here
        self.change_slit_position.emit(emitted_list)

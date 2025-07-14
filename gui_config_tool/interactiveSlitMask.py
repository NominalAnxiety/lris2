"""
This is the interactive slit mask feature. It will interact with the bar table on the left.
when you click the bar on the left then the image will display which row that is
additionally It will also interact with the target list
it will display where the slit is place and what stars will be shown
"""
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QGraphicsItem,
    QGraphicsView,
    QGraphicsScene,
    QLayout,
    QGraphicsRectItem,

)

class interactiveScene(QGraphicsScene): #this is the model
    def __init__(self):
        super().__init__()
        self.sceneRect = (0,0,400,200)

class interactiveView(QGraphicsView): #this is the view
    def __init__(self):
        super().__init__()
        

class interactiveBars(QGraphicsRectItem):
    def __init__(self,x,y,this_id):
        super().__init__()
        #creates a rectangle that can cha
        self.setRect(x,y, 100,50)
        self.id = this_id
        self.setBrush = QBrush(Qt.GlobalColor.white)
        self.setPen = QPen(Qt.GlobalColor.black).setWidth(1)

    def check_id(self,other):
        return self.id
    def setcolor(self):
        pass


class interactiveSlits(QGraphicsItem):
    def __init__(self):
        super().__init__()
        
        

class interactiveSlitMask(QLayout):
    def __init__(self):
        super().__init__()
        #this will display the image
        view = interactiveView(interactiveScene())
        #rect_items =
        #I need to create a list of rectangles that can be accessed later to click on them
        #.stackafter allows you to stack your items after another item in a scene
        #scene.selectedItems()

    def highlightBar(self):
        #this will take the signal from the row table and highlight the corresponding bar
        pass
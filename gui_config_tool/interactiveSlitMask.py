"""
This is the interactive slit mask feature. It will interact with the bar table on the left.
when you click the bar on the left then the image will display which row that is
additionally It will also interact with the target list
it will display where the slit is place and what stars will be shown
"""
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QBrush, QPen, QPainter, QColor
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
    QStyleOptionGraphicsItem,


)



class interactiveBars(QGraphicsRectItem):
    is_selected = pyqtSlot()
    def __init__(self,x,y,this_id):
        super().__init__()
        #creates a rectangle that can cha
        self.setRect(x,y, 480,7)
        self.id = this_id
        self.setBrush = QBrush(Qt.GlobalColor.white)
        self.setPen = QPen(Qt.GlobalColor.black).setWidth(1)
        self.setFlags(self.GraphicsItemFlag.ItemIsSelectable)


    def check_id(self):
        return self.id
    
    def paint(self, painter: QPainter, option, widget = None):
        if self.isSelected():
            #self.setBrush = QBrush(Qt.GlobalColor.blue)
            painter.setBrush(QBrush(Qt.GlobalColor.cyan))
            painter.setPen(QPen(QColor("black"), 1))
        else:
            painter.setBrush(QBrush(Qt.GlobalColor.white))
            painter.setPen(QPen(QColor("black"), 1))
        painter.drawRect(self.rect())
            
        #return super().paint(painter, option, widget)

        


class interactiveSlits(QGraphicsItem):
    def __init__(self):
        super().__init__()
        

class interactiveSlitMask(QVBoxLayout):
    def __init__(self):
        super().__init__()
        #this will display the image
        self.scene = QGraphicsScene(0,0,480,550)
        
        master_rect = interactiveBars(10,10,0)
        rect_list = []
        for i in range(72):
            rect_list.append(interactiveBars(10,10+i*7,i))

        self.scene.addItem(master_rect)

        for i in range(1,72):
            self.scene.addItem(rect_list[i])
        
        view = QGraphicsView(self.scene)
        #view.setRenderHint(QPainter.RenderHint.Antialiasing)

        #I need to create a list of rectangles that can be accessed later to click on them
        #.stackafter allows you to stack your items after another item in a scene
        #scene.selectedItems()

        self.addWidget(view)


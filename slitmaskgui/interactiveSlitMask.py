"""
This is the interactive slit mask feature. It will interact with the bar table on the left.
when you click the bar on the left then the image will display which row that is
additionally It will also interact with the target list
it will display where the slit is place and what stars will be shown
"""
from PyQt6.QtCore import Qt, pyqtSlot, QLineF, QParallelAnimationGroup, QPropertyAnimation, QMetaProperty, QPointF
from PyQt6.QtGui import QBrush, QPen, QPainter, QColor, QFont
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
    QGraphicsLineItem,
    QGraphicsTextItem,
    QGraphicsItemGroup,


)

#will have another thing that will dispaly all the stars in the sky at the time


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
            



class interactiveSlits(QGraphicsItemGroup):
    def __init__(self,x,y):
        super().__init__()
        #line length will be dependent on the amount of slits
        #line position will depend on the slit position of the slits (need to check slit width and postion)
        #will have default lines down the middle
        #default NONE next to lines that don't have a star
        self.line = QGraphicsLineItem(x,y,x,y+7)
        #self.line = QLineF(x,y,x,y+7)
        self.line.setPen(QPen(Qt.GlobalColor.red, 2))

        self.star = QGraphicsTextItem("NONE")
        self.star.setDefaultTextColor(Qt.GlobalColor.red)
        self.star.setFont(QFont("Arial",6))
        self.star.setPos(x+5,y-4)

        self.addToGroup(self.line)
        self.addToGroup(self.star)


    
#random line position maker
        

class interactiveSlitMask(QWidget):
    def __init__(self):
        super().__init__()
        #this will display the image
        #I think it would be cool to make the bars on the GUI move instead of just the slits moving
        self.scene = QGraphicsScene(0,0,480,520)

        for i in range(72):
            temp_rect = interactiveBars(0,i*7+7,i)
            self.scene.addItem(temp_rect)
        for i in range(72):
            temp_slit = interactiveSlits(240,7*i+7)
            self.scene.addItem(temp_slit)

        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = QVBoxLayout()
        layout.addWidget(view)


        self.setLayout(layout)

    @pyqtSlot(float,name="slit position")
    def slit_and_name_animation(self,pos):

        for item in self.scene.items():
            if isinstance(item, QGraphicsItemGroup):
                print('hi')


        pass

    @pyqtSlot(str,name="star name")
    def change_star(self,star_name):
        #self.star.setPlainText(star_name)
        pass


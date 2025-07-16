"""
The GUI is in its very early stages. Its current features are the ability to take in a starlist file
and then display that file in a list
and a menu that doesn't do anything. 7/9/25
"""
"""
random stuff
GUI has to be able to send a command with the target lists to the mask back end
to call the slit mask algorithm with the code from the backend

the back end kind of already parses through a file that sorts all of the objects so I will
just take that and display that instead of through my awful input targets function 
(they also have a function to view the list)
"""


#just importing everything for now. When on the final stages I will not import what I don't need
from slitmaskgui.target_list_widget import TargetDisplayWidget
from slitmaskgui.import_target_list import MaskGenWidget
from slitmaskgui.menu_bar import MenuBar
from slitmaskgui.interactive_slit_mask import interactiveSlitMask
from slitmaskgui.mask_configurations import MaskConfigurationsWidget
from slitmaskgui.slit_position_table import SlitDisplay
from PyQt6.QtCore import Qt
import sys
import random
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
)

pos_dict = {1:(240,"none")}
for i in range(2,73):
    pos_dict[i]=(random.randint(100,400),"bob")


class TempWidgets(QLabel):
    def __init__(self,w,h,text:str="hello"):
        super().__init__()
        self.setFixedSize(w,h)
        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet("border: 2px solid black;")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LRIS-2 Slit Configuration Tool")
        self.setGeometry(100,100,1000,700)
        self.setMenuBar(MenuBar()) #sets the menu bar

        main_layout = QHBoxLayout()
        layoutH1 = QHBoxLayout()
        layoutV1 = QVBoxLayout() #left side
        layoutV2 = QVBoxLayout() #right side

        mask_config_widget = MaskConfigurationsWidget()
        mask_config_widget.setMaximumHeight(200)
        import_target_list_display = MaskGenWidget()
        sample_data = [[0,1,1,1],[1,0,1,1]]

        target_display = TargetDisplayWidget(sample_data)
        interactive_slit_mask = interactiveSlitMask()
        interactive_slit_mask.setFixedSize(520,550)

        interactive_slit_mask.change_slit_and_star(pos_dict)
        

        slit_position_table = SlitDisplay()
        slit_position_table.setFixedSize(220,550)
        
        
        slit_position_table.highlight_other.connect(interactive_slit_mask.select_corresponding_row)
        interactive_slit_mask.row_selected.connect(slit_position_table.select_corresponding)

        #should use size policy and size hint

        #temp_widget1 = TempWidgets(250,300,"Mask Configurations\nWill display a list of\nall previous configurations")
        #temp_widget2 = TempWidgets(200,500,"This will display\nall of the widths\nand positions of\nthe bar pairs")
        #temp_widget3 = TempWidgets(500,500,"This will display the current Mask Configuration")


        import_target_list_display.change_data.connect(target_display.change_data)

        layoutV2.addWidget(mask_config_widget)#temp_widget1
        layoutV2.addWidget(import_target_list_display)
        layoutV2.setSpacing(1)

        layoutH1.addWidget(slit_position_table)#temp_widget2)
        layoutH1.addWidget(interactive_slit_mask) #temp_widget3
        layoutH1.setSpacing(1)
        
        layoutV1.addLayout(layoutH1)
        layoutV1.addWidget(target_display)
        layoutV1.setSpacing(1)

        main_layout.addLayout(layoutV1)
        main_layout.addLayout(layoutV2)
        main_layout.setSpacing(1)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
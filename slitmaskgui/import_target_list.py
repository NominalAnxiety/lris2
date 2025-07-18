
from slitmaskgui.input_targets import TargetList
from slitmaskgui.backend.star_list import stars_list
from slitmaskgui.target_list_widget import TargetDisplayWidget
from PyQt6.QtCore import QObject, pyqtSignal, Qt, QSize
from PyQt6.QtWidgets import (
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QStackedLayout,
    QLineEdit,
    QFormLayout,
    QGroupBox,
    QBoxLayout,
    QSizePolicy,
    
)



class MaskGenWidget(QWidget):
    change_data = pyqtSignal(list)
    change_slit_image = pyqtSignal(dict)
    change_row_widget = pyqtSignal(list)
    def __init__(self):
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        import_target_list_button = QPushButton(text = "Import Target List")
        name_of_mask = QLineEdit()
        name_of_mask.setAlignment(Qt.AlignmentFlag.AlignTop)
        import_target_list_button.setFixedSize(150,40)

        group_box = QGroupBox()
        main_layout = QVBoxLayout()
        secondary_layout = QFormLayout()
        group_layout = QVBoxLayout()
        group_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        import_target_list_button.clicked.connect(self.starlist_file_button_clicked)

        secondary_layout.addRow("Mask Name:",name_of_mask)
        group_layout.addLayout(secondary_layout)

        group_layout.addWidget(import_target_list_button)
        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)

        self.setLayout(main_layout)
    
    def sizeHint(self):
        return QSize(40,120)
        

    def starlist_file_button_clicked(self):
        text_file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "All files (*)" 
        )

        if text_file_path: 
            print(f"Selected file: {text_file_path}")
            target_list = TargetList(text_file_path)
            slit_mask = stars_list(target_list.send_json())
            interactive_slit_mask = slit_mask.send_interactive_slit_list()

            self.change_slit_image.emit(interactive_slit_mask)

            self.change_data.emit(slit_mask.send_target_list())
            self.change_row_widget.emit(slit_mask.send_row_widget_list())


            #now we need to configure the mask
            #we already configure the table but we need to have the table configured after it says its
            #distance from center

            #we also need to send the configured rows to the row_list
            #we also need to send the slit mask configuration to the interactive slit mask




            

            
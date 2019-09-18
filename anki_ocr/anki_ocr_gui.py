import sys
import os
from PyQt5.QtWidgets import *
import anki_ocr


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "anki_ocr_gui"
        self.initUI()

    def initUI(self):
        # Creating our widgets
        self.deck_field_label = QLabel('Enter Deck Name')
        self.deck_name_field = QLineEdit()
        self.img_dir_btn = QPushButton('Choose img directory')
        self.img_field = QLineEdit()
        self.ocr_check_box = QCheckBox(
            'Convert images to text with OCR (Good Hand-Writing required)')
        self.run_btn = QPushButton('Convert to anki package')
        self.cwd_label = QLabel(os.getcwd())

        # Gathering the widgets in a layout object
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.deck_field_label)
        self.layout.addWidget(self.deck_name_field)
        self.layout.addWidget(self.img_dir_btn)
        self.layout.addWidget(self.img_field)
        self.layout.addWidget(self.ocr_check_box)
        self.layout.addWidget(self.run_btn)
        self.layout.addWidget(self.cwd_label)


        # Connecting the buttons to their functions
        self.img_dir_btn.clicked.connect(self.on_img_dir_btn)
        self.run_btn.clicked.connect(self.on_run_btn)

        # Adding or widgets to the window then showing the window
        self.setLayout(self.layout)
        self.show()

    def on_img_dir_btn(self):
        img_directory = QFileDialog.getExistingDirectory(
            None, "Select image folder", '/home')
        self.img_field.setText(f'{img_directory}')

    def on_run_btn(self):
        # Check if fields are filled
        if (self.img_field.text()) and (self.deck_name_field.text()):
            print('fields filled, conversion running...')
            img_directory = self.img_field.text()
            deck_name = self.deck_name_field.text()
            # Check if OCR is enabled
            ocr_option = False
            if self.ocr_check_box.isChecked():
                ocr_option = True
            anki_ocr.main(img_directory, deck_name, ocr=ocr_option)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    Window = Window()
    app.exec_()

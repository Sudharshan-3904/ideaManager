from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QDialog, QLabel, QLineEdit, QTextEdit
from PyQt6.QtCore import pyqtSignal
from datetime import datetime
from components.hurdle import Hurdle
from utils.formatters import format_date

class AddHurdleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Hurdle")
        self.init_ui()

    def init_ui(self):
        self.setObjectName("card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("NEW HURDLE")
        header.setObjectName("heading")
        layout.addWidget(header)

        layout.addWidget(QLabel("Main Setback"))
        self.setback_input = QLineEdit()
        self.setback_input.setPlaceholderText("e.g., Technical limitations, Funding...")
        layout.addWidget(self.setback_input)

        layout.addWidget(QLabel("Description"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Explain the challenge in detail...")
        layout.addWidget(self.desc_input)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        self.add_btn = QPushButton("Log Hurdle")
        self.add_btn.setObjectName("primary")
        self.add_btn.setMinimumHeight(40)
        self.add_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.cancel_btn)
        layout.addLayout(buttons)

    def get_data(self):
        return {
            'main_setback': self.setback_input.text(),
            'description': self.desc_input.toPlainText()
        }

class HurdlePanel(QWidget):
    hurdleAdded = pyqtSignal(object) # Passes the new Hurdle object

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(10)
        
        header = QLabel("HURDLES")
        header.setObjectName("heading")
        layout.addWidget(header)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Date", "Setback", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(150)
        layout.addWidget(self.table)

        self.add_btn = QPushButton("+ Add Hurdle")
        self.add_btn.setMinimumHeight(35)
        self.add_btn.clicked.connect(self.on_add_hurdle)
        layout.addWidget(self.add_btn)

    def set_hurdles(self, hurdles):
        self.table.setRowCount(0)
        for h in hurdles:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(format_date(h.date)))
            self.table.setItem(row, 1, QTableWidgetItem(h.main_setback))
            self.table.setItem(row, 2, QTableWidgetItem(h.description))

    def on_add_hurdle(self):
        dialog = AddHurdleDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            new_hurdle = Hurdle(date=datetime.now(), main_setback=data['main_setback'], description=data['description'])
            self.hurdleAdded.emit(new_hurdle)

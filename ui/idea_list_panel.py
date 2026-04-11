from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QLineEdit, QAbstractItemView, QFrame
from PyQt6.QtCore import pyqtSignal, Qt

class IdeaListPanel(QWidget):
    # Signal emitted when an idea is selected. Passes the idea title.
    ideaSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Card Container
        self.container = QFrame()
        self.container.setObjectName("card")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        container_layout.setSpacing(15)

        header = QLabel("IDEAS")
        header.setObjectName("heading")
        container_layout.addWidget(header)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search ideas...")
        self.search_bar.setMinimumHeight(40)
        self.search_bar.textChanged.connect(self.filter_ideas)
        container_layout.addWidget(self.search_bar)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Title", "Hurdles"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        container_layout.addWidget(self.table)
        main_layout.addWidget(self.container)

    def populate_ideas(self, ideas):
        self.ideas = ideas
        self.update_table(ideas)

    def update_table(self, ideas):
        self.table.setRowCount(0)
        for idea in ideas:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(idea.title))
            self.table.setItem(row, 1, QTableWidgetItem(str(len(idea.hurdles))))

    def filter_ideas(self, text):
        filtered = [i for i in self.ideas if text.lower() in i.title.lower()]
        self.update_table(filtered)

    def on_selection_changed(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            # First column is the title
            title = selected_items[0].text()
            self.ideaSelected.emit(title)

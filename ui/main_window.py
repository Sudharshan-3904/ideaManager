from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSplitter, QMessageBox, QDialog, QLabel, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt
from ui.idea_list_panel import IdeaListPanel
from ui.idea_detail_panel import IdeaDetailPanel
from data.idea_repository import IdeaRepository
from components.idea import Idea

class AddIdeaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Idea")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        layout.addWidget(self.desc_input)

        layout.addWidget(QLabel("Target Customers:"))
        self.customers_input = QLineEdit()
        layout.addWidget(self.customers_input)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def get_data(self):
        return {
            'title': self.title_input.text(),
            'description': self.desc_input.toPlainText(),
            'target_customers': self.customers_input.text()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Idea Manager")
        self.resize(1000, 700)
        
        # In-memory storage for syncing current selection
        self.repository = IdeaRepository('ideas.csv')
        self.original_selection_title = None

        self.init_ui()
        self.refresh_idea_list()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Splitter to allow resizing of left/right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Panel (List + Controls)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.list_panel = IdeaListPanel()
        self.list_panel.ideaSelected.connect(self.on_idea_selected)
        left_layout.addWidget(self.list_panel)

        self.add_idea_btn = QPushButton("+ New Idea")
        self.add_idea_btn.clicked.connect(self.on_add_idea)
        left_layout.addWidget(self.add_idea_btn)
        
        self.delete_idea_btn = QPushButton("- Delete Idea")
        self.delete_idea_btn.clicked.connect(self.on_delete_idea)
        left_layout.addWidget(self.delete_idea_btn)

        splitter.addWidget(left_widget)

        # Right Panel (Detail)
        self.detail_panel = IdeaDetailPanel()
        self.detail_panel.ideaUpdated.connect(self.on_idea_updated)
        splitter.addWidget(self.detail_panel)

        main_layout.addWidget(splitter)

    def refresh_idea_list(self):
        ideas = self.repository.get_all_ideas()
        self.list_panel.populate_ideas(ideas)

    def on_idea_selected(self, title):
        self.original_selection_title = title
        ideas = self.repository.get_all_ideas()
        selected_idea = next((i for i in ideas if i.title == title), None)
        if selected_idea:
            self.detail_panel.set_idea(selected_idea)

    def on_add_idea(self):
        dialog = AddIdeaDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data['title'].strip():
                QMessageBox.warning(self, "Validation Error", "Title is required!")
                return
            
            new_idea = Idea(
                title=data['title'],
                description=data['description'],
                target_customers=data['target_customers']
            )
            self.repository.add_idea(new_idea)
            self.refresh_idea_list()

    def on_delete_idea(self):
        if not self.original_selection_title:
            QMessageBox.information(self, "No Selection", "Please select an idea to delete.")
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete '{self.original_selection_title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.repository.delete_idea(self.original_selection_title)
            self.original_selection_title = None
            self.detail_panel.clear()
            self.refresh_idea_list()

    def on_idea_updated(self, updated_idea):
        self.repository.update_idea(self.original_selection_title, updated_idea)
        self.original_selection_title = updated_idea.title
        self.refresh_idea_list()
        QMessageBox.information(self, "Success", "Idea updated successfully!")

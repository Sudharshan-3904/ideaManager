from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import pyqtSignal, Qt
from ui.hurdle_panel import HurdlePanel

class IdeaDetailPanel(QWidget):
    # Signal emitted when an idea is saved/updated
    ideaUpdated = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_idea = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Main Card
        self.container = QFrame()
        self.container.setObjectName("card")
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        header = QLabel("DETAILS")
        header.setObjectName("heading")
        container_layout.addWidget(header)

        # Form as a scrollable area if it gets too long
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        form_widget = QWidget()
        form_widget.setStyleSheet("background-color: transparent;")
        self.form_layout = QFormLayout(form_widget)
        self.form_layout.setSpacing(10)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title_input = QLineEdit()
        self.form_layout.addRow("Title", self.title_input)

        self.desc_input = QTextEdit()
        self.desc_input.setMinimumHeight(80)
        self.form_layout.addRow("Description", self.desc_input)

        self.customers_input = QLineEdit()
        self.form_layout.addRow("Target Customers", self.customers_input)

        self.deliverables_input = QTextEdit()
        self.deliverables_input.setMaximumHeight(80)
        self.form_layout.addRow("Minimal Deliverables", self.deliverables_input)

        self.extensions_input = QTextEdit()
        self.extensions_input.setMaximumHeight(80)
        self.form_layout.addRow("Future Extensions", self.extensions_input)

        scroll.setWidget(form_widget)
        container_layout.addWidget(scroll)

        self.hurdle_panel = HurdlePanel()
        self.hurdle_panel.hurdleAdded.connect(self.on_hurdle_added)
        container_layout.addWidget(self.hurdle_panel)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setObjectName("primary")
        self.save_btn.setMinimumHeight(45)
        self.save_btn.clicked.connect(self.save_changes)
        container_layout.addWidget(self.save_btn)

        main_layout.addWidget(self.container)

    def set_idea(self, idea):
        self.current_idea = idea
        self.title_input.setText(idea.title)
        self.desc_input.setText(idea.description)
        self.customers_input.setText(idea.target_customers)
        self.deliverables_input.setText(idea.minimal_deliverables)
        self.extensions_input.setText(idea.future_extensions)
        self.hurdle_panel.set_hurdles(idea.hurdles)

    def on_hurdle_added(self, hurdle):
        if self.current_idea:
            self.current_idea.add_hurdle(hurdle)
            self.hurdle_panel.set_hurdles(self.current_idea.hurdles)

    def save_changes(self):
        if self.current_idea:
            self.current_idea.title = self.title_input.text()
            self.current_idea.description = self.desc_input.toPlainText()
            self.current_idea.target_customers = self.customers_input.text()
            self.current_idea.minimal_deliverables = self.deliverables_input.toPlainText()
            self.current_idea.future_extensions = self.extensions_input.toPlainText()
            self.ideaUpdated.emit(self.current_idea)

    def clear(self):
        self.current_idea = None
        self.title_input.clear()
        self.desc_input.clear()
        self.customers_input.clear()
        self.deliverables_input.clear()
        self.extensions_input.clear()
        self.hurdle_panel.set_hurdles([])

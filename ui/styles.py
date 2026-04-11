def get_modern_stylesheet():
    return """
    /* Main Window */
    QMainWindow {
        background-color: #0B1015;
    }

    QWidget#main_bg {
        background-color: #0B1015;
    }

    QWidget {
        color: #FFFFFF;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Cards / Containers */
    #card, QFrame#card {
        background-color: #1A1D21;
        border-radius: 16px;
        border: 1px solid #2D333B;
    }

    /* Input Fields */
    QLineEdit, QTextEdit {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 10px;
        color: #E6EDF3;
        font-size: 14px;
    }

    QLineEdit:focus, QTextEdit:focus {
        border: 1px solid #00FF9E;
        background-color: #1C2128;
    }

    /* Buttons */
    QPushButton {
        background-color: #1A1D21;
        color: #FFFFFF;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 13px;
    }

    QPushButton:hover {
        background-color: #30363D;
        border: 1px solid #484F58;
    }

    QPushButton#primary {
        background-color: #00FF9E;
        color: #0B1015;
        border: none;
    }

    QPushButton#primary:hover {
        background-color: #33FFB1;
    }

    QPushButton#danger {
        background-color: #FF4D4D;
        color: #FFFFFF;
        border: none;
    }

    QPushButton#danger:hover {
        background-color: #FF6666;
    }

    /* Tables */
    QTableWidget {
        background-color: transparent;
        border: none;
        gridline-color: transparent;
    }

    QHeaderView::section {
        background-color: transparent;
        color: #94A3B8;
        padding: 8px;
        border: none;
        font-weight: 800;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 1px;
    }

    QTableWidget::item {
        padding: 12px;
        border-bottom: 1px solid #282C31;
    }

    QTableWidget::item:selected {
        background-color: #2D333B;
        color: #00FF9E;
        border-radius: 4px;
    }

    /* Labels */
    QLabel {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 500;
    }

    QLabel#heading {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* Scrollbars */
    QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 8px;
    }

    QScrollBar::handle:vertical {
        background: #30363D;
        min-height: 30px;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical:hover {
        background: #484F58;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    /* Splitter */
    QSplitter::handle {
        background-color: transparent;
    }
    """

import re
from enum import Enum

from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from rsc_icons import Icons


class TxtMode(Enum):
    DIGIT_ONLY = "mode_to_digit_only"
    TO_9_DIGIT = "mode_to_9_digit"
    DECIMAL_DOT = "mode_digit_decimal_dot"
    TO_COMMA = "mode_dot_to_comma"
    DECIMAL_COMMA = "mode_digit_decimal_comma"
    TO_DOT = "mode_comma_to_dot"


class Digitizer(QWidget):
    def __init__(self):
        super().__init__()

        self.digitizer_ui()

    def digitizer_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.input_ui())
        layout.addWidget(self.output_ui())
        layout.addStretch()

    def input_ui(self):
        # Widgets
        self.txt_input = QLineEdit()

        btn_clear = QPushButton("Clear")
        btn_clear.setIcon(Icons.CLEAR.icon())
        btn_clear.clicked.connect(self.txt_input.clear)

        btn_paste = QPushButton("Paste")
        btn_paste.setIcon(Icons.PASTE.icon())
        btn_paste.clicked.connect(
            lambda: self.txt_input.setText(
                # allow multiple paste text, strip on paste
                self.txt_input.text() + QApplication.clipboard().text().strip()
            )
        )

        # Add to Main Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.txt_input)
        input_layout.addWidget(btn_clear)
        input_layout.addWidget(btn_paste)

        # wrap in group box
        group_input = QGroupBox("Paste teks di sini")
        group_input.setLayout(input_layout)

        return group_input

    def output_ui(self):
        # Grid Layout
        result_grid_layout = QGridLayout()

        # [1] Digit Only
        result_grid_layout.addWidget(QLabel("Digit only (full)"), 0, 0)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.DIGIT_ONLY), 1, 0
        )
        result_grid_layout.addWidget(
            QLabel("to 9 digit:"), 1, 1, Qt.AlignmentFlag.AlignRight
        )
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.TO_9_DIGIT), 1, 2
        )

        # [2] Digit Decimal Dot
        result_grid_layout.addWidget(QLabel("Digit decimal dot"), 2, 0)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.DECIMAL_DOT), 3, 0
        )
        result_grid_layout.addWidget(
            QLabel("to comma:"), 3, 1, Qt.AlignmentFlag.AlignRight
        )
        result_grid_layout.addLayout(self.create_txt_btn_layout(TxtMode.TO_COMMA), 3, 2)

        # [3] Digit Decimal Comma
        result_grid_layout.addWidget(QLabel("Digit decimal comma"), 4, 0)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.DECIMAL_COMMA), 5, 0
        )
        result_grid_layout.addWidget(
            QLabel("to dot:"), 5, 1, Qt.AlignmentFlag.AlignRight
        )
        result_grid_layout.addLayout(self.create_txt_btn_layout(TxtMode.TO_DOT), 5, 2)

        # Main Layout
        group_result = QGroupBox("Results")
        group_result.setLayout(result_grid_layout)

        return group_result

    def create_txt_btn_layout(self, mode):
        layout = QHBoxLayout()

        txt_result = QLineEdit()
        txt_result.setReadOnly(True)

        btn_copy = QPushButton()
        btn_copy.setIcon(Icons.COPY.icon())
        btn_copy.setToolTip("Copy")
        btn_copy.clicked.connect(
            lambda: QApplication.clipboard().setText(txt_result.text())
        )

        layout.addWidget(txt_result)
        layout.addWidget(btn_copy)

        # Connect
        self.txt_input.textChanged.connect(
            lambda: txt_result.setText(self.create_txt_function(mode))
        )

        return layout

    def create_txt_function(self, mode):
        txt_cleaned = self.txt_input.text().strip()

        digit_only = re.sub(r"[^0-9]", "", txt_cleaned)
        digit_decimal_dot = re.sub(r"[^0-9.]", "", txt_cleaned)
        digit_dot_to_comma = digit_decimal_dot.replace(".", ",")
        digit_decimal_comma = re.sub(r"[^0-9,]", "", txt_cleaned)
        digit_comma_to_dot = digit_decimal_comma.replace(",", ".")

        match mode:
            case TxtMode.DIGIT_ONLY:
                return digit_only
            case TxtMode.TO_9_DIGIT:
                return digit_only[:9]
            case TxtMode.DECIMAL_DOT:
                return digit_decimal_dot
            case TxtMode.TO_COMMA:
                return digit_dot_to_comma
            case TxtMode.DECIMAL_COMMA:
                return digit_decimal_comma
            case TxtMode.TO_DOT:
                return digit_comma_to_dot
            case _:
                return ""

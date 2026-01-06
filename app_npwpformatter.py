import re
from enum import Enum

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
    NPWP_15_FORMAT = "mode_npwp_15_format"
    NPWP_16 = "mode_npwp_16"
    NPWP_9_6 = "mode_npwp_9_6"
    NITKU_PUSAT = "mode_nitku_pusat"


class NPWPFormatter(QWidget):
    def __init__(self):
        super().__init__()

        self.npwpformatter_ui()

    def npwpformatter_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.input_ui())
        layout.addWidget(self.output_ui())
        layout.addStretch()

    def input_ui(self):
        # Widgets
        self.npwp_input = QLineEdit()

        btn_clear = QPushButton("Clear")
        btn_clear.setIcon(Icons.CLEAR.icon())
        btn_clear.clicked.connect(self.npwp_input.clear)

        btn_paste = QPushButton("Paste")
        btn_paste.setIcon(Icons.PASTE.icon())
        btn_paste.clicked.connect(
            lambda: self.npwp_input.setText(
                # don't allow multiple paste text, strip on paste
                QApplication.clipboard().text().strip()
            )
        )

        # Add to Main Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.npwp_input)
        input_layout.addWidget(btn_clear)
        input_layout.addWidget(btn_paste)

        # wrap in group box
        group_input = QGroupBox("Paste teks di sini")
        group_input.setLayout(input_layout)

        return group_input

    def output_ui(self):
        # Grid Layout
        result_grid_layout = QGridLayout()

        # Group 1
        result_grid_layout.addWidget(QLabel("NPWP 15:"), 0, 0)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.DIGIT_ONLY),
            1,
            0,
        )

        result_grid_layout.addWidget(QLabel("NPWP 9:"), 0, 2)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.TO_9_DIGIT), 1, 2
        )

        # Group 2
        result_grid_layout.addWidget(QLabel("NPWP 15 Format:"), 2, 0)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.NPWP_15_FORMAT),
            3,
            0,
        )

        result_grid_layout.addWidget(QLabel("NPWP 9-6:"), 2, 2)
        result_grid_layout.addLayout(self.create_txt_btn_layout(TxtMode.NPWP_9_6), 3, 2)

        # Group 3
        result_grid_layout.addWidget(QLabel("NPWP 16:"), 4, 0)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.NPWP_16),
            5,
            0,
        )

        result_grid_layout.addWidget(QLabel("NITKU Pusat:"), 4, 2)
        result_grid_layout.addLayout(
            self.create_txt_btn_layout(TxtMode.NITKU_PUSAT), 5, 2
        )

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
        self.npwp_input.textChanged.connect(
            lambda: txt_result.setText(self.create_txt_function(mode))
        )

        return layout

    def create_txt_function(self, mode: TxtMode):
        txt_cleaned = self.npwp_input.text().strip()

        d = re.sub(r"[^0-9]", "", txt_cleaned)

        match mode:
            case TxtMode.DIGIT_ONLY:
                return d
            case TxtMode.TO_9_DIGIT:
                return d[:9]
            case TxtMode.NPWP_15_FORMAT:
                return (
                    (
                        d[:2]
                        + "."
                        + d[2:5]
                        + "."
                        + d[5:8]
                        + "."
                        + d[8:9]
                        + "-"
                        + d[9:12]
                        + "."
                        + d[12:15]
                    )
                    if d != ""
                    else ""
                )
            case TxtMode.NPWP_16:
                return d.zfill(16) if d != "" else ""
            case TxtMode.NPWP_9_6:
                return d[:9] + "-" + d[9:15] if d != "" else ""
            case TxtMode.NITKU_PUSAT:
                return d + "000000" if d != "" else ""

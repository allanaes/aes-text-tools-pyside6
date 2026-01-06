import json
import re
from importlib.resources import files

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from rsc_icons import Icons
from window_message import window_message


class ChangeCase(QWidget):
    def __init__(self):
        super().__init__()

        self.changecase_ui()

    def changecase_ui(self):
        layout = QVBoxLayout(self)

        self.plain_text = QPlainTextEdit()

        layout.addLayout(self.create_action_buttons())
        layout.addWidget(self.plain_text)
        layout.addLayout(self.create_changecase_buttons())

    def create_action_buttons(self):
        layout = QHBoxLayout()

        btn_copy = QPushButton("Copy All")
        btn_copy.setIcon(Icons.COPY.icon())
        btn_copy.clicked.connect(
            lambda: QApplication.clipboard().setText(self.plain_text.toPlainText())
        )

        btn_trim = QPushButton("Trim")
        btn_trim.setIcon(Icons.TRIM.icon())
        btn_trim.clicked.connect(
            lambda: self.plain_text.setPlainText(
                self.trim_text(self.plain_text.toPlainText())
            )
        )

        btn_paste = QPushButton("Paste")
        btn_paste.setIcon(Icons.PASTE.icon())
        btn_paste.clicked.connect(
            lambda: self.plain_text.setPlainText(
                # allow multiple paste text
                self.plain_text.toPlainText() + QApplication.clipboard().text()
            )
        )

        btn_clear = QPushButton("Clear")
        btn_clear.setIcon(Icons.CLEAR.icon())
        btn_clear.clicked.connect(lambda: self.plain_text.setPlainText(""))

        layout.addWidget(btn_copy)
        layout.addWidget(btn_trim)
        layout.addWidget(btn_paste)
        layout.addWidget(btn_clear)

        return layout

    def create_changecase_buttons(self):
        layout = QHBoxLayout()

        btn_upper = QPushButton("UPPER CASE")
        btn_lower = QPushButton("lower case")
        btn_propper = QPushButton("Proper Case")
        btn_sentence = QPushButton("Sentence case")

        # change case functions
        # 1. To UPPER
        btn_upper.clicked.connect(
            lambda: self.plain_text.setPlainText(self.plain_text.toPlainText().upper())
        )

        # 2. To lower
        btn_lower.clicked.connect(
            lambda: self.plain_text.setPlainText(self.plain_text.toPlainText().lower())
        )

        # 3. To Propper
        btn_propper.clicked.connect(
            lambda: self.plain_text.setPlainText(
                self.change_case_multi(self.plain_text.toPlainText(), "propper")
            )
        )

        # 4. To Sentence
        btn_sentence.clicked.connect(
            lambda: self.plain_text.setPlainText(
                self.change_case_multi(self.plain_text.toPlainText(), "sentence")
            )
        )

        layout.addWidget(btn_upper)
        layout.addWidget(btn_lower)
        layout.addWidget(btn_propper)
        layout.addWidget(btn_sentence)

        return layout

    def change_case_multi(self, text="", text_function="propper"):
        text = text.lower()
        sentences = re.split("([.!?\\n]\\s*)", text)

        modified_sentences = ""
        if text_function == "propper":
            modified_sentences = [s.title() for s in sentences]
        if text_function == "sentence":
            modified_sentences = [s.capitalize() for s in sentences]

        text = "".join(modified_sentences)

        modified_text = self.replace_common(text)

        return modified_text

    def load_json(self):
        path = files("aes_text_tools").joinpath("includes/replacements.json")
        return path

    def replace_common(self, text=""):
        # replace common words
        replacements = {}

        try:
            with open("includes/replacements.json", "r", encoding="utf-8") as f:
                replacements = json.load(f)

        except FileNotFoundError:
            title = "Error"
            msg = "File 'replacements.json' tidak ada dalam folder 'includes'."
            print(f"{title}: {msg}")
            window_message(self, title, msg, is_error=True)

        except json.JSONDecodeError:
            title = "Error"
            msg = "Gagal mendecode JSON dari file 'replacements.json'. Cek apakah data sudah sesuai format JSON."
            print(f"{title}: {msg}")
            window_message(self, title, msg, is_error=True)

        for old, new in replacements.items():
            pattern = re.compile(rf"\b{re.escape(old)}\b", re.IGNORECASE)
            text = pattern.sub(new, text)

        return text

    def trim_text(self, text=""):
        text = text.expandtabs(4).strip()
        text = re.sub(" +", " ", text)

        return text

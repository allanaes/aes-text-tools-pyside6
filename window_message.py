import struct

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox


def window_message(self, title="", message="", is_error=False, is_info=False):
    msg_window = QMessageBox(self)

    msg_window.setText(message)
    msg_window.setWindowTitle(title)
    msg_window.setFixedWidth(240)
    msg_window.setIcon(QMessageBox.Icon.NoIcon)
    msg_window.setWindowFlags(
        Qt.WindowType.Dialog
        | Qt.WindowType.CustomizeWindowHint
        | Qt.WindowType.WindowTitleHint
    )

    if is_error:
        msg_window.setIcon(QMessageBox.Icon.Critical)

    if is_info:
        msg_window.setIcon(QMessageBox.Icon.Information)

    msg_window.exec()


def msg_about_app(self):
    title = "Tentang Aplikasi"

    bits = struct.calcsize("P") * 8
    message = f"""
        <h1>AES Text Tools</h1>
        <p>Versi 0.1.20251224 ({bits}-bit)</p>
        <p>Copyleft (ɔ) 2025 by allanaes</p>
        <p>Aplikasi sederhana untuk memudahkan<br />
        dalam memformat angka dan teks tanpa harus <br />
        hapus karakter secara manual.</p>
        <p>App Icon: Flaticon.com<br />
        Button Icons: Fugue Icon&lt;p.yusukekamiyamane.com&gt;</p>
        """

    window_message(self, title, message)

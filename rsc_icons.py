from enum import Enum

from PySide6.QtGui import QIcon

import resources  # noqa


class Icons(Enum):
    APP = ":/icons/icon_app.png"
    PASTE = ":/icons/icon_paste.png"
    COPY = ":/icons/icon_copy.png"
    CLEAR = ":/icons/icon_clear.png"
    TRIM = ":/icons/icon_trim.png"
    EXIT = ":/icons/icon_exit.png"

    def icon(self):
        return QIcon(self.value)

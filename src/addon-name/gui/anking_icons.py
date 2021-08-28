from aqt.qt import *
from aqt.utils import openLink


class AnkingIconsHeader(QHBoxLayout):
    def __init__(self, parent: QWidget) -> None:
        QHBoxLayout.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setup()
        parent.setLayout(self)

    def setup(self) -> None:
        self.addStretch()
        icon_objs = [
            ("AnKingSmall.png", (31, 31), "https://www.ankingmed.com"),
            ("YouTube.png", (31, 31), "https://www.youtube.com/theanking"),
            ("Patreon.png", (221, 31), "https://www.patreon.com/ankingmed"),
            ("Instagram.png", (31, 31), "https://instagram.com/ankingmed"),
            ("Facebook.png", (31, 31), "https://facebook.com/ankingmed"),
        ]
        for obj in icon_objs:
            (image, size, url) = obj
            icon = QIcon(QPixmap(f":/AnKing/{image}"))
            button = QToolButton()
            button.setIcon(icon)
            button.setIconSize(QSize(size[0], size[1]))
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.setStyleSheet("QToolButton { border: none; }")
            button.setToolTip(url)
            button.clicked.connect(lambda _, url=url: openLink(url))
            self.addWidget(button)
        self.addStretch()

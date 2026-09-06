APP_STYLESHEET = """
QWidget {
    color: #F4FBFF;
    font-family: "SF Pro Display", "Segoe UI Variable", "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
    font-size: 14px;
}

QMainWindow, QWidget#root {
    background: transparent;
}

QLabel#heroTitle {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 700;
    letter-spacing: -0.4px;
}

QLabel#heroArtist {
    color: rgba(236, 250, 255, 0.72);
    font-size: 17px;
    font-weight: 400;
}

QLabel#heroAlbum {
    color: rgba(186, 230, 253, 0.58);
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.4px;
}

QLabel#timeLabel {
    color: rgba(226, 246, 255, 0.7);
    font-size: 12px;
    font-weight: 500;
}

QLabel#sectionTitle {
    color: rgba(255, 255, 255, 0.9);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.4px;
}

QLabel#statusLabel {
    color: rgba(214, 240, 255, 0.62);
    font-size: 12px;
}

QPushButton#folderButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(125, 211, 252, 0.28), stop:1 rgba(56, 189, 248, 0.16));
    border: 1px solid rgba(186, 230, 253, 0.32);
    border-radius: 16px;
    color: #F0FBFF;
    font-weight: 600;
    padding: 10px 18px;
    min-height: 22px;
}

QPushButton#folderButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(125, 211, 252, 0.4), stop:1 rgba(56, 189, 248, 0.24));
    border-color: rgba(224, 242, 254, 0.48);
}

QPushButton#folderButton:pressed {
    background: rgba(14, 116, 144, 0.35);
}

QSlider#seekSlider::groove:horizontal {
    height: 8px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.12);
}

QSlider#seekSlider::sub-page:horizontal {
    border-radius: 4px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #67E8F9, stop:1 #38BDF8);
}

QSlider#seekSlider::add-page:horizontal {
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.08);
}

QSlider#seekSlider::handle:horizontal {
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
    background: #F0FDFF;
    border: 2px solid rgba(103, 232, 249, 0.9);
}

QSlider#seekSlider::handle:horizontal:hover {
    background: #FFFFFF;
}

QSlider#volumeSlider::groove:horizontal {
    height: 5px;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.14);
}

QSlider#volumeSlider::sub-page:horizontal {
    border-radius: 3px;
    background: rgba(125, 211, 252, 0.85);
}

QSlider#volumeSlider::handle:horizontal {
    width: 12px;
    height: 12px;
    margin: -4px 0;
    border-radius: 6px;
    background: #ECFEFF;
}

QListView#libraryView {
    background: transparent;
    border: none;
    outline: none;
    padding: 4px 2px 12px 2px;
}

QListView#libraryView::item {
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 8px 2px 8px 0;
}

QScrollBar::handle:vertical {
    background: rgba(186, 230, 253, 0.28);
    border-radius: 5px;
    min-height: 36px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(186, 230, 253, 0.46);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    height: 0;
    background: transparent;
}

QScrollBar:horizontal {
    height: 0;
}

QToolTip {
    background: rgba(8, 25, 48, 0.94);
    color: #F8FBFF;
    border: 1px solid rgba(186, 230, 253, 0.28);
    border-radius: 8px;
    padding: 6px 8px;
}
"""

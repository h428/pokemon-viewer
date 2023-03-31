import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPoint, QMargins


class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 200)

        label = QLabel(self)
        label.setGeometry(0, 0, 400, 200)
        label.setStyleSheet("QLabel { background-color : rgba(255, 255, 255, 0.2); color : rgba(0, 0, 0, 255); }")
        label.setText("This is a transparent GUI program!")

        button = QPushButton('Close', self)
        button.clicked.connect(self.close)
        button.setGeometry(350, 10, 40, 25)

        self.setWindowOpacity(0.7)

        # 窗口居中显示
        screenGeometry = QApplication.desktop().screenGeometry()
        self.setGeometry((screenGeometry.width() - self.width()) / 2, screenGeometry.height() - 100 - self.height(),
                          self.width(), self.height())

        # 添加窗口拖动事件
        self.dragPos = QPoint(0, 0)
        label.mouseMoveEvent = self.mouseMoveEvent
        label.mousePressEvent = self.mousePressEvent

        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TransparentWindow()
    sys.exit(app.exec_())

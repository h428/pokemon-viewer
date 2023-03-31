import sys
from PyQt5.QtCore import Qt, QEvent, QObject, QThread, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from main import capture_and_process
from pynput.keyboard import Key, Listener
import pygame
from threading import Thread
from queue import Queue


class KeyListener(QObject):
    key_pressed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key.char == ' ':
                self.key_pressed.emit('detection')
        except AttributeError:
            if key == Key.space:
                self.key_pressed.emit('detection')


class Worker(QThread):
    on_detection_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.key_listener = KeyListener()
        self.key_listener.key_pressed.connect(self.on_key_pressed)

    def on_key_pressed(self, key):
        if key == 'detection':
            # 发送信号到主线程
            self.on_detection_signal.emit(key)

    def run(self):
        while True:
            self.msleep(100)


class PokemonWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口的标题和大小
        self.setWindowTitle('宝可梦对战属性')
        # 窗口居中显示
        screenGeometry = QApplication.desktop().screenGeometry()
        w = 800
        h = 300
        self.setGeometry((screenGeometry.width() - w) / 2, screenGeometry.height() - 100 - h, w, h)

        # 创建一个网格布局
        layout = QGridLayout()

        # 创建四个标签
        name_label = QLabel('宝可梦:')
        name_label.setStyleSheet("QLabel { background-color : rgba(0, 0, 0, 100); color : rgba(0, 0, 0, 255); } \
                                      QLabel#myLabel { background-color : rgba(255, 255, 255, 255); }")
        self.name_value = QLabel()
        type_label = QLabel('属性:')
        self.type_value = QLabel()
        weakness_label = QLabel('推荐属性:')
        self.weakness_value = QLabel()
        resistance_label = QLabel('不建议属性:')
        self.resistance_value = QLabel()

        # 将标签添加到布局中
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.name_value, 0, 1)
        layout.addWidget(type_label, 1, 0)
        layout.addWidget(self.type_value, 1, 1)
        layout.addWidget(weakness_label, 2, 0)
        layout.addWidget(self.weakness_value, 2, 1)
        layout.addWidget(resistance_label, 3, 0)
        layout.addWidget(self.resistance_value, 3, 1)

        # 设置布局
        self.setLayout(layout)
        self.setWindowOpacity(0.2)

        # 创建一个队列来保存键盘事件
        self.worker = Worker()
        self.worker.on_detection_signal.connect(self.on_detection)

        # 处理 xbox 事件
        # 初始化 pygame
        # pygame.init()
        #
        # # 连接到第一个可用的游戏手柄
        # self.joystick = pygame.joystick.Joystick(0)
        # self.joystick.init()
        #
        # # 开始监听按键事件
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.on_rb_click)
        # self.timer.start(50)

    def on_rb_click(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                self.on_detection('detection')

    def on_detection(self, key):
        if key == 'detection':
            pokemon_data, double_type, half_type = capture_and_process()
            print(pokemon_data, double_type, half_type)

            # 显示新宝可梦信息
            if pokemon_data and double_type and half_type:
                type_all = f"{pokemon_data['type1']}, {pokemon_data.get('type2')}"
                self.show_pokemon_info(pokemon_data["name"], type_all, str(double_type), str(half_type))

    def show_pokemon_info(self, name, pokemon_type, weakness, resistance):
        # 更新标签的值
        self.name_value.setText(name)
        self.type_value.setText(pokemon_type)
        self.weakness_value.setText(weakness)
        self.resistance_value.setText(resistance)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = PokemonWindow()
    window.show()

    sys.exit(app.exec_())

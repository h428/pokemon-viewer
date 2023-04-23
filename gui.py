import sys

import pygame
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

from main import capture_and_process


class PokemonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label_name = None
        self.label_category = None
        self.label_recommend = None
        self.label_not_recommend = None
        self.timer = None
        self.joystick = None
        self.initUI()
        self.initXbox()

    def initXbox(self):
        pygame.init()
        pygame.joystick.init()

        # 使用主线程的定时器来处理 xbox 的事件循环
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.xbox_event_loop)
        self.timer.start()

    def xbox_event_loop(self):
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.JOYBUTTONDOWN and event.button == 4:
                self.on_rb_click()
            elif event.type == pygame.JOYDEVICEADDED:
                self.joystick = pygame.joystick.Joystick(event.device_index)
                self.joystick.init()
                print("Xbox 已连接...")
            elif event.type == pygame.JOYDEVICEREMOVED:
                print("Xbox 已断开...")

    def initUI(self):
        self.setWindowTitle('宝可梦对战识别器')
        self.resize(300, 200)
        # self.setWindowOpacity(0.3)

        font = QFont("楷体", 33, QFont.Bold)

        self.label_name = QLabel("名称")
        self.label_name.setFont(font)

        self.label_recommend = QLabel("推荐属性")
        self.label_recommend.setFont(font)

        self.label_not_recommend = QLabel("不推荐属性")
        self.label_not_recommend.setFont(font)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_name)
        vbox.addWidget(self.label_recommend)
        vbox.addWidget(self.label_not_recommend)

        self.setLayout(vbox)
        self.show()

    def on_rb_click(self):
        capture_result = capture_and_process()

        if not capture_result or not len(capture_result) == 3:
            return

        pokemon_data, double_type, half_type = capture_result
        print(pokemon_data, double_type, half_type)

        # 显示新宝可梦信息
        if pokemon_data and double_type and half_type:
            type1 = pokemon_data.get('type1')
            type2 = pokemon_data.get('type2')
            type_all = f"{type1}, {type2}" if type2 else type1
            recommend = "/".join(double_type)
            not_recommend = "/".join(half_type)
            self.show_pokemon_info(pokemon_data["name"], type_all, recommend, not_recommend)

    def show_pokemon_info(self, name, pokemon_type, weakness, resistance):
        # 更新标签的值
        self.label_name.setText(f"{name}/{pokemon_type}")
        self.label_recommend.setText(weakness)
        self.label_not_recommend.setText(resistance)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = PokemonWindow()
    window.show()

    sys.exit(app.exec_())

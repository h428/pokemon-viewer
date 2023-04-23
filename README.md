# 宝可梦对战识别器

本项目为基于 [Paddle OCR](https://github.com/PaddlePaddle/PaddleOCR) 的宝可梦对战识别器，相关功能主要包括：
- 识别出对战宝可梦名称
- 根据名称判断

## 环境搭建

- 基于 python 3.7 创建环境： `conda create -n pokemon python=3.7`
- 安装 paddle `pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple`
- 有可能包 protobuf 冲突问题，本次的解决方案是：
  - paddlepaddle 2.4.2 requires protobuf<=3.20.0，因此安装 3.20.0： `pip install protobuf==3.20.0`
  - 但 onnx 1.13.1 requires protobuf<4,>=3.20.2，降低 onnx 版本为 `pip install onnx==1.11`
- 安装 pyqt5：`pip install pyqt5`

## 参考链接

- [PaddleOCR 快速开始](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/quickstart.md)
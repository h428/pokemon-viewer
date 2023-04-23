from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import os
import re

# 加载中文语言模型
model = PaddleOCR(use_angle_cls=True, lang="ch")
prefix = "正准备派出"


def process_ocr_text(ocr_text):
    if ocr_text.startswith(prefix):
        ocr_text = ocr_text.replace(prefix, "")

    # 仅保留字符串中的中文
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    chinese_only = "".join(pattern.findall(ocr_text))

    return chinese_only


def parse_image_result(image_result):
    """
    解析一张图片的识别结果
    :param image_result:
    :return:
    """

    # 在当前图片识别到 box_bum 个文字结果
    box_bum = len(image_result)

    ocr_text_list = []
    for i in range(box_bum):
        # 逐个取出结果
        box_result = image_result[i]
        # 取出矩形框，和对应的文字结果
        # point_list 是二维数组，分别描述 4 个点，
        point_list, text_result = box_result[0], box_result[1]
        # text_result 包含两个元素，第一个是文本，第二个是置信度
        ocr_text, confidence = text_result[0], text_result[1]
        ocr_text = process_ocr_text(ocr_text)

        if ocr_text:
            ocr_text_list.append(ocr_text)

    if len(ocr_text_list) > 0:
        return ocr_text_list[0]

    return ""


def ocr_pokemon_name_by_image(img_path):
    result = model.ocr(img_path, cls=False)

    if len(result[0]) == 0:
        return ""

    image_result = result[0]
    name = parse_image_result(image_result)

    return name


if __name__ == '__main__':

    img_idr = "imgs"

    for file in os.listdir(img_idr):
        path = os.path.join(img_idr, file)
        text = ocr_pokemon_name_by_image(path)
        print(f"{path}: {text}")

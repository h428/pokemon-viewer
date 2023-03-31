from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import os
import re

# 加载中文语言模型
model = PaddleOCR(use_angle_cls=True, lang="ch")
prefix = "正准备派出"


def ocr_pokemon_name_by_image(img_path):
    result = model.ocr(img_path, cls=False)

    if len(result[0]) == 0:
        return ""

    item = result[0][0]

    name = item[1][0]

    if name.startswith("Lv") or name.startswith("lv"):
        return ""

    if name.startswith(prefix):
        name = name.replace(prefix, "")

    name = re.sub('[?@の。\t\n]+', '', name)

    return name


if __name__ == '__main__':

    img_idr = "imgs"

    for file in os.listdir(img_idr):
        path = os.path.join(img_idr, file)
        text = ocr_pokemon_name_by_image(path)
        print(f"{path}: {text}")

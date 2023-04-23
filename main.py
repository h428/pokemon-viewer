import PIL.ImageGrab
from model import ocr_pokemon_name_by_image
from pokemon import load_pokemon
from rule import decide_fight_type
import re
import difflib

# box_list = [
#     [1530, 145, 250, 50],
#     [500, 200, 1000, 365],
#     [240, 830, 600, 160]
# ]

box_list = [
    # [1530, 95, 250, 55],
    [0, 0, 1920, 560],
    [280, 790, 400, 55],
]

box_image_pattern = "cache/box{}.png"

top_box_path = "cache/top_box.png"
center_box_path = "cache/center_box.png"
bottom_box_path = "cache/bottom_box.png"

pokemon_map, pokemon_name_list = load_pokemon()


def convert_to_bbox(box):
    """
    将 (x1, y1, w, h) 格式的盒子转化为 (x1, y1, x2, y2) 格式的盒子
    :param box:
    :return:
    """
    return box[0], box[1], box[0] + box[2], box[1] + box[3]


def find_closest_pokemon(name, pokemon_list):
    """
    使用近似算法，从 pokemon_list 找出最接近 name 的结果
    :param name:
    :param pokemon_list:
    :return:
    """
    closest_match = difflib.get_close_matches(name, pokemon_list, n=1)
    return closest_match[0] if len(closest_match) > 0 else ""


def capture_screen_and_ocr_unique_name():
    tmp_box_list = box_list

    image_path_list = []
    for i, box in enumerate(tmp_box_list):
        # 截取屏幕指定区域的截图
        image = PIL.ImageGrab.grab(bbox=convert_to_bbox(box))
        image_path = box_image_pattern.format(i)
        image.save(image_path)
        image_path_list.append(image_path)

    # 识别截图中的文字
    for image_path in image_path_list:
        name = ocr_pokemon_name_by_image(image_path)
        if name:
            return name

    return ""


def capture_and_process():
    pokemon_name = capture_screen_and_ocr_unique_name()
    pokemon_data = pokemon_map.get(pokemon_name)

    if not pokemon_name:
        print("未识别到可用宝可梦名称")
        return []

    if not pokemon_data:
        print(f"无法完全匹配 {pokemon_name}，采用近似算法")
        pokemon_name = find_closest_pokemon(pokemon_name, pokemon_name_list)
        pokemon_data = pokemon_map.get(pokemon_name)
        print(f"近似采用 {pokemon_name}")

    if not pokemon_name:
        print(f"近似名称为空")
        return []

    type1, type2 = pokemon_data["type1"], pokemon_data.get("type2")
    double_type, half_type = decide_fight_type(type1, type2)
    return pokemon_data, double_type, half_type


if __name__ == '__main__':
    print(capture_and_process())

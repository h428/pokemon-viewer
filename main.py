import PIL.ImageGrab
from model import ocr_pokemon_name_by_image
from pokemon import load_pokemon
from rule import decide_fight_type
import re
import difflib

top_box = [1400, 75, 250, 60]
bottom_box = [240, 830, 600, 160]
top_box_path = "cache/top_box.png"
bottom_box_path = "cache/bottom_box.png"

pokemon_map, pokemon_name_list = load_pokemon()


def count_bbox(box):
    return box[0], box[1], box[0] + box[2], box[1] + box[3]


def find_closest_pokemon(name, pokemon_list):
    closest_match = difflib.get_close_matches(name, pokemon_list, n=1)
    return closest_match[0]


def capture_screen_and_ocr():
    # 截取屏幕指定区域的截图
    right_image = PIL.ImageGrab.grab(bbox=count_bbox(top_box))
    bottom_image = PIL.ImageGrab.grab(bbox=count_bbox(bottom_box))
    right_image.save(top_box_path)
    bottom_image.save(bottom_box_path)
    # 识别截图中的文字
    return ocr_pokemon_name_by_image(top_box_path), ocr_pokemon_name_by_image(bottom_box_path)


def capture_and_process():
    top_name, bottom_name = capture_screen_and_ocr()
    pokemon_name = top_name or bottom_name
    pokemon_data = pokemon_map.get(pokemon_name)

    if not pokemon_data:
        print(f"无法完全匹配 {pokemon_name}，采用近似算法")
        pokemon_name = find_closest_pokemon(pokemon_name, pokemon_name_list)
        pokemon_data = pokemon_map.get(pokemon_name)
        print(f"近似采用 {pokemon_name}")

    type1, type2 = pokemon_data["type1"], pokemon_data.get("type2")
    double_type, half_type = decide_fight_type(type1, type2)
    return pokemon_data, double_type, half_type


if __name__ == '__main__':
    print(capture_and_process())

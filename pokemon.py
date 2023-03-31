import requests
from bs4 import BeautifulSoup
import json
import os


def down_html(url):
    local_path = "cache/pokemon.html"

    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return f.read()

    # 发送 http 请求
    headers = {'Accept-Language': 'zh-CN'}
    response = requests.get(url, headers=headers)
    # 获取网页内容
    html = response.text
    with open(local_path, 'w', encoding="utf-8") as f:
        f.write(html)
    return html


def parse_and_save():
    html = down_html("https://wiki.52poke.com/zh-hans/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89")
    soup = BeautifulSoup(html, 'lxml')

    elements = soup.select("table.roundy tbody tr")

    pokemon_list = []
    for elem in elements:
        tds = elem.find_all("td")

        if not len(tds) == 8:
            continue

        no = tds[0].text.strip()
        name = tds[3].find_all("a")[0].text.strip()
        type1 = tds[6].text.strip()

        obj = {"no": no, "name": name, "type1": type1}

        if "hide" not in tds[7].attrs.get("class", []):
            type2 = tds[7].text.strip()
            obj["type2"] = type2

        pokemon_list.append(obj)

    print(pokemon_list)

    with open("pokemon.json", "w", encoding="utf-8") as f:
        json.dump(pokemon_list, f, ensure_ascii=False)


def load_pokemon():

    with open("pokemon.json", "r", encoding="utf-8") as f:
        pokemon_list = json.load(f)
        pokemon_map = {}
        pokemon_name_list = []

        for pokemon in pokemon_list:
            name = pokemon['name']
            pokemon_name_list.append(name)
            pokemon_map[name] = pokemon

        return pokemon_map, pokemon_name_list


if __name__ == '__main__':
    parse_and_save()
    print(load_pokemon)

import json


def load_fight_type():
    with open("fight_type.json", "r", encoding="utf-8") as f:
        tab = json.load(f)

        for key, array in tab.items():
            double_type = set(array[0])
            half_type = set(array[1])
            array[0] = double_type
            array[1] = half_type

        return tab


fight_type_dict = load_fight_type()


def decide_fight_type(type1, type2=None):
    if not type2:
        return fight_type_dict[type1]

    data1 = fight_type_dict[type1]
    data2 = fight_type_dict[type2]

    # 对 type1 和 type2 的双倍取并集
    double_type = data1[0].union(data2[0])

    # 对 type1 和 type 的 0.5 取并集
    half_type = data1[1].union(data2[1])

    # 做差集得到结果
    double_type = double_type - half_type

    return double_type, half_type


if __name__ == '__main__':
    print(decide_fight_type("格斗"))

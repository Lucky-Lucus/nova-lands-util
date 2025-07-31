from helpers import *


class Item:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
    
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def get_all(self):
        sub_ingr = []
        for ingr in self.ingredients:
            sub_ingr += ingr[0].get_all()
        return sub_ingr + self.ingredients

    def print_self(self):
        output = self.name + "\n"
        for ingr in self.ingredients:
            output += "   " + str(ingr[1]) + "x " + ingr[0].print_self()
        return output


def build_tree(item_list, name):
    item = Item(name)
    if item_list.get(name) is not None:
        components = item_list.get(name)["recipe"]
        amounts = item_list.get(name)["amounts"]
        for i in range(len(components)):
            item.add_ingredient((build_tree(item_list, components[i]), amounts[i]))
    return item


def print_item(item_list, name):
    thin_div()
    item = item_list.get(name)
    if item is None:
        print("Selected item does not exist, is a basic component or wrong command was entered (type \"help\" for a list of commands)")
        thin_div()
        return
    time = item["ttm"]
    alt_time = item["ttm"] * item["tmod"]
    alt_amount = 3 if item["alt"] else 2
    bench = decode_bench(item["bench"])

    title = f"[{1} / {alt_amount}] {name.upper()}"
    assembly_detail = f"in {bench} [ {sec_to_min(time)} / {sec_to_min(alt_time)}]"

    print(f"{title:<35} {assembly_detail:>38}")
    print(f"Ingeredients:")
    ingredients = get_ingredients(item)
    for i in range(len(ingredients)):
        ingr, num_ingr = ingredients[i]
        print(f" - {ingr} x [{num_ingr} / {num_ingr * 2}]")
    thin_div()


def count_ingredients(item_list, name, basic_only=False):
    thin_div()
    item = item_list.get(name)
    if item is None:
        print("Selected item does not exist or is a basic component")
        thin_div()
        return
    recipe_tree = build_tree(item_list, name)
    ingr_list = recipe_tree.get_all()
    ingr_names = []
    ingr_count = []
    for ingr in ingr_list:
        if ingr[0].name not in ingr_names:
            ingr_names.append(ingr[0].name)
            ingr_count.append(ingr[1])
        else:
            ingr_count[ingr_names.index(ingr[0].name)] += ingr[1]
    if basic_only:
        for name in ingr_names:
            if item_list.get(name) is None:
                print(f"{ingr_count[ingr_names.index(name)]:>2} x  {name}")
    else:
        for i in range(len(ingr_names)):
            print(f"{ingr_count[i]:>2} x  {ingr_names[i]}")
    thin_div()


def get_ingredients(item):
    ingredients = []
    if item is None:
        return None
    for i in range(len(item["recipe"])):
        ingr = item["recipe"][i]
        num_ingr = item["amounts"][i]
        ingredients.append((ingr, num_ingr))
    return ingredients
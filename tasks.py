from math import ceil, inf, isinf

from helpers import *

USING_ADVANCED = False

# Class to hold a crafting tree
class Item:
    def __init__(self, name):
        self.name = name        # name of an item
        self.bench = None       # crafting bench
        self.ttm = None         # time required to craft an item (time-to-make)
        self.ttm_a = None       # time required to craft an item in an advanced version of a bench
        self.alt = False         # whether the advanced recipe uses 2x (F) or 3x (T) the number of components
        self.ingredients = []   # list of crafting components
    
    # Add attrbutes of an item related to the crafting
    def add_attributes(self, bench, ttm, tmod, alt):
        self.bench = bench
        self.ttm = ttm
        self.ttm_a = tmod * ttm
        self.alt = alt
    
    # Add component to a list of components/ingredients and its amount (tuple: (item, amount))
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    # Get all components of an item (recursively, until leaves (basic ingredients) are reached) (returns list of tuples (name, amount needed))
    def get_all(self):
        if self.is_basic():
            return []
        sub_ingr = []
        for ingr in self.ingredients:
            sub_ingr += ingr[0].get_all()
        return sub_ingr + self.ingredients

    # Print formatted important information about an item
    def print_self(self):
        output = self.name + "\n"
        for ingr in self.ingredients:
            output += "   " + str(ingr[1]) + "x " + ingr[0].print_self()
        return output
    
    # Check if the ingredient is a basic one
    def is_basic(self):
        return not self.ingredients

# Build a tree of components (nodes: items, leaves: basic ingredients)
def build_tree(item_list, name):
    item = Item(name)
    if item_list.get(name) is not None:
        # fill out crafting attributes if the item is not a basic ingredient
        bench = item_list.get(name)["bench"]
        ttm = item_list.get(name)["ttm"]
        tmod = item_list.get(name)["tmod"]
        alt = item_list.get(name)["alt"]
        # add components/ingredients
        components = item_list.get(name)["recipe"]
        amounts = item_list.get(name)["amounts"]
        item.add_attributes(bench, ttm, tmod, alt)
        for i in range(len(components)):
            item.add_ingredient((build_tree(item_list, components[i]), amounts[i]))
    return item

# Print an item overview
def print_item(item_list, name):
    thin_div()
    item = item_list.get(name)
    # chech for item validity
    if item is None:
        print("Selected item does not exist, is a basic component or wrong command was entered (type \"help\" for a list of commands)")
        thin_div()
        return
    # get important attributes
    time = item["ttm"]
    alt_time = item["ttm"] * item["tmod"]
    alt_amount = 3 if item["alt"] else 2
    bench = parse_bench(item["bench"])

    # formatted "stat line" of an item
    title = f"[{1} / {alt_amount}] {name.upper()}"
    assembly_detail = f"in {bench} [ {sec_to_min(time)} / {sec_to_min(alt_time)}]"

    # formatted list of components/ingredients
    print(f"{title:<35} {assembly_detail:>38}")
    print(f"Ingeredients:")
    ingredients = get_ingredients(item)
    for i in range(len(ingredients)):
        ingr, num_ingr = ingredients[i]
        print(f" - {ingr} x [{num_ingr} / {num_ingr * 2}]")
    thin_div()

# Count the number of all components/ingredients required for an item
def count_ingredients(item_list, name, basic_only=False):
    thin_div()
    item = item_list.get(name)
    # check for item validity
    if item is None:
        print("Selected item does not exist or is a basic component")
        thin_div()
        return
    # create component tree and then component list
    recipe_tree = build_tree(item_list, name)
    ingr_list = recipe_tree.get_all()
    ingr_names = []
    ingr_count = []
    # go through the list and get all components/ingredients and their amounts
    for ingr in ingr_list:
        if ingr[0].name not in ingr_names:
            ingr_names.append(ingr[0].name)
            ingr_count.append(ingr[1])
        else:
            ingr_count[ingr_names.index(ingr[0].name)] += ingr[1]
    # include only basic ingredients
    if basic_only:
        for name in ingr_names:
            if item_list.get(name) is None:
                print(f"{ingr_count[ingr_names.index(name)]:>2} x  {name}")
    # include all components/ingredients
    else:
        for i in range(len(ingr_names)):
            print(f"{ingr_count[i]:>2} x  {ingr_names[i]}")
    thin_div()


# Get immediate components of an item
def get_ingredients(item):
    ingredients = []
    if item is None:
        return None
    for i in range(len(item["recipe"])):
        ingr = item["recipe"][i]
        num_ingr = item["amounts"][i]
        ingredients.append((ingr, num_ingr))
    return ingredients

# Count number of machines required to craft an item (does not take into account crafting time)
def get_benches(item_list, name, use_advanced=False):
    USING_ADVANCED = use_advanced
    thin_div()
    item = item_list.get(name)
    # check for item validity
    if item is None:
        print("Selected item does not exist or is a basic component")
        thin_div()
        return
    # create component tree
    recipe_tree = build_tree(item_list, name)
    # create list of all ingredients
    ingr_list = recipe_tree.get_all()
    # create dictionary of all benches needed and their amounts
    benches = {recipe_tree.bench: 1}
    for ingr in ingr_list:
        ingredient = ingr[0]
        # skip basic ingredients
        if ingredient.is_basic():
            continue
        amount = ingr[1]
        bench = ingredient.bench
        # if considering advanced benches
        if USING_ADVANCED:
            a_mod = 3 if ingredient.alt else 2
            amount = ceil(amount / a_mod)
        # count number of benches needed
        if bench in benches:
            benches[bench] += amount
        else:
            benches[bench] = amount
    # formatted print of the benches
    benches = dict(sorted(benches.items()))
    for b in benches:
        print(f"{benches[b]:>2} x  {"Advanced " if USING_ADVANCED and b != 'B' else ""}{parse_bench(b)}")
    thin_div()
    USING_ADVANCED = False

# Count minimal number of machines required to craft an item (changing recipes required) (suboptimal)
def get_minimal_benches(item_list, name, use_advanced=False):
    USING_ADVANCED = use_advanced
    thin_div()
    print("Sorry, this functionality is not yet tested. Enjoy anyway...")
    item = item_list.get(name)
    # check for item validity
    if item is None:
        print("Selected item does not exist or is a basic component")
        thin_div()
        return
    # create component tree
    recipe_tree = build_tree(item_list, name)
    # count minimal number of benches needed (BFS of item tree)
    benches = {}
    _process_item((recipe_tree, 1), benches, 0)
    # print final findings
    benches = dict(sorted(benches.items()))
    for b in benches.keys():
        print(f"{len(benches[b]):>2} x {"Advanced " if USING_ADVANCED and b != 'B' else ""}{parse_bench(b)}")
    thin_div()
    USING_ADVANCED = False
    pass

# Process next node
def _process_item(node, bench_dict, time_to_root=0):
    item = node[0]
    # if item is a basic ingredient then skip (reached a leaf)
    if item.is_basic():
        return
    amount = node[1]
    t_to_make = amount * (item.ttm_a if USING_ADVANCED else item.ttm)
    # breadth first search
    for child in item.ingredients:
        _process_item(child, bench_dict, time_to_root + t_to_make)
    # array of working times for given type of bench (if it exists, if not, append it with the time)
    try:
        bench_times = bench_dict[item.bench]
    except KeyError:
        bench_dict[item.bench] = [time_to_root + t_to_make]
        return
    # find if any of the machines will be available at the moment of need
    t_poss_bench = inf
    for t in bench_times:
        # find the biggest one (maximise working time)
        if t <= time_to_root + t_to_make:
            if t_poss_bench < t:
                t_poss_bench = t
    # if no available bench is found, add new time to availability
    if isinf(t_poss_bench):
        bench_times.append(time_to_root + t_to_make)
    else:
        bench_times = list(map(lambda x: (time_to_root + t_to_make) if x == t_poss_bench else (x), bench_times))
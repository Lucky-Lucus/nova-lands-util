import json

from tasks import *
from helpers import thick_div, help


def main():
    item_list = json.load(open("./items.json"))
    thick_div()
    while True:
        print("> Select which item you want details for (or \"exit\" to end): ", end="")
        user = input()
        words = user.split()
        if user == "exit":
            break
        if user == "help":
            help()
        elif words[0] == "comp":
            count_ingredients(item_list, " ".join(words[1:]))
        elif words[0] == "basic":
            count_ingredients(item_list, " ".join(words[1:]), basic_only=True)
        else:
            print_item(item_list, user)
    thick_div()


if __name__ == "__main__":
    main()
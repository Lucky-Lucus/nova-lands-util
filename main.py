import json

from tasks import *
from helpers import thick_div, help


def main():
    # initialize list of items
    item_list = json.load(open("./items.json"))
    thick_div()
    # main program loop (user input and corresponding behaviour)
    while True:
        print("> Select which item you want details for (or \"exit\" to end): ", end="")
        user = input()
        words = user.split()
        # quit program
        if user == "exit":
            break
        # print help
        elif user == "help":
            help()
        # count and list number of all ingredients
        elif words[0] == "comp":
            count_ingredients(item_list, " ".join(words[1:]))
        # count and list only basic ingredients
        elif words[0] == "basic":
            count_ingredients(item_list, " ".join(words[1:]), basic_only=True)
        # print general overview of an item
        else:
            print_item(item_list, user)
    thick_div()
    # end of program


if __name__ == "__main__":
    main()
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
        # list ingredients commmands
        elif words[0] == "comp":
            # basic ingredients
            if words[1] == "-b":
                count_ingredients(item_list, " ".join(words[2:]), basic_only=True)
            # all ingredients
            else:
                count_ingredients(item_list, " ".join(words[1:]))
        # list benches commands
        elif words[0] == "bench":
            # consider flags
            flags = 0
            use_adv = False
            minimal = False
            if "-a" in words:
                use_adv = True
                flags += 1
            if "-m" in words:
                minimal = True
                flags += 1
            # call correct command
            if use_adv and minimal:
                get_minimal_benches(item_list, " ".join(words[3:]), use_advanced=True)
            elif use_adv and not minimal:
                get_benches(item_list, " ".join(words[2:]), use_advanced=True)
            elif minimal:
                get_minimal_benches(item_list, " ".join(words[2:]))
            else:
                get_benches(item_list, " ".join(words[1:]))
        # print general overview of an item
        else:
            print_item(item_list, user)
    thick_div()
    # end of program


if __name__ == "__main__":
    main()
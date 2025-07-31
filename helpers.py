DIV_LEN = 75


def sec_to_min(s):
    s = s
    m = 0
    while True:
        if s - 60 >= 0:
            s -= 60
            m += 1
        else:
            break
    output = f"{m}m{s}s"
    if s == 0:
        output = f"{m}m"
    elif m == 0:
        output = f"{s}s"
    return output


def decode_bench(c):
    if c == "A":
        return "Assembler"
    elif c == "R":
        return "Refinery"
    elif c == "EF":
        return "Electric Furnace"
    elif c == "F":
        return "Furnace"
    elif c == "B":
        return "Barn"
    else:
        return "Unknown"


def thick_div():
    div = ""
    for _ in range(DIV_LEN):
        div += "="
    print(div)


def thin_div():
    div = ""
    for _ in range(DIV_LEN):
        div += "-"
    print(div)


def help():
    thin_div()
    print("List of helpful commands:")
    print(" > basic [item name]     : list of all basic materials needed for given item and their amounts")
    print(" > comp [item name]      : list of all materials needed for given item and their amounts")
    print(" > [item name]           : overview of an item with all useful information")
    print(" > help                  : list of all helpful commands")
    print(" > exit                  : end the program")
    thin_div()
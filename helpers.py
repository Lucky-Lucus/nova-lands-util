# MACROS:
DIV_LEN = 75        # length of the divider

# Convert seconds to minutes
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

# Convert workbench identifier to string
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

# Print thick divider
def thick_div():
    div = ""
    for _ in range(DIV_LEN):
        div += "="
    print(div)

# Print thin divider
def thin_div():
    div = ""
    for _ in range(DIV_LEN):
        div += "-"
    print(div)

# Print help
def help():
    thin_div()
    print("List of helpful commands:")
    print(" > [item name]                   : overview of an item with all useful information")
    print(" > comp [flags] [item name]      : list all materials required for crafting an item")
    print("     - -b   : list only basic materials needed")
    print(" > bench [flags] [item name]   : list all basic machines required for crafting")
    print("     - -m   : list minimal number of machines needed (takes into consideration crafting time)")
    print("     - -a   : list number of advanced machines required for crafting")
    print(" > help                          : list of all helpful commands")
    print(" > exit                          : end the program")
    thin_div()
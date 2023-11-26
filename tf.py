def stringToListOfTag(string: str):
    # I.S Pokonya stringnya ga boleh ngaco.

    # Contoh input
    # <hello> -> ["<hello>"]
    # <hello><world> -> ["<hello>", "<world>"]

    tags = string.split("><")
    for i in range(len(tags)):
        tags[i] = tags[i].replace("<", "")
        tags[i] = tags[i].replace(">", "")
        tags[i] = "<" + tags[i] + ">"

    return tags


with open("tf.txt", "r") as f:
    # I.S. FINAL STATE SEMUA SAMA, INITIAL STATE SEMUA SAMA
    tf_line = f.readline()
    if (tf_line != ""):
        t_function = tf_line.split(" ")
        print(f"FROM INITIAl STATE: {t_function[0]} TO {t_function[3]}:")
    while tf_line != "":
        t_function = tf_line.split(" ")

        bef_state = t_function[0]
        input_symbol = t_function[1]
        bef_top_stack = t_function[2]
        aft_state = t_function[3]
        aft_top_stack = stringToListOfTag(t_function[4])
        print(input_symbol, end=" ")
        print(bef_top_stack, end="/")
        print(t_function[4], end=" ")
        tf_line = f.readline()

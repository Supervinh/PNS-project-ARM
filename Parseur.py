import os.path
import re
import sys
import webbrowser
from tkinter import filedialog, Tk

import prettytable

new_file_name = "Parsed_File.bin"


# Converts an Integer to a Binary String
def int_2_bin(n, size=0):
    return f"{int(onlyInts(str(n))):0{size}b}"


# Converts a Binary string to Hexadecimal string
def bin_2_hex(bin_string, size=0):
    return f"{int(bin_string, 2):#0{size}x}"


# Only Keeps Integers in a String
def onlyInts(text):
    return re.sub("[^0-9]", "", text)


# Move back to line with Label
def gotoLabel(f, label_name):
    f.seek(0)
    line_nb = 0
    for _line in f.readlines():
        if _line == label_name:
            break
        line_nb += 1
    return line_nb


# Matches Keyword with Instructions
def parse_from_line(w):
    binary = ""
    args = ""
    match w[0]:
        case "lsl":
            if len(w) == 4:
                args = "Rd=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2]) + ", imm5=" + onlyInts(w[3])
                binary = "00000" + int_2_bin(w[3], 5) + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000010" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "lsr":
            if len(w) == 4:
                args = "Rd=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2]) + ", imm5=" + onlyInts(w[3])
                binary = "00001" + int_2_bin(w[3], 5) + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000011" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "asr":
            if len(w) == 4:
                args = "Rd=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2]) + ", imm5=" + onlyInts(w[3])
                binary = "00010" + int_2_bin(w[3], 5) + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000100" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "add":
            if len(w) == 4 and w[3][:1] == "r":
                args = "Rd=" + onlyInts(w[1]) + ", Rn=" + onlyInts(w[2]) + ", Rm=" + onlyInts(w[3])
                binary = "0001100" + int_2_bin(w[3], 3) + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)
            if len(w) == 4 and w[3][:1] == "#":
                args = "Rd=" + onlyInts(w[1]) + ", Rn=" + onlyInts(w[2]) + ", imm3=" + onlyInts(w[3])
                binary = "0001110" + int_2_bin(w[3], 3) + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)
            if len(w) == 3 and w[1] != "sp":  # Number of Arguments ? Can change ?
                args = "Rdn=" + onlyInts(w[1]) + ", imm8=" + onlyInts(w[2])
                binary = "00110" + int_2_bin(w[1], 3) + int_2_bin(w[2], 8)
            if len(w) == 3 and w[1] == "sp":
                args = "imm7=" + onlyInts(w[2])
                binary = "101100000" + int_2_bin(int(int(onlyInts(w[2])) / 4), 7)

        case "sub":
            if len(w) == 4 and w[3][:1] == "r":
                args = "Rd=" + onlyInts(w[1]) + ", Rn=" + onlyInts(w[2]) + ", Rm=" + onlyInts(w[3])
                binary = "0001101" + int_2_bin(w[3], 3) + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)
            if len(w) == 4 and w[3][:1] == "#":
                args = "Rd=" + onlyInts(w[1]) + ", Rn=" + onlyInts(w[2]) + ", imm3=" + onlyInts(w[3])
                binary = "0001111" + int_2_bin(w[3], 3) + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)
            if len(w) == 3 and w[1] != "sp":  # Number of Arguments ? Can Change ?
                args = "Rdn=" + onlyInts(w[1]) + ", imm8=" + onlyInts(w[2])
                binary = "00111" + int_2_bin(w[1], 3) + int_2_bin(w[2], 8)
            if len(w) == 3 and w[1] == "sp":
                args = "imm7=" + onlyInts(w[2])
                binary = "101100001" + int_2_bin(int(int(onlyInts(w[2])) / 4), 7)

        case "mov":
            if len(w) == 3:
                args = "Rd=" + onlyInts(w[1]) + ", imm8=" + onlyInts(w[2])
                binary = "00100" + int_2_bin(w[1], 3) + int_2_bin(w[2], 8)

        case "cmp":
            if len(w) == 3 and w[2][:1] == "#":
                args = "Rd=" + onlyInts(w[1]) + ", imm8=" + onlyInts(w[2])
                binary = "00101" + int_2_bin(w[1], 3) + int_2_bin(w[2], 8)
            if len(w) == 3 and w[2][:1] == "r":
                args = "Rn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100001010" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "and":
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000000" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "eor":
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000001" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "adc":
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000101" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "sbc":
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000110" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "ror":
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100000111" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "tst":
            if len(w) == 3:
                args = "Rn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100001000" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "rsb":
            if len(w) == 4:
                args = "Rd=" + onlyInts(w[1]) + ", Rn=" + onlyInts(w[2])
                binary = "0100001001" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "cmn":
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100001011" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "orr":
            if len(w) == 3:
                args = "Rdm=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100001100" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "mul":
            if len(w) == 4:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2]) + ", Rdm=" + onlyInts(w[3])
                binary = "0100001101" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "bic":
            if len(w) == 3:
                args = "Rdn=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100001110" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "mvn":
            if len(w) == 3:
                args = "Rd=" + onlyInts(w[1]) + ", Rm=" + onlyInts(w[2])
                binary = "0100001111" + int_2_bin(w[2], 3) + int_2_bin(w[1], 3)

        case "str":
            if len(w) == 3:
                w.append("0")
            if len(w) == 4:
                args = "Rt=" + onlyInts(w[1]) + ", imm8=" + onlyInts(w[3])
                binary = "10010" + int_2_bin(w[1], 3) + int_2_bin(int(int(onlyInts(w[3])) / 4), 8)

        case "ldr":
            print(w)
            if len(w) == 3:
                w.append("0")
            if len(w) == 4:
                args = "Rt=" + onlyInts(w[1]) + ", imm8=" + onlyInts(w[3])
                binary = "10011" + int_2_bin(w[1], 3) + int_2_bin(int(int(onlyInts(w[3])) / 4), 8)

        case "b":  # Branches Conditional and Unconditional
            if len(w) == 3:  # words[1] & words[2] ?
                args = "cond=" + onlyInts(w[1]) + ", imm8=" + onlyInts(w[2])
                binary = "1101" + int_2_bin(w[2], 4) + int_2_bin(w[1], 8)
            elif len(w) == 2:
                args = "imm11=" + onlyInts(w[1])
                binary = "11100" + int_2_bin(w[1], 11)  # words[1] ?

        case _:
            sys.stdout.write("Error")
    return bin_2_hex(binary, 6), args


def table_width(tab):
    nb = 0
    for char in tab.get_string():
        if char != "\n":
            nb += 1
        else:
            break
    return nb


if __name__ == '__main__':
    # Initialise list of Instructions and Count
    instructions_total = []
    count_instructions_total = 0
    pc_count = 0

    # Setting up variables for Visuals
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    table = prettytable.PrettyTable()

    # Choosing File to Parse
    files_path = filedialog.askopenfilenames(parent=root, title="Python Parser - Select File to Parse",
                                             filetypes=[("S File", ".s")])

    if not files_path:
        print("No Files Selected")
        exit(0)

    for file_path in files_path:
        instructions = []
        count_instructions = 0
        print()
        table.clear()
        table.field_names = ["PC", "Instruction", "Arguments", "Hex Op"]
        file = None
        try:
            file = open(file_path, 'r')
        except Exception as e:
            print("No File was Selected ->", e)
            exit(0)

        # Reads from given File
        t, title = os.path.split(file_path)
        for line in file.readlines():

            line = line.replace("\n", "").replace(",", " ").replace("  ", " ").lower()
            if line[-1:] == " ":
                line = line[:-1]

            # Only Reads lines that are not empty and not in comments
            if line[:1] != "@" and line[:1] != "." and line:
                words = line.split(" ")
                words[0] = words[0][:3]

                # Setting Text for Table
                pc = bin_2_hex(int_2_bin(pc_count), 6)
                instruction = line
                hex_op, arguments = parse_from_line(words)

                # Adding Binary string to Instructions
                if hex_op:
                    instructions.append(hex_op)

                # Increment Counters
                pc_count += 2
                count_instructions += 1
                table.add_row([pc, line, arguments, hex_op])
        file.close()
        for i in instructions:
            instructions_total.append(i)
        count_instructions_total += count_instructions

        # Calculate Indentation Title
        title = "--- Parsing " + title + " ---"
        count_chars = table_width(table)
        before_spaces = int((count_chars - len(title)) * 0.5)
        print(" " * before_spaces + title)

        # Show Table
        table.align["Instruction"] = "l"
        table.align["Arguments"] = "l"
        print(table)

        # Calculate Indentation Results
        result = str(len(instructions)) + "/" + str(count_instructions) + " Instructions Parsed"
        before_spaces = int((count_chars - len(result)) * 0.5)
        print(" " * before_spaces + result)
        print()

    # Delete New File if it already Exists
    if os.path.exists(new_file_name):
        os.remove(new_file_name)

    # Writing Hexadecimals to New File
    file = open(new_file_name, "w")
    file.write("v2.0 raw\n")
    count = 0
    for h in instructions_total:
        count += 1
        file.write(h.replace("0x", "") + " ")
        if count % 16 == 0:
            file.write("\n")
    file.close()

    webbrowser.open(new_file_name)

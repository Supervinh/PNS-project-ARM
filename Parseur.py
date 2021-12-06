import os.path
import sys
from tkinter import filedialog, Tk
import webbrowser

new_file_name = "Parsed_File.bin"


# Converts an Integer to a Binary String
def int_2_bin(n, size=0):
    n = str(n).replace("#", "").replace("r", "")
    binary_text = "{0:b}".format(int(n))
    if size != 0 and len(binary_text) > size:
        binary_text = binary_text[len(binary_text) - size:]
    return "0" * (size - len(binary_text)) + binary_text


# Converts a Binary string to Hexadecimal string
def bin_2_hex(bin_string):
    return hex(int(bin_string, 2))


if __name__ == '__main__':
    # Initialise list of Instructions and Count
    instructions = []
    count_instructions = 0

    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

    # Choosing File to Parse
    file_path = filedialog.askopenfilename(parent=root, title="Python Parser - Select File to Parse",
                                           filetypes=[("S File", ".s")])
    try:
        file = open(file_path, 'r')
    except Exception as e:
        print("No File was Selected ->", e)
        exit(0)

    # Reads from given File
    print("--- Parsing ---")
    for line in file.readlines():
        line = line.replace("\n", "").replace(",", "").lower()
        if line[-1:] == " ":
            line = line[:-1]

        # Only Reads lines that are not empty and not in comments
        if line[:1] != "@" and line:
            sys.stdout.write(line)
            binary = ""
            words = line.split(" ")
            words[0] = words[0][:3]

            # Matches Keyword with Instructions
            match words[0]:
                case "lsl":
                    if len(words) == 4:
                        binary = "00000" + int_2_bin(words[3], 5) + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)
                    if len(words) == 3:
                        binary = "0100000010" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "lsr":
                    if len(words) == 4:
                        binary = "00001" + int_2_bin(words[3], 5) + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)
                    if len(words) == 3:
                        binary = "0100000011" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "asr":
                    if len(words) == 4:
                        binary = "00010" + int_2_bin(words[3], 5) + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)
                    if len(words) == 3:
                        binary = "0100000100" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "add":
                    if len(words) == 4 and words[3][:1] == "r":
                        binary = "0001100" + int_2_bin(words[3], 3) + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)
                    if len(words) == 4 and words[3][:1] == "#":
                        binary = "0001110" + int_2_bin(words[3], 3) + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)
                    if len(words) == 3:  # Number of Arguments ? Can change ?
                        binary = "00110" + int_2_bin(words[1], 3) + int_2_bin(words[2], 8)

                case "sub":
                    if len(words) == 4 and words[3][:1] == "r":
                        binary = "0001101" + int_2_bin(words[3], 3) + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)
                    if len(words) == 4 and words[3][:1] == "#":
                        binary = "0001111" + int_2_bin(words[3], 3) + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)
                    if len(words) == 3:  # Number of Arguments ? Can Change ?
                        binary = "00111" + int_2_bin(words[1], 3) + int_2_bin(words[2], 8)

                case "mov":
                    if len(words) == 3:
                        binary = "00100" + int_2_bin(words[1], 3) + int_2_bin(words[2], 8)

                case "cmp":
                    if len(words) == 3 and words[2][:1] == "#":
                        binary = "00101" + int_2_bin(words[1], 3) + int_2_bin(words[2], 8)
                    if len(words) == 3 and words[2][:1] == "r":
                        binary = "0100001010" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "and":
                    if len(words) == 3:
                        binary = "0100000000" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "eor":
                    if len(words) == 3:
                        binary = "0100000001" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "adc":
                    if len(words) == 3:
                        binary = "0100000101" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "sbc":
                    if len(words) == 3:
                        binary = "0100000110" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "ror":
                    if len(words) == 3:
                        binary = "0100000111" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "tst":
                    if len(words) == 3:
                        binary = "0100001000" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "rsb":
                    if len(words) == 4:
                        binary = "0100001001" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "cmn":
                    if len(words) == 3:
                        binary = "0100001011" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "orr":
                    if len(words) == 3:
                        binary = "0100001100" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "mul":
                    if len(words) == 4:
                        binary = "0100001101" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "bic":
                    if len(words) == 3:
                        binary = "0100001110" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "mvn":
                    if len(words) == 3:
                        binary = "0100001111" + int_2_bin(words[2], 3) + int_2_bin(words[1], 3)

                case "str":
                    if len(words) == 3:
                        binary = "10010" + int_2_bin(words[1], 3) + int_2_bin(int(int(words[2]) / 4), 8)

                case "ldr":
                    if len(words) == 3:
                        binary = "10011" + int_2_bin(words[1], 3) + int_2_bin(int(int(words[2]) / 4), 8)

                case "add":  # With SP
                    if len(words) == 3:  # Number of Arguments ?
                        binary = "101100000" + int_2_bin(int(int(words[2]) / 4), 7)

                case "sub":  # With SP
                    if len(words) == 3:  # Number of Arguments ?
                        binary = "101100001" + int_2_bin(int(int(words[2]) / 4), 7)

                case "B":  # Branches Conditional and Unconditional
                    if len(words) == 3:  # words[1] & words[2] ?
                        binary = "1101" + int_2_bin(words[2], 4) + int_2_bin(words[1], 8)
                    elif len(words) == 2:
                        binary = "11100" + int_2_bin(words[1], 11)  # words[1] ?

                case _:
                    sys.stdout.write("Nothing ")

            # Adding Binary string to Instructions
            if binary:
                instructions.append(binary)
            count_instructions += 1
            print()
    file.close()
    print()

    # Convert all Binaries to Hexadecimals
    for i in range(len(instructions)):
        instructions[i] = bin_2_hex(instructions[i])

    # Delete New File if it already Exists
    if os.path.exists(new_file_name):
        os.remove(new_file_name)

    # Writing Hexadecimals to New File
    file = open(new_file_name, "w")
    for h in instructions:
        file.write(h.replace("0x", "") + " ")
    file.close()

    # Show Results
    print("--- Instructions Parsed ---")
    print(instructions, str(len(instructions)) + "/" + str(count_instructions), "Instructions")

    webbrowser.open(new_file_name)

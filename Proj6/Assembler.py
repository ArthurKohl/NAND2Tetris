import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
    "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111",
    "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101", "M": "1110000", "!M": "1110001",
    "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"
}

DEST = {
    "null": "000", "M": "001", "D": "010", "MD": "011", "DM": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111", "ADM": "111"
}

JUMP = {
    "null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def assemble(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        line = line.split('//')[0].strip()
        line = line.replace(" ", "")
        if line:
            cleaned_lines.append(line)

    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        symbols[f"R{i}"] = i

    instructions = []
    rom_address = 0
    for line in cleaned_lines:
        if line.startswith('(') and line.endswith(')'):
            label = line[1:-1]
            symbols[label] = rom_address
        else:
            instructions.append(line)
            rom_address += 1

    output = []
    ram_address = 16
    for line in instructions:
        if line.startswith('@'):
            val = line[1:]
            if val.isdigit():
                address = int(val)
            else:
                if val not in symbols:
                    symbols[val] = ram_address
                    ram_address += 1
                address = symbols[val]
            output.append(f"{address:016b}")
        else:
            dest_str = "null"
            comp_str = line
            jump_str = "null"

            if "=" in comp_str:
                dest_str, comp_str = comp_str.split("=")
            if ";" in comp_str:
                comp_str, jump_str = comp_str.split(";")

            c_bits = COMP[comp_str]
            d_bits = DEST[dest_str]
            j_bits = JUMP[jump_str]
            output.append("111" + c_bits + d_bits + j_bits)

    out_filepath = filepath.replace(".asm", ".hack")
    with open(out_filepath, 'w') as file:
        file.write('\n'.join(output) + '\n')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        assemble(sys.argv[1])

import sys
import os

SEGMENTS = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
JUMPS = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
OPERATORS = {"add": "D+M", "sub": "M-D", "and": "D&M", "or": "D|M"}


def translate(filepath):
    with open(filepath, 'r') as file:
        lines = [line.split('//')[0].strip() for line in file]

    filename = os.path.basename(filepath).replace('.vm', '')
    output = []
    label_count = 0

    for line in lines:
        if not line:
            continue

        parts = line.split()
        command = parts[0]
        output.append("// " + line)

        if command == "push":
            segment, index = parts[1], parts[2]
            # coloca o valor em D
            if segment == "constant":
                output.append(f"@{index}\nD=A")
            elif segment in SEGMENTS:
                output.append(f"@{index}\nD=A\n@{SEGMENTS[segment]}\nA=D+M\nD=M")
            elif segment == "temp":
                output.append(f"@{5 + int(index)}\nD=M")
            elif segment == "pointer":
                output.append(f"@{3 + int(index)}\nD=M")
            elif segment == "static":
                output.append(f"@{filename}.{index}\nD=M")
            # empurra D para a pilha
            output.append("@SP\nA=M\nM=D\n@SP\nM=M+1")

        elif command == "pop":
            segment, index = parts[1], parts[2]
            if segment in SEGMENTS:
                # guarda o endereco de destino em R13
                output.append(f"@{index}\nD=A\n@{SEGMENTS[segment]}\nD=D+M\n@R13\nM=D")
                output.append("@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D")
            else:
                if segment == "temp":
                    addr = str(5 + int(index))
                elif segment == "pointer":
                    addr = str(3 + int(index))
                elif segment == "static":
                    addr = f"{filename}.{index}"
                output.append(f"@SP\nAM=M-1\nD=M\n@{addr}\nM=D")

        elif command in OPERATORS:
            output.append(f"@SP\nAM=M-1\nD=M\nA=A-1\nM={OPERATORS[command]}")

        elif command == "neg":
            output.append("@SP\nA=M-1\nM=-M")

        elif command == "not":
            output.append("@SP\nA=M-1\nM=!M")

        elif command in JUMPS:
            n = label_count
            label_count += 1
            output.append(f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
                          f"@TRUE_{n}\nD;{JUMPS[command]}\n"
                          f"@SP\nA=M-1\nM=0\n@END_{n}\n0;JMP\n"
                          f"(TRUE_{n})\n@SP\nA=M-1\nM=-1\n(END_{n})")

    out_filepath = filepath.replace('.vm', '.asm')
    with open(out_filepath, 'w') as file:
        file.write('\n'.join(output) + '\n')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        translate(sys.argv[1])

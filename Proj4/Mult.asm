// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/mult/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1] and RAM[2], respectively.)
// Assumes R0 >= 0, R1 >= 0, and R0 * R1 < 32768.
//
// Strategy: repeated addition. Add R0 to an accumulator R1 times.
//   R2 = 0
//   for (i = 0; i < R1; i++)
//       R2 = R2 + R0

// R2 = 0  (never assume RAM starts clean)
    @R2
    M=0

// i = 0  (i is a variable; the assembler allocates it at RAM[16])
    @i
    M=0

(LOOP)
// D = i - R1 ; if (D >= 0) goto END
    @i
    D=M
    @R1
    D=D-M
    @END
    D;JGE

// R2 = R2 + R0
    @R0
    D=M
    @R2
    M=D+M

// i = i + 1
    @i
    M=M+1

    @LOOP
    0;JMP

(END)
// Infinite loop: halts the program without letting the CPU
// run off into whatever garbage follows in ROM.
    @END
    0;JMP

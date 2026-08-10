// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/fill/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed,
// the screen is cleared.
//
// Memory map:
//   SCREEN = 16384 .. 24575  (8192 words, 512 x 256 pixels, 16 pixels per word)
//   KBD    = 24576           (0 when no key is pressed)
// Note that KBD is also the first address *after* the screen, which is
// what makes it a convenient end-of-screen sentinel below.

(MAIN)
// D = keyboard value ; if (D == 0) goto WHITE
    @KBD
    D=M
    @WHITE
    D;JEQ

// A key is pressed: color = -1 = 1111111111111111 = 16 black pixels
    @color
    M=-1
    @PAINT
    0;JMP

(WHITE)
// No key pressed: color = 0 = 0000000000000000 = 16 white pixels
    @color
    M=0

(PAINT)
// addr = SCREEN  (@SCREEN puts the constant 16384 in A, so read it with D=A, not D=M)
    @SCREEN
    D=A
    @addr
    M=D

(PAINT_LOOP)
// D = addr - 24576 ; if (D >= 0) the whole screen is painted, so re-check the keyboard
    @addr
    D=M
    @KBD
    D=D-A
    @MAIN
    D;JGE

// RAM[addr] = color
    @color
    D=M
    @addr
    A=M       // point A at the screen word itself
    M=D       // write the color into it

// addr = addr + 1
    @addr
    M=M+1

    @PAINT_LOOP
    0;JMP

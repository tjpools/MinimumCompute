; Hello, World! Program
; Our first program for the NAND Compute architecture
; Outputs "Hello, World!" followed by a newline

.ORG 0x00

main:
    ; Output 'H' (ASCII 72)
    LOADI R0, 72
    OUT R0
    
    ; Output 'e' (ASCII 101)
    LOADI R0, 101
    OUT R0
    
    ; Output 'l' (ASCII 108)
    LOADI R0, 108
    OUT R0
    
    ; Output 'l' again
    OUT R0
    
    ; Output 'o' (ASCII 111)
    LOADI R0, 111
    OUT R0
    
    ; Output ',' (ASCII 44)
    LOADI R0, 44
    OUT R0
    
    ; Output ' ' (space, ASCII 32)
    LOADI R0, 32
    OUT R0
    
    ; Output 'W' (ASCII 87)
    LOADI R0, 87
    OUT R0
    
    ; Output 'o' (ASCII 111)
    LOADI R0, 111
    OUT R0
    
    ; Output 'r' (ASCII 114)
    LOADI R0, 114
    OUT R0
    
    ; Output 'l' (ASCII 108)
    LOADI R0, 108
    OUT R0
    
    ; Output 'd' (ASCII 100)
    LOADI R0, 100
    OUT R0
    
    ; Output '!' (ASCII 33)
    LOADI R0, 33
    OUT R0
    
    ; Output newline (ASCII 10)
    LOADI R0, 10
    OUT R0
    
    ; Stop execution
    HALT

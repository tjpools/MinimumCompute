; Counter Program
; Counts from 0 to 9 and outputs each digit

.ORG 0x00

main:
    ; Initialize counter to '0' (ASCII 48)
    LOADI R0, 48
    
    ; Set limit to ':' (ASCII 58, which is '9' + 1)
    LOADI R1, 58

loop:
    ; Output current digit
    OUT R0
    
    ; Increment counter
    INC R0
    
    ; Check if we reached the limit
    ; R2 = R0 - R1
    SUB R2, R0, R1
    
    ; If R2 != 0, continue loop
    JNZ R2, loop
    
    ; Output newline
    LOADI R0, 10
    OUT R0
    
    ; Stop
    HALT

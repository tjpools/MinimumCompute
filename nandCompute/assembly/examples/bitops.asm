; Bit Operations Demo
; Demonstrates logical operations

.ORG 0x00

main:
    ; Load test values
    LOADI R0, 0b11110000  ; 240
    LOADI R1, 0b10101010  ; 170
    
    ; AND operation
    AND R2, R0, R1
    ; Result should be 0b10100000 = 160
    
    ; OR operation
    OR R3, R0, R1
    ; Result should be 0b11111010 = 250
    
    ; XOR operation
    XOR R4, R0, R1
    ; Result should be 0b01011010 = 90
    
    ; NOT operation
    NOT R5, R0
    ; Result should be 0b00001111 = 15
    
    ; Output results as decimal digits
    ; For simplicity, just output 'OK' if logic works
    
    ; Quick test: R2 should be 160
    LOADI R6, 160
    SUB R7, R2, R6
    JNZ R7, error
    
    ; If we get here, it worked
    LOADI R0, 79   ; 'O'
    OUT R0
    LOADI R0, 75   ; 'K'
    OUT R0
    LOADI R0, 10   ; newline
    OUT R0
    HALT

error:
    LOADI R0, 69   ; 'E'
    OUT R0
    LOADI R0, 82   ; 'R'
    OUT R0
    LOADI R0, 82   ; 'R'
    OUT R0
    LOADI R0, 10   ; newline
    OUT R0
    HALT

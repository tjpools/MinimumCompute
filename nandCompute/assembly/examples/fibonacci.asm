; Fibonacci Sequence
; Outputs first few Fibonacci numbers as ASCII digits

.ORG 0x00

main:
    ; Initialize F(0) = 0, F(1) = 1
    LOADI R0, 0
    LOADI R1, 1
    
    ; Counter for how many numbers to output
    LOADI R3, 8
    
    ; Output first number (0)
    LOADI R6, 48      ; ASCII '0'
    ADD R4, R0, R6    ; Convert to ASCII
    OUT R4
    LOADI R5, 32      ; Space
    OUT R5

fib_loop:
    ; Output F(1) - convert to ASCII
    LOADI R6, 48      ; ASCII '0'
    ADD R4, R1, R6    ; Add to convert number to ASCII
    OUT R4
    OUT R5            ; Space
    
    ; Calculate next: R2 = R0 + R1
    ADD R2, R0, R1
    
    ; Shift values: R0 = R1, R1 = R2
    LOADI R7, 0
    ADD R0, R1, R7    ; R0 = R1 (R1 + 0)
    ADD R1, R2, R7    ; R1 = R2 (R2 + 0)
    
    ; Decrement counter
    DEC R3
    
    ; Continue if counter != 0
    JNZ R3, fib_loop
    
    ; Output newline
    LOADI R0, 10
    OUT R0
    
    HALT

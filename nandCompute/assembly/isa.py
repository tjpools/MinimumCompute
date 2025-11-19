"""
Assembly Language Specification

This document defines the Instruction Set Architecture (ISA) for our NAND-based computer.
"""

# Assembly language specification

ISA = """
# NAND Compute - Instruction Set Architecture (ISA)

## Overview

- **Architecture**: 8-bit data path, 8-bit address space
- **Registers**: 8 general-purpose registers (R0-R7)
- **Memory**: 256 bytes of RAM (addresses 0x00-0xFF)
- **Instruction Width**: 16 bits (for simplicity in encoding)

## Instruction Format

```
| 15-12 | 11-8 | 7-4 | 3-0 |
|-------|------|-----|-----|
| OPCODE| Rd   | Rs1 | Rs2 |
```

For instructions with immediate values or addresses:
```
| 15-12 | 11-8 |  7-0    |
|-------|------|---------|
| OPCODE| Reg  | IMM/ADDR|
```

## Instruction Set

### Data Movement

**LOAD Rd, addr** - Load from memory to register
- Opcode: `0001` (1)
- Format: `0001 dddd aaaaaaaa`
- Operation: `Rd = MEM[addr]`
- Example: `LOAD R0, 42` loads value at memory address 42 into R0

**LOADI Rd, imm** - Load immediate value to register
- Opcode: `0010` (2)
- Format: `0010 dddd iiiiiiii`
- Operation: `Rd = imm`
- Example: `LOADI R0, 72` loads decimal 72 ('H') into R0

**STORE Rs, addr** - Store register to memory
- Opcode: `0011` (3)
- Format: `0011 ssss aaaaaaaa`
- Operation: `MEM[addr] = Rs`
- Example: `STORE R0, 100` stores R0's value at memory address 100

### Arithmetic Operations

**ADD Rd, Rs1, Rs2** - Add two registers
- Opcode: `0100` (4)
- Format: `0100 dddd ssss tttt`
- Operation: `Rd = Rs1 + Rs2`
- Example: `ADD R0, R1, R2` computes R0 = R1 + R2

**SUB Rd, Rs1, Rs2** - Subtract two registers
- Opcode: `0101` (5)
- Format: `0101 dddd ssss tttt`
- Operation: `Rd = Rs1 - Rs2`
- Example: `SUB R0, R1, R2` computes R0 = R1 - R2

**INC Rd** - Increment register
- Opcode: `0110` (6)
- Format: `0110 dddd 0000 0000`
- Operation: `Rd = Rd + 1`
- Example: `INC R0` increments R0

**DEC Rd** - Decrement register
- Opcode: `0111` (7)
- Format: `0111 dddd 0000 0000`
- Operation: `Rd = Rd - 1`
- Example: `DEC R0` decrements R0

### Logical Operations

**AND Rd, Rs1, Rs2** - Bitwise AND
- Opcode: `1000` (8)
- Format: `1000 dddd ssss tttt`
- Operation: `Rd = Rs1 & Rs2`
- Example: `AND R0, R1, R2`

**OR Rd, Rs1, Rs2** - Bitwise OR
- Opcode: `1001` (9)
- Format: `1001 dddd ssss tttt`
- Operation: `Rd = Rs1 | Rs2`
- Example: `OR R0, R1, R2`

**XOR Rd, Rs1, Rs2** - Bitwise XOR
- Opcode: `1010` (10)
- Format: `1010 dddd ssss tttt`
- Operation: `Rd = Rs1 ^ Rs2`
- Example: `XOR R0, R1, R2`

**NOT Rd, Rs** - Bitwise NOT
- Opcode: `1011` (11)
- Format: `1011 dddd ssss 0000`
- Operation: `Rd = ~Rs`
- Example: `NOT R0, R1`

### Control Flow

**JMP addr** - Unconditional jump
- Opcode: `1100` (12)
- Format: `1100 0000 aaaaaaaa`
- Operation: `PC = addr`
- Example: `JMP 10` jumps to address 10

**JZ Rs, addr** - Jump if zero
- Opcode: `1101` (13)
- Format: `1101 ssss aaaaaaaa`
- Operation: `if Rs == 0 then PC = addr`
- Example: `JZ R0, 10` jumps to address 10 if R0 is zero

**JNZ Rs, addr** - Jump if not zero
- Opcode: `1110` (14)
- Format: `1110 ssss aaaaaaaa`
- Operation: `if Rs != 0 then PC = addr`
- Example: `JNZ R0, 10` jumps to address 10 if R0 is not zero

### I/O Operations

**OUT Rs** - Output register value as ASCII character
- Opcode: `1111` (15)
- Format: `1111 ssss 0000 0000`
- Operation: `print(char(Rs))`
- Example: `OUT R0` outputs the ASCII character in R0

### Special

**HALT** - Stop execution
- Opcode: `0000` (0)
- Format: `0000 0000 0000 0000`
- Operation: Stop the CPU
- Example: `HALT`

**NOP** - No operation
- Same as HALT opcode but can be used differently
- Just advances PC

## Register Convention

- **R0-R7**: General purpose registers
- No dedicated register conventions (all are general purpose)
- Programmer's choice for temporary values, parameters, etc.

## Memory Map

```
0x00-0x7F (0-127):   Program Code
0x80-0xFF (128-255): Data and Stack
```

## Assembly Syntax

### Comments
```
; This is a comment
```

### Labels
```
loop:           ; Define a label
    LOADI R0, 65
    OUT R0
    JMP loop    ; Reference a label
```

### Directives

**.ORG addr** - Set assembly origin address
```
.ORG 0x00      ; Start at address 0
```

**.DATA** - Define data in memory
```
.ORG 0x80
.DATA 72, 101, 108, 108, 111  ; "Hello" in ASCII
```

## Example Programs

### Hello World
```asm
; Hello World Program
.ORG 0x00

main:
    LOADI R0, 72    ; 'H'
    OUT R0
    LOADI R0, 101   ; 'e'
    OUT R0
    LOADI R0, 108   ; 'l'
    OUT R0
    OUT R0          ; 'l' again
    LOADI R0, 111   ; 'o'
    OUT R0
    LOADI R0, 44    ; ','
    OUT R0
    LOADI R0, 32    ; ' '
    OUT R0
    LOADI R0, 87    ; 'W'
    OUT R0
    LOADI R0, 111   ; 'o'
    OUT R0
    LOADI R0, 114   ; 'r'
    OUT R0
    LOADI R0, 108   ; 'l'
    OUT R0
    LOADI R0, 100   ; 'd'
    OUT R0
    LOADI R0, 33    ; '!'
    OUT R0
    LOADI R0, 10    ; newline
    OUT R0
    HALT
```

### Counter (0-9)
```asm
; Count from 0 to 9
.ORG 0x00

    LOADI R0, 48    ; ASCII '0'
    LOADI R1, 58    ; ASCII '9' + 1 (stopping point)

loop:
    OUT R0          ; Output current digit
    INC R0          ; Next digit
    SUB R2, R0, R1  ; R2 = R0 - R1
    JNZ R2, loop    ; Continue if not equal
    
    LOADI R0, 10    ; Newline
    OUT R0
    HALT
```

### Fibonacci (first 10 numbers)
```asm
; Fibonacci sequence
.ORG 0x00

    LOADI R0, 0     ; F(0)
    LOADI R1, 1     ; F(1)
    LOADI R3, 10    ; Counter

loop:
    ADD R2, R0, R1  ; R2 = R0 + R1
    ; Convert to ASCII digit (assuming < 10)
    ADD R4, R2, 48  ; Add ASCII '0'
    OUT R4
    
    ; Shift values
    ADD R0, R1, 0   ; R0 = R1 (using ADD as MOV)
    ADD R1, R2, 0   ; R1 = R2
    
    DEC R3
    JNZ R3, loop
    
    HALT
```

## Encoding Reference

| Instruction | Opcode | Binary | Hex |
|-------------|--------|--------|-----|
| HALT        | 0      | 0000   | 0x0 |
| LOAD        | 1      | 0001   | 0x1 |
| LOADI       | 2      | 0010   | 0x2 |
| STORE       | 3      | 0011   | 0x3 |
| ADD         | 4      | 0100   | 0x4 |
| SUB         | 5      | 0101   | 0x5 |
| INC         | 6      | 0110   | 0x6 |
| DEC         | 7      | 0111   | 0x7 |
| AND         | 8      | 1000   | 0x8 |
| OR          | 9      | 1001   | 0x9 |
| XOR         | 10     | 1010   | 0xA |
| NOT         | 11     | 1011   | 0xB |
| JMP         | 12     | 1100   | 0xC |
| JZ          | 13     | 1101   | 0xD |
| JNZ         | 14     | 1110   | 0xE |
| OUT         | 15     | 1111   | 0xF |

## Notes

- All arithmetic is 8-bit unsigned (0-255)
- No hardware stack - must be implemented in software if needed
- No subroutine call/return instructions - implement with JMP
- Flags are not exposed to programmer (internal to CPU only)
"""

if __name__ == "__main__":
    print(ISA)

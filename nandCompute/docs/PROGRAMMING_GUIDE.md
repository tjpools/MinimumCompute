# Building Your Own Programs

## Getting Started

Create a new assembly file in `assembly/examples/`:

```bash
touch assembly/examples/myprogram.asm
```

## Basic Program Structure

```asm
; Comments start with semicolon
.ORG 0x00          ; Start at address 0

main:              ; Label for main entry point
    LOADI R0, 65   ; Load ASCII 'A' into R0
    OUT R0         ; Output it
    HALT           ; Stop
```

## Available Instructions

### Data Movement
- `LOADI Rd, imm` - Load immediate value
- `LOAD Rd, addr` - Load from memory
- `STORE Rs, addr` - Store to memory

### Arithmetic
- `ADD Rd, Rs1, Rs2` - Add two registers
- `SUB Rd, Rs1, Rs2` - Subtract
- `INC Rd` - Increment
- `DEC Rd` - Decrement

### Logic
- `AND Rd, Rs1, Rs2` - Bitwise AND
- `OR Rd, Rs1, Rs2` - Bitwise OR
- `XOR Rd, Rs1, Rs2` - Bitwise XOR
- `NOT Rd, Rs` - Bitwise NOT

### Control Flow
- `JMP addr` - Unconditional jump
- `JZ Rs, addr` - Jump if zero
- `JNZ Rs, addr` - Jump if not zero

### I/O
- `OUT Rs` - Output ASCII character

### Special
- `HALT` - Stop execution

## Tips

1. **Use registers wisely**: You have R0-R7
2. **ASCII values**: 'A'=65, 'a'=97, '0'=48, space=32, newline=10
3. **Loops**: Use labels and JNZ
4. **Comments**: Explain your logic!

## Running Your Program

```bash
python3 vm/emulator.py assembly/examples/myprogram.asm
```

Debug mode:
```bash
python3 vm/emulator.py assembly/examples/myprogram.asm --debug
```

## Example: Print ABC

```asm
.ORG 0x00

    LOADI R0, 65    ; 'A'
    LOADI R1, 3     ; Counter
    
loop:
    OUT R0          ; Output character
    INC R0          ; Next character
    DEC R1          ; Decrement counter
    JNZ R1, loop    ; Continue if not zero
    
    LOADI R0, 10    ; Newline
    OUT R0
    HALT
```

Have fun building!

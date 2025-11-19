# NAND Compute: Building a Computer from First Principles

A complete implementation of a simple computer architecture built entirely from NAND gates up to running custom assembly language programs.

## Project Philosophy

Starting with only NAND gates (a universal logic gate), we build every component needed for a functioning computer that can execute programs, including displaying "Hello, World!".

## Architecture Overview

### 1. Logic Layer (`logic/`)
- **NAND Gate**: The only primitive
- **Basic Gates**: NOT, AND, OR, XOR built from NAND
- **Composite Gates**: MUX, DMUX, multi-bit gates

### 2. Arithmetic Layer (`arithmetic/`)
- **Half Adder & Full Adder**: Binary addition
- **ALU**: Arithmetic Logic Unit with operations: ADD, SUB, AND, OR, NOT
- **Comparators**: Zero detection, equality, less than

### 3. Memory Layer (`memory/`)
- **Flip-Flops**: SR, D, T flip-flops
- **Registers**: 8-bit, 16-bit data storage
- **RAM**: Random Access Memory
- **Program Counter**: Sequential instruction addressing

### 4. CPU Layer (`cpu/`)
- **Instruction Decoder**: Parses machine code
- **Control Unit**: Orchestrates data flow
- **Execution Unit**: Performs operations
- **CPU Integration**: Complete processor

### 5. Assembly Language (`assembly/`)
- **Instruction Set Architecture (ISA)**
- **Assembler**: Converts assembly to machine code
- **Examples**: Programs demonstrating capabilities

### 6. Virtual Machine (`vm/`)
- **Emulator**: Runs machine code
- **Memory Model**: Simulated RAM and registers
- **I/O System**: Character output for "Hello, World!"

## Quick Start

```bash
# Run the hello world program
python3 vm/emulator.py assembly/examples/hello_world.asm

# Or build and run manually
python3 assembly/assembler.py assembly/examples/hello_world.asm -o output.bin
python3 vm/emulator.py output.bin
```

## Instruction Set Architecture (ISA)

Our simple 16-bit computer with 8 registers and 256 bytes of RAM:

| Instruction | Opcode | Format | Description |
|-------------|--------|--------|-------------|
| LOAD        | 0001   | LOAD Rd, addr | Load from memory to register |
| STORE       | 0010   | STORE Rs, addr | Store register to memory |
| ADD         | 0011   | ADD Rd, Rs1, Rs2 | Rd = Rs1 + Rs2 |
| SUB         | 0100   | SUB Rd, Rs1, Rs2 | Rd = Rs1 - Rs2 |
| AND         | 0101   | AND Rd, Rs1, Rs2 | Rd = Rs1 & Rs2 |
| OR          | 0110   | OR Rd, Rs1, Rs2 | Rd = Rs1 | Rs2 |
| NOT         | 0111   | NOT Rd, Rs | Rd = ~Rs |
| JMP         | 1000   | JMP addr | Jump to address |
| JZ          | 1001   | JZ Rs, addr | Jump if Rs == 0 |
| OUT         | 1010   | OUT Rs | Output register value as ASCII |
| HALT        | 1111   | HALT | Stop execution |

## Building Blocks

### From NAND to Gates
```python
def NAND(a, b):
    return not (a and b)

def NOT(a):
    return NAND(a, a)

def AND(a, b):
    return NOT(NAND(a, b))

def OR(a, b):
    return NAND(NOT(a), NOT(b))
```

### Hello World Assembly
```asm
; Load 'H' and output
LOAD R0, 72
OUT R0

; Load 'e' and output
LOAD R0, 101
OUT R0

; Continue for "llo, World!"
; ...

HALT
```

## Project Structure

```
nandCompute/
├── README.md                 # This file
├── logic/                    # Logic gates from NAND
│   ├── nand.py              # NAND gate (primitive)
│   ├── basic_gates.py       # NOT, AND, OR, XOR
│   ├── composite_gates.py   # MUX, DMUX, multi-bit
│   └── tests/
├── arithmetic/              # Arithmetic circuits
│   ├── adder.py            # Half/Full adders
│   ├── alu.py              # Arithmetic Logic Unit
│   └── tests/
├── memory/                  # Memory components
│   ├── flip_flop.py        # SR, D, T flip-flops
│   ├── register.py         # Data registers
│   ├── ram.py              # Random Access Memory
│   └── tests/
├── cpu/                     # Central Processing Unit
│   ├── decoder.py          # Instruction decoder
│   ├── control.py          # Control unit
│   ├── cpu.py              # Complete CPU
│   └── tests/
├── assembly/                # Assembly language
│   ├── isa.md              # ISA specification
│   ├── assembler.py        # Assembly to machine code
│   └── examples/
│       ├── hello_world.asm
│       ├── fibonacci.asm
│       └── counter.asm
├── vm/                      # Virtual Machine
│   ├── emulator.py         # Main emulator
│   ├── memory_model.py     # RAM simulation
│   └── io_system.py        # I/O handling
└── docs/                    # Documentation
    ├── architecture.md     # Detailed architecture
    ├── building_blocks.md  # Component explanations
    └── tutorials.md        # Step-by-step guides
```

## Educational Goals

1. **Understand Computing Fundamentals**: See how complex systems emerge from simple components
2. **Hardware-Software Interface**: Bridge the gap between logic gates and programs
3. **Computer Architecture**: Learn CPU design, instruction sets, and execution
4. **Assembly Programming**: Low-level programming without abstractions
5. **Systems Thinking**: Appreciate the layers of a complete computing system

## Inspiration

- **Nand2Tetris**: Building a modern computer from first principles
- **Ben Eater's 8-bit Computer**: Breadboard CPU implementation
- **RISC Architecture**: Simplified instruction set design

## Testing

Each component includes comprehensive tests:

```bash
# Test logic gates
python3 -m pytest logic/tests/

# Test ALU
python3 -m pytest arithmetic/tests/

# Test CPU
python3 -m pytest cpu/tests/

# Run all tests
python3 -m pytest
```

## Contributing

This is a learning project! Feel free to:
- Add more assembly examples
- Optimize the emulator
- Extend the ISA
- Improve documentation
- Add visualization tools

## License

MIT License - Educational purposes

## Resources

- [Nand2Tetris Course](https://www.nand2tetris.org/)
- [Digital Logic Design](https://en.wikipedia.org/wiki/Logic_gate)
- [Computer Architecture](https://en.wikipedia.org/wiki/Computer_architecture)
- [Assembly Language](https://en.wikipedia.org/wiki/Assembly_language)

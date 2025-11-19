# MyAssembly - Microcode-Based CPU Architecture

A realistic 8-bit computer implementation using microcode, designed to bridge the gap between theory and hardware implementation. Inspired by Ben Eater's 8-bit breadboard computer.

## Philosophy

This project implements a microcode-based CPU that can:
- Run on a **virtual machine** (Python emulator)
- Be programmed into **EEPROMs** for hardware implementation
- Work on **Arduino** or similar microcontrollers
- Be built on a **breadboard** with discrete components

The microcode approach mirrors how real CPUs work, making this an ideal stepping stone to hardware implementation.

## Architecture Overview

### 8-bit CPU with Microcode Control

- **Data Path**: 8-bit
- **Address Space**: 16-bit (64KB addressable)
- **Registers**: 4 general purpose (A, B, C, D) + SP, PC
- **Microcode ROM**: 256 bytes (can fit in AT28C16 EEPROM)
- **Control Signals**: 16 lines for datapath control

### Key Components

1. **Microcode ROM** - Controls CPU operations via control signals
2. **Instruction Register** - Holds current instruction
3. **Program Counter** - Points to next instruction
4. **Stack Pointer** - Manages subroutine calls
5. **ALU** - 8-bit arithmetic and logic operations
6. **Registers** - Fast storage (A, B, C, D)

## Microcode Format

Each instruction is implemented as a sequence of microcode steps.

**Microcode Word (16 bits):**
```
| 15-12: ALU Op | 11-8: Src | 7-4: Dst | 3-0: Control |
```

**Control Signals:**
- `PC_OUT` - Put PC on bus
- `PC_INC` - Increment PC
- `MAR_IN` - Load memory address register
- `RAM_OUT` - Read from RAM
- `RAM_IN` - Write to RAM
- `IR_IN` - Load instruction register
- `A_IN`, `A_OUT` - Register A control
- `B_IN`, `B_OUT` - Register B control
- `ALU_OUT` - Put ALU result on bus
- `HALT` - Stop execution

## Instruction Set Architecture

Compatible with nandCompute assembly language, but with enhanced features:

### Data Movement
- `MOV dst, src` - Move data between registers
- `LDI reg, imm` - Load immediate
- `LDA reg, addr` - Load from memory
- `STA reg, addr` - Store to memory
- `PUSH reg` - Push to stack
- `POP reg` - Pop from stack

### Arithmetic
- `ADD reg1, reg2` - Add
- `SUB reg1, reg2` - Subtract
- `INC reg` - Increment
- `DEC reg` - Decrement

### Logic
- `AND reg1, reg2` - Bitwise AND
- `OR reg1, reg2` - Bitwise OR
- `XOR reg1, reg2` - Bitwise XOR
- `NOT reg` - Bitwise NOT

### Control Flow
- `JMP addr` - Unconditional jump
- `JZ addr` - Jump if zero
- `JNZ addr` - Jump if not zero
- `CALL addr` - Call subroutine
- `RET` - Return from subroutine

### I/O
- `OUT reg` - Output to display
- `IN reg` - Input from keyboard (future)

### Special
- `NOP` - No operation
- `HALT` - Stop execution

## Project Structure

```
MyAssembly/
├── README.md              # This file
├── assembler/
│   └── assembler.py      # Assembly → machine code
├── emulator/
│   ├── cpu.py            # CPU emulator
│   ├── microcode.py      # Microcode engine
│   └── bus.py            # System bus simulation
├── microcode/
│   ├── generator.py      # Generate microcode from spec
│   ├── microcode.hex     # Intel HEX format (EEPROM ready)
│   ├── microcode.lst     # Symbolic listing
│   ├── microcode.bin     # Raw binary
│   └── spec.yml          # Microcode specification
├── programs/
│   ├── hello.asm         # Hello World
│   ├── blink.asm         # LED blink (for hardware)
│   └── fibonacci.asm     # Fibonacci sequence
├── hardware/
│   ├── arduino/          # Arduino implementation
│   ├── breadboard/       # Breadboard schematics
│   └── eeprom/           # EEPROM programming tools
└── docs/
    ├── architecture.md   # Detailed architecture
    ├── microcode.md      # Microcode guide
    └── hardware.md       # Hardware build guide
```

## Quick Start

### Virtual Machine Mode
```bash
# Assemble a program
python3 assembler/assembler.py programs/hello.asm -o programs/hello.bin

# Run on emulator
python3 emulator/cpu.py programs/hello.bin

# With microcode tracing
python3 emulator/cpu.py programs/hello.bin --trace
```

### Hardware Mode

#### EEPROM Programming
```bash
# Generate microcode for EEPROM
python3 microcode/generator.py -o microcode/microcode.hex

# Program AT28C16 EEPROM
minipro -p AT28C16 -w microcode/microcode.hex
```

#### Arduino
```bash
cd hardware/arduino
# Upload Arduino sketch
arduino-cli compile --fqbn arduino:avr:uno MyAssemblyCPU
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno MyAssemblyCPU
```

#### Breadboard
See `docs/hardware.md` for complete breadboard build guide.

## Comparison with nandCompute

| Feature | nandCompute | MyAssembly |
|---------|-------------|------------|
| **Focus** | Educational theory | Hardware implementation |
| **Starting Point** | NAND gates | Microcode ROM |
| **Control** | Direct execution | Microcode sequencer |
| **Hardware Ready** | No | Yes (EEPROM/Arduino) |
| **Complexity** | Simple | Realistic |
| **Assembly** | Compatible | Compatible+ |

Both projects use **the same assembly language**, so programs are portable!

## Hardware Requirements

### Minimal Virtual Setup
- Python 3.8+
- No additional libraries

### EEPROM Hardware Build
- AT28C16 or similar EEPROM (16Kx8)
- EEPROM programmer (TL866II or similar)
- Basic logic ICs (74LS series)
- Clock circuit (555 timer or crystal)
- See `docs/hardware.md` for complete BOM

### Arduino Implementation
- Arduino Uno or compatible
- Breadboard and jumper wires
- Optional: LCD display, LEDs

## Learning Path

1. **Start with Emulator** - Understand microcode execution
2. **Study Microcode** - See how instructions map to control signals
3. **Build Arduino Version** - Software implementation of hardware
4. **Breadboard Build** - Real discrete logic implementation
5. **EEPROM Programming** - Create your own microcode ROM

## Design Philosophy

### Why Microcode?

1. **Realistic** - How real CPUs work (Intel 8086, 68000, etc.)
2. **Flexible** - Change instruction behavior by reprogramming ROM
3. **Educational** - See the hardware-software boundary
4. **Hardware-Ready** - Direct path to physical implementation

### Ben Eater Inspiration

This project follows Ben Eater's excellent design principles:
- Start simple, add complexity gradually
- Make everything visible and traceable
- Use real hardware components
- Build understanding from first principles

## Resources

- **Ben Eater's 8-bit Computer**: https://eater.net/8bit
- **nandCompute**: Companion project (theory from NAND gates)
- **Intel HEX Format**: Standard format for ROM programming
- **Microcode Basics**: See `docs/microcode.md`

## Contributing

This is a learning project! Feel free to:
- Add new instructions to the ISA
- Optimize microcode sequences
- Contribute hardware implementations
- Improve documentation

## License

MIT License - Educational and hardware projects encouraged!

---

**From microcode to machine - build it yourself! 🔧**

"""
Assembler - Converts assembly language to machine code

This assembler translates our assembly language into 16-bit machine code
that can be executed by our virtual machine.
"""

import re
import sys
from typing import List, Tuple, Dict

# Opcode mapping
OPCODES = {
    'HALT':  0x0,
    'LOAD':  0x1,
    'LOADI': 0x2,
    'STORE': 0x3,
    'ADD':   0x4,
    'SUB':   0x5,
    'INC':   0x6,
    'DEC':   0x7,
    'AND':   0x8,
    'OR':    0x9,
    'XOR':   0xA,
    'NOT':   0xB,
    'JMP':   0xC,
    'JZ':    0xD,
    'JNZ':   0xE,
    'OUT':   0xF,
}


class Assembler:
    """Assembles assembly language to machine code."""
    
    def __init__(self):
        self.labels: Dict[str, int] = {}
        self.current_address = 0
        self.instructions: List[Tuple[int, int]] = []  # (address, instruction)
        self.data_section: List[Tuple[int, int]] = []  # (address, value)
    
    def parse_register(self, reg_str: str) -> int:
        """Parse register name (R0-R7) to register number."""
        reg_str = reg_str.strip().upper()
        if not reg_str.startswith('R'):
            raise ValueError(f"Invalid register: {reg_str}")
        
        try:
            reg_num = int(reg_str[1:])
            if reg_num < 0 or reg_num > 7:
                raise ValueError(f"Register out of range: {reg_str}")
            return reg_num
        except ValueError:
            raise ValueError(f"Invalid register: {reg_str}")
    
    def parse_immediate(self, imm_str: str) -> int:
        """Parse immediate value or address."""
        imm_str = imm_str.strip()
        
        # Check if it's a label
        if imm_str in self.labels:
            return self.labels[imm_str]
        
        # Parse as number (decimal, hex, or binary)
        try:
            if imm_str.startswith('0x') or imm_str.startswith('0X'):
                return int(imm_str, 16)
            elif imm_str.startswith('0b') or imm_str.startswith('0B'):
                return int(imm_str, 2)
            else:
                return int(imm_str)
        except ValueError:
            raise ValueError(f"Invalid immediate value: {imm_str}")
    
    def encode_instruction(self, opcode: int, rd: int = 0, rs1: int = 0, 
                          rs2: int = 0, imm: int = 0) -> int:
        """
        Encode instruction into 16-bit machine code.
        
        Format 1 (3 registers): | opcode(4) | rd(4) | rs1(4) | rs2(4) |
        Format 2 (reg + imm):   | opcode(4) | reg(4) | imm(8) |
        """
        if opcode in [0x1, 0x2, 0x3, 0xC, 0xD, 0xE]:  # Instructions with immediate
            # Format: opcode(4) | reg(4) | imm(8)
            return (opcode << 12) | (rd << 8) | (imm & 0xFF)
        else:
            # Format: opcode(4) | rd(4) | rs1(4) | rs2(4)
            return (opcode << 12) | (rd << 8) | (rs1 << 4) | rs2
    
    def assemble_line(self, line: str, address: int) -> Tuple[int, int]:
        """
        Assemble a single line of code.
        
        Returns: (address, encoded_instruction)
        """
        # Remove comments
        line = line.split(';')[0].strip()
        
        if not line:
            return None
        
        # Split into parts
        parts = re.split(r'[,\s]+', line)
        instruction = parts[0].upper()
        
        if instruction not in OPCODES:
            raise ValueError(f"Unknown instruction: {instruction}")
        
        opcode = OPCODES[instruction]
        
        # Encode based on instruction type
        if instruction == 'HALT':
            return (address, self.encode_instruction(opcode))
        
        elif instruction == 'LOADI':
            # LOADI Rd, imm
            rd = self.parse_register(parts[1])
            imm = self.parse_immediate(parts[2])
            return (address, self.encode_instruction(opcode, rd=rd, imm=imm))
        
        elif instruction in ['LOAD', 'STORE']:
            # LOAD/STORE Rd, addr
            rd = self.parse_register(parts[1])
            addr = self.parse_immediate(parts[2])
            return (address, self.encode_instruction(opcode, rd=rd, imm=addr))
        
        elif instruction in ['ADD', 'SUB', 'AND', 'OR', 'XOR']:
            # ADD Rd, Rs1, Rs2
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            rs2 = self.parse_register(parts[3])
            return (address, self.encode_instruction(opcode, rd=rd, rs1=rs1, rs2=rs2))
        
        elif instruction in ['INC', 'DEC']:
            # INC Rd
            rd = self.parse_register(parts[1])
            return (address, self.encode_instruction(opcode, rd=rd))
        
        elif instruction == 'NOT':
            # NOT Rd, Rs
            rd = self.parse_register(parts[1])
            rs1 = self.parse_register(parts[2])
            return (address, self.encode_instruction(opcode, rd=rd, rs1=rs1))
        
        elif instruction == 'JMP':
            # JMP addr
            addr = self.parse_immediate(parts[1])
            return (address, self.encode_instruction(opcode, imm=addr))
        
        elif instruction in ['JZ', 'JNZ']:
            # JZ Rs, addr
            rs = self.parse_register(parts[1])
            addr = self.parse_immediate(parts[2])
            return (address, self.encode_instruction(opcode, rd=rs, imm=addr))
        
        elif instruction == 'OUT':
            # OUT Rs
            rs = self.parse_register(parts[1])
            return (address, self.encode_instruction(opcode, rd=rs))
        
        else:
            raise ValueError(f"Unimplemented instruction: {instruction}")
    
    def first_pass(self, lines: List[str]):
        """First pass: collect labels and calculate addresses."""
        address = 0
        
        for line in lines:
            # Remove comments
            line = line.split(';')[0].strip()
            
            if not line:
                continue
            
            # Check for directives
            if line.startswith('.ORG'):
                # Set origin address
                parts = line.split()
                address = self.parse_immediate(parts[1])
                self.current_address = address
                continue
            
            if line.startswith('.DATA'):
                # Data directive - skip for now
                continue
            
            # Check for labels
            if line.endswith(':'):
                label = line[:-1].strip()
                self.labels[label] = address
                continue
            
            # Regular instruction - increment address
            address += 1
    
    def second_pass(self, lines: List[str]):
        """Second pass: assemble instructions."""
        address = 0
        
        for line_num, line in enumerate(lines, 1):
            # Remove comments
            line = line.split(';')[0].strip()
            
            if not line:
                continue
            
            # Handle directives
            if line.startswith('.ORG'):
                parts = line.split()
                address = self.parse_immediate(parts[1])
                continue
            
            if line.startswith('.DATA'):
                # TODO: Handle data section
                continue
            
            # Skip labels
            if line.endswith(':'):
                continue
            
            # Assemble instruction
            try:
                result = self.assemble_line(line, address)
                if result:
                    self.instructions.append(result)
                    address += 1
            except Exception as e:
                print(f"Error on line {line_num}: {line}", file=sys.stderr)
                print(f"  {e}", file=sys.stderr)
                raise
    
    def assemble(self, source_code: str) -> List[int]:
        """
        Assemble complete program.
        
        Returns: List of 16-bit machine code instructions
        """
        lines = source_code.split('\n')
        
        # Two-pass assembly
        self.first_pass(lines)
        self.second_pass(lines)
        
        # Create output array
        if not self.instructions:
            return []
        
        max_addr = max(addr for addr, _ in self.instructions)
        output = [0] * (max_addr + 1)
        
        for addr, instruction in self.instructions:
            output[addr] = instruction
        
        return output
    
    def assemble_file(self, input_file: str, output_file: str = None):
        """Assemble from file and optionally write to output file."""
        with open(input_file, 'r') as f:
            source_code = f.read()
        
        machine_code = self.assemble(source_code)
        
        if output_file:
            with open(output_file, 'wb') as f:
                for instruction in machine_code:
                    # Write as 16-bit little-endian
                    f.write(instruction.to_bytes(2, byteorder='little'))
        
        return machine_code
    
    def disassemble(self, machine_code: List[int]) -> str:
        """Disassemble machine code back to assembly (for debugging)."""
        lines = []
        
        opcode_names = {v: k for k, v in OPCODES.items()}
        
        for addr, instruction in enumerate(machine_code):
            if instruction == 0:
                continue
            
            opcode = (instruction >> 12) & 0xF
            rd = (instruction >> 8) & 0xF
            rs1 = (instruction >> 4) & 0xF
            rs2 = instruction & 0xF
            imm = instruction & 0xFF
            
            op_name = opcode_names.get(opcode, f"UNKNOWN({opcode})")
            
            if opcode in [0x1, 0x2, 0x3, 0xC, 0xD, 0xE]:
                lines.append(f"{addr:3d}: {op_name} R{rd}, {imm}")
            elif opcode == 0xF:
                lines.append(f"{addr:3d}: {op_name} R{rd}")
            elif opcode in [0x6, 0x7]:
                lines.append(f"{addr:3d}: {op_name} R{rd}")
            elif opcode == 0xB:
                lines.append(f"{addr:3d}: {op_name} R{rd}, R{rs1}")
            else:
                lines.append(f"{addr:3d}: {op_name} R{rd}, R{rs1}, R{rs2}")
        
        return '\n'.join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <input.asm> [output.bin]")
        sys.exit(1)
    
    assembler = Assembler()
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        machine_code = assembler.assemble_file(input_file, output_file)
        
        print(f"Assembly successful!")
        print(f"Generated {len(machine_code)} instructions")
        
        if output_file:
            print(f"Output written to: {output_file}")
        
        print("\nDisassembly:")
        print(assembler.disassemble(machine_code))
        
    except Exception as e:
        print(f"Assembly failed: {e}", file=sys.stderr)
        sys.exit(1)

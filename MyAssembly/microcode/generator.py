"""
Microcode Generator

Generates microcode ROM images from specification file.
Outputs in multiple formats:
- .bin: Raw binary (for direct ROM programming)
- .hex: Intel HEX format (standard EEPROM format)
- .lst: Symbolic listing (human-readable debug format)
"""

import yaml
import sys
from pathlib import Path


class MicrocodeGenerator:
    """Generate microcode ROM from specification."""
    
    def __init__(self, spec_file):
        with open(spec_file, 'r') as f:
            self.spec = yaml.safe_load(f)
        
        self.control_signals = self.spec['control_signals']
        self.instructions = self.spec['instructions']
        self.rom_size = self.spec['rom_config']['size']
        
        # Initialize ROM
        self.rom = bytearray(256)
    
    def parse_control_word(self, signals):
        """Convert signal names to control word value."""
        if isinstance(signals, str):
            signals = [s.strip() for s in signals.split('|')]
        elif isinstance(signals, int):
            return signals
        
        control_word = 0
        for signal in signals:
            if signal in self.control_signals:
                control_word |= self.control_signals[signal]
        
        return control_word
    
    def generate_rom(self):
        """Generate complete microcode ROM."""
        # Initialize ROM with zeros (256 bytes = 128 words)
        rom = bytearray(256)
        
        # Process each instruction
        for opcode_val, instruction in self.instructions.items():
            if isinstance(opcode_val, str):
                opcode = int(opcode_val, 0)  # Handle hex strings
            else:
                opcode = opcode_val
            
            steps = instruction['steps']
            
            # Each instruction can have up to 8 micro-steps
            for step_num, step_signals in enumerate(steps):
                if step_num >= 8:
                    break
                
                # ROM address: opcode (upper 4 bits) | step (lower 3 bits)
                addr = (opcode << 3) | step_num
                
                # Parse control signals
                control_word = self.parse_control_word(step_signals)
                
                # Store as 16-bit little-endian
                if addr * 2 + 1 < len(rom):
                    rom[addr * 2] = control_word & 0xFF          # Low byte
                    rom[addr * 2 + 1] = (control_word >> 8) & 0xFF  # High byte
        
        self.rom = rom
        return rom
    
    def write_binary(self, output_file):
        """Write raw binary file."""
        with open(output_file, 'wb') as f:
            f.write(bytes(self.rom))
        print(f"Generated binary: {output_file}")
    
    def write_intel_hex(self, output_file):
        """Write Intel HEX format."""
        lines = []
        
        # Data records (16 bytes per line)
        for addr in range(0, len(self.rom), 16):
            chunk = self.rom[addr:addr+16]
            byte_count = len(chunk)
            record_type = 0x00  # Data record
            
            # Calculate checksum
            checksum = byte_count + (addr >> 8) + (addr & 0xFF) + record_type
            checksum += sum(chunk)
            checksum = (~checksum + 1) & 0xFF
            
            # Format line
            line = f":{byte_count:02X}{addr:04X}{record_type:02X}"
            line += ''.join(f"{b:02X}" for b in chunk)
            line += f"{checksum:02X}"
            lines.append(line)
        
        # End-of-file record
        lines.append(":00000001FF")
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(lines) + '\n')
        
        print(f"Generated Intel HEX: {output_file}")
    
    def write_listing(self, output_file):
        """Write symbolic listing file."""
        lines = []
        lines.append("=" * 80)
        lines.append("MICROCODE LISTING")
        lines.append("=" * 80)
        lines.append("")
        
        # Control signal reference
        lines.append("Control Signals:")
        lines.append("-" * 40)
        for name, value in sorted(self.control_signals.items(), key=lambda x: x[1]):
            lines.append(f"  {name:12s} = 0x{value:04X}")
        lines.append("")
        
        # Instruction microcode
        lines.append("Instruction Microcode:")
        lines.append("=" * 80)
        
        for opcode_val, instruction in sorted(self.instructions.items()):
            if isinstance(opcode_val, str):
                opcode = int(opcode_val, 0)
            else:
                opcode = opcode_val
            
            name = instruction['name']
            lines.append(f"\n[0x{opcode:02X}] {name}")
            lines.append("-" * 40)
            
            for step_num, step_signals in enumerate(instruction['steps']):
                addr = (opcode << 3) | step_num
                control_word = self.parse_control_word(step_signals)
                
                # Decode signals
                active_signals = []
                for sig_name, sig_value in self.control_signals.items():
                    if control_word & sig_value:
                        active_signals.append(sig_name)
                
                signals_str = ' | '.join(active_signals) if active_signals else 'NOP'
                lines.append(f"  T{step_num}: [0x{addr:03X}] 0x{control_word:04X}  {signals_str}")
        
        lines.append("\n" + "=" * 80)
        lines.append(f"ROM Size: {self.rom_size} bytes")
        lines.append("=" * 80)
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(lines) + '\n')
        
        print(f"Generated listing: {output_file}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generator.py <spec.yml> [output_dir]")
        sys.exit(1)
    
    spec_file = sys.argv[1]
    output_dir = Path(sys.argv[2] if len(sys.argv) > 2 else 'microcode')
    output_dir.mkdir(exist_ok=True)
    
    print(f"Generating microcode from {spec_file}...")
    
    generator = MicrocodeGenerator(spec_file)
    generator.generate_rom()
    
    # Write all output formats
    generator.write_binary(output_dir / 'microcode.bin')
    generator.write_intel_hex(output_dir / 'microcode.hex')
    generator.write_listing(output_dir / 'microcode.lst')
    
    print("\nMicrocode generation complete!")
    print(f"Files written to: {output_dir}/")


if __name__ == '__main__':
    main()

"""
NAND Gate - The Universal Logic Gate

This is the ONLY primitive in our system. Everything else is built from NAND gates.

NAND (NOT AND) Truth Table:
A | B | NAND(A,B)
--|---|----------
0 | 0 | 1
0 | 1 | 1
1 | 0 | 1
1 | 1 | 0

Fun Fact: NAND is functionally complete - you can build ANY logic circuit
using only NAND gates!
"""

def NAND(a: bool, b: bool) -> bool:
    """
    The primitive NAND gate.
    
    This is the ONLY gate we consider "hardware".
    Everything else will be built from this.
    
    Args:
        a: First input bit
        b: Second input bit
    
    Returns:
        NOT (a AND b)
    """
    return not (a and b)


def NAND_multi(inputs: list[bool]) -> bool:
    """
    Multi-input NAND gate.
    Equivalent to NAND of all inputs.
    
    Args:
        inputs: List of boolean inputs
    
    Returns:
        NOT (AND of all inputs)
    """
    if not inputs:
        return True
    
    result = inputs[0]
    for bit in inputs[1:]:
        result = result and bit
    
    return not result


class NANDGate:
    """
    Object-oriented representation of a NAND gate.
    Useful for building more complex circuits.
    """
    
    def __init__(self):
        self.input_a = False
        self.input_b = False
        self._output = True
    
    def set_inputs(self, a: bool, b: bool):
        """Set the gate inputs."""
        self.input_a = a
        self.input_b = b
        self._compute()
    
    def _compute(self):
        """Compute the output based on inputs."""
        self._output = NAND(self.input_a, self.input_b)
    
    def output(self) -> bool:
        """Get the gate output."""
        return self._output
    
    def __call__(self, a: bool, b: bool) -> bool:
        """Allow gate to be called as a function."""
        return NAND(a, b)
    
    def __repr__(self):
        return f"NAND({self.input_a}, {self.input_b}) = {self._output}"


if __name__ == "__main__":
    # Demonstrate NAND gate behavior
    print("NAND Gate Truth Table:")
    print("A | B | NAND(A,B)")
    print("--|---|----------")
    
    for a in [False, True]:
        for b in [False, True]:
            result = NAND(a, b)
            a_str = '1' if a else '0'
            b_str = '1' if b else '0'
            r_str = '1' if result else '0'
            print(f"{a_str} | {b_str} | {r_str}")
    
    print("\n" + "="*50)
    print("NAND is the ONLY primitive in our system!")
    print("Everything else is built from NAND gates.")
    print("="*50)

"""
Composite Logic Gates - MUX, DMUX, and Multi-bit Operations

These gates are essential for building the CPU and memory systems.
"""

from .basic_gates import AND, OR, NOT


def MUX(a: bool, b: bool, sel: bool) -> bool:
    """
    Multiplexer (2-to-1 selector).
    
    If sel == 0: output = a
    If sel == 1: output = b
    
    MUX(a, b, sel) = (NOT(sel) AND a) OR (sel AND b)
    """
    return OR(AND(NOT(sel), a), AND(sel, b))


def DMUX(input_bit: bool, sel: bool) -> tuple[bool, bool]:
    """
    Demultiplexer (1-to-2 distributor).
    
    If sel == 0: a = input, b = 0
    If sel == 1: a = 0, b = input
    
    Returns: (a, b)
    """
    a = AND(input_bit, NOT(sel))
    b = AND(input_bit, sel)
    return (a, b)


def MUX4WAY(a: bool, b: bool, c: bool, d: bool, sel: list[bool]) -> bool:
    """
    4-way multiplexer.
    
    sel[1] sel[0] | output
    --------------|-------
       0     0    |   a
       0     1    |   b
       1     0    |   c
       1     1    |   d
    """
    assert len(sel) == 2, "Need 2 select bits for 4-way MUX"
    
    mux_ab = MUX(a, b, sel[0])
    mux_cd = MUX(c, d, sel[0])
    return MUX(mux_ab, mux_cd, sel[1])


def MUX8WAY(inputs: list[bool], sel: list[bool]) -> bool:
    """
    8-way multiplexer.
    
    Args:
        inputs: 8 input bits [a, b, c, d, e, f, g, h]
        sel: 3 select bits [sel2, sel1, sel0]
    """
    assert len(inputs) == 8, "Need 8 inputs"
    assert len(sel) == 3, "Need 3 select bits for 8-way MUX"
    
    # First level: 4 2-way muxes
    m0 = MUX(inputs[0], inputs[1], sel[0])
    m1 = MUX(inputs[2], inputs[3], sel[0])
    m2 = MUX(inputs[4], inputs[5], sel[0])
    m3 = MUX(inputs[6], inputs[7], sel[0])
    
    # Second level: 2 2-way muxes
    m4 = MUX(m0, m1, sel[1])
    m5 = MUX(m2, m3, sel[1])
    
    # Final level: 1 2-way mux
    return MUX(m4, m5, sel[2])


def DMUX4WAY(input_bit: bool, sel: list[bool]) -> tuple[bool, bool, bool, bool]:
    """
    4-way demultiplexer.
    
    Routes input to one of 4 outputs based on 2 select bits.
    """
    assert len(sel) == 2, "Need 2 select bits for 4-way DMUX"
    
    # First level
    ab, cd = DMUX(input_bit, sel[1])
    
    # Second level
    a, b = DMUX(ab, sel[0])
    c, d = DMUX(cd, sel[0])
    
    return (a, b, c, d)


def DMUX8WAY(input_bit: bool, sel: list[bool]) -> list[bool]:
    """
    8-way demultiplexer.
    
    Routes input to one of 8 outputs based on 3 select bits.
    """
    assert len(sel) == 3, "Need 3 select bits for 8-way DMUX"
    
    # First level
    lower, upper = DMUX(input_bit, sel[2])
    
    # Second level
    a, b, c, d = DMUX4WAY(lower, sel[:2])
    e, f, g, h = DMUX4WAY(upper, sel[:2])
    
    return [a, b, c, d, e, f, g, h]


# Multi-bit operations
def MUX_n(a: list[bool], b: list[bool], sel: bool) -> list[bool]:
    """
    N-bit multiplexer.
    Apply MUX to each bit position.
    """
    assert len(a) == len(b), "Input arrays must be same length"
    return [MUX(a[i], b[i], sel) for i in range(len(a))]


def MUX4WAY_n(a: list[bool], b: list[bool], c: list[bool], d: list[bool], 
              sel: list[bool]) -> list[bool]:
    """
    N-bit 4-way multiplexer.
    """
    n = len(a)
    assert all(len(x) == n for x in [b, c, d]), "All inputs must be same length"
    return [MUX4WAY(a[i], b[i], c[i], d[i], sel) for i in range(n)]


def MUX8WAY_n(inputs: list[list[bool]], sel: list[bool]) -> list[bool]:
    """
    N-bit 8-way multiplexer.
    
    Args:
        inputs: 8 n-bit inputs
        sel: 3 select bits
    """
    assert len(inputs) == 8, "Need 8 input arrays"
    n = len(inputs[0])
    assert all(len(x) == n for x in inputs), "All inputs must be same length"
    
    return [MUX8WAY([inputs[j][i] for j in range(8)], sel) for i in range(n)]


if __name__ == "__main__":
    print("Composite Logic Gates\n")
    
    # Test MUX
    print("MUX (2-to-1 Multiplexer):")
    print("A | B | SEL | OUT")
    print("--|---|-----|----")
    for a in [False, True]:
        for b in [False, True]:
            for sel in [False, True]:
                out = MUX(a, b, sel)
                print(f"{int(a)} | {int(b)} | {int(sel)}   | {int(out)}")
    
    # Test DMUX
    print("\nDMUX (1-to-2 Demultiplexer):")
    print("IN | SEL | A | B")
    print("---|-----|---|---")
    for inp in [False, True]:
        for sel in [False, True]:
            a, b = DMUX(inp, sel)
            print(f"{int(inp)}  | {int(sel)}   | {int(a)} | {int(b)}")
    
    # Test multi-bit MUX
    print("\n16-bit MUX example:")
    a = [True] * 8 + [False] * 8  # 0xFF00
    b = [False] * 8 + [True] * 8  # 0x00FF
    result_a = MUX_n(a, b, False)
    result_b = MUX_n(a, b, True)
    
    def bits_to_hex(bits):
        val = sum(b << i for i, b in enumerate(reversed(bits)))
        return f"0x{val:04X}"
    
    print(f"a = {bits_to_hex(a)}")
    print(f"b = {bits_to_hex(b)}")
    print(f"MUX(a, b, 0) = {bits_to_hex(result_a)}")
    print(f"MUX(a, b, 1) = {bits_to_hex(result_b)}")

"""
Basic Logic Gates - All Built from NAND

This module implements fundamental logic gates using only NAND gates.
This demonstrates how NAND is functionally complete.
"""

from .nand import NAND


def NOT(a: bool) -> bool:
    """
    NOT gate built from NAND.
    
    NOT(a) = NAND(a, a)
    
    Truth Table:
    A | NOT(A)
    --|------
    0 | 1
    1 | 0
    """
    return NAND(a, a)


def AND(a: bool, b: bool) -> bool:
    """
    AND gate built from NAND.
    
    AND(a, b) = NOT(NAND(a, b))
              = NAND(NAND(a, b), NAND(a, b))
    
    Truth Table:
    A | B | AND(A,B)
    --|---|--------
    0 | 0 | 0
    0 | 1 | 0
    1 | 0 | 0
    1 | 1 | 1
    """
    nand_out = NAND(a, b)
    return NAND(nand_out, nand_out)


def OR(a: bool, b: bool) -> bool:
    """
    OR gate built from NAND.
    
    OR(a, b) = NAND(NOT(a), NOT(b))
             = NAND(NAND(a, a), NAND(b, b))
    
    Truth Table:
    A | B | OR(A,B)
    --|---|-------
    0 | 0 | 0
    0 | 1 | 1
    1 | 0 | 1
    1 | 1 | 1
    """
    not_a = NAND(a, a)
    not_b = NAND(b, b)
    return NAND(not_a, not_b)


def XOR(a: bool, b: bool) -> bool:
    """
    XOR (Exclusive OR) gate built from NAND.
    
    XOR(a, b) = (a AND NOT(b)) OR (NOT(a) AND b)
    
    Truth Table:
    A | B | XOR(A,B)
    --|---|--------
    0 | 0 | 0
    0 | 1 | 1
    1 | 0 | 1
    1 | 1 | 0
    """
    nand_ab = NAND(a, b)
    nand_a_nand = NAND(a, nand_ab)
    nand_b_nand = NAND(b, nand_ab)
    return NAND(nand_a_nand, nand_b_nand)


def NOR(a: bool, b: bool) -> bool:
    """
    NOR gate built from NAND.
    
    NOR(a, b) = NOT(OR(a, b))
    """
    or_out = OR(a, b)
    return NOT(or_out)


def XNOR(a: bool, b: bool) -> bool:
    """
    XNOR (Exclusive NOR) gate built from NAND.
    
    XNOR(a, b) = NOT(XOR(a, b))
    
    Truth Table:
    A | B | XNOR(A,B)
    --|---|----------
    0 | 0 | 1
    0 | 1 | 0
    1 | 0 | 0
    1 | 1 | 1
    """
    xor_out = XOR(a, b)
    return NOT(xor_out)


# Multi-bit versions
def NOT_n(bits: list[bool]) -> list[bool]:
    """Apply NOT to each bit in a list."""
    return [NOT(bit) for bit in bits]


def AND_n(a: list[bool], b: list[bool]) -> list[bool]:
    """Bitwise AND of two bit arrays."""
    assert len(a) == len(b), "Bit arrays must be same length"
    return [AND(a[i], b[i]) for i in range(len(a))]


def OR_n(a: list[bool], b: list[bool]) -> list[bool]:
    """Bitwise OR of two bit arrays."""
    assert len(a) == len(b), "Bit arrays must be same length"
    return [OR(a[i], b[i]) for i in range(len(a))]


def XOR_n(a: list[bool], b: list[bool]) -> list[bool]:
    """Bitwise XOR of two bit arrays."""
    assert len(a) == len(b), "Bit arrays must be same length"
    return [XOR(a[i], b[i]) for i in range(len(a))]


if __name__ == "__main__":
    print("Basic Logic Gates - Built from NAND\n")
    
    gates = [
        ("NOT", lambda: [(a, NOT(a)) for a in [False, True]]),
        ("AND", lambda: [(a, b, AND(a, b)) for a in [False, True] for b in [False, True]]),
        ("OR", lambda: [(a, b, OR(a, b)) for a in [False, True] for b in [False, True]]),
        ("XOR", lambda: [(a, b, XOR(a, b)) for a in [False, True] for b in [False, True]]),
        ("NOR", lambda: [(a, b, NOR(a, b)) for a in [False, True] for b in [False, True]]),
        ("XNOR", lambda: [(a, b, XNOR(a, b)) for a in [False, True] for b in [False, True]]),
    ]
    
    for name, func in gates:
        print(f"\n{name} Gate:")
        results = func()
        if len(results[0]) == 2:  # Unary gate
            print("A | OUT")
            print("--|----")
            for a, out in results:
                print(f"{int(a)} | {int(out)}")
        else:  # Binary gate
            print("A | B | OUT")
            print("--|---|----")
            for a, b, out in results:
                print(f"{int(a)} | {int(b)} | {int(out)}")

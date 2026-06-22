from types import MappingProxyType
from math import log10

"""
Assumptions:
1) "Roman numerals" refers to the standard Roman numeral system using only the conventional characters I through M 
2) The programme should consider this (and only this) numeral system
3) A Roman numeral is invalid is it is not in canoncial form, and hence should result in a conversion error
4) Converting an integer to a Roman numeral when no canonical representation exists should result in a conversion error
5) An empty string is considered an invalid Roman numeral
6) Roman numerals should be case insensitive, with a preference for capital letters
"""

type RomanNumeral = str

_VALUES: MappingProxyType[str, int] = MappingProxyType({
    'I' : 1,
    'V' : 5,
    'X' : 10,
    'L' : 50,
    'C' : 100,
    'D' : 500,
    'M' : 1000,
})

_NUMERALS: MappingProxyType[int, str] = MappingProxyType({v : k for k,v in _VALUES.items()})

def _resolve_place(x: int, lower: int) -> str:
    match x:
        case n if n <= 3:
            return n * _NUMERALS[lower] # e.g I - III
        case 4:
            return _NUMERALS[lower] + _NUMERALS[5 * lower] # e.g IV
        case n if 5 <= n and n < 9:
            return _NUMERALS[5 * lower] + _NUMERALS[lower] * (x-5) # e.g V - VIII
        case 9:
            return _NUMERALS[lower] + _NUMERALS[10 * lower] # e.g IX
        case _:
            raise RuntimeError("Place values should be from 1-9")
    

def int_to_numeral(value: int) -> RomanNumeral:
    """
    Converts an integer into a Roman numeral string 

    Parameters
    ----------
    value : An integer

    Returns
    ----------
    A Roman numeral string with an equivalent value

    Raises
    ----------
    `ValueError` : Input argument is out of range for a standard Roman numeral
    """

    if value <= 0:
        raise ValueError(f"{value} out of range for Roman numerals")

    x = value
    out: list[str] = []

    for i in range(int(log10(value)), -1, -1):
        shift = 10 ** i
        place = x // shift
        x -= place * shift

        try:
            out.append(_resolve_place(place, shift))
        except KeyError:
            raise ValueError(f"{value} out of range for Roman numerals")
        
    return "".join(out)
    
def numeral_to_int(numerals: RomanNumeral) -> int:
    """
    Converts a Roman numeral string into an integer

    Parameters
    ----------
    numerals : A Roman numeral string in standard form

    Returns
    ----------
    An integer with an equivalent value

    Raises
    ----------
    `ValueError` : Input argument is not a valid Roman numeral string
    """
    if numerals == "":
        raise ValueError("Empty string is not a valid Roman numeral")

    normal_numerals = numerals.upper()
    acc = 0
    try:
        values = [_VALUES[numeral] for numeral in normal_numerals]
    except KeyError:
        raise ValueError(f"{normal_numerals} contains unrecognised numerals, allowed numerals are: {list(_VALUES.keys())}")

    for a,b in zip(values, values[1:] + [0]):
        acc += a if a >= b else -a

    if normal_numerals != int_to_numeral(acc):
        raise ValueError(f"{normal_numerals} is not in canonical form")
    
    return acc     
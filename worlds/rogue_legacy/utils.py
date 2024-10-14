roman_numerals = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def int_to_roman(num: int) -> str:
    """Converts a decimal int to its roman number equivalent."""
    output = ""
    while num > 0:
        for i, r in roman_numerals:
            while num >= i:
                output += r
                num -= i

    return output

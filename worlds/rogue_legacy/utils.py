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

# fmt: off
allowed_characters = {
    # Straight from the Junicode font from Rogue Legacy. If it's not in here, then the game wouldn't load it anyway.
    " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
    "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "]", "^", "_", "`",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
    "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "¡", "¢",
    "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³",
    "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿", "À", "Á", "Â", "Ã",
    "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", "Ð", "Ñ", "Ò", "Ó",
    "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û", "Ü", "Ý", "Þ", "ß", "à", "á", "â", "ã",
    "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", "ð", "ñ", "ò", "ó",
    "ô", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ", "ą", "Ć", "ć", "Ę",
    "ę", "Ł", "ł", "Ń", "ń", "œ", "Ś", "ś", "ź", "Ż", "ż", "А", "Б", "В", "Г", "Д",
    "Е", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф",
    "Х", "Ц", "Ч", "Ш", "Щ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д", "е",
    "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х",
    "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", "–", "—", "―", "’", "”", "„",
    "…", "\\",
}

# fmt: on


def int_to_roman(num: int) -> str:
    """Converts a decimal int to its roman number equivalent."""
    output = ""
    while num > 0:
        for i, r in roman_numerals:
            while num >= i:
                output += r
                num -= i

    return output


def check_name_allowed(name: str) -> tuple[bool, set[str]]:
    """Returns if a name only contains characters allowed by RL and a set of any disallowed characters, if any."""
    disallowed_chars = set()
    for char in name:
        if char not in allowed_characters:
            disallowed_chars.add(char)

    return len(disallowed_chars) == 0, disallowed_chars

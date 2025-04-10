from dataclasses import dataclass
from typing import Iterable, Mapping, NamedTuple

from Options import DefaultOnToggle, FreeText, OptionError, OptionSet, PerGameCommonOptions, PlandoTexts, Range, Removed
from .data import POSSIBLE_BUTTON_COLORS


class Buttonsanity(Range):
    """Adds extra buttons to the item pool that must be found and pressed to activate **The Button**."""

    display_name = "Buttonsanity"
    range_start = 0
    range_end = 20
    default = 0


class Dissatisfaction(Range):
    """Adds a percentage of extra buttons to the item pool that only contain the **Feeling of Dissatisfaction**. Adding
    extra trapped buttons causes some **Extra Button** to become **Extra Two Buttons** to fit in the item pool.

    Activating these buttons does not count towards **The Button** activation requirement.
    """

    display_name = "Dissatisfaction"
    range_start = 0
    range_end = 80
    default = 20


class DissatisfactionLink(DefaultOnToggle):
    """Send DeathLinks to all DeathLink-participating players if you receive the **Feeling of Dissatisfaction**.

    DeathLinks are always sent when a button is pressed with the text, "DeathLink", printed on it. There is no escape.
    """

    display_name = "DissatisfactionLink"


class ColorBlacklist(OptionSet):
    """Prevents certain colors from randomly appearing on any buttons.
    
    Supported colors include::
        red, orange, yellow, green, cyan, blue, magenta, purple, pink, brown, black, gray, white, pride, trans
    """

    display_name = "Color Blacklist"
    valid_keys = POSSIBLE_BUTTON_COLORS

    def verify_keys(self) -> None:
        super().verify_keys()
        if self.value == set(POSSIBLE_BUTTON_COLORS):
            raise OptionError(f"Cannot blacklist all possible colors; at least one color must be allowed!")


class EasterEgg(FreeText):
    """Special codes that may cause special effects on the Clique client."""

    display_name = "Code Entry"
    default = ""


class CliquePlandoTexts(PlandoTexts):
    """Override the text and color of specific buttons. Button text will be rendered uppercased on client. This requires
    the host to have enabled the ``text`` plando option on generation.

    The format is as follows::
        - at: the_button           # The specific button to modify.
          text: "You're Winner!"   # The specific text for this button. Defaults to ``null``, if omitted.
          color: "red"             # The specific color for this button. Defaults to "random", if omitted.
          percentage: 100          # Chance of overriding this button text. Defaults to 100 (guaranteed), if omitted.

    You can also, optionally, choose weights for the ``at``, ``text``, and/or ``color`` properties. For example::
        - at:
            button_1: 5
            any_button: 5
            any_trap_button: 1
          text:
            "Release Surprise": 5
            "Release %ITEM%": 1
            "": 1                  # Empty strings are allowed and will force blank buttons.
            null: 1                # Client will choose a random text on initial connection.
          color:
            "red": 1
            "#123fff": 5           # Custom hex-colors are supported (case-insensitive).
            "random": 5            # Client will choose a random non-blacklisted color on initial connection.

    Notes:
        - Valid ``at`` keys are as follows:
            - ``the_button``: Corresponds to the final button that sends the goal completion.
            - ``button_{i}``: Corresponds to the ``i``th button.
                - e.g., ``button_2`` corresponds to the button that releases the item from **Extra Button 2**.
            - ``any_button``: Randomly picks any button (excluding **The Button**).
            - ``any_safe_button``: Randomly picks any button that contains an item (excluding **The Button**).
            - ``any_trap_button``: Randomly picks any button that contains a **Feeling of Dissatisfaction** trap.
        - The ``any``-style ``at`` keys will not override explicit text set on an ``button_{i}``.
        - Any ``text`` values can also contain any of the following placeholder text to have it change based on room:
            - ``%SELF%``: Becomes your slot's name.
            - ``%RANDOM%``: Becomes any random slot name in the multiworld.
            - ``%ITEM%``: Becomes the name of the containing item, unless it's a trap (then it will be a random item).
            - ``%PLAYER%``: Becomes the slot name of the player that would receive this item when pressed.
            - ``%GAME%``: Becomes the game name of the player that would receive this item when pressed.
            - ``%COLOR%``: Becomes the color of this button.
        - If any button contains the string, "DeathLink", the button will send a DeathLink when pressed.
        - If ``text`` is set to ``null``, the text will be automatically chosen by the client.
        - ``text`` is limited to 128 characters; any additional characters will be truncated.
    """

    class PlandoText(NamedTuple):
        at: str
        text: str | None
        color: str
        percentage: int = 100

    value: list[PlandoText]
    valid_placeholders = {"SELF", "RANDOM", "ITEM", "PLAYER", "GAME", "COLOR"}
    valid_keys = [
        "the_button",
        "any_button",
        "any_safe_button",
        "any_trap_button",
        *[f"button_{i + 1}" for i in range(Buttonsanity.range_end * 2)],
    ]

    @staticmethod
    def verify_colors(colors: Iterable[str]) -> bool:
        import re

        valid_colors = {*POSSIBLE_BUTTON_COLORS, "random"}
        for color in colors:
            # If color is a hex value, ensure it's a supported format.
            if color.startswith("#") and re.match(r"^#(?:[0-9a-f]{3}){1,2}$", color, re.IGNORECASE):
                continue

            if color not in valid_colors:
                return False

        return True

    @classmethod
    def get_option_name(cls, value: list[PlandoText]) -> str:
        return str({
            text.at: {
                "text": text.text,
                "color": text.color,
            } for text in value
        })

    @classmethod
    def warn_unknown_placeholders(cls, text: str):
        import logging
        import re

        # That's a scary regex, but it's only looking for specific `%value%` values.
        matches = [match.group().upper() for match in re.finditer(r"(?:^|\s)%([^\s%]+?)%(?:$|\s)", text)]
        for match in matches:
            if match not in cls.valid_placeholders:
                continue

            logging.warning(f'Unknown placeholder: "%{match}%" in "plando_texts"; client likely won\'t change text.')

    @classmethod
    def from_any(cls, data):
        import logging
        import random

        texts: dict[str, cls.PlandoText] = {}
        if not isinstance(data, Iterable):
            raise OptionError(f"Cannot convert plando texts from non-list, got {type(data)}.")

        for entry in data:
            if isinstance(entry, Mapping):
                entry: Mapping[str, any]
                if random.random() >= float(entry.get("percentage", 100) / 100):
                    continue

                # 'at' Validation
                at: str = entry.get("at")
                if not at:
                    raise OptionError('"at" must be a valid string or weighted list of valid strings.')
                elif isinstance(at, dict):
                    at = random.choices(list(at.keys()), list(at.values()))[0]

                # 'text' Validation
                text: str | None = entry.get("text")
                if isinstance(text, dict):
                    if not text:
                        text = None
                    else:
                        text = random.choices(list(text.keys()), list(text.values()))[0]
                        if text == "null":
                            text = None

                if text:
                    cls.warn_unknown_placeholders(text)

                    # Strip excess whitespace and truncate text, if needed.
                    text = text.strip()
                    if len(text) > 128:
                        text = text[:128]
                        logging.warning(f'Truncated plando texts on "{at}" to 128 characters.')

                # 'color' Validation
                color: str = entry.get("color", "random")
                if isinstance(color, dict):
                    if cls.verify_colors(color.keys()):
                        color = random.choices(list(color.keys()), list(color.values()))[0]
                    else:
                        raise OptionError('"color" must be a valid color or weighted list of valid colors.')
                elif not cls.verify_colors([color]):
                    raise OptionError('"color" must be a valid color or weighted list of valid colors.')

                if not text and color == "random":
                    # If both are set to default, then remove from dict, if it exists.
                    texts.pop(at, None)
                else:
                    texts[at] = cls.PlandoText(at, text, color, entry.get("percentage", 100))

            elif isinstance(entry, cls.PlandoText) and random.random() < float(entry.percentage / 100):
                texts[entry.at] = entry
            else:
                raise OptionError(f"Cannot create plando texts from non-dictionary, got {type(entry)}.")

        return cls(list(texts.values()))


# Removed options.
class ButtonColor(Removed):
    """This option has been removed and superseded by the *Plando Texts* option."""
    pass


class HardMode(Removed):
    """This option has been removed and superseded by the *Buttonsanity* option."""
    pass


@dataclass
class CliqueOptions(PerGameCommonOptions):
    # Clique 2.0 Options
    buttonsanity: Buttonsanity
    dissatisfaction: Dissatisfaction
    dissatisfaction_link: DissatisfactionLink
    color_blacklist: ColorBlacklist
    code_entry: EasterEgg
    plando_texts: CliquePlandoTexts

    # Clique 1.x Options - Removed
    color: ButtonColor
    hard_mode: HardMode

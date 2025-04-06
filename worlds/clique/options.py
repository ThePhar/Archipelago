import random
from dataclasses import dataclass
from typing import Iterable, Mapping, NamedTuple
from typing_extensions import Self

import Options
from Options import Choice, NamedRange, OptionError, OptionGroup, OptionSet, PerGameCommonOptions, Range, Removed
from .data import POSSIBLE_BUTTON_COLORS


class Mode(Choice):
    """The game mode's activation condition for activating **The Button** and completing your objective.

        - `classic` - **The Button** is activated from the start, allowing the player to win when ready.
        - `activation` - **The Button** requires a **Button Activation** item to be pressed.
        - `buttons` - **The Button** requires finding and pressing a certain number of additional buttons before
            **The Button** can be pressed.

    In non-classic modes, you are given a freebie item to start.
    """
    display_name = "Activation Condition"
    option_classic = 0
    option_activation = 1
    option_buttons = 2
    default = 0


class ExtraButtons(Range):
    """Adds a number of extra buttons to add to the item pool that must be found and pressed to activate **The Button**.

    This option is ignored if the *Mode* is not set to `buttons`.
    """
    display_name = "Extra Buttons"
    range_start = 1
    range_end = 64
    default = 1


class Dissatisfaction(Range):
    """Creates a percentage of client-only fake buttons, that contain the **Feeling of Dissatisfaction**. Pressing these
    buttons does not count towards your buttons requirement nor awards any hint points. Each fake button added replaces
    an **Extra Button** with an **Extra Two Buttons** item in the pool.

    Obtaining **The Feeling of Satisfaction** makes the player immune to the **Feeling of Dissatisfaction** effects.

    This option is ignored if the *Mode* is not set to `buttons`.
    """
    display_name = "Dissatisfaction Rate"
    range_start = 0
    range_end = 100
    default = 0


class ButtonColors(OptionSet):
    """Sets the available colors for any buttons."""
    display_name = "Button Color(s)"
    valid_keys = POSSIBLE_BUTTON_COLORS
    default = valid_keys

    def verify_keys(self) -> None:
        super().verify_keys()

        # No empty sets allowed.
        if not self.value:
            raise OptionError(f"At least 1 color must be supplied: {', '.join(sorted(list(POSSIBLE_BUTTON_COLORS)))}")


class DeathLink(Options.DeathLink):
    """Allow this slot to send and receive DeathLinks to all other participating players. Receiving a DeathLink gives
    you the **Feeling of Dissatisfaction**.

    You will send a DeathLinks if you:
        - Find a **Feeling of Dissatisfaction**.
        - Push a button with the literal text, `DeathLink`, printed on it.
    """
    display_name = "DeathLink"
    default = True


class PlandoTexts(Options.PlandoTexts):
    """Override the text of specific buttons with your own text. Requires host to have enabled "Text" plando.

    The format is as follows::
        - at: the_button
          text: "Your Desired Button Text"
          color: "red"  # A specific color for this button. Optional, and defaults to "random", if omitted.
          percentage: 100  # Chance of overriding this button text. Optional, and defaults to 100, if omitted.

    You can also, optionally, weight the `at`, `text`, and/or `color` properties. For example::
        - at:
            the_button: 5
            extra_button_1: 5
            extra_button_2: 10
            trap_button_1: 1
          text:
            "This Is A Button": 5
            "This Is Another Button": 10
            "": 1  # Empty strings are also allowed (will make blank buttons)!
          color:
            red: 1
            orange: 4
            random: 5

    Valid location keys are: `the_button`, `extra_button_<i>`, or `fake_button_<i>` (with <i> being a number).
    """
    class PlandoText(NamedTuple):
        at: str
        text: str
        color: str
        percentage: int = 100

    value: list[PlandoText]
    valid_keys = [
        "the_button",
        *[f"extra_button_{i}" for i in range(1, ExtraButtons.range_end)],
        *[f"trap_button_{i}" for i in range(1, ExtraButtons.range_end)],
    ]

    @staticmethod
    def verify_color(colors: Iterable[str]) -> bool:
        for color in colors:
            if color not in {*POSSIBLE_BUTTON_COLORS, "random"}:
                return False

        return True

    @classmethod
    def from_any(cls, data: Options.PlandoTextsFromAnyType) -> Self:
        texts: list[cls.PlandoText] = []
        if isinstance(data, Iterable):
            for entry in data:
                if isinstance(entry, Mapping):
                    if random.random() < float(entry.get("percentage", 100) / 100):
                        at = entry.get("at", None)
                        if at is None:
                            raise Options.OptionError('"at" must be a valid string or weighted list of strings!')

                        if isinstance(at, dict):
                            if not at:
                                raise Options.OptionError('"at" must be a valid string or weighted list of strings!')

                            at = random.choices(list(at.keys()), weights=list(at.values()), k=1)[0]

                        color = entry.get("color", "random")
                        if isinstance(color, dict):
                            if not color:
                                color = "random"
                            elif cls.verify_color(color.keys()):
                                color = random.choices(list(color.keys()), weights=list(color.values()), k=1)[0]
                            else:
                                raise Options.OptionError(
                                    '"color" can only contain supported color values: '
                                    f'{", ".join(sorted([*POSSIBLE_BUTTON_COLORS, "random"]))}')
                        elif isinstance(color, str):
                            if not cls.verify_color([color]):
                                raise Options.OptionError(
                                    '"color" can only contain supported color values: '
                                    f'{", ".join(sorted([*POSSIBLE_BUTTON_COLORS, "random"]))}')

                        text = entry.get("text", None)
                        if text is None:
                            raise Options.OptionError('"text" must be a valid string or weighted list of strings!')

                        if isinstance(text, dict):
                            if not text:
                                raise Options.OptionError('"text" must be a valid string or weighted list of strings!')

                            text = random.choices(list(text.keys()), weights=list(text.values()), k=1)[0]

                        texts.append(cls.PlandoText(at, text, color, entry.get("percentage", 100)))

                elif isinstance(entry, cls.PlandoText):
                    if random.random() < float(entry.percentage / 100):
                        texts.append(entry)
                else:
                    raise Exception(f"Cannot create plando text from non-dictionary type, got {type(entry)}")

            return cls(texts)
        else:
            raise NotImplementedError(f"Cannot Convert from non-list, got {type(data)}")


# Removed options.
class ButtonColor(Removed):
    """This option has been replaced with the *Button Colors* option."""
    pass


class HardMode(Removed):
    """This option has been replaced with the *Button Pool* option."""
    pass


# Overrides for built-in common options.
class ExcludeLocations(Options.ExcludeLocations):
    __doc__ = Options.ExcludeLocations.__doc__

class PriorityLocations(Options.PriorityLocations):
    __doc__ = Options.PriorityLocations.__doc__
    default = {"Final Button", "Starting Button"}


@dataclass
class CliqueOptions(PerGameCommonOptions):
    progression_balancing: Options.ProgressionBalancing
    accessibility: Options.Accessibility

    mode: Mode
    extra_buttons: ExtraButtons
    dissatisfaction_rate: Dissatisfaction
    button_colors: ButtonColors
    death_link: DeathLink
    plando_texts: PlandoTexts

    # Removed options from v1.x versions of Clique.
    color: ButtonColor
    hard_mode: HardMode

    # Overrides
    priority_locations: PriorityLocations
    exclude_locations: ExcludeLocations
    start_inventory: Options.StartInventoryPool


option_groups: list[OptionGroup] = [
    OptionGroup("Multiworld Options", [
        Options.ProgressionBalancing,
        Options.Accessibility,
        DeathLink,
        PriorityLocations,
        ExcludeLocations,
    ]),
]

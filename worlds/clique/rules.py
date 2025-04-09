from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from BaseClasses import CollectionState
    from . import CliqueWorld
    from .locations import CliqueLocation, CliqueRegion
    from .items import CliqueItem


def can_access_region(state: "CollectionState", region: "CliqueRegion") -> bool:
    return state.has(f"Access {region.name}", region.player)


def can_win(state: "CollectionState", world: "CliqueWorld") -> bool:
    return state.has_all_counts(
        {
            "Buttons": world.extras,
            "Feeling of Satisfaction": 1,
            "Congraturations": 1,
        },
        world.player,
    )


def can_access_final_button(state: "CollectionState", world: "CliqueWorld") -> bool:
    return state.has("Buttons", world.player, world.extras)


def get_safe_buttons(item: "CliqueItem") -> int:
    safe_buttons = 0
    location: "CliqueLocation"
    for location in item.unlocking_region.locations:
        if not location.fake:
            safe_buttons += 1

    return safe_buttons

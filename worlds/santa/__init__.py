from typing import List

from BaseClasses import Item, ItemClassification, MultiWorld
from worlds.AutoWorld import World
from Fill import fill_restrictive

BASE_ID_OFFSET = 0o31_000000  # Because OCT31 == DEC 25
BASE_GAME_NAME = "Pharcryption 2"  # Because I'm hilarious.


class SantaItem(Item):
    game = BASE_GAME_NAME


class SantaWorld(World):
    """A cool game."""
    game = BASE_GAME_NAME
    hidden = True
    location_name_to_id = {
        "Dummy Location":     BASE_ID_OFFSET + 0,
    }
    item_name_to_id = {
        "Milk & Cookies":     BASE_ID_OFFSET + 0,
        "The Christmas Slay": BASE_ID_OFFSET + 1,
        "Lump of Coal":       BASE_ID_OFFSET + 2,
    }

    def create_item(self, name) -> SantaItem:
        if name == "Milk & Cookies":
            classification = ItemClassification.useful
        else:
            classification = ItemClassification.trap

        return SantaItem(name, classification, self.item_name_to_id[name], self.player)

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld) -> None:
        # Get number of worlds (minus self).
        santa_world = [world.player for world in multiworld.worlds.values() if world.game == BASE_GAME_NAME][0]

        # Configure these as necessary.
        for world in multiworld.worlds.values():
            if world.game == BASE_GAME_NAME:
                continue

            location_pool = multiworld.get_unfilled_locations(world.player)
            world.random.shuffle(location_pool)

            item_pool: List[SantaItem] = []
            item_pool += [SantaItem("Milk & Cookies", ItemClassification.useful, cls.item_name_to_id["Milk & Cookies"], santa_world) for _ in range(5)]
            item_pool += [SantaItem("The Christmas Slay", ItemClassification.trap, cls.item_name_to_id["The Christmas Slay"], santa_world) for _ in range(2)]

            location_pool = location_pool[:len(item_pool)]

            fill_restrictive(
                multiworld,
                multiworld.get_all_state(use_cache=True),
                location_pool,
                item_pool,
            )

    def get_filler_item_name(self) -> str:
        return "The Christmas Slay"

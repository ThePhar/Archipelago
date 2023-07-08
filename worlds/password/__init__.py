from typing import List

from BaseClasses import CollectionState, Item, ItemClassification, Location, Region
from worlds.AutoWorld import World
from .Options import password_options


class PasswordItem(Item):
    game = "The Password Game"


class PasswordLocation(Location):
    game = "The Password Game"


class PasswordWorld(World):
    """
    Please choose a password.
    """

    game = "The Password Game"
    option_definitions = password_options

    location_name_to_id = {
        "Rule 1":  8008_000,
        "Rule 2":  8008_001,
        "Rule 3":  8008_002,
        "Rule 4":  8008_003,
        "Rule 5":  8008_004,
        "Rule 6":  8008_005,
        "Rule 7":  8008_006,
        "Rule 8":  8008_007,
        "Rule 9":  8008_008,
        "Rule 10": 8008_009,
        "Rule 11": 8008_010,
        "Rule 12": 8008_011,
        "Rule 13": 8008_012,
        "Rule 14": 8008_013,
        "Rule 15": 8008_014,
        "Rule 16": 8008_015,
        "Rule 17": 8008_016,
        "Rule 18": 8008_017,
        "Rule 19": 8008_018,
        "Rule 20": 8008_019,
        "Rule 21": 8008_020,
        "Rule 22": 8008_021,
        "Rule 23": 8008_022,
        "Rule 24": 8008_023,
        "Rule 25": 8008_024,
        "Rule 26": 8008_025,
        "Rule 27": 8008_026,
        "Rule 28": 8008_027,
        "Rule 29": 8008_028,
        "Rule 30": 8008_029,
        "Rule 31": 8008_030,
        "Rule 32": 8008_031,
        "Rule 33": 8008_032,
        "Rule 34": 8008_033,
        "Rule 35": 8008_034,
        "Re-enter Your Password": 8008_035,
    }

    item_name_to_id = {}

    def generate_early(self):
        if len([world for world in self.multiworld.worlds if isinstance(world, PasswordWorld)]) == self.multiworld.players:
            raise RuntimeError("Cannot generate in a multiworld where there is only Password games!")

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        menu_region.add_locations(self.location_name_to_id, PasswordLocation)

        self.multiworld.priority_locations[self.player].value = set(self.location_name_to_id.keys())

        victory = PasswordLocation(self.player, "Entered Password Successfully", None, menu_region)
        victory.place_locked_item(PasswordItem("My Password", ItemClassification.progression, None, self.player))
        menu_region.locations.append(victory)

    def get_filler_item_name(self) -> str:
        return "Nothing"

    def create_items(self):
        invalid_worlds: List[int] = []
        items: List[Item] = []
        while len(items) < 36:  # Number of items that needs to be created.
            # This is horrible, but I'm really lazy to make this better.
            try:
                random_world = self.multiworld.random.choice([
                    id for id, world in self.multiworld.worlds.items()
                    if not isinstance(world, PasswordWorld) and id not in invalid_worlds])
            except IndexError:  # No valid worlds to generate filler items from.
                raise RuntimeError("Not enough non-Password worlds have a valid get_filler_item_name function to "
                                   "generate.")

            try:
                items.append(self.multiworld.worlds[random_world].create_item(
                    self.multiworld.worlds[random_world].get_filler_item_name()))
            except Exception:
                invalid_worlds.append(random_world)
                continue

        self.multiworld.itempool += items

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("My Password", self.player)

    def fill_slot_data(self):
        return {
            "death_link": bool(getattr(self.multiworld, "death_link")[self.player])
        }


def can_reach_spot(state: CollectionState, player: int, previous_location: PasswordLocation) -> bool:
    return state.can_reach(previous_location, None, player)

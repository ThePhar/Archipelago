from datetime import timedelta
from typing import ClassVar

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, MultiWorld, Region
from worlds.AutoWorld import World
from worlds.generic import GenericWorld
from .Options import *

# I'm hilarious, I know.
GAME_ID_OFFSET = 420_000_000


class PharcryptionWorld(World):
    """
    A meta-game for Archipelago multi-worlds where all players must work together to "decrypt" their progression items
    that were encrypted by a "ransom" attack. Pay the ransom with Pharcoins before the time runs out and all the
    encrypted items are lost forever!
    """

    game = "Pharcryption"
    data_version = 0
    hidden = True
    option_definitions = pharcryption_options
    location_name_to_id = {f"Encrypted Item #{i + 1}": i + GAME_ID_OFFSET for i in range(0, 3_000)}
    item_name_to_id = {
        "1 Pharcoin":  GAME_ID_OFFSET,
        "2 Pharcoins": GAME_ID_OFFSET + 1,
        "3 Pharcoins": GAME_ID_OFFSET + 2,
    }
    item_name_groups = {"Pharcoins": {"1 Pharcoin", "2 Pharcoins", "3 Pharcoins"}}

    world_count: ClassVar[int]
    encrypted_items: EncryptedItems
    payment_amount: PaymentAmount
    extra_pharcoins: ExtraPharcoins
    enable_timelimit: EnableTimelimit
    timelimit: timedelta

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        pharcryption_worlds = len([pw for pw in multiworld.worlds.values() if isinstance(pw, PharcryptionWorld)])
        cls.world_count = len([
            w for w in multiworld.worlds.values()
            if not isinstance(w, PharcryptionWorld) or not isinstance(w, GenericWorld)
        ])

        # Only 1 Pharcryption world can be present in a given multiworld.
        if pharcryption_worlds > 1:
            raise RuntimeError(f"Only 1 Pharcryption world allowed. Found {pharcryption_worlds} Pharcryption worlds.")

        # Do not allow only Pharcryption/Archipelago worlds.
        if cls.world_count == 0:
            raise RuntimeError(f"You must have at least 1 other playable world!")

        # Only a maximum of 100 non-Archipelago and non-Pharcryption worlds.
        if cls.world_count > 100:
            raise RuntimeError(f"Pharcryption only allows 100 or fewer worlds. Found {cls.world_count} worlds.")

    def fill_slot_data(self) -> Dict[str, any]:
        return {
            "world_count": self.world_count,
            "encrypted_items": self.encrypted_items,
            "payment_amount": self.payment_amount,
            "enable_timelimit": self.enable_timelimit,
            "timelimit": self.timelimit.total_seconds(),
        }

    def create_item(self, name: str) -> Item:
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def generate_early(self) -> None:
        # Ensure no local items are set.
        self.multiworld.local_items[self.player].value.clear()

        # All items for Pharcryption are non-local.
        self.multiworld.non_local_items[self.player].value.add("1 Pharcoin")
        self.multiworld.non_local_items[self.player].value.add("2 Pharcoins")
        self.multiworld.non_local_items[self.player].value.add("3 Pharcoins")

        # Set options.
        self.encrypted_items = getattr(self.multiworld, "encrypted_items")[self.player]
        self.payment_amount = getattr(self.multiworld, "payment_amount")[self.player]
        self.extra_pharcoins = getattr(self.multiworld, "extra_pharcoins")[self.player]
        self.enable_timelimit = getattr(self.multiworld, "enable_timelimit")[self.player]
        self.timelimit = timedelta(
            days=getattr(self.multiworld, "timelimit_days")[self.player].value,
            hours=getattr(self.multiworld, "timelimit_hours")[self.player].value,
            minutes=getattr(self.multiworld, "timelimit_minutes")[self.player].value,
        )

        # If timer is set, validate we have at least 30 minutes for the time limit.
        if self.enable_timelimit and timedelta(minutes=30) > self.timelimit:
            raise ValueError("If timelimit is enabled, timelimit must be at least 30 minutes.")

    def create_items(self) -> None:
        items_to_create = self.world_count * self.encrypted_items
        extra_pharcoins_to_create = self.extra_pharcoins.value
        while extra_pharcoins_to_create > 0:
            extra = self.multiworld.random.choice([1, 2])
            if extra_pharcoins_to_create == 1 or extra == 1:
                self.multiworld.itempool.append(self.create_item("2 Pharcoins"))
            else:
                self.multiworld.itempool.append(self.create_item("3 Pharcoins"))

            extra_pharcoins_to_create -= extra
            items_to_create -= 1

        self.multiworld.itempool += [self.create_item("1 Pharcoin") for _ in range(0, items_to_create)]

    def create_regions(self) -> None:
        locations = [f"Encrypted Item #{i + 1}" for i in range(0, self.encrypted_items * self.world_count)]
        self.multiworld.regions += [
            create_region(self.multiworld, self.player, "Menu", None, ["Legit Download"]),
            create_region(self.multiworld, self.player, "Ransomware", locations)
        ]

        self.multiworld.get_entrance("Legit Download", self.player) \
            .connect(self.multiworld.get_region("Ransomware", self.player))

        # Set all locations to priority.
        self.multiworld.priority_locations[self.player].value = set(locations)

    def get_filler_item_name(self) -> str:
        raise NotImplementedError("This game does not support creating filler items.")

    def set_rules(self) -> None:
        locations = [location for location in self.multiworld.get_locations(self.player)]
        for i in range(0, len(locations)):
            required_amount = self.payment_amount * ((i // self.payment_amount) + 1)
            locations[i].access_rule = lambda state: True

        self.multiworld.completion_condition[self.player] = \
            lambda state: has_pharcoins(state, self.player, self.world_count)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations:
            location = Location(player, location_name, world.worlds[player].location_name_to_id[location_name], region)
            location.game = "Pharcryption"
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region


def has_pharcoins(state: CollectionState, player: int, amount: int):
    coins = state.count("1 Pharcoin", player) + \
            state.count("2 Pharcoins", player) * 2 + \
            state.count("3 Pharcoins", player) * 3

    return coins >= amount

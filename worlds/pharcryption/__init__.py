from datetime import timedelta
from typing import ClassVar, Dict

from BaseClasses import CollectionState, Item, ItemClassification, Location, MultiWorld, Region
from worlds.AutoWorld import World
from worlds.generic import GenericWorld
from .Options import EnableTimelimit, EncryptedItems, ExtraPharcoins, FreeDecryptions, PaymentAmount, options

GAME_ID_OFFSET = 420_000_000  # I'm hilarious, I know.
MAXIMUM_WORLDS = 100          # I'd be careful setting this too high.


class PharcryptionItem(Item):
    game = "Pharcryption"


class PharcryptionLocation(Location):
    game = "Pharcryption"


class PharcryptionWorld(World):
    """
    A meta-game for Archipelago multi-worlds where all players must work together to "decrypt" their progression items
    that were encrypted by a "ransom" attack. Pay the ransom with Pharcoins before the time runs out and all the
    encrypted items are lost forever!
    """

    game = "Pharcryption"
    hidden = True
    option_definitions = options
    location_name_to_id = {
        f"Encrypted Item #{i + 1}": i + GAME_ID_OFFSET for i in range(EncryptedItems.range_end * MAXIMUM_WORLDS)
    }
    item_name_to_id = {
        "1 Pharcoin":   GAME_ID_OFFSET,
        "2 Pharcoins":  GAME_ID_OFFSET + 1,
        "3 Pharcoins":  GAME_ID_OFFSET + 2,
    }
    item_name_groups = {"Pharcoins": {"1 Pharcoin", "2 Pharcoins", "3 Pharcoins"}}

    world_count: ClassVar[int]
    encrypted_items: EncryptedItems
    free_decryptions: FreeDecryptions
    payment_amount: PaymentAmount
    extra_pharcoins: ExtraPharcoins
    enable_timelimit: EnableTimelimit
    timelimit: timedelta

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        pharcryption_worlds = len([pw for pw in multiworld.worlds.values() if isinstance(pw, PharcryptionWorld)])
        cls.world_count = len([
            world for world in multiworld.worlds.values()
            if not isinstance(world, PharcryptionWorld) and not isinstance(world, GenericWorld)
        ])

        # Only 1 Pharcryption world can be present in a given multiworld.
        if pharcryption_worlds > 1:
            raise RuntimeError(f"Only 1 Pharcryption world allowed. Found {pharcryption_worlds} Pharcryption worlds.")

        # Do not allow only Pharcryption/Archipelago worlds.
        if cls.world_count == 0:
            raise RuntimeError(f"You must have at least 1 other playable world with Pharcryption!")

        # Only a maximum of MAXIMUM_WORLDS non-Archipelago and non-Pharcryption worlds.
        if cls.world_count > MAXIMUM_WORLDS:
            raise RuntimeError(
                f"Pharcryption only allows {MAXIMUM_WORLDS} or fewer worlds. Found {cls.world_count} worlds.")

    @staticmethod
    def _has_pharcoins(state: CollectionState, player: int, amount: int) -> bool:
        coins = state.count("1 Pharcoin", player) + \
                state.count("2 Pharcoins", player) * 2 + \
                state.count("3 Pharcoins", player) * 3

        return coins >= amount

    def fill_slot_data(self) -> Dict[str, any]:
        return {
            "world_count": self.world_count,
            "encrypted_items": self.encrypted_items.value,
            "free_decryptions": self.free_decryptions.value,
            "payment_amount": self.payment_amount.value,
            "enable_timelimit": self.enable_timelimit.value,
            "timelimit": self.timelimit.total_seconds(),
            "items": [
                {
                    "location": location.address,
                    "item": location.item.code,
                    "player": location.item.player,
                } for location in self.multiworld.get_locations(self.player) if location.address is not None
            ]
        }

    def create_item(self, name: str) -> PharcryptionItem:
        return PharcryptionItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def generate_early(self) -> None:
        # We do not honor local items in this household.
        self.multiworld.local_items[self.player].value.clear()

        # All items for Pharcryption are non-local.
        self.multiworld.non_local_items[self.player].value.update({"1 Pharcoin", "2 Pharcoins", "3 Pharcoins"})

        # Set options in class.
        self.encrypted_items = getattr(self.multiworld, "encrypted_items")[self.player]
        self.free_decryptions = getattr(self.multiworld, "free_decryptions")[self.player]
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
            raise ValueError("If Pharcryption timelimit is enabled, timelimit must be at least 30 minutes.")

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

        self.multiworld.itempool += [self.create_item("1 Pharcoin") for _ in range(items_to_create)]

    def create_regions(self) -> None:
        # Generate all locations and region.
        locations = [f"Encrypted Item #{i + 1}" for i in range(self.encrypted_items * self.world_count)]
        region = Region("Menu", self.player, self.multiworld)
        region.add_locations(locations, PharcryptionLocation)
        self.multiworld.regions.append(region)

        # Set all locations to priority and pre-hint everything.
        self.multiworld.priority_locations[self.player].value = set(locations)
        self.multiworld.start_location_hints[self.player].value = set(locations)

    def get_filler_item_name(self) -> str:
        raise NotImplementedError("Pharcryption does not support creating filler items.")

    def set_rules(self) -> None:
        # Generate each batch of locations in their own "sphere".
        locations = self.multiworld.get_locations(self.player)
        for i in range(len(locations)):
            requirement = self.payment_amount * ((i // self.payment_amount) + 1)
            locations[i].access_rule = lambda state, r=requirement: self._has_pharcoins(state, self.player, r)

        # Game is only completed when you have all the pharcoins required.
        self.multiworld.completion_condition[self.player] = \
            lambda state: self._has_pharcoins(state, self.player, self.world_count * self.encrypted_items)

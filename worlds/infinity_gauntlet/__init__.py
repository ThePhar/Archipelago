from BaseClasses import CollectionState, Item, ItemClassification, Location, Region
from worlds.AutoWorld import World


class IGItem(Item):
    game = "Infinity Gauntlet"


class IGLocation(Location):
    game = "Infinity Gauntlet"


class IGWorld(World):
    """There's literally no reason to be looking up this game."""
    game = "Infinity Gauntlet"
    data_version = 0
    hidden = True

    location_name_to_id = {
        "Taped to the Space Stone":   69_888_000,
        "Taped to the Reality Stone": 69_888_001,
        "Taped to the Power Stone":   69_888_002,
        "Taped to the Soul Stone":    69_888_003,
        "Taped to the Mind Stone":    69_888_004,
        "Taped to the Time Stone":    69_888_005,
    }

    item_name_to_id = {
        "Space Stone":   69_888_000,
        "Reality Stone": 69_888_001,
        "Power Stone":   69_888_002,
        "Soul Stone":    69_888_003,
        "Mind Stone":    69_888_004,
        "Time Stone":    69_888_005,

        # "Snapped" Items
        "the dusted remains of a single arrow":              69_889_000 + 0x43,
        "the dusted remains of 10 arrows":                   69_889_000 + 0x44,
        "the dusted remains of a single bomb":               69_889_000 + 0x27,
        "the dusted remains of 3 bombs":                     69_889_000 + 0x28,
        "the dusted remains of 10 bombs":                    69_889_000 + 0x31,
        "the dusted remains of some Red Mail":               69_889_000 + 0x60,
        "the dusted remains of a Mirror Shield":             69_889_000 + 0x5F,
        "the dusted remains of a Boss Heart Container":      69_889_000 + 0x3E,
        "the dusted remains of a Sanctuary Heart Container": 69_889_000 + 0x3F,
        "the dusted remains of a Piece of Heart":            69_889_000 + 0x17,
        "the dusted remains of a green rupee":               69_889_000 + 0x34,
        "the dusted remains of a blue rupee":                69_889_000 + 0x35,
        "the dusted remains of a red rupee":                 69_889_000 + 0x36,
        "the dusted remains of a purple rupee":              69_889_000 + 0x41,
        "the dusted remains of an orange rupee":             69_889_000 + 0x40,
        "the dusted remains of a silver rupee":              69_889_000 + 0x46,
        "the dusted remains of a map":                       69_889_000 + 9999,
        "the dusted remains of a compass":                   69_889_000 + 9998,
        "the dusted remains of a bee":                       69_889_000 + 0x0E,
        "the dusted remains of a bunch of bees":             69_889_000 + 0xB0,
        "the dusted remains of a sword":                     69_889_000 + 0x5E,
    }

    def create_item(self, name: str) -> IGItem:
        classification = ItemClassification.progression_skip_balancing
        if name.startswith("The dusted"):
            classification = ItemClassification.trap

        return IGItem(name, classification, self.item_name_to_id[name], self.player)

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        menu_region.add_locations(self.location_name_to_id, IGLocation)

    def get_filler_item_name(self) -> str:
        return "Nothing"

    def has_all_stones(self, state: CollectionState):
        return state.has_all(
            set([item for item in self.item_name_to_id.keys() if not item.startswith("The dusted")]),
            self.player
        )

    def set_rules(self):
        self.multiworld.get_location("Taped to the Space Stone", self.player).access_rule = lambda state: state.has(
            "Space Stone", self.player)
        self.multiworld.get_location("Taped to the Reality Stone", self.player).access_rule = lambda state: state.has(
            "Reality Stone", self.player)
        self.multiworld.get_location("Taped to the Power Stone", self.player).access_rule = lambda state: state.has(
            "Power Stone", self.player)
        self.multiworld.get_location("Taped to the Soul Stone", self.player).access_rule = lambda state: state.has(
            "Soul Stone", self.player)
        self.multiworld.get_location("Taped to the Mind Stone", self.player).access_rule = lambda state: state.has(
            "Mind Stone", self.player)
        self.multiworld.get_location("Taped to the Time Stone", self.player).access_rule = lambda state: state.has(
            "Time Stone", self.player)

        self.multiworld.completion_condition[self.player] = lambda state: self.has_all_stones(state)

    def create_items(self):
        self.multiworld.itempool += [
            self.create_item("Space Stone"),
            self.create_item("Reality Stone"),
            self.create_item("Power Stone"),
            self.create_item("Soul Stone"),
            self.create_item("Mind Stone"),
            self.create_item("Time Stone"),
        ]

from math import ceil
from typing import TYPE_CHECKING, TextIO

from BaseClasses import ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import CliqueItem, CliqueItemData, item_data, item_groups, item_table
from .locations import CliqueLocation, CliqueRegion, location_groups, location_table
from .options import CliqueOptions
from .rules import can_access_final_button, can_access_region, can_win, get_safe_buttons

if TYPE_CHECKING:
    from BaseClasses import MultiWorld, CollectionState


class CliqueWebWorld(WebWorld):
    theme = "partyTime"
    rich_text_options_doc = True
    bug_report_page = "https://github.com/ThePhar/Clique/issues"
    options_page = "https://clique.pharware.com/create"
    tutorials = [
        Tutorial(
            tutorial_name="The Clique Beginners Guide",
            description="The definitive “getting started” multiworld guide for 2.0 Cliquers.",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Phar", "The Tempter"]
        )
    ]


class CliqueWorld(World):
    """The greatest “game” of all time, now with more buttons!"""
    game = "Clique"
    web = CliqueWebWorld()
    options: CliqueOptions
    options_dataclass = CliqueOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    required_client_version = (0, 6, 1)
    location_name_groups = location_groups
    item_name_groups = item_groups
    origin_region_name = "The Tempter's Realm"

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        self.extras: int = 0
        self.traps: int = 0
        self.button_index = 1
        self.extra_buttons: list[CliqueItem] = []
        self.regions: list[CliqueRegion] = []

    def create_item(self, name: str, track_button = False) -> CliqueItem:
        item = CliqueItem(name, item_data[name].classification, item_data[name].code, self.player)
        if track_button:
            self.extra_buttons.append(item)

        # If traps are in the pool, receiving a button could open up to dissatisfaction!
        if "Button" in name and self.traps:
            item.classification = ItemClassification.progression | ItemClassification.trap

        return item

    def create_location(self, name: str, region: CliqueRegion, increment_index = False) -> CliqueLocation:
        location = CliqueLocation(self.player, name, location_table.get(name, None), region)
        if increment_index:
            self.button_index += 1

        return location

    def get_filler_item_name(self) -> str:
        return "Nothing"

    def generate_early(self) -> None:
        if self.options.buttonsanity > 0:
            self.extras = self.options.buttonsanity.value
            self.traps = ceil(self.extras * (self.options.dissatisfaction.value / 100))

    def create_regions(self) -> None:
        start_region = CliqueRegion("The Tempter's Realm", self.player, self.multiworld)
        final_region = CliqueRegion("The Golden Pedestal", self.player, self.multiworld)
        start_region.connect(final_region, rule=lambda state: can_access_final_button(state, self))

        # Create static locations.
        final_region.locations.append(self.create_location("The Button", final_region))
        if self.options.buttonsanity > 0:
            start_region.locations.append(self.create_location("The Tempter's Gift", start_region))

        # Event item for victory condition.
        victory_event = self.create_location("Press The Button", final_region)
        victory_event.place_locked_item(CliqueItem("Congraturations", ItemClassification.progression, None, self.player))
        final_region.locations.append(victory_event)

        # Create a region for each button in the item pool.
        for i in range(self.extras):
            region = CliqueRegion(f"Button Region {i}", self.player, self.multiworld)
            start_region.connect(region, rule=lambda state, r=region: can_access_region(state, r))

            # If dissatisfaction traps are in the pool, we need to signal that these regions will have two buttons.
            if i < self.traps:
                region.dual_region = True

            self.regions.append(region)

        # Shuffle regions and create locations (shuffled so it's not predictable which region has two locations).
        self.random.shuffle(self.regions)
        for region in self.regions:
            region.locations.append(self.create_location(f"Extra Button {self.button_index}", region, True))
            if region.dual_region:
                region.locations.append(self.create_location(f"Extra Button {self.button_index}", region, True))

        self.multiworld.regions += [start_region, *self.regions, final_region]

    def create_items(self) -> None:
        # Every world must have a logical satisfaction item (it's the law).
        item_pool: list[CliqueItem] = [self.create_item("Feeling of Satisfaction")]
        item_pool[0].classification = ItemClassification.progression

        # All buttonsanity seeds include lore snippets.
        if self.options.buttonsanity > 0:
            item_pool.append(self.create_item("Clique Lore"))

        # Create buttons and assign them to the regions.
        for region in self.regions:
            item_name = "Extra Two Buttons" if region.dual_region else "Extra Button"
            item = self.create_item(item_name, True)
            item.unlocking_region = region
            item_pool.append(item)

        # Place traps in random locations, if dissatisfaction present.
        if self.traps:
            button_locs: list[CliqueLocation] = [location for region in self.regions for location in region.locations]
            self.random.shuffle(button_locs)
            for i in range(self.traps):
                button_locs[i].place_locked_item(self.create_item("Feeling of Dissatisfaction"))
                button_locs[i].fake = True

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        # The Button is always priority!
        self.options.priority_locations.value.add("The Button")

        self.multiworld.completion_condition[self.player] = lambda state: can_win(state, self)

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        hint_data[self.player] = {}
        for button in self.extra_buttons:
            location_owner = self.multiworld.get_player_name(button.location.player)
            hint_text = f"{location_owner}'s {button.location.name}"

            location: CliqueLocation
            for location in button.unlocking_region.locations:
                hint_data[self.player][location.address] = hint_text

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.options.buttonsanity == 0:
            return

        spoiler_handle.write(f"\nClique Extra Button Mappings - {self.player_name}:\n")
        strings: list[tuple[str, str]] = []
        longest = -1
        for button in self.extra_buttons:
            owner = self.multiworld.get_player_name(button.location.player)
            location = button.location.name
            mapping = [location.name for location in button.unlocking_region.locations]

            prefix = f"\t[{', '.join(mapping)}]"
            suffix = f" ← {owner}'s ({location})\n"
            strings.append((prefix, suffix))
            longest = max(longest, len(prefix))

        for prefix, suffix in strings:
            spoiler_handle.write(prefix.ljust(longest) + suffix)

    def fill_slot_data(self) -> dict[str, any]:
        logic_mapping = {}
        for button in self.extra_buttons:
            location: CliqueLocation
            logic_mapping[f"{button.location.player}-{button.location.address}"] = [
                location.address for location in button.unlocking_region.locations
            ]

        plando_texts: list[list[any]] = []
        for text in self.options.plando_texts:
            plando_texts.append(list(text)[:-1])

        return {
            "version": 2,
            "mapping": logic_mapping,
            "goal": self.options.buttonsanity.value,
            "code": self.options.code_entry.value[:64],
            "dissatisfaction_link": bool(self.options.dissatisfaction_link.value),
            "blacklist": list(self.options.color_blacklist.value),
            "plando": plando_texts,
        }

    def collect(self, state: "CollectionState", item: CliqueItem) -> bool:
        state_changed = super().collect(state, item)
        if state_changed and "Button" in item.name:
            state.prog_items[self.player]["Buttons"] += get_safe_buttons(item)
            if item.unlocking_region:
                state.prog_items[self.player][f"Access {item.unlocking_region.name}"] += 1
        return state_changed

    def remove(self, state: "CollectionState", item: CliqueItem) -> bool:
        state_changed = super().remove(state, item)
        if state_changed and "Button" in item.name:
            state.prog_items[self.player]["Buttons"] -= get_safe_buttons(item)
            if item.unlocking_region:
                state.prog_items[self.player][f"Access {item.unlocking_region.name}"] -= 1
        return state_changed

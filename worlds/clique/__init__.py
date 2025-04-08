from math import ceil
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import CliqueItem, CliqueItemData, item_data, item_table
from .locations import CliqueLocation, CliqueRegion, location_groups, location_table
from .options import CliqueOptions

if TYPE_CHECKING:
    from BaseClasses import MultiWorld, CollectionState


class CliqueWebWorld(WebWorld):
    theme = "partyTime"
    rich_text_options_doc = True
    bug_report_page = "https://github.com/ThePhar/Clique/issues"
    options_page = "https://clique.pharware.com/create"
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Start Guide",
            description="The definitive “getting started” guide for 2.0 Cliquers.",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Phar"]
        )
    ]


class CliqueWorld(World):
    """The greatest game of all time."""
    game = "Clique"
    web = CliqueWebWorld()
    options: CliqueOptions
    options_dataclass = CliqueOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    required_client_version = (0, 6, 0)
    location_name_groups = location_groups
    origin_region_name = "The Tempter's Realm"


    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        self.extras: int = 0
        self.traps: int = 0
        self.button_index = 1
        self.buttons: list[CliqueItem] = []
        self.regions: list[CliqueRegion] = []
        self.satisfaction = self.create_item("Feeling of Satisfaction")

    def create_item(self, name: str, track_button = False) -> CliqueItem:
        item = CliqueItem(name, item_data[name].classification, item_data[name].code, self.player)

        # Classify buttons as prog+trap if dissatisfaction is in the item pool.
        if "Button" in name and self.traps:
            item.classification = ItemClassification.progression | ItemClassification.trap

        if track_button:
            self.buttons.append(item)

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
        start_region.connect(final_region, rule=self._can_access_final_button)

        # Create static locations.
        final_region.locations.append(self.create_location("The Button", final_region))
        if self.options.buttonsanity > 0:
            start_region.locations.append(self.create_location("The Tempter's Gift", start_region))

        # Create a region for each button in the item pool.
        for i in range(self.extras):
            region = CliqueRegion(f"Button Region {i}", self.player, self.multiworld)
            start_region.connect(region, rule=lambda state, r=region: self._can_access_region(state, r))

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
        # Every world must have a satisfaction item (it's the law).
        item_pool: list[CliqueItem] = [self.satisfaction]

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

        self.multiworld.completion_condition[self.player] = self._can_win

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        hint_data[self.player] = {}
        for button in self.buttons:
            location_owner = self.multiworld.get_player_name(button.location.player)
            hint_text = f"{location_owner}'s {button.location.name}"

            location: CliqueLocation
            for location in button.unlocking_region.locations:
                hint_data[self.player][location.address] = hint_text

        print()


    def fill_slot_data(self) -> dict[str, any]:
        mapping = {}
        for button in self.buttons:
            location: CliqueLocation
            mapping[f"{button.location.player}-{button.location.address}"] = [location.address for location in button.unlocking_region.locations]

        return {
            "version": 2,
            "mapping": mapping
        }

    def collect(self, state: "CollectionState", item: CliqueItem) -> bool:
        state_changed = super().collect(state, item)
        if state_changed and "Button" in item.name:
            state.prog_items[self.player][f"Access {item.unlocking_region.name}"] += 1
            state.prog_items[self.player]["Buttons"] += self._get_safe_buttons(item)
        return state_changed

    def remove(self, state: "CollectionState", item: CliqueItem) -> bool:
        state_changed = super().remove(state, item)
        if state_changed and "Button" in item.name:
            state.prog_items[self.player][f"Access {item.unlocking_region.name}"] -= 1
            state.prog_items[self.player]["Buttons"] -= self._get_safe_buttons(item)
        return state_changed

    def _can_access_region(self, state: "CollectionState", region: CliqueRegion):
        return state.has(f"Access {region.name}", self.player)

    def _can_win(self, state: "CollectionState"):
        return state.has_all_counts({
            "Buttons": self.extras,
            "Feeling of Satisfaction": 1,
        }, self.player)

    def _can_access_final_button(self, state: "CollectionState"):
        return state.has("Buttons", self.player, self.extras)

    @staticmethod
    def _get_safe_buttons(item: CliqueItem) -> int:
        safe_buttons = 0
        location: CliqueLocation
        for location in item.unlocking_region.locations:
            if not location.fake:
                safe_buttons += 1

        return safe_buttons

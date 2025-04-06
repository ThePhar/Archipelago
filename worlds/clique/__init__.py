from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import CliqueItem, CliqueItemData, item_data, item_table
from .locations import CliqueLocation, CliqueRegion, location_groups, location_table
from .options import CliqueOptions, option_groups

if TYPE_CHECKING:
    from BaseClasses import MultiWorld, CollectionState


class CliqueWebWorld(WebWorld):
    theme = "partyTime"
    bug_report_page = "https://github.com/ThePhar/Clique/issues"
    rich_text_options_doc = True
    option_groups = option_groups
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
        self.regions: list[CliqueRegion] = []
        self.colors: list[str] = []
        self.satisfaction = self.create_item("Feeling of Satisfaction")
        self.trap_order: list[int] = []

    def create_item(self, name: str, track_button = False) -> CliqueItem:
        item = CliqueItem(name, item_data[name].type, item_data[name].code, self.player)

        # Classify buttons as prog+trap if dissatisfaction is in the item pool.
        if "Button" in name and self.traps:
            item.classification = ItemClassification.progression | ItemClassification.trap

        return item

    def create_location(self, name: str, region: Region) -> CliqueLocation:
        return CliqueLocation(self.player, name, location_table.get(name, None), region)

    def generate_early(self) -> None:
        # Get all allowed colors for additional buttons and sort the set to guarantee determinism.
        self.colors = list(self.options.button_colors.value).sort()

        # Determine extra counts.
        if self.options.mode == "buttons":
            self.extras = self.options.extra_buttons.value
            self.traps = round(self.extras * (self.options.dissatisfaction_rate.value / 100))

        # Enforce traps as local.
        self.options.non_local_items.value.discard("Feeling of Dissatisfaction")
        self.options.local_items.value.add("Feeling of Satisfaction")

    def create_regions(self) -> None:
        start_region = CliqueRegion("The Tempter's Realm", self.player, self.multiworld)
        final_region = CliqueRegion("The Final Button Pedestal", self.player, self.multiworld)
        start_region.connect(final_region, rule=self._can_win)

        if self.options.mode != "classic":
            start_region.locations.append(self.create_location("The Tempter's Gift", start_region))

        # If we're running a single button seed, we just create the one button.
        if self.options.mode != "buttons":
            final_region.locations.append(self.create_location("The Button", start_region))
            self.multiworld.regions += [start_region, final_region]
            return

        final_region.locations.append(self.create_location("The Final Button", final_region))

        # Deal with the extra buttons.
        for i in range(self.extras):
            region = CliqueRegion(f"Extra Region {i}", self.player, self.multiworld)
            region.locations.append(self.create_location(f"Extra Button {i + 1}", region))
            start_region.connect(region, rule=lambda s, r=region: self._can_access_region(s, r))
            self.regions.append(region)

        self.multiworld.regions += [start_region, *self.regions, final_region]

    def create_items(self) -> None:
        # Every world must have a satisfaction item (it's the law).
        item_pool: list[CliqueItem] = [self.satisfaction]

        if self.options.mode == "activation":
            item_pool.append(self.create_item("Button Activation"))

        for i in range(self.extras):
            if i < self.traps:
                item_name = "Extra Two Buttons"
            else:
                item_name = "Extra Button"

            item = self.create_item(item_name, True)
            item_pool.append(item)

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        self.trap_order = [*[0 for _ in range(self.extras)], *[1 for _ in range(self.traps)]]
        self.random.shuffle(self.trap_order)

        region_index = 0
        for i in range(len(self.trap_order)):
            # Ignore traps.
            if i:
                continue

            self.regions[region_index].button_requirement = i + 1
            region_index += 1

        # Completion condition for minimal accessibility.
        self.multiworld.completion_condition[self.player] = self._can_win

    def get_filler_item_name(self) -> str:
        return "A Filler Item That Does Nothing"

    def fill_slot_data(self) -> dict[str, any]:
        location: CliqueLocation
        return {
            "version": 2,
            "mapping": self.trap_order,
        }

    def collect(self, state: "CollectionState", item: CliqueItem) -> bool:
        state_changed = super().collect(state, item)
        if state_changed and "Button" in item.name:
            state.prog_items[self.player]["Buttons"] += 1 if item.name == "Extra Button" else 2

        return state_changed

    def remove(self, state: "CollectionState", item: CliqueItem) -> bool:
        state_changed = super().remove(state, item)
        if state_changed and "Button" in item.name:
            state.prog_items[self.player]["Buttons"] -= 1 if item.name == "Extra Button" else 2

        return state_changed

    def _can_access_region(self, state: "CollectionState", region: CliqueRegion):
        return state.has(f"Buttons", self.player, region.button_requirement)

    def _can_win(self, state: "CollectionState"):
        if self.options.mode == "classic":
            return state.has("Feeling of Satisfaction", self.player)

        if self.options.mode == "activation":
            return state.has("Button Activation", self.player)

        if self.options.mode == "buttons":
            return state.has("Buttons", self.player, self.extras + self.traps)

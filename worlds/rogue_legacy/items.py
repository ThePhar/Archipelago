from dataclasses import dataclass

from BaseClasses import Item, ItemClassification


@dataclass
class ItemData:
    name: str
    classification: ItemClassification
    event: bool = False
    id: int | None = None

    __index = 1

    def __post_init__(self):
        if self.id is None and not self.event:
            self.id = self.__index
            self.__index += 1


class RogueLegacyItem(Item):
    game = "Rogue Legacy"


# fmt: off
rl_items_data: dict[str, ItemData] = {
    # Classes
    "class_knight":     ItemData("Progressive Knights",        ItemClassification.useful),
    "class_mage":       ItemData("Progressive Mages",          ItemClassification.useful),
    "class_barbarian":  ItemData("Progressive Barbarians",     ItemClassification.useful),
    "class_knave":      ItemData("Progressive Knaves",         ItemClassification.useful),
    "class_shinobi":    ItemData("Progressive Shinobi",        ItemClassification.useful),
    "class_miner":      ItemData("Progressive Miners",         ItemClassification.useful),
    "class_lich":       ItemData("Progressive Liches",         ItemClassification.useful),
    "class_spellthief": ItemData("Progressive Spellthieves",   ItemClassification.useful),
    "class_dragon":     ItemData("Dragons",                    ItemClassification.progression),
    "class_traitor":    ItemData("Traitors",                   ItemClassification.useful),

    # Skills
    "skill_hp":         ItemData("Health Up",                  ItemClassification.progression_skip_balancing),
    "skill_mp":         ItemData("Mana Up",                    ItemClassification.progression_skip_balancing),
    "skill_at":         ItemData("Attack Up",                  ItemClassification.progression_skip_balancing),
    "skill_md":         ItemData("Magic Damage Up",            ItemClassification.progression_skip_balancing),
    "skill_ar":         ItemData("Armor Up",                   ItemClassification.useful),
    "skill_eq":         ItemData("Equip Up",                   ItemClassification.progression_skip_balancing),
    "skill_cc":         ItemData("Crit Chance Up",             ItemClassification.useful),
    "skill_cd":         ItemData("Crit Damage Up",             ItemClassification.useful),
    "skill_ds":         ItemData("Down Strike Up",             ItemClassification.filler),
    "skill_gg":         ItemData("Gold Gain Up",               ItemClassification.filler),
    "skill_pe":         ItemData("Potion Efficiency Up",       ItemClassification.filler),
    "skill_it":         ItemData("Invuln Time Up",             ItemClassification.filler),
    "skill_mc":         ItemData("Mana Cost Down",             ItemClassification.filler),
    "skill_dd":         ItemData("Death Defy",                 ItemClassification.useful),
    "skill_ha":         ItemData("Haggling",                   ItemClassification.filler),
    "skill_rc":         ItemData("Randomize Children",         ItemClassification.useful),

    # Blueprints
    "bp_squire":        ItemData("Squire Blueprints",          ItemClassification.filler),
    "bp_silver":        ItemData("Silver Blueprints",          ItemClassification.filler),
    "bp_guardian":      ItemData("Guardian Blueprints",        ItemClassification.filler),
    "bp_imperial":      ItemData("Imperial Blueprints",        ItemClassification.filler),
    "bp_royal":         ItemData("Royal Blueprints",           ItemClassification.progression),
    "bp_knight":        ItemData("Knight Blueprints",          ItemClassification.filler),
    "bp_ranger":        ItemData("Ranger Blueprints",          ItemClassification.filler),
    "bp_sky":           ItemData("Sky Blueprints",             ItemClassification.progression),
    "bp_dragon":        ItemData("Dragon Blueprints",          ItemClassification.filler),
    "bp_slayer":        ItemData("Slayer Blueprints",          ItemClassification.useful),
    "bp_blood":         ItemData("Blood Blueprints",           ItemClassification.useful),
    "bp_sage":          ItemData("Sage Blueprints",            ItemClassification.filler),
    "bp_retribution":   ItemData("Retribution Blueprints",     ItemClassification.useful),
    "bp_holy":          ItemData("Holy Blueprints",            ItemClassification.useful),
    "bp_dark":          ItemData("Dark Blueprints",            ItemClassification.progression),

    # Vendor Slots
    "slot_bp_sword":    ItemData("Blacksmith Sword Slot",      ItemClassification.progression),
    "slot_bp_helm":     ItemData("Blacksmith Helm Slot",       ItemClassification.progression),
    "slot_bp_chest":    ItemData("Blacksmith Chest Slot",      ItemClassification.progression),
    "slot_bp_limbs":    ItemData("Blacksmith Limbs Slot",      ItemClassification.progression),
    "slot_bp_cape":     ItemData("Blacksmith Cape Slot",       ItemClassification.progression),
    "slot_rune_sword":  ItemData("Enchantress Sword Slot",     ItemClassification.progression),
    "slot_rune_helm":   ItemData("Enchantress Helm Slot",      ItemClassification.progression),
    "slot_rune_chest":  ItemData("Enchantress Chest Slot",     ItemClassification.progression),
    "slot_rune_limbs":  ItemData("Enchantress Limbs Slot",     ItemClassification.progression),
    "slot_rune_cape":   ItemData("Enchantress Cape Slot",      ItemClassification.progression),

    # Runes
    "rune_vault":       ItemData("Vault Runes",                ItemClassification.progression),
    "rune_sprint":      ItemData("Sprint Runes",               ItemClassification.progression),
    "rune_vampire":     ItemData("Vampire Runes",              ItemClassification.useful),
    "rune_sky":         ItemData("Sky Runes",                  ItemClassification.progression),
    "rune_siphon":      ItemData("Siphon Runes",               ItemClassification.useful),
    "rune_retaliation": ItemData("Retaliation Runes",          ItemClassification.filler),
    "rune_bounty":      ItemData("Bounty Runes",               ItemClassification.filler),
    "rune_haste":       ItemData("Haste Runes",                ItemClassification.filler),
    "rune_curse":       ItemData("Curse Runes",                ItemClassification.filler),
    "rune_grace":       ItemData("Grace Runes",                ItemClassification.filler),
    "rune_balance":     ItemData("Balance Runes",              ItemClassification.useful),

    # Misc. Key Items
    "fountain_piece":   ItemData("Fountain Piece",             ItemClassification.progression_skip_balancing),
    "cap_level":        ItemData("Level Cap Increase",         ItemClassification.progression),
    "obol_khidr":       ItemData("Khidr's Obol",               ItemClassification.progression),
    "obol_alex":        ItemData("Alexander's Obol",           ItemClassification.progression),
    "obol_leon":        ItemData("Ponce de Leon's Obol",       ItemClassification.progression),
    "obol_herodotus":   ItemData("Herodotus' Obol",            ItemClassification.progression),
    "obol_traitor":     ItemData("Traitor's Obol",             ItemClassification.progression),

    # Junk/Filler
    "junk_gold_1000":   ItemData("1000 Gold Pieces",           ItemClassification.filler),
    "junk_gold_3000":   ItemData("3000 Gold Pieces",           ItemClassification.filler),
    "junk_gold_5000":   ItemData("5000 Gold Pieces",           ItemClassification.filler),
    "junk_gold_1":      ItemData("1 Gold Piece",               ItemClassification.filler),
    "junk_stats":       ItemData("Stat Pack",                  ItemClassification.filler),

    # Traps
    "trap_teleport":    ItemData("Teleportation",              ItemClassification.trap),
    "trap_vertigo":     ItemData("Vertigo",                    ItemClassification.trap),
    "trap_shuffle":     ItemData("Genetic Lottery",            ItemClassification.trap),

    # Boss Events
    "evt_khidr":        ItemData("Defeat Khidr",               ItemClassification.progression, event=True),
    "evt_alex":         ItemData("Defeat Alexander",           ItemClassification.progression, event=True),
    "evt_leon":         ItemData("Defeat Ponce de Leon",       ItemClassification.progression, event=True),
    "evt_herodotus":    ItemData("Defeat Herodotus",           ItemClassification.progression, event=True),
    "evt_khidr_ex":     ItemData("Defeat Neo Khidr",           ItemClassification.progression, event=True),
    "evt_alex_ex":      ItemData("Defeat Alexander IV",        ItemClassification.progression, event=True),
    "evt_leon_ex":      ItemData("Defeat Ponce de Freon",      ItemClassification.progression, event=True),
    "evt_herodotus_ex": ItemData("Defeat Astrodotus",          ItemClassification.progression, event=True),
    "evt_johannes":     ItemData("Defeat Johannes",            ItemClassification.progression, event=True),
    "evt_johannes_ex":  ItemData("Defeat the Brohannes",       ItemClassification.progression, event=True),
    "evt_fountain":     ItemData("Defeat the Fountain",        ItemClassification.progression, event=True),
}


# fmt:on

filler = [
    rl_items_data["junk_gold_5000"],
    rl_items_data["junk_gold_3000"],
    rl_items_data["junk_gold_1000"],
    rl_items_data["junk_stats"],
    # Only a single 1 Gold Piece pack is shuffled in filler, 'cause I think it's funny.
]

traps = [
    rl_items_data["trap_teleport"],
    rl_items_data["trap_shuffle"],
    rl_items_data["trap_vertigo"],
]

item_name_to_id: dict[str, int] = {data.name: data.id for data in rl_items_data.values() if not data.event}

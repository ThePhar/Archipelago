from dataclasses import dataclass
from typing import NamedTuple

from BaseClasses import Item, ItemClassification


class RogueLegacyItem(Item):
    game = "Rogue Legacy"


class ItemData(NamedTuple):
    name: str
    default_classification: ItemClassification
    event: bool = False


# fmt: off
@dataclass
class RogueLegacyItems:
    # Classes
    class_knight =     ItemData("Progressive Knights",        ItemClassification.useful)
    class_mage =       ItemData("Progressive Mages",          ItemClassification.useful)
    class_barbarian =  ItemData("Progressive Barbarians",     ItemClassification.useful)
    class_knave =      ItemData("Progressive Knaves",         ItemClassification.useful)
    class_shinobi =    ItemData("Progressive Shinobi",        ItemClassification.useful)
    class_miner =      ItemData("Progressive Miners",         ItemClassification.useful)
    class_lich =       ItemData("Progressive Liches",         ItemClassification.useful)
    class_spellthief = ItemData("Progressive Spellthieves",   ItemClassification.useful)
    class_dragon =     ItemData("Dragons",                    ItemClassification.progression)
    class_traitor =    ItemData("Traitors",                   ItemClassification.useful)

    # Skills
    skill_hp =         ItemData("Health Up",                  ItemClassification.progression_skip_balancing)
    skill_mp =         ItemData("Mana Up",                    ItemClassification.progression_skip_balancing)
    skill_at =         ItemData("Attack Up",                  ItemClassification.progression_skip_balancing)
    skill_md =         ItemData("Magic Damage Up",            ItemClassification.progression_skip_balancing)
    skill_ar =         ItemData("Armor Up",                   ItemClassification.useful)
    skill_eq =         ItemData("Equip Up",                   ItemClassification.useful)
    skill_cc =         ItemData("Crit Chance Up",             ItemClassification.useful)
    skill_cd =         ItemData("Crit Damage Up",             ItemClassification.useful)
    skill_ds =         ItemData("Down Strike Up",             ItemClassification.filler)
    skill_gg =         ItemData("Gold Gain Up",               ItemClassification.filler)
    skill_pe =         ItemData("Potion Efficiency Up",       ItemClassification.filler)
    skill_it =         ItemData("Invuln Time Up",             ItemClassification.filler)
    skill_mc =         ItemData("Mana Cost Down",             ItemClassification.filler)
    skill_dd =         ItemData("Death Defy",                 ItemClassification.useful)
    skill_ha =         ItemData("Haggling",                   ItemClassification.filler)
    skill_rc =         ItemData("Randomize Children",         ItemClassification.useful)

    # Blueprints
    bp_progressive =   ItemData("Progressive Blueprints",     ItemClassification.useful)
    bp_squire =        ItemData("Squire Blueprints",          ItemClassification.useful)
    bp_silver =        ItemData("Silver Blueprints",          ItemClassification.useful)
    bp_guardian =      ItemData("Guardian Blueprints",        ItemClassification.useful)
    bp_imperial =      ItemData("Imperial Blueprints",        ItemClassification.useful)
    bp_royal =         ItemData("Royal Blueprints",           ItemClassification.useful)
    bp_knight =        ItemData("Knight Blueprints",          ItemClassification.useful)
    bp_ranger =        ItemData("Ranger Blueprints",          ItemClassification.useful)
    bp_sky =           ItemData("Sky Blueprints",             ItemClassification.useful)
    bp_dragon =        ItemData("Dragon Blueprints",          ItemClassification.useful)
    bp_slayer =        ItemData("Slayer Blueprints",          ItemClassification.useful)
    bp_blood =         ItemData("Blood Blueprints",           ItemClassification.useful)
    bp_sage =          ItemData("Sage Blueprints",            ItemClassification.useful)
    bp_retribution =   ItemData("Retribution Blueprints",     ItemClassification.useful)
    bp_holy =          ItemData("Holy Blueprints",            ItemClassification.useful)
    bp_dark =          ItemData("Dark Blueprints",            ItemClassification.useful)

    # Vendor Slots
    slot_bp_sword =    ItemData("Blacksmith Sword Upgrades",  ItemClassification.useful)
    slot_bp_helm =     ItemData("Blacksmith Helm Upgrades",   ItemClassification.useful)
    slot_bp_chest =    ItemData("Blacksmith Chest Upgrades",  ItemClassification.useful)
    slot_bp_limbs =    ItemData("Blacksmith Limbs Upgrades",  ItemClassification.useful)
    slot_bp_cape =     ItemData("Blacksmith Cape Upgrades",   ItemClassification.useful)
    slot_rune_sword =  ItemData("Enchantress Sword Upgrades", ItemClassification.useful)
    slot_rune_helm =   ItemData("Enchantress Helm Upgrades",  ItemClassification.useful)
    slot_rune_chest =  ItemData("Enchantress Chest Upgrades", ItemClassification.useful)
    slot_rune_limbs =  ItemData("Enchantress Limbs Upgrades", ItemClassification.useful)
    slot_rune_cape =   ItemData("Enchantress Cape Upgrades",  ItemClassification.useful)

    # Runes
    rune_vault =       ItemData("Vault Runes",                ItemClassification.progression)
    rune_sprint =      ItemData("Sprint Runes",               ItemClassification.progression)
    rune_vampire =     ItemData("Vampire Runes",              ItemClassification.useful)
    rune_sky =         ItemData("Sky Runes",                  ItemClassification.progression)
    rune_siphon =      ItemData("Siphon Runes",               ItemClassification.useful)
    rune_retaliation = ItemData("Retaliation Runes",          ItemClassification.filler)
    rune_bounty =      ItemData("Bounty Runes",               ItemClassification.filler)
    rune_haste =       ItemData("Haste Runes",                ItemClassification.filler)
    rune_curse =       ItemData("Curse Runes",                ItemClassification.filler)
    rune_grace =       ItemData("Grace Runes",                ItemClassification.filler)
    rune_balance =     ItemData("Balance Runes",              ItemClassification.useful)

    # Key Items
    fountain_piece =   ItemData("Fountain Piece",             ItemClassification.progression_skip_balancing)

    # Junk/Filler
    junk_gold_1000 =   ItemData("1000 Gold Pieces",           ItemClassification.filler)
    junk_gold_3000 =   ItemData("3000 Gold Pieces",           ItemClassification.filler)
    junk_gold_5000 =   ItemData("5000 Gold Pieces",           ItemClassification.filler)
    junk_gold_1 =      ItemData("1 Gold Piece",               ItemClassification.filler)
    junk_stats =       ItemData("Stat Pack",                  ItemClassification.filler)

    # Traps
    trap_teleport =    ItemData("Teleport Trap",              ItemClassification.trap)
    trap_vertigo =     ItemData("Vertigo",                    ItemClassification.trap)
    trap_shuffle =     ItemData("Genetic Lottery",            ItemClassification.trap)

    # Boss Events
    evt_khidr =        ItemData("Defeat Khidr",               ItemClassification.progression, True)
    evt_alex =         ItemData("Defeat Alexander",           ItemClassification.progression, True)
    evt_leon =         ItemData("Defeat Ponce de Leon",       ItemClassification.progression, True)
    evt_herodotus =    ItemData("Defeat Herodotus",           ItemClassification.progression, True)
    evt_khidr_ex =     ItemData("Defeat Neo Khidr",           ItemClassification.progression, True)
    evt_alex_ex =      ItemData("Defeat Alexander IV",        ItemClassification.progression, True)
    evt_leon_ex =      ItemData("Defeat Ponce de Freon",      ItemClassification.progression, True)
    evt_herodotus_ex = ItemData("Defeat Astrodotus",          ItemClassification.progression, True)
    evt_johannes =     ItemData("Defeat Johannes",            ItemClassification.progression, True)
    evt_johannes_ex =  ItemData("Defeat the Brohannes",       ItemClassification.progression, True)
    evt_fountain =     ItemData("Defeat the Fountain",        ItemClassification.progression, True)

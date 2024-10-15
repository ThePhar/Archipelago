from dataclasses import dataclass
from typing import TYPE_CHECKING

from Options import (
    Choice,
    OptionSet,
    OptionError,
    PerGameCommonOptions,
    Visibility,
    Range,
    Toggle,
    DefaultOnToggle,
    NamedRange,
    OptionGroup,
    ProgressionBalancing,
    Accessibility,
    StartInventoryPool,
)

from .locations import (
    MIN_BROWN_CHESTS,
    MAX_BROWN_CHESTS,
    MIN_SILVER_CHESTS,
    MAX_SILVER_CHESTS,
    MIN_GOLD_CHESTS,
    MAX_GOLD_CHESTS,
    MIN_FAIRY_CHESTS,
    MAX_FAIRY_CHESTS,
    MIN_DIARIES,
    MAX_DIARIES,
)
from .utils import check_name_allowed

if TYPE_CHECKING:
    from . import RogueLegacyWorld


class EnemyScaling(Choice):
    """A modifier for scaling enemy levels and stats, the deeper in the castle as the player explores. Also affects
    bosses.

    - **Relaxed**: Scales enemies back 25%, compared to vanilla Rogue Legacy.
    - **Normal**: The standard enemy scaling in Rogue Legacy.
    - **Hard**: Scales enemies up 50%, compared to vanilla Rogue Legacy.
    - **Harder**: Scales enemies up 100%, compared to vanilla Rogue Legacy.
    - **Absurd**: Scales enemies up 200%, compared to vanilla Rogue Legacy.
    """

    display_name = "Enemy Scaling Modifier"
    option_relaxed = 75
    option_normal = 100
    option_hard = 150
    option_harder = 200
    option_absurd = 300
    default = option_normal


class CastleScaling(Choice):
    """A modifier for scaling the size of Castle Hamson and its 4 areas, relative to the number of chest locations.

    - **Normal**: Scales the castle in lockstep with the number of chest locations.
    - **Large**: Scales the castle an additional 33% on top of "Normal".
    - **Very Large**: Scales the castle an additional 66% on top of "Normal".
    - **Labyrinth**: Scales the castle an additional 100% on top of "Normal".
    """

    display_name = "Castle Scaling Modifier"
    option_normal = 100
    option_large = 133
    option_very_large = 166
    option_labyrinth = 200
    default = option_normal


class BossChamberShuffle(Toggle):
    """Shuffles the boss chambers of all bosses (excluding The Fountain Room). If Neo Bosses are enabled, those are also
    shuffled in the boss pool.
    """

    display_name = "Boss Chamber Shuffle"

    def generate_boss_order(self, world: RogueLegacyWorld):
        boss_order = ["khidr", "alex", "leon", "herodotus"]
        if world.options.neo_bosses:
            boss_order.extend(["khidr_neo", "alex_neo", "leon_neo", "herodotus_neo", "traitor_neo"])
        if self:  # If enabled.
            world.random.shuffle(boss_order)

        return boss_order


class BrownChests(Range):
    """The minimum number of brown chests (shared between all 4 areas) that may contain items; may be larger to
    accommodate a larger item pool depending on other settings. Chests have defined locations in the world at generation
    and are highlighted on the player's map, if hinted.

    Brown chests are typically easily accessible and may contain any item and/or gold.

    Can all be targeted with the "Brown Chests" location group.
    """

    display_name = "Brown Chest Locations"
    range_start = MIN_BROWN_CHESTS
    range_end = MAX_BROWN_CHESTS
    default = range_start


class SilverChests(Range):
    """The minimum number of silver chests (shared between all 4 areas) that may contain items; may be larger to
    accommodate a larger item pool depending on other settings. Chests have defined locations in the world at generation
    and are highlighted on the player's map, if hinted.

    Silver chests may require additional movement to access and may contain any item and/or gold.

    Can all be targeted with the "Silver Chests" location group.
    """

    display_name = "Silver Chest Locations"
    range_start = MIN_SILVER_CHESTS
    range_end = MAX_SILVER_CHESTS
    default = range_start


class GoldChests(Range):
    """The number of gold chests (shared between all 4 areas) that may contain items. Chests have defined locations in
    the world at generation and are highlighted on the player's map, if hinted (excluding Compass Room).

    Gold chests require beating mini-bosses, finding difficult to find rooms, or winning certain mini-games, and may
    contain any item, gold, and/or stat increase.

    Can all be targeted with the "Gold Chests" location group.
    """

    display_name = "Gold Chest Locations"
    range_start = MIN_GOLD_CHESTS
    range_end = MAX_GOLD_CHESTS
    default = range_start


class FairyChests(Range):
    """The number of fairy chests (shared between all 4 areas) that may contain items. Chests have defined locations in
    the world at generation and are highlighted on the player's map, if hinted.

    Fairy chests may require additional movement and beating certain room challenges and may contain any item and/or
    triple stat increase.

    Can all be targeted with the "Fairy Chests" location group.
    """

    display_name = "Fairy Chest Locations"
    range_start = MIN_FAIRY_CHESTS
    range_end = MAX_FAIRY_CHESTS
    default = 0


class DiaryEntries(Range):
    """The number of diary entries that can be discovered. Diaries do not have defined locations and are incremental, so
    "Diary Entry #1" precedes "Diary Entry #2" and so on...

    There will always be at least 2 entries: one in the entry room (always available) and one outside the Fountain room
    (requires opening the Fountain Room Door).

    Can all be targeted with the "Diaries" location group.
    """

    display_name = "Diary Entries"
    range_start = MIN_DIARIES
    range_end = MAX_DIARIES
    default = 25


class NeoBosses(Choice):
    """Adds the 5 challenge bosses and their accompanying rewards and obol to access their boss chamber to the item/location
    pool.

    - **Excluded**: These bosses are not accessible or expected.
    - **Included**: Includes these bosses, but does not require their completion to open the Fountain Door.
    - **Required**: Includes these bosses and requires beating all of them to open the Fountain Door.
    """

    display_name = "Neo Bosses"
    option_excluded = 0
    option_included = 1
    option_required = 2
    default = option_excluded


class AdditionalChallenges(DefaultOnToggle):
    """Adds a list of additional challenges that may contain items, whose progress can be viewed in the pause menu."""

    display_name = "Additional Challenges"


class NGPRequirement(Range):
    """Determines the number of times required to defeat The Fountain on New Game Plus.

    Also affects the number of chests available per play-through and fountain pieces required for the Fountain Door, if
    Fountain Hunt is enabled."""

    display_name = "New Game Plus Requirement"
    range_start = 0
    range_end = 2
    default = 0


class LevelCap(Toggle):
    """If enabled, the player can only purchase skills up to the given level cap before requiring an "Unlocked
    Potential" item to increase the level cap.

    Level limits are as followed:

    - **0**: Level Limit @ 25
    - **1**: Level Limit @ 50
    - **2**: Level Limit @ 75
    - **3**: Level Limit @ 100
    - **4**: Level Limit @ 150
    - **5**: No Level Limit

    Also allows selling purchased skills back for 75% of the gold originally spent on that level.
    """

    display_name = "Level Progression Limit"


class GoldGainMultiplier(Choice):
    """Affects the amount of gold gained from all sources.

    - **Halved**: Obtain 50% of gold, compared to normal.
    - **Reduced**: Obtain 75% of gold, compared to normal.
    - **Normal**: Obtain 100% of gold, compared to normal.
    - **Increased**: Obtain 150% of gold, compared to normal.
    - **Doubled**: Obtain 200% of gold, compared to normal.
    - **Tripled**: Obtain 300% of gold, compared to normal.
    - **Quadrupled**: Obtain 400% of gold, compared to normal.
    """

    display_name = "Gold Gain Multiplier"
    option_halved = 50
    option_reduced = 75
    option_normal = 100
    option_increased = 150
    option_doubled = 200
    option_tripled = 300
    option_quadrupled = 400
    default = option_normal


class ShuffleBlacksmithSlots(Toggle):
    """Shuffles the 5 equipment purchase slots for the Blacksmith, requiring the slot in addition to the blueprint to
    purchase new equipment, into the item pool.
    """

    display_name = "Shuffle Blacksmith Slots"


class ShuffleEnchantressSlots(Toggle):
    """Shuffles the 5 equipment purchase slots for the Enchantress, requiring the slot in addition to the rune to
    purchase new runes, into the item pool.
    """

    display_name = "Shuffle Enchantress Slots"


class Charon(DefaultOnToggle):
    """Determines if Charon is gate-keeping access to Castle Hamson until the player pays the toll. If disabled, Charon
    goes on vacation, and the player doesn't have to pay the toll to enter.
    """

    display_name = "Charon Gatekeeper Toll"


class Children(NamedRange):
    """Determines the number of offspring that can be chosen from each life.

    Can also be set to one of the following special values:

    - **Vanilla**: An alias for 3, which matches vanilla Rogue Legacy.
    - **Variable**: Picks a random number of children each life between 2 and 5.
    - **Shuffle Children**: Can only select from 1 child per life until a "Child" item is received.
    """

    display_name = "Children"
    range_start = 1
    range_end = 5
    default = 3
    special_range_names = {
        "vanilla": 3,
        "variable": -1,
        "shuffle_children": -2,
    }


class TrapPercentage(Range):
    """Determines the % of filler items that can get replaced with various trapped items that cause negative effects."""

    display_name = "Filler Trapped Items %"
    range_start = 0
    range_end = 100
    default = 0


class SkillLevelMaximum(Choice):
    option_25 = 25
    option_30 = 30
    option_35 = 35
    option_40 = 40
    option_45 = 45
    option_50 = 50
    option_55 = 55
    option_60 = 60
    option_65 = 65
    option_70 = 70
    option_75 = 75
    default = option_75


class MaxHealthLevel(SkillLevelMaximum):
    """Determines the maximum Health Up level, by removing extras from the item pool (vanilla is 75)."""

    display_name = "Health Up Max Level"


class MaxManaLevel(SkillLevelMaximum):
    """Determines the maximum Mana Up level, by removing extras from the item pool (vanilla is 75)."""

    display_name = "Mana Up Max Level"


class MaxAttackLevel(SkillLevelMaximum):
    """Determines the maximum Attack Up level, by removing extras from the item pool (vanilla is 75)."""

    display_name = "Attack Up Max Level"


class MaxMagicLevel(SkillLevelMaximum):
    """Determines the maximum Magic Damage Up level, by removing extras from the item pool (vanilla is 75)."""

    display_name = "Magic Damage Up Max Level"


class FountainHunt(Toggle):
    """Adds a requirement to open the final door to the Fountain Room, by requiring a certain number of Fountain Pieces.

    If New Game Plus Requirement is enabled, the amount needed per door is divided by the number of passes required.
    """

    display_name = "Fountain Hunt"


class FountainPiecesAvailable(Range):
    """Determines the number of Fountain Pieces available, if Fountain Hunt is enabled."""

    display_name = "Fountain Pieces Available"
    range_start = 1
    range_end = 80
    default = 5


class FountainPiecesRequired(Range):
    """Determines the percentage of available Fountain Pieces available that are required, if Fountain Hunt is enabled."""

    display_name = "Fountain Pieces Required"
    range_start = 1
    range_end = 100
    default = 75


class DeathLink(Choice):
    """*When you die, everyone dies. Of course, the reverse is also true.*

    - **Forbidden**: The player starts with DeathLink disabled and cannot toggle it on.
    - **Disabled**: The player starts with DeathLink disabled, but can toggle it in-game at any time.
    - **Enabled**: The player starts with DeathLink enabled, but can toggle it in-game at any time.
    - **Enforced**: The player starts with DeathLink enabled and cannot toggle it off.
    """

    display_name = "Death Link"
    option_forbidden = 0
    option_disabled = 1
    option_enabled = 2
    option_enforced = 3
    alias_true = 2
    alias_false = 1
    default = option_disabled


class SirCharacterNames(OptionSet):
    """Define a pool of potential names for the player's 'sir' offspring.

    Names only support a limited set of characters allowed by the game. Any invalid characters will cause a generation
    error, along with a set of the characters not allowed. All printable ASCII characters are allowed.

    `__default` is a special value that includes names defined in the game's `Content/HeroNames.txt` file. It cannot be
    used as a character's name.
    """

    display_name = "Character Names for Sirs"
    default = {"__default"}
    valid_keys = ["__default"]
    visibility = Visibility.template + Visibility.spoiler

    def verify_keys(self) -> None:
        dataset = set(self.value) - self.default  # Ignore __default
        invalid_names: dict[str, set[str]] = {}
        for name in dataset:
            result, invalid_chars = check_name_allowed(name)
            if not result:
                invalid_names[name] = invalid_chars

        if invalid_names:
            raise OptionError(
                f"The following 'Sir' character name(s) contain invalid characters:\n\t"
                + "\n\t".join([f"{name}: {invalid_chars}" for name, invalid_chars in invalid_names.items()])
                + "\n\nPlease make the required adjustments and retry."
            )


class LadyCharacterNames(OptionSet):
    """Define a pool of potential names for the player's 'lady' offspring.

    Names only support a limited set of characters allowed by the game. Any invalid characters will cause a generation
    error, along with a set of the characters not allowed. All printable ASCII characters are allowed.

    `__default` is a special value that includes names defined in the game's `Content/HeroineNames.txt` file. It cannot
    be used as a character's name.
    """

    display_name = "Character Names for Ladies"
    default = {"__default"}
    valid_keys = ["__default"]
    visibility = Visibility.template + Visibility.spoiler

    def verify_keys(self) -> None:
        dataset = set(self.value) - self.default  # Ignore __default
        invalid_names: dict[str, set[str]] = {}
        for name in dataset:
            result, invalid_chars = check_name_allowed(name)
            if not result:
                invalid_names[name] = invalid_chars

        if invalid_names:
            raise OptionError(
                f"The following 'Lady' character name(s) contain invalid characters:\n\t"
                + "\n\t".join([f"{name}: {invalid_chars}" for name, invalid_chars in invalid_names.items()])
                + "\n\nPlease make the required adjustments and retry."
            )


@dataclass
class RogueLegacyOptions(PerGameCommonOptions):
    children: Children
    level_limit: LevelCap
    shuffle_blacksmith: ShuffleBlacksmithSlots
    shuffle_enchantress: ShuffleEnchantressSlots
    chests_brown: BrownChests
    chests_silver: SilverChests
    chests_gold: GoldChests
    chests_fairy: FairyChests
    diary_entries: DiaryEntries
    neo_bosses: NeoBosses
    additional_challenges: AdditionalChallenges
    enemy_scaling: EnemyScaling
    castle_scaling: CastleScaling
    ngplus_requirement: NGPRequirement
    boss_shuffle: BossChamberShuffle
    gold_gain: GoldGainMultiplier
    charon: Charon
    fountain_hunt: FountainHunt
    fountain_pieces_available: FountainPiecesAvailable
    fountain_pieces_required: FountainPiecesRequired
    character_names_sir: SirCharacterNames
    character_names_lady: LadyCharacterNames
    max_health: MaxHealthLevel
    max_mana: MaxManaLevel
    max_attack: MaxAttackLevel
    max_magic_damage: MaxMagicLevel
    trap_percentage: TrapPercentage
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool


rl_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Generation",
        [
            Children,
            BrownChests,
            SilverChests,
            GoldChests,
            FairyChests,
            DiaryEntries,
            AdditionalChallenges,
            EnemyScaling,
            CastleScaling,
        ],
    ),
    OptionGroup(
        "Items & Economy",
        [
            Accessibility,
            ShuffleBlacksmithSlots,
            ShuffleEnchantressSlots,
            Charon,
            GoldGainMultiplier,
            MaxHealthLevel,
            MaxManaLevel,
            MaxAttackLevel,
            MaxMagicLevel,
            TrapPercentage,
        ],
    ),
    OptionGroup(
        "Logic",
        [
            LevelCap,
            NeoBosses,
            BossChamberShuffle,
            NGPRequirement,
            FountainHunt,
            FountainPiecesAvailable,
            FountainPiecesRequired,
        ],
    ),
    OptionGroup(
        "Multiworld",
        [
            ProgressionBalancing,
            DeathLink,
        ],
    ),
]

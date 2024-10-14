from worlds.AutoWorld import World


class RogueLegacyWorld(World):
    """Rogue Legacy is a genealogical rogue-"lite", where anyone can be a hero. Each time you die, your child will
    succeed you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a
    dwarf. But that's OK, because no one is perfect, and you don't have to be to succeed.
    """

    game = "Rogue Legacy"
    required_client_version = (0, 5, 1)

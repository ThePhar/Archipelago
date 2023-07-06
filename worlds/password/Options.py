from Options import DeathLink


class PasswordDeathLink(DeathLink):
    """
    When you die, all non-Password games die. You do not die from other DeathLinks.

    For now... (if I feel like it).
    """


password_options = {
    "death_link": PasswordDeathLink,
}

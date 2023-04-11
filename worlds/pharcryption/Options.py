from typing import Dict

from Options import AssembleOptions, DefaultOnToggle, Range


class EncryptedItems(Range):
    """
    Number of items per player to "encrypt".

    Warning: Will cause generation failure if there are not enough progression items available to fulfil this
    requirement.
    """
    display_name = "Items to Encrypt per Player"
    default = 15
    range_start = 10
    range_end = 50


class FreeDecryptions(Range):
    """Amount of free-choice "decryptions" given to Pharcryption per player."""
    display_name = "Free Decryptions per Player"
    default = 1
    range_start = 0
    range_end = 5


class PaymentAmount(Range):
    """Interval number of Pharcoins to pay for items to be "decrypted"."""
    display_name = "Payment Amount"
    default = 5
    range_start = 1
    range_end = 10


class ExtraPharcoins(Range):
    """
    Number of extra Pharcoins that can be found to help pay the ransom. Setting to 0, would require "mining" all
    Pharcoins before time runs out.
    """
    display_name = "Extra Pharcoins"
    default = 0
    range_start = 0
    range_end = 100


class EnableTimelimit(DefaultOnToggle):
    """Enables/Disables the time limit. For those who want a more... "lax" ransomware experience."""
    display_name = "Enable Timelimit"


class TimelimitDays(Range):
    """Timelimit until all remaining items are encrypted forever, provided Enable Timelimit is not disabled."""
    display_name = "Timelimit in Days"
    default = 0
    range_start = 0
    range_end = 31


class TimelimitHours(Range):
    """Timelimit until all remaining items are encrypted forever, provided Enable Timelimit is not disabled."""
    display_name = "Timelimit in Hours"
    default = 4
    range_start = 0
    range_end = 23


class TimelimitMinutes(Range):
    """Timelimit until all remaining items are encrypted forever, provided Enable Timelimit is not disabled."""
    display_name = "Timelimit in Minutes"
    default = 0
    range_start = 0
    range_end = 59


options: Dict[str, AssembleOptions] = {
    "encrypted_items":   EncryptedItems,
    "free_decryptions":  FreeDecryptions,
    "payment_amount":    PaymentAmount,
    "extra_pharcoins":   ExtraPharcoins,
    "enable_timelimit":  EnableTimelimit,
    "timelimit_days":    TimelimitDays,
    "timelimit_hours":   TimelimitHours,
    "timelimit_minutes": TimelimitMinutes,
}

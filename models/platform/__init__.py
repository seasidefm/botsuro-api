import enum
from typing import Literal

Platform = Literal["TWITCH", "DISCORD", "MINECRAFT"]


class PlatformEnum(enum.Enum):
    """
    Represents a platform enum.

    Attributes:
        TWITCH: Represents the Twitch platform.
        DISCORD: Represents the Discord platform.
        MINECRAFT: Represents the Minecraft platform.
    """

    TWITCH = ("TWITCH",)
    DISCORD = ("DISCORD",)
    MINECRAFT = "MINECRAFT"

    @classmethod
    def from_str(cls, platform: Platform):
        """
        Converts a string to a PlatformEnum.

        :param platform: The platform to convert.
        :type platform: str

        :return: The converted platform.
        :rtype: PlatformEnum
        """
        return cls[platform.upper()]

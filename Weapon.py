from Stat import Stat
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Character import Character


class Weapon:
    def __init__(self):
        self._mWeaponName = 'Weapon'
        self._mMainStat: Stat = Stat()
        self._mSubStat: Stat = Stat()
        self._mSubSubStat: Stat = Stat()

    def DoFeedback(self, character: 'Character'):
        pass

    def GetMainStat(self):
        return self._mMainStat

    def GetSubStat(self):
        return self._mSubStat

    def GetSubSubStat(self):
        return self._mSubSubStat

    def GetName(self):
        return self._mWeaponName 
import Stat
import numpy as np
import Character

class Weapon:
    _mWeaponName = 'Weapon'
    _mMainStat: Stat = Stat()
    _mSubStat: Stat = Stat()
    _mSubSubStat: Stat = Stat()

    def DoFeedback (character: Character):
        pass

    def GetMainStat(self):
        return self._mMainStat

    def GetSubStat(self):
        return self._mSubStat

    def GetSubSubStat(self):
        return self._mSubSubStat

    def GetName(self):
        return self._mWeaponName 
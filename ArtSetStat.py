from Stat import Stat
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Character import Character


class ArtSetStat:
    def __init__(self):
        self.__mCharacterUsingThis = []
        self.__mStat: Stat = Stat()
    
    def AlertModified(self):
        for character in self.__mCharacterUsingThis:
            character.ConfirmArtSetStatModified()

    def DoFeedback(self, character: 'Character'):
        pass

    def SaveCharacterPointer(self, character: 'Character'):
        self.__mCharacterUsingThis.append(character)

    def DeleteCharacterPointer(self, character: 'Character'):
        self.__mCharacterUsingThis.remove(character)

    def SetZero(self):
        self.__mStat.SetZero()
        self.AlertModified()

    def Update(self):
        self.__mStat.Update()
        self.AlertModified()

    def GetStat(self):
        return self.__mStat

    def GetOption(self, index: int):
        return self.__mStat.GetOption(index)

    def SetOption(self, index: int, amount: float):
        self.__mStat.SetOption(index, amount)
        self.AlertModified()

    def AddOption(self, index: int, amount: float):
        self.__mStat.AddOption(index, amount)
        self.AlertModified()

    def IsUsingThis(self, character: 'Character'):
        return any(character == self.__mCharacterUsingThis[i] for i in range(len(self.__mCharacterUsingThis)))
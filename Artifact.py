import Stat
import numpy as np
import random as rd


MAXMAINOPTIONLIST = np.array([  31.1, 62.2, 46.6, 311., 51.8,
                                46.6, 4780., 187., 58.3, 0.,
                                46.6, 46.6, 46.6, 46.6, 46.6,
                                46.6, 46.6, 46.6, 35.9 ])

SUBOPTPROB = np.array([ 3, 3, 4, 6, 4, 4, 6, 4, 4, 6 ])
OPTIONARRAY = np.array([[2.72000003606081, 3.10999993234873, 3.50000001490116, 3.88999991118908],
                        [5.44000007212162, 6.21999986469746, 6.98999986052513, 7.76999965310097],
                        [4.08000014722347, 4.65999990701675, 5.24999983608723, 5.82999996840954],
                        [13.6199998855591, 15.5600004196166, 17.5100002288818, 19.4500007629395],
                        [4.52999994158745, 5.18000014126301, 5.82999996840954, 6.4800001680851 ],
                        [4.08000014722347, 4.65999990701675, 5.24999983608723, 5.82999996840954],
                        [209.130004882813, 239.            , 268.880004882813, 298.75          ],
                        [16.3199996948242, 18.6499996185303, 20.9799995422363, 23.3099994659424],
                        [5.09999990463257, 5.82999996840954, 6.56000003218651, 7.28999972343445],
                        [16.2000007629395, 18.5200004577637, 20.8299999237061, 23.1499996185303]])


# class Character:
#    pass


def CheckIsThereIn(element: int, list: np.array):
	returnBool = False
	for i in range(4):
		if (element == list[i]):
			returnBool = True
			break
	return returnBool


class Artifact:
    __mMainType = 0

    __mMainStat: Stat = Stat()
    __mSubStat: Stat = Stat()
    
    __mCharactersUsingThis = []

    def __UseCummulatedWeight(self, cummulatedWeight: np.array):
        # generate random integer from 0 to the sum of probability table
        length = cummulatedWeight.size()
        
        if (cummulatedWeight[length - 1] == 1):
            tempInt = 1
        else:
            tempInt = rd.randrange(0, cummulatedWeight[length - 1]) + 1

        selectedInt = 0
        for i in range(length): # for문을 돌리면서 대소비교를 한다.
            nowElement = cummulatedWeight[i]
            if (tempInt > beforeElement and tempInt <= nowElement):
                selectedInt = i # 랜덤 int를 가지고 어느 주옵인지 결정한다.
                break
            beforeElement = nowElement
        return selectedInt
    
    def __GenerateMainOption(self):
        selectedInt = self.__UseCummulatedWeight(self._mCummulatedWeight)
        self.SetMainType(selectedInt)

    def __GenerateSubOption(self):
        subCummulatedWeight: np.array = self.__GenerateCummulatedWeight()
		# 1. 메인옵션을 확인해서 확률표에서 해당 부분을 0으로 만든다.
			# 1-1. 이걸 가지고 cummulatedWeight을 만든다.
				# This cummulatedWeight is for subOption
				# Therefore the length of cummulatedWeight is 10.

        whether4OptStart: bool = self.__Selected3or4OptStart()
            # 2. 처음에 3개인지 4개인지 고른다. -> 8개 or 9개
        startOptList: np.array = self.__GenerateStartOpt(subCummulatedWeight)
            # 3. 처음 옵션 4개가 무엇인지 결정한다. 4개를 겹치지 않게 생성한다.

        self.__UpgradeSubOption(startOptList, whether4OptStart)
            # 4. 기존 4개를 랜덤으로 각각 1회 고정에 랜덤으로 4회 또는 5회 증가시킨다.

    def __GenerateCummulatedWeight(self):
        returnList = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for x in returnList:
            x = SUBOPTPROB[i]
        if ((self.__mMainType >= 0) and (self.__mMainType < 10) and (self.__mMainType != 3) and (self.__mMainType != 6)):
            returnList[self.__mMainType] = 0
        for i in range(9):
            returnList[i + 1] += returnList[i]
        return returnList
        
    def __Selected3or4OptStart(self):
        if (rd.randrange(0, 5) == 0):
            return True
        else:
            return False
        
    def __GenerateStartOpt(self, cummulatedWeight):
        returnList = np.array([ -1, -1, -1, -1 ])
        returnList[0] = self.__UseCummulatedWeight(cummulatedWeight)
        for j in range(3):
            i = j + 1
            temp = self.__UseCummulatedWeight(cummulatedWeight)
            while (CheckIsThereIn(temp, returnList)):
                temp = self.__UseCummulatedWeight(cummulatedWeight)
            returnList[i] = temp
        return returnList
        
    def __UpgradeSubOption(self, startOptList, whether4OptStart):
        numUpgrade = 4
        if (whether4OptStart):
            numUpgrade = 5

        # 각각 1회씩
        for i in range(4):
            optIndex = startOptList[i]
            randomStat = OPTIONARRAY[optIndex][rd.randrange(0, 4)]
            self.__mSubStat.AddOption(optIndex, randomStat)

        # 랜덤으로 numUpgrade만큼
        for i in range(numUpgrade):
            randomIndex = startOptList[rd.randrange(0, 4)]
            randomStat = OPTIONARRAY[randomIndex][rd.randrange(0, 4)]
            self.__mSubStat.AddOption(randomIndex, randomStat)
        
    def __AlertModified(self):
        for character in self.__mCharactersUsingThis:
            character.ConfirmArtifactMainStatModified()


    _mType: int = 0
    _mProbabilityWeight = np.array([])
    _mCummulatedWeight = np.array([])


    def Generation(self):
        self.__mMainStat.SetZero()
        self.__mSubStat.SetZero()
        self.__GenerateMainOption() # 메인옵션 : 부위마다 다름.
        self.__GenerateSubOption() # 부옵션 : 부위마다, 메인옵션마다 다름.
        self.__AlertModified()

    def Generation(self, mainType):
        self.__mMainStat.SetZero()
        self.__mSubStat.SetZero()
        self.SetMainType(mainType)
        self.__GenerateSubOption()
        self.__AlertModified()

    def GetType(self):
        return self._mType

    def GetMainType(self):
        return self.__mMainType

    def SetMainType(self, mainType):
        self.__mMainStat.SetZero()
        self.__mMainStat.SetOption(mainType, MAXMAINOPTIONLIST[mainType])
        self.__mMainType = mainType
        self.__AlertModified()

    def GetMainStat(self):
        return self.__mMainStat

    def GetSubStat(self):
        return self.__mSubStat

    def GetSubStatValue(self, index):
        return self.__mSubStat.GetOption(self, index)

    def SetSubStat(self, stat):
        self.__mSubStat = stat
        self.__AlertModified(self)

    def SaveCharacterPointer(self, character):
        self.__mCharactersUsingThis.append(character)

    def DeleteCharacterPointer(self, character):
        size = len(self.__mCharactersUsingThis)
        if (size == 0):
            pass
        if (size == 1 and self.__mCharactersUsingThis[0] == character):
            del self.__mCharactersUsingThis[0]
        else:
            self.__mCharactersUsingThis.remove(character)

    def IsUsingThis(self, character):
        returnBool = False
        length = len(self.__mCharactersUsingThis)
        for i in range(length):
            if (character == self.__mCharactersUsingThis[i]):
                returnBool = True
                break
        return returnBool

    def GetPossibleMainOption(self):
        return 0

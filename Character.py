from Stat import Stat
from Weapon import Weapon
from Artifact import Artifact
from ArtFlower import ArtFlower
from ArtFeather import ArtFeather
from ArtClock import ArtClock
from ArtCup import ArtCup
from ArtCrown import ArtCrown
from ArtSetStat import ArtSetStat
import numpy as np
from copy import deepcopy
from dataclasses import dataclass

PLUSARRAY = np.array([  3.88999991118908, 7.76999965310097, 5.82999996840954,
                        19.4500007629395, 6.4800001680851,  5.82999996840954,
                        298.75,           23.3099994659424, 7.28999972343445,
                        23.1499996185303 ])


@dataclass
class MainOptionsAndDamage:
    mainOptions: np.ndarray
    damage: float


def FindNthLargestOption(damArray, nth):
    tempList = []
    for i in range(10):
        tempList.append((damArray[i], i))
    tempList.sort(key=lambda x: x[0], reverse=True)
    return tempList[nth - 1][1]


class Character:
    __mArtFlower: ArtFlower
    __mArtFeather: ArtFeather
    __mArtClock: ArtClock
    __mArtCup: ArtCup
    __mArtCrown: ArtCrown
    __mArtSetStat: ArtSetStat

    def __init__(self, weapon: Weapon, artSetStat: ArtSetStat, flower: ArtFlower, feather: ArtFeather, clock: ArtClock, cup: ArtCup, crown: ArtCrown):
        self.__mStatAfterUpdateFromCharacterResonance: Stat = Stat() # never do initialization
        self.__mStatAfterUpdateFromWeapon: Stat = Stat() # never do initialization
        self.__mStatAfterUpdateFromArtSetStat: Stat = Stat() # never do initialization
        self.__mStatAfterUpdateFromArtifactMainStat: Stat = Stat() # never do initialization
        self.__mStatAfterUpdateFromArtifactSubStat: Stat = Stat() # never do initialization

        self.__mUpdateState: int

        self.__CHARACTERRESONANCEUPDATED: int = 1
        self.__WEAPONSTATUPDATED: int = 2
        self.__ARTSETSTATUPDATED: int = 3
        self.__ARTIFACTMAINSTATUPDATED: int = 4
        self.__ARTIFACTSUBSTATUPDATED: int = 5

        self.__mIsManualMode: bool = False

        self.__mSavedFunction: np.ndarray = np.zeros(46)
        self.__mEffectionArray: np.ndarray = np.zeros(19)

        self.__mStat: Stat = Stat()
        self.__mCharacterStat: Stat = Stat()
        self.__mFeedbackedStat: Stat = Stat()
        self.__mTargetEC: float = 100
        self.__mWeapon: Weapon
        self.SetArtifact(flower, feather, clock, cup, crown)
        self.SetArtSetStat(artSetStat)
        self.__mResonanceStat: Stat = Stat()

        self.__mWeapon = weapon

    def __del__(self):
        self.__mArtSetStat.DeleteCharacterPointer(self)
        self.__mArtFlower.DeleteCharacterPointer(self)
        self.__mArtFeather.DeleteCharacterPointer(self)
        self.__mArtClock.DeleteCharacterPointer(self)
        self.__mArtCup.DeleteCharacterPointer(self)
        self.__mArtCrown.DeleteCharacterPointer(self)

    def __UpdateFromCharacterResonance(self):
        # 캐릭터 옵션 : 0 ~ 34, b0 ~ b2
        self.__mStatAfterUpdateFromCharacterResonance.SetZero()
        for i in range(35):
            self.__mStatAfterUpdateFromCharacterResonance.AddOption(i, self.__mCharacterStat.GetOption(i))
        for i in range(3):
            self.__mStatAfterUpdateFromCharacterResonance.SetBaseOption(i, self.__mCharacterStat.GetBaseOption(i))

        # 공명 : 0, 2, 5, 7, 10 ~ 17, 27
        self.__mStatAfterUpdateFromCharacterResonance.AddOption(0, self.__mResonanceStat.GetOption(0))
        self.__mStatAfterUpdateFromCharacterResonance.AddOption(2, self.__mResonanceStat.GetOption(2))
        self.__mStatAfterUpdateFromCharacterResonance.AddOption(5, self.__mResonanceStat.GetOption(5))
        self.__mStatAfterUpdateFromCharacterResonance.AddOption(7, self.__mResonanceStat.GetOption(7))
        self.__mStatAfterUpdateFromCharacterResonance.AddOption(27, self.__mResonanceStat.GetOption(27))
        for j in range(10):
            i = j + 10
            self.__mStatAfterUpdateFromCharacterResonance.AddOption(i, self.__mResonanceStat.GetOption(i))

    def __UpdateFromWeapon(self):
        WeaponMainStat: Stat = self.__mWeapon.GetMainStat()
        WeaponSubStat: Stat = self.__mWeapon.GetSubStat()
        WeaponSubSubStat: Stat = self.__mWeapon.GetSubSubStat()
        
        self.__mStatAfterUpdateFromWeapon = self.__mStatAfterUpdateFromCharacterResonance

        # 무기 주옵 : b0
        self.__mStatAfterUpdateFromWeapon.SetBaseOption(0, self.__mStatAfterUpdateFromWeapon.GetBaseOption(0) + WeaponMainStat.GetBaseOption(0))

        # 무기 부옵 : 0 ~ 18 # 완전히 배제된 것은 아님
        for i in range(19):
            self.__mStatAfterUpdateFromWeapon.AddOption(i, WeaponSubStat.GetOption(i))

        # 무기 부부옵 : 0 ~ 23, 27, 28 # 완전히 배제된 것은 아님
        for i in range(24):
            self.__mStatAfterUpdateFromWeapon.AddOption(i, WeaponSubSubStat.GetOption(i))
        self.__mStatAfterUpdateFromWeapon.AddOption(27, WeaponSubSubStat.GetOption(27))
        self.__mStatAfterUpdateFromWeapon.AddOption(28, WeaponSubSubStat.GetOption(28))

    def __UpdateFromArtSetStat(self):
        self.__mStatAfterUpdateFromArtSetStat = self.__mStatAfterUpdateFromWeapon

        # 성유물 세트 : 0 ~ 23, 27, 28 # 완전히 배제된 것은 아님
        for i in range(24):
            self.__mStatAfterUpdateFromArtSetStat.AddOption(i, self.__mArtSetStat.GetOption(i))
        self.__mStatAfterUpdateFromArtSetStat.AddOption(27, self.__mArtSetStat.GetOption(27))
        self.__mStatAfterUpdateFromArtSetStat.AddOption(28, self.__mArtSetStat.GetOption(28))

    def __UpdateFromArtifactMainStat(self):
        self.__mStatAfterUpdateFromArtifactMainStat = self.__mStatAfterUpdateFromArtSetStat
    
        # 성유물 주옵 : 0 ~ 8, 10 ~ 18
        FlowerMainStat: Stat = self.__mArtFlower.GetMainStat()
        FeatherMainStat: Stat = self.__mArtFeather.GetMainStat()
        ClockMainStat: Stat = self.__mArtClock.GetMainStat()
        CupMainStat: Stat = self.__mArtCup.GetMainStat()
        CrownMainStat: Stat = self.__mArtCrown.GetMainStat()
        
        self.__mStatAfterUpdateFromArtifactMainStat.AddOption(6, FlowerMainStat.GetOption(6))
        self.__mStatAfterUpdateFromArtifactMainStat.AddOption(3, FeatherMainStat.GetOption(3))
        self.__mStatAfterUpdateFromArtifactMainStat.AddOption(self.__mArtClock.GetMainType(), ClockMainStat.GetOption(self.__mArtClock.GetMainType()))
        self.__mStatAfterUpdateFromArtifactMainStat.AddOption(self.__mArtCup.GetMainType(), CupMainStat.GetOption(self.__mArtCup.GetMainType()))
        self.__mStatAfterUpdateFromArtifactMainStat.AddOption(self.__mArtCrown.GetMainType(), CrownMainStat.GetOption(self.__mArtCrown.GetMainType()))

    def __UpdateFromArtifactSubStat(self):
        self.__mStatAfterUpdateFromArtifactSubStat = self.__mStatAfterUpdateFromArtifactMainStat
    
        # 성유물 부옵 : 0 ~ 9
        for i in range(10):
            self.__mStatAfterUpdateFromArtifactSubStat.AddOption(i, self.__mArtFlower.GetSubStatValue(i))
            self.__mStatAfterUpdateFromArtifactSubStat.AddOption(i, self.__mArtFeather.GetSubStatValue(i))
            self.__mStatAfterUpdateFromArtifactSubStat.AddOption(i, self.__mArtClock.GetSubStatValue(i))
            self.__mStatAfterUpdateFromArtifactSubStat.AddOption(i, self.__mArtCup.GetSubStatValue(i))
            self.__mStatAfterUpdateFromArtifactSubStat.AddOption(i, self.__mArtCrown.GetSubStatValue(i))

    def __UpdateFromFeedback(self):
        self.__mFeedbackedStat.SetZero()
        self.__mWeapon.DoFeedback(self)
        self.__mArtSetStat.DoFeedback(self)
        self.DoFeedback()
        for i in range(24):
            self.__mStat.AddOption(i, self.__mFeedbackedStat.GetOption(i))
        self.__mStat.AddOption(27, self.__mFeedbackedStat.GetOption(27))
        self.__mStat.AddOption(28, self.__mFeedbackedStat.GetOption(28))

    def __MakeScoreFunctionMainOptionFixed(self, main3: int, main4: int, main5: int):
        mainOp = np.zeros(10) # It will be checked which main option is activated.
        if (self.__mArtClock.GetMainType() < 10):
            mainOp[self.__mArtClock.GetMainType()] = 1
        if (self.__mArtCup.GetMainType() < 10):
            mainOp[self.__mArtCup.GetMainType()] = 1
        if (self.__mArtCrown.GetMainType() < 10):
            mainOp[self.__mArtCrown.GetMainType()] = 1

        numArray = np.zeros(10) # It will be recorded in this array how many times each option is added.
        damArray = np.zeros(10) # It will be recorded in this array how much damage will be if each option is added.

        tempCharacter: Character
        tempSubStatArray = [Stat(), Stat(), Stat(), Stat(), Stat(),
                            Stat(), Stat(), Stat(), Stat(), Stat()]# Flower에만 적용될 것이다.

        # Character를 10개를 복사한 다음에, 각 Character에게 부옵이 전부 비어있는 Artifact를 준다.
        emptyFlower = ArtFlower()
        emptyFeather = ArtFeather()
        emptyClock = ArtClock()
        emptyClock.SetMainType(main3)
        emptyCup = ArtCup()
        emptyCup.SetMainType(main4)
        emptyCrown = ArtCrown()
        emptyCrown.SetMainType(main5)

        tempCharacter = deepcopy(self)
        tempCharacter.SetArtFlower(emptyFlower)
        tempCharacter.SetArtFeather(emptyFeather)
        tempCharacter.SetArtClock(emptyClock)
        tempCharacter.SetArtCup(emptyCup)
        tempCharacter.SetArtCrown(emptyCrown)
        
        tempSubStat = Stat()

        tempCharacter.Update()
        self.__mSavedFunction[0] = tempCharacter.GetDamage()

        for i in range(45): # for문으로 45회동안, 
            difEC = self.__mTargetEC - tempCharacter.GetStat().GetOption(4) # check the element charge is enough or not.
            whetherNotEnoughEC = difEC > 0

            if (i < 20):
                # If the element charge is not enouth, add element charge.
                if (whetherNotEnoughEC and (5 - mainOp[4] > numArray[4])):
                    tempSubStat.AddOption(4, PLUSARRAY[4])
                    numArray[4] += 1
                else: # If impossible,
                    # record how much damage will be if each option is added at damArray.
                    for j in range(10):
                        tempSubStatArray[j] = tempSubStat
                        tempSubStatArray[j].AddOption(j, PLUSARRAY[j])
                        tempCharacter.GetArtFlower().SetSubStat(tempSubStatArray[j])
                        tempCharacter.Update()
                        damArray[j] = tempCharacter.GetDamage()

                    # 가장 점수가 높은 스탯에 대해서 ((5 - 주옵여부) 보다 적게 채웠는가?)를 확인하고 채운다.
                        # If impossible,
                            # 다음 점수가 높은 스탯에 대해서 확인한다. (최대 5회 반복)
                    for j in range(1, 5):
                        largeStat = FindNthLargestOption(damArray, j)
                        if 5 - mainOp[largeStat] > numArray[largeStat]:
                            if (damArray[largeStat] == damArray[4]) and (5 - mainOp[4] > numArray[4]):
                                largeStat = 4
                            tempSubStat.AddOption(largeStat, PLUSARRAY[largeStat])
                            numArray[largeStat] += 1
                            break
            else:
                if whetherNotEnoughEC:
                    tempSubStat.AddOption(4, PLUSARRAY[4])
                    numArray[4] += 1
                else:
                    for j in range(10):
                        tempSubStatArray[j] = tempSubStat
                        tempSubStatArray[j].AddOption(j, PLUSARRAY[j])
                        tempCharacter.GetArtFlower().SetSubStat(tempSubStatArray[j])
                        tempCharacter.Update()
                        damArray[j] = tempCharacter.GetDamage()

                    for j in range(1, 3):
                        largeStat = FindNthLargestOption(damArray, j)
                        if 30 - mainOp[largeStat] != numArray[largeStat]:
                            tempSubStat.AddOption(largeStat, PLUSARRAY[largeStat])
                            numArray[largeStat] += 1
                            break

            tempCharacter.GetArtFlower().SetSubStat(tempSubStat)
            self.__mSavedFunction[i + 1] = tempCharacter.GetDamage()

    def _SetBasicCharacterStat(self):
        self.__mCharacterStat.SetZero()	
        self.__mCharacterStat.SetCriticalRate(5.)
        self.__mCharacterStat.SetCriticalBonus(50.)
        self.__mCharacterStat.SetElementCharge(100.)
        self.__mCharacterStat.SetLevel(90.)
        self.__mCharacterStat.SetMonsterLevel(100.)
        self.__mCharacterStat.SetMonsterResist(10.)

    def _SetCharacterStatEach(self, index: int, amount: float):
        self.__mCharacterStat.SetOption(index, amount)
        self.__mUpdateState = 0

    def _SetCharacterStat(self, stat: Stat):
        self.__mCharacterStat = stat
        self.__mUpdateState = 0

    def _AddCharacterStat(self, index: int, amount: float):
        self.__mCharacterStat.AddOption(index, amount)
        self.__mUpdateState = 0

    def _SetCharacterBaseStat(self, index: int, amount: float):
        self.__mCharacterStat.SetBaseOption(index, amount)

    # Stat Update & UpdateState
    def DoFeedback(self):
        pass

    def Update(self):
        # Process
            # CharacterStat + ResonanceStat
            # WeaponStat (Main + Sub + SubSub)
            # ArtSetStat
            # Artifact Main Stat
            # Artifact Sub Stat
            # Stat Update
            # Feedback
            # Stat Update Once Again

        if (self.__mUpdateState < self.__CHARACTERRESONANCEUPDATED):
            self.__UpdateFromCharacterResonance()
            self.__mUpdateState = self.__CHARACTERRESONANCEUPDATED
        if (self.__mUpdateState < self.__WEAPONSTATUPDATED):
            self.__UpdateFromWeapon()
            self.__mUpdateState = self.__WEAPONSTATUPDATED
        if (self.__mUpdateState < self.__ARTSETSTATUPDATED):
            self.__UpdateFromArtSetStat()
            self.__mUpdateState = self.__ARTSETSTATUPDATED
        if (self.__mUpdateState < self.__ARTIFACTMAINSTATUPDATED):
            self.__UpdateFromArtifactMainStat()
            self.__mUpdateState = self.__ARTIFACTMAINSTATUPDATED
        if (self.__mUpdateState < self.__ARTIFACTSUBSTATUPDATED):
            self.__UpdateFromArtifactSubStat()
            self.__mUpdateState = self.__ARTIFACTSUBSTATUPDATED
        self.__mStat = self.__mStatAfterUpdateFromArtifactSubStat
        self.__mStat.Update()
        self.__UpdateFromFeedback()
        self.__mStat.Update()

    def ConfirmResonanceStatModified(self):
        if self.__mUpdateState >= self.__CHARACTERRESONANCEUPDATED:
            self.__mUpdateState = self.__CHARACTERRESONANCEUPDATED - 1

    def ConfirmWeaponStatModified(self):
        if self.__mUpdateState >= self.__WEAPONSTATUPDATED:
            self.__mUpdateState = self.__WEAPONSTATUPDATED - 1

    def ConfirmArtSetStatModified(self):
        if self.__mUpdateState >= self.__ARTSETSTATUPDATED:
            self.__mUpdateState = self.__ARTSETSTATUPDATED - 1

    def ConfirmArtifactMainStatModified(self):
        if self.__mUpdateState >= self.__ARTIFACTMAINSTATUPDATED:
            self.__mUpdateState = self.__ARTIFACTMAINSTATUPDATED - 1

    def ConfirmArtifactSubStatModified(self):
        if self.__mUpdateState >= self.__ARTIFACTSUBSTATUPDATED:
            self.__mUpdateState = self.__ARTIFACTSUBSTATUPDATED - 1

    def GetUpdateState(self):
        return self.__mUpdateState

    # Set Manual Mode
    def SetManualMode(self, isManualMode: bool):
        self.__mIsManualMode = isManualMode

    def GetManualMode(self):
        return self.__mIsManualMode

    # Damage and EffectionArray
    def GetDamage(self):
        return self.GetDamageWithStat(self.__mStat)

    def GetDamageWithStat(self, stat: Stat):
        AP = stat.GetAttackPer()
        ATK = stat.GetAttack()
        BaseATK = stat.GetBaseAttack()
        CR = stat.GetCriticalRate()
        if CR > 100:
            CR = 100.
        elif CR < 0:
            CR = 0.
        CB = stat.GetCriticalBonus()

        return (BaseATK * (1 + AP / 100.) + ATK) * (1 + CR * CB / 10000.)

    # Score (algorithm by jangddol)
    def MakeEffectionArray(self):
        tempCharacter: Character
        tempArtSetStat: ArtSetStat      # 계산에 필요한 부옵 추가는 ResonanceStat으로 한다.
                                            # 이유는, 그냥 Stat이라서 접근이 편함.
                                            # Update가 오래걸리긴 하지만, 심각하진 않음.
                                        # 230131
                                            # ResonanceStat 에 대한 Update Optimization 과정에서
                                            # 깡옵과 치피가 사용되지 않는 것 때문에
                                            # 이 함수가 망가짐. 
                                            # 0 ~ 18 모두 사용되는 것을 사용해야한다.
                                            # ArtSetStat이 맞는 듯 하다.

        defaultDamage = self.GetDamage() # 현재 스펙을 기록한다.
        for i in range(19):
            tempCharacter = deepcopy(self)
            tempArtSetStat = self.CopyArtSetStat()
            tempArtSetStat.AddOption(i, 1.)
            tempCharacter.SetArtSetStat(tempArtSetStat)
            tempCharacter.Update()
            self.__mEffectionArray[i] = tempCharacter.GetDamage() - defaultDamage

    def MakeScoreFunction(self):
        optimizationResult = self.OptimizeMainOption()
        optimizedMainOption = optimizationResult[0].mainOptions
        self.__MakeScoreFunctionMainOptionFixed(optimizedMainOption[0], optimizedMainOption[1], optimizedMainOption[2])

    def GetScoreFunction(self, index: int):
        return self.__mSavedFunction[index]

    def GetScore(self):
        score = 0
        damage = self.GetDamage()

        # Return 0 if the saved function is equal to the damage
        if self.__mSavedFunction[0] == damage:
            return 0

        # Find the score by iterating through the saved function array
        for i in range(45):
            if self.__mSavedFunction[i] < damage and damage <= self.__mSavedFunction[i + 1]:
                score = i + (damage - self.__mSavedFunction[i]) / (self.__mSavedFunction[i + 1] - self.__mSavedFunction[i])
                break

        # Adjust the score based on the element charge
        elementChargeDifference = self.__mTargetEC - self.__mStat.GetElementCharge()
        if elementChargeDifference > 0:
            score -= elementChargeDifference / PLUSARRAY[4]

        return score

    def GetEffection(self, index: int):
        return self.__mEffectionArray[index]

    # Score (algorithm by MonkeyMagic)
    def GetScore_MonkeyMagic(self):
        return 0

    # Artifact MainOption Optimization
    def OptimizeMainOption(self):
        clockPossibleMain = ArtClock().GetPossibleMainOption()
        cupPossibleMain = ArtCup().GetPossibleMainOption()
        crownPossibleMain = ArtCrown().GetPossibleMainOption()

        tempChar = deepcopy(self)
        tempChar.GetArtFlower().SetSubStat(Stat())
        tempChar.GetArtFeather().SetSubStat(Stat())
        tempChar.GetArtClock().SetSubStat(Stat())
        tempChar.GetArtCup().SetSubStat(Stat())
        tempChar.GetArtCrown().SetSubStat(Stat())
        tempChar.Update()

        top10Options = [MainOptionsAndDamage(np.array([0, 0]), 0)] * 10

        for clockOpt in clockPossibleMain:
            for cupOpt in cupPossibleMain:
                for crownOpt in crownPossibleMain:
                    tempChar.__MakeScoreFunctionMainOptionFixed(clockOpt, cupOpt, crownOpt)
                    temp28Damage = tempChar.GetScoreFunction(28)

                    # tempDamage가 top10Option에 있는 minOption보다 클 경우
                    if (temp28Damage > top10Options[9].damage):
                        for i in range(10):# 몇번째로 들어가는 지 파악하고, 넣어준다.
                            if temp28Damage > top10Options[i].damage:
                                j = 8
                                while j > i:
                                    top10Options[j + 1] = top10Options[j]
                                    j -= 1
                                # push to backside if damage is less than temp28Damage
                                top10Options[i].mainOptions = np.array([ clockOpt, cupOpt, crownOpt ])
                                top10Options[i].damage = temp28Damage
                                break
        return top10Options

    # Stat
    def GetStat(self):
        return self.__mStat

    def SetStat(self, stat: Stat):
        self.__mStat = stat
        self.__mUpdateState = self.__ARTIFACTSUBSTATUPDATED

    # Character Stat
    def GetCharacterStat(self):
        return self.__mCharacterStat

    # Resonance Stat
    def GetResonanceStat(self):
        return self.__mResonanceStat

    def SetResonanceStat(self, stat: Stat):
        self.__mResonanceStat = stat
        self.ConfirmResonanceStatModified()

    # Weapon
    def GetWeapon(self):
        return self.__mWeapon

    def GetWeaponName(self):
        pass

    def CopyWeapon(self):
        pass

    def SetWeapon(self, weapon: Weapon):
        self.__mWeapon = weapon
        self.ConfirmWeaponStatModified()

    # ArtSetStat
    def GetArtSetStat(self):
        return self.__mArtSetStat

    def CopyArtSetStat(self):
        return deepcopy(self.__mArtSetStat)

    def SetArtSetStat(self, artSetStat: ArtSetStat):
        self.__mArtSetStat.DeleteCharacterPointer(self)
        self.__mArtSetStat = artSetStat
        self.__mArtSetStat.SaveCharacterPointer(self)
        self.ConfirmArtSetStatModified()

    # Artifact
    def SetArtifact(self, flower: ArtFlower , feather: ArtFeather, clock: ArtClock, cup: ArtCup, crown: ArtCrown):
        self.SetArtFlower(flower)
        self.SetArtFeather(feather)
        self.SetArtClock(clock)
        self.SetArtCup(cup)
        self.SetArtCrown(crown)

    def GetArtFlower(self):
        return self.__mArtFlower

    def CopyArtFlower(self): 
        return deepcopy(self.__mArtFlower)

    def SetArtFlower(self, artFlower: ArtFlower):
        self.ConfirmArtifactSubStatModified()
        if not self.__mIsManualMode:
            self.__mArtFlower.DeleteCharacterPointer(self)
            artFlower.SaveCharacterPointer(self)
        self.__mArtFlower = artFlower

    def GetArtFeather(self):
        return self.__mArtFeather

    def CopyArtFeather(self): 
        return deepcopy(self.__mArtFeather)

    def SetArtFeather(self, artFeather: ArtFeather):
        self.ConfirmArtifactSubStatModified()
        if not self.__mIsManualMode:
            self.__mArtFeather.DeleteCharacterPointer(self)
            artFeather.SaveCharacterPointer(self)
        self.__mArtFeather = artFeather

    def GetArtClock(self):
        return self.__mArtClock

    def CopyArtClock(self):
        return deepcopy(self.__mArtClock)

    def SetArtClock(self, artClock: ArtClock):
        self.ConfirmArtifactMainStatModified()
        if not self.__mIsManualMode:
            self.__mArtClock.DeleteCharacterPointer(self)
            artClock.SaveCharacterPointer(self)
        self.__mArtClock = artClock

    def GetArtCup(self):
        return self.__mArtCup

    def CopyArtCup(self):
        return deepcopy(self.__mArtCup)

    def SetArtCup(self, artCup: ArtCup):
        self.ConfirmArtifactMainStatModified()
        if not self.__mIsManualMode:
            self.__mArtCup.DeleteCharacterPointer(self)
            artCup.SaveCharacterPointer(self)
        self.__mArtCup = artCup

    def GetArtCrown(self):
        return self.__mArtCrown

    def CopyArtCrown(self):
        return deepcopy(self.__mArtCrown)

    def SetArtCrown(self, artCrown: ArtCrown):
        self.ConfirmArtifactMainStatModified()
        if not self.__mIsManualMode:
            self.__mArtCrown.DeleteCharacterPointer(self)
            artCrown.SaveCharacterPointer(self)
        self.__mArtCrown = artCrown

    # Feedbacked Stat
    def GetFeedbackedStat(self):
        return self.__mFeedbackedStat

    def SetFeedbackedStat(self, stat: Stat):
        self.__mFeedbackedStat = stat

    def AddFeedbackedStat(self, index: int, amount: float):
        self.__mFeedbackedStat.AddOption(index, amount)

    # TargetEC
    def GetTargetEC(self):
        return self.__mTargetEC
    
    def SetTargetEC(self, targetEC: float):
        self.__mTargetEC = targetEC

    def GetStatAfterUpdateFromCharacterResonance(self): 
        return self.__mStatAfterUpdateFromCharacterResonance
    def GetStatAfterUpdateFromWeapon(self): 
        return self.__mStatAfterUpdateFromWeapon
    def GetStatAfterUpdateFromArtSetStat(self): 
        return self.__mStatAfterUpdateFromArtSetStat
    def GetStatAfterUpdateFromArtifactMainStat(self): 
        return self.__mStatAfterUpdateFromArtifactMainStat
    def GetStatAfterUpdateFromArtifactSubStat(self): 
        return self.__mStatAfterUpdateFromArtifactSubStat


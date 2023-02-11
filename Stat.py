import numpy as np

BASESTATSTRING = ["Base ATK", "Base HP", "Base DEF"]
STATSTRING = ["CR", "CB", "ATK%%", "ATK", "EC", 
		"HP%%", "HP", "EM", "DEF%%", "DEF",
		"Pyro", "Elec", "Cryo", "Hydro", "Anymo",
		"Geo", "Phys", "Dendro", "Heal", "Normal Attack Bonus", 
		"Strong Attack Bonus", "Dodge Attack Bonus", "E Skill Bonus", "Q Skill Bonus", "Total ATK",
		"Total HP", "Total DEF", "Resist Cut", "DEF Cut", "Monster Resist",
		"Resist Coef", "DEF Coef", "Lv", "Monster Lv", "Lv Coef"]

class Stat:
    __mStat = np.zeros(35)
    __mBaseStat = np.zeros(3)
    
    def SetZero(self):
        self.__mStat = np.zeros(35)
        self.__mBaseStat = np.zeros(3)

    
    def SetOption(self, index, amount):
        self.__mStat[index] = amount
	
    def AddOption(self, index, amount):
        self.__mStat[index] += amount
	
    def GetOption(self, index):
        return self.__mStat[index]

	
    def SetCriticalRate(self, CR):
        self.__mStat[0] = CR
	
    def GetCriticalRate(self):
        return self.__mStat[0]
	
    def SetCriticalBonus(self, CB):
        self.__mStat[1] = CB
	
    def GetCriticalBonus(self):
        return self.__mStat[1]
	
    def SetAttackPer(self, AP):
        self.__mStat[2] = AP
	
    def GetAttackPer(self):
        return self.__mStat[2]
	
    def SetAttack(self, attack):
        self.__mStat[3] = attack
	
    def GetAttack(self):
        return self.__mStat[3]
	
    def SetElementCharge(self, EC):
        self.__mStat[4] = EC
	
    def GetElementCharge(self):
        return self.__mStat[4]
	
    def SetHPPer(self, HPP):
        self.__mStat[5] = HPP
	
    def GetHPPer(self):
        return self.__mStat[5]
	
    def SetHP(self, HP):
        self.__mStat[6] = HP
	
    def GetHP(self):
        return self.__mStat[6]
	
    def SetElementalMastery(self, EM):
        self.__mStat[7] = EM
	
    def GetElementalMastery(self):
        return self.__mStat[7]
	
    def SetDefensePer(self, DP):
        self.__mStat[8] = DP
	
    def GetDefensePer(self):
        return self.__mStat[8]
	
    def SetDefense(self, defense):
        self.__mStat[9] = defense
	
    def GetDefense(self):
        return self.__mStat[9]
	
    def SetPiroBonus(self, piroBonus):
        self.__mStat[10] = piroBonus
	
    def GetPiroBonus(self):
        return self.__mStat[10]
	
    def SetElectroBonus(self, electroBonus):
        self.__mStat[11] = electroBonus
	
    def GetElectroBonus(self):
        return self.__mStat[11]
	
    def SetCryoBonus(self, cryoBonus):
        self.__mStat[12] = cryoBonus
	
    def GetCryoBonus(self):
        return self.__mStat[12]
	
    def SetHydroBonus(self, hydroBonus):
        self.__mStat[13] = hydroBonus
	
    def GetHydroBonus(self):
        return self.__mStat[13]
	
    def SetAnemoBonus(self, anemoBonus):
        self.__mStat[14] = anemoBonus
	
    def GetAnemoBonus(self):
        return self.__mStat[14]
	
    def SetGeoBonus(self, geoBonus):
        self.__mStat[15] = geoBonus
	
    def GetGeoBonus(self):
        return self.__mStat[15]
	
    def SetPhysicalBonus(self, physicalBonus):
        self.__mStat[16] = physicalBonus
	
    def GetPhysicalBonus(self):
        return self.__mStat[16]
	
    def SetDendroBonus(self, dendroBonus):
        self.__mStat[17] = dendroBonus
	
    def GetDendroBonus(self):
        return self.__mStat[17]
	
    def SetHealBonus(self, healBonus):
        self.__mStat[18] = healBonus
	
    def GetHealBonus(self):
        return self.__mStat[18]
	
    def SetNormalAttackBonus(self, normalAttackBonus):
        self.__mStat[19] = normalAttackBonus
	
    def GetNormalAttackBonus(self):
        return self.__mStat[19]
	
    def SetStrongAttackBonus(self, strongAttackBonus):
        self.__mStat[20] = strongAttackBonus
	
    def GetStrongAttackBonus(self):
        return self.__mStat[20]
	
    def SetFlungeAttackBonus(self, flungeAttackBonus):
        self.__mStat[21] = flungeAttackBonus
	
    def GetFlungeAttackBonus(self):
        return self.__mStat[21]
	
    def SetEBonus(self,  eBonus):
        self.__mStat[22] = eBonus
	
    def GetEBonus(self):
        return self.__mStat[22]
	
    def SetQBonus(self,  qBonus):
        self.__mStat[23] = qBonus
	
    def GetQBonus(self):
        return self.__mStat[23]
	
    def GetTotalAttack(self):
        return self.__mStat[24]
	
    def GetTotalHP(self):
        return self.__mStat[25]
	
    def GetTotalDefense(self):
        return self.__mStat[26]
	
    def SetResistCut(self, resistCut):
        self.__mStat[27] = resistCut
	
    def GetResistCut(self):
        return self.__mStat[27]
	
    def SetDefenseCut(self, defenseCut):
        self.__mStat[28] = defenseCut
	
    def GetDefenseCut(self):
        return self.__mStat[28]
	
    def SetMonsterResist(self, monsterResist):
        self.__mStat[29] = monsterResist
	
    def GetMonsterResist(self):
        return self.__mStat[29]
	
    def GetResistCoef(self):
        return self.__mStat[30]
	
    def GetDefenseCoef(self):
        return self.__mStat[31]
	
    def SetLevel(self, level):
        self.__mStat[32] = level
	
    def GetLevel(self):
        return self.__mStat[32]
	
    def SetMonsterLevel(self, monsterLevel):
        self.__mStat[33] = monsterLevel
	
    def GetMonsterLevel(self):
        return self.__mStat[33]
	
    def GetLevelCoef(self):
        return self.__mStat[34]

	
    def GetBaseOption(self, index):
        return self.__mBaseStat[index]
	
    def SetBaseOption(self, index, amount):
        self.__mBaseStat[index] = amount
	
    def GetBaseAttack(self):
        return self.__mBaseStat[0]
	
    def SetBaseAttack(self, baseATK):
        self.__mBaseStat[0] = baseATK
	
    def GetBaseHP(self):
        return self.__mBaseStat[1]
	
    def SetBaseHP(self, baseHP):
        self.__mBaseStat[1] = baseHP
	
    def GetBaseDefense(self):
        return self.__mBaseStat[2]
	
    def SetBaseDefense(self, baseDEF):
        self.__mBaseStat[2] = baseDEF


    def CalTotalAttack(self):
        self.__mStat[24] = self.__mBaseStat[0] * (1. + self.__mStat[2] / 100.) + self.__mStat[3]
	
    def CalTotalHP(self):
        self.__mStat[25] = self.__mBaseStat[1] * (1. + self.__mStat[5] / 100.) + self.__mStat[6]
	
    def CalTotalDefense(self):
        self.__mStat[26] = self.__mBaseStat[2] * (1. + self.__mStat[8] / 100.) + self.__mStat[9]

    def CalResistCoef(self):
        monsterResist = self.GetMonsterResist()
        resistCut = self.GetResistCut()
        result = 0
        if (monsterResist - resistCut > 75):
            result = 1. / ((monsterResist - resistCut) / 25. + 1.)
        elif (monsterResist - resistCut < 0):
            result = 1. - (monsterResist - resistCut) / 200.
        else:
            result = 1. - (monsterResist - resistCut) / 100.
        self.__mStat[30] = result

    def CalDefenseCoef(self):
        charLv = self.GetLevel()
        monsterLv = self.GetMonsterLevel()
        defenseCut = self.GetDefenseCut()
        self.__mStat[31] = (charLv + monsterLv + 200) / ((charLv + 100) + (monsterLv + 100) * (1 - defenseCut / 100))

    def CalLevelCoef(self):
        charLv = self.GetLevel()
        monsterLv = self.GetMonsterLevel()
        self.__mStat[34] = (charLv + 100) / (charLv + monsterLv + 200)

    def Update(self):
        self.CalTotalAttack()
        self.CalTotalHP()
        self.CalTotalDefense()
        self.CalResistCoef()
        self.CalDefenseCoef()
        self.CalLevelCoef()

    
    
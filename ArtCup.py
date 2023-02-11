from Artifact import Artifact


class ArtCup(Artifact):
    def __init__(self):
        super().__init__()
        self._mType = 4
        self._mProbabilityWeight = [ 0, 0, 23,  0,  0, 23,  0,  3, 23,  0,  6,  6,  6,  6,   6,   6,   6,   6,   0 ]
        self._mCummulatedWeight  = [ 0, 0, 23, 23, 23, 46, 46, 49, 72, 72, 78, 84, 90, 96, 102, 108, 114, 120, 120 ]
    
    def GetPossibleMainOption(self):
        return [2, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17]
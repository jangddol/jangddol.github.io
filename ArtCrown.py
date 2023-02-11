from Artifact import Artifact


class ArtCrown(Artifact):
    def __init__(self):
        super().__init__()
        self._mType = 5
        self._mProbabilityWeight = [ 5,  5, 11,  0,  0, 11,  0,  2, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5 ]
        self._mCummulatedWeight  = [ 5, 10, 21, 21, 21, 32, 32, 34, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 50 ]
    
    def GetPossibleMainOption(self):
        return [0, 1, 2, 5, 7, 8, 18]
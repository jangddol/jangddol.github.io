import Artifact


class ArtClock(Artifact):
    def __init__(self):
        super().__init__(self)
        self._mType = 3
        self._mProbabilityWeight = [ 0, 0, 8, 0,  3,  8,  0,  3,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ]
        self._mCummulatedWeight  = [ 0, 0, 8, 8, 11, 19, 19, 22, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30 ]
        
    def GetPossibleMainOption():
        return [2, 4, 5, 7, 8]
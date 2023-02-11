import Artifact


class ArtFlower(Artifact):
    def __init__(self):
        super().__init__(self)
        self._mType = 1
        self._mProbabilityWeight = [ 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        self._mCummulatedWeight = [ 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
        self.SetMainType(6)
    
    def GetPossibleMainOption():
        return [6]
from Artifact import Artifact


class ArtFeather(Artifact):
    def __init__(self):
        super().__init__()
        self._mType = 2
        self._mProbabilityWeight = [ 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        self._mCummulatedWeight = [ 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
        self.SetMainType(3)

    def GetPossibleMainOption(self):
        return [3]
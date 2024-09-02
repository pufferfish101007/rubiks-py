from Cubelet import Cubelet, NaiveCubelet
from constants import AXES

class BaseSolver:
    def __init__(self, cubelets, cubelet=Cubelet):
        self.cubelets = { cubelet(*[c.sides[:], c.pos[:], self][:(3 if cubelet == NaiveCubelet else 2)]) for c in cubelets }
        self.moves = []
    def __getState(self, side):
        return [
            self.findCubelets((side, AXES[side][0], AXES[side][3]), mode="pos")[0].getColourOnFace(side),
            self.findCubelets((side, AXES[side][0]), mode="pos")[0].getColourOnFace(side),
            self.findCubelets((side, AXES[side][1], AXES[side][0]), mode="pos")[0].getColourOnFace(side),
            self.findCubelets((side, AXES[side][3]), mode="pos")[0].getColourOnFace(side),
            side,
            self.findCubelets((side, AXES[side][1]), mode="pos")[0].getColourOnFace(side),
            self.findCubelets((side, AXES[side][3], AXES[side][2]), mode="pos")[0].getColourOnFace(side),
            self.findCubelets((side, AXES[side][2]), mode="pos")[0].getColourOnFace(side),
            self.findCubelets((side, AXES[side][2], AXES[side][1]), mode="pos")[0].getColourOnFace(side)
        ]
    def solved(self):
        return all(map(lambda c: c.sides == c.pos, cubelets))
    def findCubelets(self, sides, mode="sides", cond=lambda x: True, exact=False):
        f = [cubelet for cubelet in self.cubelets if (((frozenset(cubelet.sides if mode == "sides" else cubelet.pos) & frozenset(sides)) == frozenset(sides)) if not exact else frozenset(cubelet.sides if mode == "sides" else cubelet.pos) == frozenset(sides)) and cond(cubelet)]
        return f
    def move(self, side, dir, recordState=True):
        self.moves.append([side, dir % 4, self.__getState(side)][:(2 + recordState)])
        for cubelet in self.cubelets:
            cubelet.move(side, dir)
    def solve(self):
        raise NotImplementedError("solve must be implemented by subclass")
    def reduceMoves(self):
        i = 0
        j = 1
        while i < len(self.moves):
            if j < len(self.moves):
                while self.moves[j][0] == self.moves[i][0]:
                    self.moves[i][1] += self.moves.pop(j)[1]
            self.moves[i][1] %= 4
            if self.moves[i][1] == 0:
                self.moves.pop(i)
            else:
                i += 1
                j += 1

from constants import AXES

class Cubelet:
    def __init__(self, sides, pos):
        self.sides = list(sides)
        self.pos = list(pos)
        self.type = len(self.pos)
    def isCorrect(self):
        if self.sides == self.pos:
             return 2
        if frozenset(self.sides) == frozenset(self.pos):
            return 1
        return 0
    def move(self, axis, dir):
        if axis in self.pos:
            index = self.pos.index(axis)
            for i, facelet in enumerate(self.pos):
                if facelet == axis:
                    continue
                newIndex = AXES[axis].index(facelet) + dir
                newIndex = (newIndex - (0 if newIndex < 0 else 0)) % 4
                self.pos[i] = AXES[axis][newIndex]
    def __str__(self):
        return str((self.sides, self.pos))
    def getColourOnFace(self, face):
        if face in self.pos:
            return self.sides[self.pos.index(face)]
        else:
            return None

class NaiveCubelet(Cubelet):
    def __init__(self, sides, pos, cube):
        super().__init__(sides, pos)
        self.cube = cube
    def isCorrect(self):
        if self.sides == self.pos:
             return 2
        if frozenset(self.sides) == frozenset(self.pos):
            return 1
        return 0
    def move(self, axis, dir):
        if axis in self.pos:
            index = self.pos.index(axis)
            for i, facelet in enumerate(self.pos):
                if facelet == axis:
                    continue
                newIndex = AXES[axis].index(facelet) + dir
                newIndex = (newIndex - (0 if newIndex < 0 else 0)) % 4
                self.pos[i] = AXES[axis][newIndex]
    def __str__(self):
        return str((self.sides, self.pos))
    def getColourOnFace(self, face):
        if face in self.pos:
            return self.sides[self.pos.index(face)]
        else:
            return None
    def solve(self):
        if self.sides == self.pos:
            return
        cube = self.cube
        match self.sides, self.pos:
            case (0, _, a), (5, *_):
                while self.pos[1] != a:
                    cube.move(5, 1)
                cube.move(a, 1)
                cube.move(5, 2)
                cube.move(AXES[0][AXES[0].index(self.pos[1]) -2], -1)
                cube.move(5, -1)
                self.solve()
            case (0, a), (5, _):
                while self.pos[1] != a:
                    cube.move(5, 1)
                cube.move(a, 2)
            case (0, a), (_, 5):
                while self.pos[0] != a:
                    cube.move(5, 1)
                cube.move(5, 1)
                p = self.pos[0]
                cube.move(p, 1)
                cube.move(self.pos[1], -1)
                cube.move(p, -1)
            case (0, a, b), (1 | 2 | 3 | 4, x, y) if 5 in (x, y):
                while not (a == self.pos[1] or b == self.pos[2]):
                    cube.move(5, 1)
                cube.move(self.pos[0], 1 if self.pos[2] == 5 else -1)
                cube.move(5, -1 if self.pos[2] == 5 else 1)
                cube.move(self.pos[1 if self.pos[2] == 5 else 2], 1 if self.pos[2] == 5 else -1)
            case (0, a), (1 | 2 | 3 | 4, 1 | 2 | 3 | 4):
                topmove = (self.pos[1]-a)%4
                cube.move(0, topmove)
                cube.move(self.pos[1], self.pos[0] - self.pos[1])
                cube.move(0, -topmove)
            case (0, _), ((a, 0) | (0, a)):
                cube.move(a, 2)
                self.solve()
            case (0, _, _), (0, *_):
                cube.move(self.pos[2], 1)
                cube.move(5, -1)
                cube.move(self.pos[0], -1)
                self.solve()
            case (0, a, b), (1 | 2 | 3 | 4, x, y) if 0 in (x, y):
                # TODO: make this cleaner
                if self.pos[2] == 0:
                    cube.move(self.pos[0], -1)
                    cube.move(5, 1)
                    cube.move(self.pos[2],  1)
                else:
                    cube.move(self.pos[2], -1)
                    cube.move(5, 1)
                    cube.move(self.pos[1],  1)
                self.solve()
            case (1 | 2 | 3 | 4 as x, 1 | 2 | 3 | 4 as y), (a, b) as c if 5 in c:
                if a == 5:
                    while self.pos[1] != y:
                        cube.move(5, 1)
                    cube.move(5, -1)
                    cube.move(x, -1)
                    cube.move(5,  1)
                    cube.move(x,  1)
                    cube.move(5,  1)
                    cube.move(y,  1)
                    cube.move(5, -1)
                    cube.move(y, -1)
                else:
                    while self.pos[0] != x:
                        cube.move(5, 1)
                    cube.move(5,  1)
                    cube.move(y,  1)
                    cube.move(5, -1)
                    cube.move(y, -1)
                    cube.move(5, -1)
                    cube.move(x, -1)
                    cube.move(5,  1)
                    cube.move(x,  1)

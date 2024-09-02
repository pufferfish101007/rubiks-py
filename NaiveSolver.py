from BaseSolver import BaseSolver
from constants import mod4not0
from Cubelet import NaiveCubelet

class NaiveSolver(BaseSolver):
    def __init__(self, cubelets):
        super().__init__(cubelets, cubelet=NaiveCubelet)
    def solve(self):
        for c in self.findCubelets([0], cond=lambda c: c.type == 2):
                c.solve()
       # print(len(self.moves))
        for c in self.findCubelets([0], cond=lambda c: c.type == 3):
                c.solve()
       # print(len(self.moves))
        while any(self.findCubelets([], cond=lambda c: c.type == 2 and set(c.sides) < { 1, 2, 3, 4 } and 5 in c.pos)):
            for c in self.findCubelets([], cond=lambda c: c.type == 2 and set(c.sides) < { 1, 2, 3, 4 } and 5 in c.pos):
                c.solve()
       # print(len(self.moves))
        for c in self.findCubelets([], cond=lambda c: c.type == 2 and set(c.sides) < { 1, 2, 3, 4 }):
            if c.sides == c.pos:
                continue
            if 5 not in c.pos: # it might have already been moved
                x, y = c.pos
                NaiveCubelet((x, y) if (x-y)%4 == 3 else (y, x), (x, 5) if (x-y)%4 == 3 else (5, x), self).solve()
            c.solve()
        #print(len(self.moves))
        yellowsSides = []
        while len(yellowsSides) != 4:
            yellows = self.findCubelets([5], mode="pos", cond=lambda c: c.type == 2 and c.pos[1] == 5)
            yellowsSides = list(map(lambda y: y.pos[0], yellows))
            if len(yellowsSides) == 2:
                if sum(yellowsSides) % 2 == 0: # cubelets are opposite
                    self.move(1, -1)
                    self.move(4, -1)
                    self.move(5, -1)
                    self.move(4, 1)
                    self.move(5, 1)
                    self.move(1, 1)
                else: # cubelets are at a right angle
                    yellowsSides = list(map(lambda s: s % 4, yellowsSides))
                    yellowsSides.sort()
                    frontSide = (yellowsSides[0] - 1) % 4
                    if frontSide in yellowsSides:
                        frontSide += 3
                    frontSide = mod4not0(frontSide)
                    self.move(frontSide, -1)
                    self.move(5, -1)
                    self.move((frontSide - 1) or 4, -1)
                    self.move(5, 1)
                    self.move((frontSide - 1) or 4, 1)
                    self.move(frontSide, 1)
                    break
            elif len(yellowsSides) == 0:
                self.move(1, -1)
                self.move(4, -1)
                self.move(5, -1)
                self.move(4, 1)
                self.move(5, 1)
                self.move(1, 1)
        #print(len(self.moves))
        yellowEdges = self.findCubelets([5], cond=lambda c: c.type == 2)
        incorrectYellowEdges = list(sorted([yellowEdge.pos[0] for yellowEdge in yellowEdges if yellowEdge.pos[0] != yellowEdge.sides[0]], reverse=True))
        while (incorrectNum := len(incorrectYellowEdges)) > 0:
            if incorrectNum == 4:
                self.move(1, -1)
                self.move(5, -1)
                self.move(1, 1)
                self.move(5, -1)
                self.move(1, -1)
                self.move(5, 2)
                self.move(1, 1)
            elif incorrectNum == 3:
                sideToMove = incorrectYellowEdges[0]
                if incorrectYellowEdges[0] == 4 and sideToMove == 1:
                    if incorrectYellowEdges[1] == 2:
                        sideToMove = 4
                    else:
                        sideToMove = 3
                self.move(sideToMove, -1)
                self.move(5, -1)
                self.move(sideToMove, 1)
                self.move(5, -1)
                self.move(sideToMove, -1)
                self.move(5, 2)
                self.move(sideToMove, 1)
            elif incorrectNum == 2:
                if sum(incorrectYellowEdges) % 2 == 0:
                    self.swapYellowEdges(incorrectYellowEdges[0] + 1, 1)
                    self.swapYellowEdges(mod4not0(incorrectYellowEdges[0] + 3), 1)
                else:
                    sideToMove = incorrectYellowEdges[0]
                    if incorrectYellowEdges[1] == 4:
                        sideToMove = 4
                    self.move(sideToMove, -1)
                    self.move(5, -1)
                    self.move(sideToMove, 1)
                    self.move(5, -1)
                    self.move(sideToMove, -1)
                    self.move(5, 2)
                    self.move(sideToMove, 1)
                    self.move(5, -1)
            else:
                print("This thing is broken")
                break
            yellowEdges = self.findCubelets([5], cond=lambda c: c.type == 2)
            incorrectYellowEdges = list(sorted([yellowEdge.pos[0] for yellowEdge in yellowEdges if yellowEdge.pos[0] != yellowEdge.sides[0]], reverse=True))
        #print(len(self.moves))
        yellowCorners = self.findCubelets([5], cond=lambda c: c.type == 3)
        incorrectYellowCorners = [list(filter(lambda s: s != 5, yellowCorner.pos)) for yellowCorner in yellowCorners if frozenset(yellowCorner.pos) != frozenset(yellowCorner.sides)]
        while (incorrectNum := len(incorrectYellowCorners)) > 0:
            if incorrectNum == 4:
                self.move(1, -1)
                self.move(5, 1)
                self.move(3, 1)
                self.move(5, -1)
                self.move(1, 1)
                self.move(5, 1)
                self.move(3, -1)
                self.move(5, -1)
            elif incorrectNum == 3:
                correctSide = next(iter(filter(lambda c: frozenset(c.pos) == frozenset(c.sides), yellowCorners)))
                rightSide = min(correctSide.pos)
                if rightSide == 1 and 4 in correctSide.pos:
                    rightSide = 4
                rightSide -= 1
                rightSide = mod4not0(rightSide)
                leftSide = mod4not0(rightSide + 2)
                self.move(rightSide, -1)
                self.move(5, 1)
                self.move(leftSide, 1)
                self.move(5, -1)
                self.move(rightSide, 1)
                self.move(5, 1)
                self.move(leftSide, -1)
                self.move(5, -1)
            yellowCorners = self.findCubelets([5], cond=lambda c: c.type == 3)
            incorrectYellowCorners = [list(filter(lambda s: s != 5, yellowCorner.pos)) for yellowCorner in yellowCorners if frozenset(yellowCorner.pos) != frozenset(yellowCorner.sides)]
        #print(len(self.moves))
        yellowCorners = self.findCubelets([5], cond=lambda c: c.type == 3)
        incorrectYellowCorners = [yellowCorner for yellowCorner in yellowCorners if yellowCorner.pos != yellowCorner.sides]
        yellowRots = 0;
        for corner in incorrectYellowCorners:
            while not { 1, 2 } < frozenset(corner.pos):
                self.move(5, 1)
                yellowRots += 1
            while corner.pos.index(5) != corner.sides.index(5):
                for x in (0,0):
                    self.move(1, 1)
                    self.move(0, 1)
                    self.move(1, -1)
                    self.move(0, -1)
        #print(len(self.moves))
        self.move(5, -yellowRots % 4)
        #print(len(self.moves))
        self.reduceMoves()
    def swapYellowEdges(self, frontSide, sideSideDir):
        sideSide = mod4not0(frontSide + sideSideDir)
        self.move(sideSide, -sideSideDir)
        self.move(5, -sideSideDir)
        self.move(sideSide, sideSideDir)
        self.move(5, -sideSideDir)
        self.move(sideSide, -sideSideDir)
        self.move(5, 2)
        self.move(sideSide, sideSideDir)
        self.move(5, -sideSideDir)
   

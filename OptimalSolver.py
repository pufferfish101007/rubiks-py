from BaseSolver import BaseSolver
from Cubelet import Cubelet

class OptimalSolver(BaseSolver):
    def __init__(self, cubelets):
        super().__init__(cubelets, cubelet=Cubelet)
        self.originalCubelets = self.cubelets.copy()
    def isG1(self):
        return all(map(lambda c: frozenset(c.sides) < { 1, 2, 3, 4 } > frozenset(c.pos) or (len({ 0, 5 } & set(c.sides)) and c.pos[c.sides.index((5 in c.sides) * 5)] in (0, 5)), self.cubelets))
##    def tryMoveToG1(self, moves, nextMove, minMoves, maxMoves):
##        self.restoreState()
##        print(len(moves), nextMove)
##        for move in moves:
##            self.move(*move, recordState=False)
##        if self.isG1():
##            print("is G1")
##            if len(moves) >= minMoves:
##                return 1
##            else:
##                return 2
##        if len(moves) < maxMoves:
##            self.move(*nextMove, recordState=False)
##            self.nextMovesToG1(self.moves, nextMove, minMoves, maxMoves)
    def nextMovesToG1(self, moves, lastMove, minMoves, maxMoves):
        for i in range(6):
            for j in range(1, 4):
                if lastMove[0] == i:
                    continue
                self.restoreState()
                print(len(moves), (i, j))
                for move in moves:
                    self.move(*move, recordState=False)
                if self.isG1():
                    print("is G1")
                    if len(moves) >= minMoves:
                        return 1
                    else:
                        return 2
                if len(moves) < maxMoves:
                    self.move(i, j, recordState=False)
                    self.nextMovesToG1(self.moves, (i, j), minMoves, maxMoves)
    def restoreState(self):
        self.cubelets = self.originalCubelets.copy()
        self.moves = []
    def solve(self):
        for i in range(1, 21):
            self.nextMovesToG1([], (None,) * 2, 0, i)
        self.reduceMoves()

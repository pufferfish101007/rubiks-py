from random import randint, choice
from tkinter import Tk, Button, Label, Frame, mainloop, messagebox
from time import sleep
from copy import deepcopy
from webbrowser import open as openInBrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from re import sub
from NaiveSolver import NaiveSolver
from OptimalSolver import OptimalSolver
from Cubelet import Cubelet
from constants import AXES, COLOURS

if __name__ != "__main__":
    print("Cannot run in this interpreter. Make sure you're running the python file directly or in the IDLE.")
    sleep(5)
    quit()

hostName = "localhost"
serverPort = 8080
head = """
<!doctype html>
<html>
<head>
<title>Rubiks Cube</title>
<script src="https://unpkg.com/vue@next"></script>
"""
nl = "\n"
with open("./display.js") as jsFile:
    head += f"<script>{''.join(jsFile.readlines())}</script>"
with open("./style.css") as cssFile:
    head += f"<style>{''.join(cssFile.readlines())}</style>"
head += "</head><body></body></html>"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"{head}", "utf-8"))
     
webServer = HTTPServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))

serverThread = Thread(target=webServer.serve_forever, daemon=True)
serverThread.start()

print("yo")

class CCube:
    def moveSide(*_):
        pass

class MoveButton(Button):
    def __init__(self, side, cube, **kwargs):
        super().__init__(width=1, bg=COLOURS[side], command=self.click, **kwargs)
        self.side = side
        self.cube = cube
    def click(self):
        self.cube.move(self.side, 1)
        self.cube.redisplay()

gridInfo = {
    (0,1,2): (2,  3),
    (0,  1): (1,  3),
    (0,2,3): (2,  5),
    (0,  2): (2,  4),
    (0,3,4): (0,  5),
    (0,  3): (1,  5),
    (0,4,1): (0,  3),
    (0,  4): (0,  4),
    (1,  4): (4,  0),
    (3,  5): (5,  7),
    (4,  5): (5, 10),
    (3,4,5): (5,  8),
    (5,  4): (8,  4),
    (3,  0): (3,  7),
    (4,  1): (4, 11),
    (1,4,5): (5,  0),
    (2,3,0): (3,  5),
    (3,0,2): (3,  6),
    (1,2,0): (3,  2),
    (1,  0): (3,  1),
    (2,  0): (3,  4),
    (4,1,0): (3, 11),
    (1,0,4): (3,  0),
    (4,5,1): (5, 11),
    (3,4,0): (3,  8),
    (4,0,3): (3,  9),
    (4,  0): (3, 10),
    (1,5,2): (5,  2),
    (5,1,4): (8,  3),
    (2,0,1): (3,  3),
    (5,2,1): (6,  3),
    (2,1,5): (5,  3),
    (2,  3): (4,  5),
    (3,  2): (4,  6),
    (1,  2): (4,  2),
    (2,  1): (4,  3),
    (2,5,3): (5,  5),
    (5,3,2): (6,  5),
    (3,2,5): (5,  6),
    (3,  4): (4,  8),
    (4,  3): (4,  9),
    (1,  5): (5,  1),
    (5,  1): (7,  3),
    (2,  5): (5,  4),
    (5,  2): (6,  4),
    (3,5,4): (5,  8),
    (5,4,3): (8,  5),
    (4,3,5): (5,  9),
    (5,  3): (7,  5)
}

btnPos = (
    {"row": 1, "column": 4},
    {"row": 4, "column": 1},
    {"row": 4, "column": 4},
    {"row": 4, "column": 7},
    {"row": 4, "column": 10},
    {"row": 7, "column": 4}
)


class Cube:
    def __init__(self):
        self.cubelets = set()
        self.moves = []
        for i in range(6):
            for j in range(4):
                sides = [i, AXES[i][j]]
                if sides == [1 ,4]:
                    sides.reverse()
                side = Cubelet(sides, sides)
                if not any(map(lambda c: frozenset(c.sides) == frozenset(side.sides), self.cubelets)):
                    self.cubelets.add(side)
                corners = [i, AXES[i][j], AXES[i][(j + 1) % 4]]
                corner = Cubelet(corners, corners)
                if not any(map(lambda c: frozenset(c.sides) == frozenset(corner.sides), self.cubelets)):
                    self.cubelets.add(corner)
        self.root = Tk()
        self.root.title("Rubiks Cube")
        self.frame2 = Frame(bg="#110011")
        self.frame = Frame(master=self.frame2, bg="#110011")
        self.labels = []
        self.labelsPos = []
        for cubelet in self.cubelets:
            pos = cubelet.pos
            for i in range(len(pos)):
                pl = len(pos)
                if pl == 2:
                    self.labelsPos.append((pos[i], pos[(i + 1) % 2]))
                else:
                    self.labelsPos.append((pos[i], pos[(i + 1) % 3], pos[(i + 2) % 3]))
                label = Label(width=2, bg=COLOURS[pos[i]], master=self.frame)
                self.labels.append(label)
                label.grid(row=gridInfo[tuple(self.labelsPos[-1])][0], column=gridInfo[tuple(self.labelsPos[-1])][1])
        for i in range(6):
            btn = MoveButton(i, self, master=self.frame)
            btn.grid(**btnPos[i])
        self.frame.grid(row=0, column=0)
        Button(text="scramble", command=self.scramble, master=self.frame2).grid(row=1, column=0)
        Button(text="solve naively", command=self.solveNaively, master=self.frame2).grid(row=2, column=0)
        Button(text="solve optimally", command=self.solveOptimally, master=self.frame2).grid(row=3, column=0)
        Button(text="show moves", command=self.showMoves, master=self.frame2).grid(row=4, column=0)
        self.frame2.grid(row=0, column=0)
        mainloop()
    def showMoves(self):
        global head
        if len(self.moves):
            print(len(self.moves))
            head = sub(r"/\*moves here\*/\[.*?\]/\*moves here\*/", f"/*moves here*/{str(self.moves)}/*moves here*/", head)
        openInBrowser("http://localhost:8080", new=2)
    def move(self, side, dir):
        for cubelet in self.cubelets:
            cubelet.move(side, dir)
    def redisplay(self):
        for i, lbl in enumerate(self.labels):
            cubelet = tuple(filter(lambda f: frozenset(f.pos) == frozenset(self.labelsPos[i]), self.cubelets))[0]
            lbl["bg"] = COLOURS[cubelet.sides[cubelet.pos.index(self.labelsPos[i][0])]]
    def scramble(self, length=40):
        for i in range(length):
            self.move(randint(0, 5), choice([1, -1]))
        self.redisplay()
    def copy(self):
        cube = Cube()
        for c in cube.cubelets:
            c.pos = self.findCubelets(c.sides)[0].pos[:]
        return cube
    def solve(self, solver):
        solver = solver(self.cubelets)
        solver.solve()
        self.moves = solver.moves[:]
        for move in self.moves:
            self.move(*move[:2])
        self.redisplay()
    def solveNaively(self):
        self.solve(NaiveSolver)
    def solveOptimally(self):
        self.solve(OptimalSolver)

cube = Cube()

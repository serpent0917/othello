# 盤面の大きさ
BOARD_SIZE = 8

# マスの状態
EMPTY = 0
BLACK = 1
WHITE = -1

# 方向
DIRECTION = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

class Othello:
    def __init__(self):
        self.grid = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE

        self.player = BLACK
        self.count = [-1, 2, 2]  # [-1(使用しない), 黒の石の数, 白の石の数]

    def inside(self, x, y):
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE
    
    def empty(self, x, y):
        return self.grid[x][y] == EMPTY
    
    def check(self, x, y):
        flippable = []

        for dx, dy in DIRECTION:
            tmp = []
            depth = 1

            while True:
                nx = x + dx * depth
                ny = y + dy * depth

                if (not self.inside(nx, ny)) or self.empty(nx, ny):
                    break
                
                if self.grid[nx][ny] == self.player:
                    flippable.extend(tmp)
                    break
                else:
                    tmp.append([nx, ny])

                depth += 1
        
        return flippable
    
    def possible_discs(self):
        possible = []

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if (not self.empty(x, y)) or self.check(x, y) == []:
                    continue
                else:
                    possible.append([x, y])
        
        return possible

    def put(self, x, y):
        if (not self.inside(x, y)) or (not self.empty(x, y)):
            return False
        
        flippable = self.check(x, y)
        if flippable == []:
            return False
        
        self.grid[x][y] = self.player
        self.count[self.player] += 1
        for x, y in flippable:
            self.flip(x, y)
            self.count[self.player] += 1
            self.count[-self.player] -= 1
        self.player *= -1

        return True
    
    def flip(self, x, y):
        self.grid[x][y] *= -1
    
    def display(self):
        possible = self.possible_discs()

        print("  ", end = "")
        for y in range(BOARD_SIZE):
            print(chr(ord("a") + y), end = " ")
        print()

        for x in range(BOARD_SIZE):
            print(x + 1, end = " ")
            for y in range(BOARD_SIZE):
                if [x, y] in possible:
                    print("*", end = " ")
                elif self.grid[x][y] == BLACK:
                    print("◯", end = " ")
                elif self.grid[x][y] == WHITE:
                    print("●", end = " ")
                else:
                    print("·", end = " ")
            print()
    
    def end(self):
        if self.possible_discs() != []:
            return False
        self.player *= -1
        if self.possible_discs() == []:
            self.player *= -1
            return True
        else:
            self.player *= -1
            return False
    
    def judge(self):
        print("Black: {} - White: {}".format(self.count[BLACK], self.count[WHITE]))
        if self.count[BLACK] > self.count[WHITE]:
            print("Black won!")
        elif self.count[BLACK] < self.count[WHITE]:
            print("White won!")
        else:
            print("Draw!")

othello = Othello()

while True:
    othello.display()

    if othello.end():
        othello.judge()
        break

    while True:
        possible = othello.possible_discs()
        if possible == []:
            if othello.player == BLACK:
                print("Black: pass")
            else:
                print("White: pass")
            othello.player *= -1
            break

        if othello.player == BLACK:
            s = input("Black: ")
        else:
            s = input("White: ")
        
        if s == "exit":
            exit()
        
        x, y = int(s[1]) - 1, ord(s[0]) - ord("a")
        if othello.put(x, y):
            break
        else:
            print("Invalid input. Please try again.")
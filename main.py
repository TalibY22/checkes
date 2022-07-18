import pygame

width,height = 600,600
rows,cols = 8,8
square_sixe = width//cols


#COLORS
white = (255,255,255)
black = (0,0,0)
turqouise = (64,224,208)
yellow = (255, 234, 0)
green = (0, 255, 127)
gray = (192, 192, 192)
brown = (102, 205, 170)
white2 = (255, 228, 225)
slate = (47, 79, 79)



#CROWN
crown = pygame.image.load('crown.png')
crown = pygame.transform.scale(crown,(44,25))




#CLASS FOR THE PIECES
class piece:
    padding = 15
    outline = 2
    def __init__(self,row,col,color):
        self.row =row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = square_sixe * self.col + square_sixe // 2
        self.y = square_sixe * self.row + square_sixe // 2

    def make_king(self):
        self.king = True

    #FUNCTION FOR MOVEMENT
    def move(self,row,col):
        self.row = row
        self.col = col
        self.calculate_position()

    def draw(self,win):
        radius = square_sixe // 2 - self.padding
        pygame.draw.circle(win,black,(self.x,self.y),radius + self.outline)

        pygame.draw.circle(win,self.color,(self.x,self.y),radius )

        if self.king:
            win.blit(crown,(self.x - crown.get_width()//2,self.y - crown.get_height()//2))
    def __repr__(self):
        return str(self.color)



#CODE TO MAKE BOARD
class board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.red_left = self.white_left = 12
        self.red_kings = self.white_king = 0
        self.draw_board()
    #FUNCTION TO DRAW THE BOARD
    def draw_cubes(self,win):
        win.fill(gray)
        for row in range(rows):
            for col in range(row % 2,cols,2):
                pygame.draw.rect(win,white2,(row*square_sixe,col*square_sixe,square_sixe,square_sixe))

    #FUNCTION TO DRAW BOARD OBJECTS
    def draw_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(piece(row,col,slate))
                    elif row > 4:
                        self.board[row].append(piece(row,col,black))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    #FUNCTION TO MOVE PIECE
    def movement(self,piece,row,col):
        self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row,col)

        if row == rows - 1 or row == 0:
            piece.make_king()
            if piece.color == slate:
                self.white_king += 1
            else:
                self.red_kings += 1


    def get_piece(self,row,col):
        return self.board[row][col]



    def draw(self,win):
        self.draw_cubes(win)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def winner(self):
        if self.red_left <= 0:
            return white2
        elif self.white_left <=0:
            return slate

    def remove(self,pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == black:
                    self.red_left -= 1
                else:
                    self.white_left -= 1





    #CHECKS THE VALIDITY OF MOVES
    def valid_moves(self,piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == black or piece.king:
            moves.update(self.left_move(row -1 ,max(row-3,-1), -1,piece.color, left))
            moves.update(self.ryt_move(row -1 ,max(row-3,-1), -1,piece.color, right))

        if piece.color == slate or piece.king:
            moves.update(self.left_move(row + 1, min(row +3, rows) ,1, piece.color, left))
            moves.update(self.ryt_move(row + 1, min(row +3, rows) ,1, piece.color, right))

        return moves





    #LEFT MOVE
    def left_move(self,start,stop,step,color,left,skipped=[]):
        moves = {}
        last = {}
        for r in range(start,stop,step):
            if left < 0:
                break


            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                   break

                elif skipped:
                    moves[(r,left)] = last + skipped
                else:
                    moves[(r,left)] = last

                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3,rows)
                    moves.update(self.left_move(r + step, row,step,color,left - 1,skipped=last))
                    moves.update(self.ryt_move(r + step, row,step,color,left + 1,skipped=last))
                    break



            elif current.color == color:
                 break
            else:
                last = [current]

            left -= 1
        return moves


    #RIGHT MOVE
    def ryt_move(self,start,stop,step,color,right,skipped=[]):
        moves = {}
        last = {}
        for r in range(start, stop, step):
            if right >= cols:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break

                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, rows)
                    moves.update(self.left_move(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self.ryt_move(r + step, row, step, color, right + 1, skipped=last))



            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves








#GAME MECHANICS
class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = board()
        self.turn = black
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.movement(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, turqouise,
                               (col * square_sixe + square_sixe // 2, row * square_sixe + square_sixe // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == black:
            self.turn = slate
        else:
            self.turn = black










def mouse_pos(pos):
    x,y = pos
    row = y // square_sixe
    col = x // square_sixe

    return row,col







win = pygame.display.set_mode((width,height))

#MAIN FUNCTION
def main():
    run = True
    clock =pygame.time.Clock
    bd2 = board()
    game2 = Game(win)
    #p2 = bd2.get_piece(0,1)
    #bd2.movement(p2, 4, 3)

    while run:
        #clock.Tick(60)
        #CONTROLS
        if game2.winner() != None:
            print(game2.winner())
            run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
               pos = pygame.mouse.get_pos()
               row,col = mouse_pos(pos)
               game2.select(row,col)

        game2.update()

    pygame.quit()





if __name__ == '__main__':
    main()
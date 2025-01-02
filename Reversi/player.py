class MyPlayer():
    '''
    Best move is chosen based on a risk of each position on the board.
    '''

    def __init__(self, my_color,opponent_color, board_size=8):
        self.name = 'kopliric' 
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
    
    def get_score(self, x, y, stones_inverted):
        '''
        compute the score of a move based on the risk of the place on the board and 
        number of inverted stones 
        
        :param x: row of the game board
        :param y: column of the game board
        :param basic_score: number of inverted oppenent's stones in case of a move
        :return: total score of a move
        '''

        # conditions for corners
        is_in_corner = ((x == 0 and y == 0) or
                        (x == 0 and y == self.board_size - 1) or
                        (x == self.board_size - 1 and y == 0) or
                        (x == self.board_size - 1 and y == self.board_size - 1))
        
        # conditions for a diagonal spaces directly in front of corners
        is_on_2nd_diag = ((x == 1 and y == 1) or
                          (x == 1 and y == self.board_size - 2) or
                          (x == self.board_size - 2 and y == 1) or
                          (x == self.board_size - 2 and y == self.board_size - 2))
        
        # conditions for spaces directly on side of corners
        is_on_corner_side = ((x == 0 and y == 1) or
                             (x == 0 and y == self.board_size - 2) or
                             (x == 1 and y == 0) or
                             (x == 1 and y == self.board_size - 1) or
                             (x == self.board_size - 1 and y == 1) or
                             (x == self.board_size - 1 and y == self.board_size - 2) or
                             (x == self.board_size - 2 and y == 0) or
                             (x == self.board_size - 2 and y == self.board_size - 1))
        
        # conditions for other edges
        is_on_edge = ((x == 0 and 1 < y < self.board_size - 2) or
                      (x == self.board_size - 1 and 1 < y < self.board_size - 2) or
                      (1 < x < self.board_size - 2 and y == 0) or
                      (1 < x < self.board_size - 2 and y == self.board_size - 1))

        # conditions for 2nd level of edges
        is_on_2nd_edge = ((x == 1 and 1 < y < self.board_size - 2) or
                          (x == self.board_size - 2 and 1 < y < self.board_size - 2) or
                          (1 < x < self.board_size - 2 and y == 1) or
                          (1 < x < self.board_size - 2 and y == self.board_size - 2))
        
        score = stones_inverted;

        # incorporate risk of the position into the score
        if is_in_corner: 
            score += 100
        elif is_on_2nd_diag:
            score -= 50
        elif is_on_corner_side:
            score -= 20
        elif is_on_edge:
            score += 10
        elif is_on_2nd_edge:
            score -= 2
        else:
            score -= 1

        return score

    def move(self,board):
        '''
        Strategy:
            * always choose a corner if possible;
            * if not, try to get on the edges of a game board;
            * avoid moves that allow an opponent to get to the corners and edges.

        :param board: game board
        :return: position on the board for the next move as tuple
        '''
        
        valid_moves = self.get_all_valid_moves(board)

        #evaluate a score for each possible move and choose the one with the highest score
        best_score = -100
        best_position = None
        for position in valid_moves:
            score = self.get_score(position[0][0], position[0][1], position[1])
            if score > best_score:
                best_score = score
                best_position = position[0]
        return best_position

    def __is_correct_move(self, move, board):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            [confirmation, stones_inverted] = self.__confirm_direction(move, dx[i], dy[i], board)
            if confirmation:
                return True, stones_inverted 
        return False, 0

    def __confirm_direction(self, move, dx, dy, board):
        posx = move[0]+dx
        posy = move[1]+dy
        opp_stones_inverted = 0
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] == self.opponent_color:
                opp_stones_inverted += 1
                while (posx >= 0) and (posx <= (self.board_size-1)) and (posy >= 0) and (posy <= (self.board_size-1)):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == -1:
                            return False, 0
                        if board[posx][posy] == self.my_color:
                            return True, opp_stones_inverted
                    opp_stones_inverted += 1

        return False, 0

    def get_all_valid_moves(self, board):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                [confirmation, stones_inverted] = self.__is_correct_move([x,y], board)
                if (board[x][y] == -1) and confirmation:
                    valid_moves.append( [(x, y), stones_inverted] )

        if len(valid_moves) <= 0:
            print('No possible move!')
            return None
        return valid_moves
    

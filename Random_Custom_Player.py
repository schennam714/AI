# Name: Shreyas Chennamaraja
# Date: 1/05/2021

import random
class RandomPlayer:
   def __init__(self):
      self.white = "#ffffff" #"O"
      self.black = "#000000" #"X"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.first_turn = True
      
   def best_strategy(self, board, color):
      # returns best move
      # (column num, row num), 0
      options = self.find_moves(board,color)
      find_index = random.choice(list(options))
      return (find_index//self.y_max, find_index%self.y_max), 0
      
     
   def find_moves(self, board, color):
      # finds all possible moves
      # returns a set, e.g., {0, 1, 2, 3, ...., 24} 
      # 0 5 10 15 20
      # 1 6 11 16 21
      # 2 7 12 17 22
      # 3 8 13 18 23
      # 4 9 14 19 24
      self.x_max = len(board)
      self.y_max = len(board[0])
      totalmoves = set()
      for i in range(len(board)):
         for j in range(len(board[i])):
            if self.first_turn and board[i][j] == '.': 
                totalmoves.add(i*self.x_max+j)
            elif(color == self.black and board[i][j] == 'X') or (color == self.white and board[i][j] == 'O'):
                for incr in self.directions:
                    x_pos = i + incr[0]
                    y_pos = j + incr[1]
                    stop = False
                    while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                        if board[x_pos][y_pos] != '.':
                           stop = True
                        if not stop:    
                           totalmoves.add(x_pos*self.x_max+y_pos)
                        x_pos += incr[0]
                        y_pos += incr[1]
      self.first_turn=False
      return totalmoves

class CustomPlayer:

   def __init__(self):
      self.white = "#ffffff" #"O"
      self.black = "#000000" #"X"
      self.directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
      self.opposite_color = {self.black: self.white, self.white: self.black}
      self.x_max = None
      self.y_max = None
      self.first_turn = True

   def best_strategy(self, board, color):
      # returns best move
      
      moves = self.find_moves(board, color)

      if(len(moves) > 23):
         if board[2][2] == '.':
            return [2,2], 0
      self.x_max = len(board)
      self.y_max = len(board[0])
      bestV = -9999
      bestM = (-1, -1)
      for p in moves:
         move = (p // self.y_max, p % self.y_max)
         nBoard = self.make_move(board, color, move)
         nVal = self.min_value(nBoard, self.opposite_color[color], 4)
         if nVal > bestV:
            bestV = nVal
            bestM = move
      return bestM, bestV

   def max_value(self, board, color, search_depth):
      possible = self.find_moves(board, color)

      if len(possible) == 0:
         return -1000
      elif len(self.find_moves(board, self.opposite_color[color]))==0:
         return 1000
      if search_depth == 1:
         return self.evaluate(board, color, possible)

      val = -9999
      for each in possible:
         move = (each // self.y_max, each % self.y_max)
         nBoard = self.make_move(board, color, move)
         val2 = self.min_value(nBoard, self.opposite_color[color], search_depth-1)
         if val2 > val:
            val = val2
      return val

   def min_value(self, board, color, search_depth):
      moves = self.find_moves(board, color)
      if len(moves) == 0: 
         return 1000
      elif len(self.find_moves(board, self.opposite_color[color])) == 0: 
         return -1000
      if search_depth == 1:
         return -1 * self.evaluate(board, color, moves)
      
      val = 9999
      for a in moves:
         move=(a//self.y_max, a % self.y_max)
         new_board = self.make_move(board, color, move)
         val2 = self.max_value(new_board, self.opposite_color[color], search_depth-1)
         if val2 < val:
            val = val2
      return val 

   def negamax(self, board, color, search_depth):
      # returns best "value"
      return 1
      
   def alphabeta(self, board, color, search_depth, alpha, beta):
      # returns best "value" while also pruning
      pass

   def make_move(self, board, color, move):
      # returns board that has been updated
      iter_copy = []
      win = 'W'
      for row in board:
         li = []
         for indent in row:
            li.append(indent)
         iter_copy.append(li)
      for x in range(self.x_max):
         for y in range(self.y_max):
            if(color == self.black and board[x][y] == 'X') or (color == self.white and board[x][y] == 'O'):
               iter_copy[x][y]=win
      if color ==self.black:
         iter_copy[move[0]][move[1]] = 'X'
      else:
         iter_copy[move[0]][move[1]] = 'O'
      return iter_copy

   def evaluate(self, board, color, possible_moves):
      # returns the utility value
      return len(possible_moves) - 2*len(self.find_moves(board, self.opposite_color[color]))

   def find_moves(self, board, color):
      # finds all possible moves
      self.x_max = len(board)
      self.y_max = len(board[0])
      moves_found = set()
      for i in range(len(board)):
         for j in range(len(board[i])):
            if self.first_turn and board[i][j] == '.': 
               moves_found.add(i*self.y_max+j)
            elif (color == self.black and board[i][j] == 'X') or (color == self.white and board[i][j] == 'O'):
               for incr in self.directions:
                   x_pos = i +incr[0]
                   y_pos = j + incr[1]
                   stop = False
                   while 0 <= x_pos < self.x_max and 0 <= y_pos < self.y_max:
                       if board[x_pos][y_pos] != '.':
                          stop = True
                       if not stop:    
                          moves_found.add(x_pos*self.y_max+y_pos)
                       x_pos += incr[0]
                       y_pos += incr[1]
      self.first_turn=False
      return moves_found


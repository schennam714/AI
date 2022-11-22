# Name: Shreyas Chennamaraja
# Date: 12/10/2020

import os, time

def check_complete(assignment, csp_table):
   if '.' not in assignment:
      return True
   return False
   
def select_unassigned_var(assignment, variables, csp_table):
   dictz = {}
   for a in variables:
      dictz[a] = variables[a]
   for num in range(81):
      if assignment[num] !='.':
         if num in dictz: 
            del dictz[num]
   search = lambda f: len(dictz[f])
   return min(dictz,key=search)

def sudoku_neighbors(csp_table):
   neighborlist = {}
   count = 0
   for num in range(0, 81):
      neighborlist[num] = []
      while count < len(csp_table)-1:
         for val in csp_table[count]:
            if num in csp_table[count]:
               if val not in neighborlist[num]:
                  neighborlist[num].append(val)
               if csp_table[count].index(val)==8:
                  count+=1
            elif count < len(csp_table)-1:
               count+=1
      for v in sudoku_csp():
         if num in v:
            for each in v:
               if each not in neighborlist[num] and each != num:
                  neighborlist[num].append(each)
   return neighborlist

def isValid(value, var_index, assignment, variables, csp_table):
   search = str(value)
   for sub in csp_table:
      if var_index in sub:
         for index in sub:
            if assignment[index] == search:
               return False  
   return True

def ordered_domain(assignment, variables, csp_table):
   
   return ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

def update_variables(value, var_index, assignment, variables, csp_table, neighbors):
   for i in neighbors[var_index]:
      if value in variables[i]: 
         variables[i].remove(value)
   return variables

def backtracking_search(puzzle, variables, csp_table, neighbors): 
   return recursive_backtracking(puzzle, variables, csp_table, neighbors)

def recursive_backtracking(assignment, variables, csp_table, neighbors):
   if check_complete(assignment, csp_table):
      return assignment
   temp = select_unassigned_var(assignment, variables, csp_table) 
   for each in ordered_domain(assignment, variables, csp_table):
      if isValid(each, temp, assignment, variables, csp_table):
         assignment = assignment[:temp] + each + assignment[temp+1:]
         up = update_variables(each, temp, assignment, variables, csp_table, neighbors)
         result = recursive_backtracking(assignment, up, csp_table, neighbors)
         if result != None:
            return result
         assignment = assignment[:temp] + '.' + assignment[temp+1:]
   return None

def display(solution):
   result = ""
   for i in range(len(solution)):
      result += solution[i] + " "
      if i%27==26:
         result += "\n\n"
      elif i%9==8:
         result += "\n"
      elif i%3==2:
         result += "  "
   return result

def sudoku_csp():
   init = [[0,1,2,9,10,11,18,19,20]]
   temp = 3
   index = 0
   for i in range(1,9):
        if i%3==0 and i!=0:
            init.append([x+((i)*9) for x in init[0]])
        else:
            init.append([x+temp for x in init[index]])
        index+=1
   return init

def initial_variables(puzzle, csp_table):
   var = {}
   for i in range(0, len(puzzle)):
      if puzzle[i] == '.': 
         var[i] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
      else:
         var[i] = [puzzle[i]]
   return var

def main():
   filename = input("file name: ")
   if not os.path.isfile(filename):
      filename = "puzzles.txt"
   start_time = time.time()
   for line, puzzle in enumerate(open(filename).readlines()):
      csp_table = sudoku_csp()   # rows, cols, and sub_blocks
      #if line == 50: break  # check point: goal is less than 0.5 sec
      line, puzzle = line+1, puzzle.rstrip()
      print ("Line {}: {}".format(line, puzzle)) 
      neighbors = sudoku_neighbors(csp_table) # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
      variables = initial_variables(puzzle, csp_table)   
      solution = backtracking_search(puzzle, variables, csp_table, neighbors)
      if solution == None:print ("No solution found."); break
      print ("solution\n" + display(solution))
   print ("Duration:", (time.time() - start_time))
   
if __name__ == '__main__': main()
# -*- coding: utf-8 -*-
import time
import copy



puzzle1 = [
			[0,8,2,0,0,0,0,0,0], 
			[1,0,0,0,0,0,0,0,0],
			[4,9,0,0,3,0,2,0,5],
			[0,1,0,0,0,0,0,0,0],
			[0,6,5,2,0,0,0,0,0],
			[3,0,0,0,0,0,0,0,4],
			[0,3,0,6,4,0,0,0,0],
			[0,0,1,0,5,0,0,4,8],
			[0,0,8,1,0,2,3,0,6],
			]


puzzle2 = [
			[1,6,0,0,0,0,8,0,0], 
			[7,0,9,0,0,4,0,5,0],
			[4,5,0,2,0,6,0,9,0],
			[2,0,0,0,6,0,7,0,0],
			[0,0,6,0,0,0,0,0,0],
			[0,0,8,4,7,0,5,0,0],
			[6,0,0,0,4,7,0,0,5],
			[0,9,0,0,2,0,0,8,0],
			[0,0,0,0,5,0,2,0,6],
			]



def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

DIGITS   = '123456789'
ROWS     = 'ABCDEFGHI'
NUMBERS   = [1,2,3,4,5,6,7,8,9]
COLS     = DIGITS
SQUARES  = cross(ROWS, COLS)
UNITLIST = ([cross(ROWS, c) for c in COLS] +
            [cross(r, COLS) for r in ROWS] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
UNITS = dict((s, [u for u in UNITLIST if s in u]) 
             for s in SQUARES)
PEERS = dict((s, set(sum(UNITS[s],[]))-set([s]))
             for s in SQUARES)

#START_SOLUTION = dict((s, [n for n in NUMBERS]) for s in SQUARES)



def transform(norvig_notation):
	#'4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	norvig = norvig_notation.replace('0', '.')
	puzzle = [[0 for y in range(9)] for x in range(9)]
	for r in range(9):
		for c in range(9):
			puzzle[r][c] = int(norvig[r*9+c]) if norvig[r*9+c] != '.' else 0
	return puzzle





def pp(solution):

	width = 1+max(len(solution[s]) for s in SQUARES)
#	width = 10
	line = '+'.join(['-'*(width*3)]*3)	
	for r in ROWS:
		print(''.join(str(''.join(str(i) for i in solution[r+c])).center(width) + ('|' if c in '36' else '') 
			for c in COLS))
		if r in 'CF':
			print(line)
	print



def parse_grid(puzzle):
	solution = dict((s, [n for n in NUMBERS]) for s in SQUARES)
	for i, r in enumerate(ROWS):
		for j, c in enumerate(COLS):
			number = puzzle[i][j]
			if number != 0:
				solution = assign(number, r+c, solution)			
#				print pp(solution)
	return solution





def solve(solution):

	if solution is False:
		return False

	if is_solved(solution):
		return solution

	# brute force the rest
	unsolved_squares = [s for s in SQUARES if len(solution[s]) > 1]
	square = unsolved_squares[0]
	for number in solution[square]:
		solution2 = solve( assign(number, square, copy.deepcopy(solution)) )
		if solution2:
			return solution2

	return False

def solve_all(puzzles):

	for puzzle in puzzles:
		solution = parse_grid(transform(puzzle))
		pp(solution)
		pp(solve(solution))



def is_solved(solution):
	return all(len(solution[s]) == 1 for s in SQUARES)


def assign(number, square, solution):

	assert(number > 0 and number <= 9)
	solution[square] = [number]

	for peer in PEERS[square]:
		if solution is False:
			return False
		if number in solution[peer]: 
			solution[peer].remove(number)
			if len(solution[peer]) == 0:
				return False

			if len(solution[peer]) == 1:
#				print' rec, was investigting ', square, ' now enter ', solution[peer][0], ' ', peer 
				solution = assign(solution[peer][0], peer, copy.deepcopy(solution))
	return solution


if __name__== "__main__":
	easy = transform('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
	easy = transform('361025900080960010400000057008000471000603000259000800740000005020018060005470329')

	hard = transform('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
#	solve_all(open("sudoku-hardest.txt"))
	solve_all(open("ak.txt"))



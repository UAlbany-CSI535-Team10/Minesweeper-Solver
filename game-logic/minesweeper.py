from random import randint

def surrounding_cells(x, y, rows, cols):
  x_0, x_1 = x-1, x+2
  y_0, y_1 = y-1, y+2
  if x_0 < 0:
    x_0 += 1
  elif x_1 > rows:
    x_1 -= 1
  if y_0 < 0:
    y_0 += 1
  elif y_1 > cols:
    y_1 -= 1
  cells = []
  for i in range(x_0, x_1):
    for j in range(y_0, y_1):
      if i==x and j==y:
        continue
      cells.append([i, j])
  return cells

def create_board(rows, cols, n):
  board = [[0]*cols for _ in range(rows)]
  mines = []
  while len(mines) != n:
    new_mine = (randint(0, rows-1), randint(0, cols-1))
    if new_mine not in mines:
      mines.append(new_mine)
      x = new_mine[0]
      y = new_mine[1]
      board[x][y] = 9
      for i, j in surrounding_cells(x, y, rows, cols):
        board[i][j] += 1
  return board, mines

def display_state(state):
  rows, cols = len(state[0]), len(state[0][0])
  rows_spacing, cols_spacing = len(str(rows)) + 1, len(str(cols)) + 1
  print('{:>{rs}}'.format(' ', rs=rows_spacing), end='')
  for i in range(cols):
    print('{:>{cs}}'.format(i, cs=cols_spacing), end='')
  print('')
  for i in range(rows):
    print('{:>{rs}}'.format(i, rs=rows_spacing), end='')
    for j in range(cols):
      print('{:>{cs}}'.format(state[0][i][j], cs = cols_spacing), end='')
    print('')

def play(row, col, state, board, flag=False):
  rows, cols = len(board), len(board[0])
  x, y = row, col
  if x < 0 or x > rows or y < 0 or y > cols:
    print('Invalid coordinates!')
    return False
  if board[x][y] > 8: # clicked on mine
    state[0][x][y] = 'X' if not flag else 'F'
    if flag:
      state[2] += 1
    return not flag # game over only if mine clicked not flagged
  if flag:
    print('No mine here!')
    return False
  queue = [[x, y]]
  while queue:
    x, y = queue.pop(0)
    if state[0][x][y] != '#': # previously clicked/recursively visited cell
      continue
    state[1] += 1
    if board[x][y] > 0: # clicked on numbered cell
      state[0][x][y] = board[x][y]
      continue
    # cell has no mine surrounding it 
    state[0][x][y] = ''
    # click on surrounding 8 cells
    queue += surrounding_cells(x, y, rows, cols)
  return False


def main():
  rows = int(input('Enter rows: '))
  cols = int(input('Enter columns: '))
  n = int(input('Enter number of mines: '))
  board, mines = create_board(rows, cols, n)
  num_mines = len(mines)
  display_state([board])
  print(mines)
  print('-'*30)
  state = [[['#']*cols for _ in range(rows)], 0, 0] # exposed grid, number of exposed cells, flagged mines
  display_state(state)
  done = False
  flag = False
  while not done:
    print('Click on ')
    try:
      x = int(input('\trow: '))
      y = int(input('\tcol: '))
    except ValueError as _:
      print('Invalid input!')
      continue
    done = play(x, y, state, board, flag)
    display_state(state)
    if (rows*cols - state[1]) == num_mines or state[2] == num_mines:
      print('Winner!')
      done = True
    elif not done:
      flag = False
      option = input('Continue (enter \'N\' to quit, \'F\' to flag)? ')
      if option == 'N':
        break
      if option == 'F':
        flag = True
    else:
      print('Game Over!')

if __name__ == '__main__':
  main()
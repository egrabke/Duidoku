# game.py
# Two Player Game
# Emerson Grabke


def play():
    '''(None) -> None

    Initiate two-player game'''

    global grid_size
    global grid
    global grid_length
    global current_player
    global watching_player

    false_grid_size = True

    while false_grid_size:
        grid_size = input('Please input grid size: ')

        if grid_size in ['4', '9', '16']:
            grid_size = int(grid_size)
            false_grid_size = False
            print('You have chosen a {} by {} grid'.format(
                int(grid_size), int(grid_size)))
        else:
            print('You have entered an invalid grid size!')

    grid = [[0]*grid_size for element in [0]*grid_size]
    grid_length = int(grid_size**0.5)

    show()

    current_player = 'B'
    watching_player = 'A'

    win_value = 0

    while win_value == 0:
        current_player, watching_player = watching_player, current_player

        move_return = 's'

        while move_return in ['s', 'l']:
            error = 1
            while(error):
                try:
                    move_return = move()
                    error = 0
                except:
                    print('Move not valid. Please enter move as: row,column,value')
                    error = 1
                    
        if move_return == 'q':
            print('Goodbye')
            return

        show()

        win_value = check_win()

    if win_value == 1:
        print('Congratulations Player ' + current_player + '. You have won!')

    else:
        print('The matrix is full. It is a tie.')


def move():
    '''(None) -> str

    Begins move sequence.
    Return one character string based on the move input.
    This string is to be interpreted in play()'''

    global grid
    global current_player

    move_not_legal = True

    while move_not_legal:
        raw_move = input('Player ' + current_player + ' enter a move: ')

        if raw_move == 's':
            save()
            return 's'
        elif raw_move == 'l':
            load()
            return 'l'
        elif raw_move == 'q':
            return 'q'

        row, column, value = raw_move.split(',')

        row, column, value = (
            int(row.strip()), int(column.strip()), int(value.strip()))

        move_not_legal = not check_move(row, column, value)

        if move_not_legal:
            print('You have entered an invalid move. Try again')

    grid[row][column] = value

    return 'y'


def check_move(row, col, value):
    '''(int, int, int) -> boolean

    Checks if a move is legal or not, where the move takes the form of:
    Row# (row), Column# (col), and value (value).
    Return True if move is legal, False if not.'''

    global grid
    global grid_size
    global grid_length

    if (row >= grid_size) or (col >= grid_size):
        return False  # Checks for range

    elif (grid[row][col] != 0) or (value in grid[row]) or (
            value not in range(1, grid_size+1)):
        return False  # Checks for row and value specified

    row_cluster = row//(grid_length)
    col_cluster = col//(grid_length)

    for row_element in range(grid_length):
        for col_element in range(grid_length):
            if value == grid[row_cluster*grid_length + row_element][(
                    col_cluster*grid_length + col_element)]:
                return False  # Checks cluster

    for row_number in range(grid_size):
        if value == grid[row_number][col]:
            return False  # Checks column

    return True


def check_win():
    '''(None) -> int

    Decides on the status of the game.
    Return 0 if game can continue.
    Return 1 if a player wins.
    Return 2 if game concludes in a tie.'''

    global grid
    global grid_size

    end_counter = 0

    for row in range(grid_size):
        if 0 not in grid[row]:
            end_counter += 1

        for column in range(grid_size):
            for value in range(1, grid_size+1):
                if check_move(row, column, value):
                    return 0

    if end_counter == grid_size:
        return 2  # Tie game case

    return 1


def save():
    '''(None) -> None

    Saves the game to an external file.'''

    global grid
    global grid_size

    write_file = input('Please input a file to save to: ')

    file_object = open(write_file, 'w')

    string_grid = ''

    for row in range(grid_size):
        for column in range(grid_size):
            string_grid += str(grid[row][column]) + ','
        string_grid = string_grid.strip(',') + '\n'

    string_grid.strip()

    file_object.write(string_grid)

    file_object.close()

    print('Game Saved')

    return


def load():
    '''(None) -> None

    Loads the game from an external file.'''

    global grid
    global grid_size
    global grid_length
    global current_player
    global watching_player

    read_file = input('Please input a file to load from: ')

    file_object = open(read_file)

    grid_size = 0

    grid = []

    for line in file_object:
        grid_size += 1
        current_line = line.strip().split(',')
        grid.append(current_line)

    turn_count = 0

    for row in range(grid_size):
        for column in range(grid_size):
            grid[row][column] = int(grid[row][column])
            if grid[row][column] == 0:
                turn_count += 1

    turns_elapsed = grid_size**2 - turn_count

    if turns_elapsed//2 == turns_elapsed/2:
        current_player = 'A'
        watching_player = 'B'
    else:
        current_player = 'B'
        watching_player = 'A'

    grid_length = int(grid_size**0.5)

    print('Game Loaded')

    show()

    file_object.close()

    return


def show():
    global grid
    global grid_size
    global grid_length

    grid_string = ''

    for row in range(grid_size):

        for column in range(grid_size):
            if (column != 0) and ((column+1)//grid_length == (
                    (column+1)/grid_length) and (column != grid_size-1)):
                grid_string += str(grid[row][column]) + '|'
            else:
                grid_string += str(grid[row][column]) + ' '

        grid_string += '\n'

        if (row != 0) and ((row+1)//grid_length == ((
                row+1)/grid_length) and (row != grid_size-1)):
            grid_string += str('-'*2*grid_size) + '\n'

    grid_string += 'l: load, s: save, q: quit'

    print(grid_string)

if __name__ == '__main__':
    play()


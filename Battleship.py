import random
import time

#Grid
grid = [[]]
# Grid size based on standard battleship rules
grid_size = 8
#ship locations on grid
ship_location = [[]]
# Number of ships based on standard battleship rules
ship_total_num = 5
# Ships that have been sunk beginning with zero sunk as is standard.
ship_sunk = 0
# Total number of turns per game. When turns run out game_over variable will return True and game will end. Standard
# rules does not have maximum turns
shot_total_num = 100
#Ends game when either shots run out or variable sunk_ship reaches 5.
game_over = False
#Alphabet to mark locations on grid.
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def grid_verify_and_ship_verify(row_start, row_end, column_start, column_end):
    # Verify ship placement choice is within grid parameters
    global grid
    global ship_location
    valid = True

    for r in range(row_start, row_end):
        for c in range(column_start, column_end):
            if grid[r][c] != ".":
                valid = False
                break

    if valid:
        ship_location.append([row_start, row_end, column_start, column_end])
        for r in range(row_start, row_end):
            for c in range(column_start, column_end):
                grid[r][c] = "O"

    return valid


def ship_place(row, column, direction, length):
    # Places ship on grid
    global grid_size

    start_row, end_row, start_column, end_column = row, row + 1, column, column + 1
    if direction == "left":
        if column - length < 0:
            return False
        start_column = column - length + 1

    elif direction == "right":
        if column + length >= grid_size:
            return False
        end_column = column + length

    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    elif direction == "down":
        if row + length >= grid_size:
            return False
        row_end = row + length

    return grid_verify_and_ship_verify(start_row, end_row, start_column, end_column)


def grid_create():
    # Creates grid with ships placed at random
    global grid
    global grid_size
    global ship_total_num
    global ship_location

    random.seed(time.time())

    rows, columns = (grid_size, grid_size)

    grid = []
    for r in range(rows):
        row = []
        for c in range(columns):
            row.append(".")
        grid.append(row)

    ship_place_num = 0
    ship_location = []

    while ship_place_num != ship_total_num:
        row_random = random.randint(0, rows - 1)
        column_random = random.randint(0, columns - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)

        if ship_place(row_random, column_random, direction, ship_size):
            ship_place_num += 1


def grid_print():
# Prints grid
    global grid
    global alphabet
    check = True

    alphabet = alphabet[0: len(grid) + 1]
    for row in range(len(grid)):
        print(alphabet[row], end=") ")
        for column in range(len(grid[row])):
            if grid[row][column] == "O":
                if check:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][column], end=" ")
        print("")

    print(" ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")


def shot_valid():
# Verifies that shot is valid
    global alphabet
    global grid

    spot_valid = False
    row = -1
    column = -1
    while spot_valid is False:
        spot = input("Enter row (A-J) and column (0-9). Example A5: ")
        spot = spot.upper()
        if len(spot) <= 0 or len(spot) > 2:
            print("Invalid row and/or column.")
            continue

        row = spot[0]
        column = spot[1]
        if not row.isalpha() or not column.isnumeric():
            print("Invalid row and/or column.")
            continue

        row = alphabet.find(row)
        if not (-1 < row < grid_size):
            print("Invalid row and/or column.")
            continue

        column = int(column)
        if not (-1 < column < grid_size):
            print("Invalid row and/or column.")
        continue

        if grid[row][column] == "@" or grid[row][column] == "X":
            print("This spot has already been chosen.")
            continue

        if grid[row][column] == "." or grid[row][column] == "O":
            spot_valid = True

    return row, column


def check_sunk(row, column):
# Checks if ship has sunk
    global ship_location
    global grid

    for location in ship_location:
        row_start = location[0]
        row_end = location[1]
        column_start = location[2]
        column_end = location[3]

        if row_start <= row <= row_end and column_start <= column <= column_end:
            for r in range(row_start, row_end):
                for c in range(column_start, column_end):
                    if grid[r][c] != "X":
                        return False
    return True


def take_shot():
# Updates grid after shot has been made
    global grid
    global ship_sunk
    global shot_total_num

    row, column = shot_valid()
    print("")
    print("---------------")

    if grid[row][column] == ".":
        print("Miss.")
        grid[row][column] == "@"

    elif grid[row][column] == "O":
        print("Hit!", end=" ")
        grid[row][column] == "X"

        if check_sunk(row, column):
            print("Ship sunk!")
            ship_sunk += 1
        else:
            print("Ship has been hit.")

    shot_total_num -= 1


def end_game():
# Checks if game has ended
    global ship_sunk
    global ship_total_num
    global shot_total_num
    global game_over

    if ship_total_num == ship_sunk:
        print("You win!")
        game_over = True
    elif shot_total_num <= 0:
        print("You ran out of shots. Game over.")
        game_over = True


def main():
    global game_over

    print("Welcome to the game Battleship.")
    print("You have 100 attempts to sink 5 ships.")

    grid_create()

    while game_over is False:
        grid_print()
        print("Remaining ships: " + str(ship_total_num - ship_sunk))
        print("Number of attempts remaining: " + str(shot_total_num))

        take_shot()
        print("-------------")
        print("")
        end_game()


if __name__ == '__main__':
    main()

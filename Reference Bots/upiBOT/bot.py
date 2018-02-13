import argparse
import json
import os
from random import choice

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0


def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def output_shot(x, y):
    move = 1  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)
    # checkBoard Random
    def searchCellSameCoor(absis , ordinat ) :
        for cells in opponent_map :
            if (cells['X'] == absis) and (cells['Y']==ordinat) :
                break
        return cells
    def aroundHit2(cells) :
        i = 0
        if(searchCellSameCoor(cells['X']+1,cells['Y'])['Damaged']) :
            i+=1
        if(searchCellSameCoor(cells['X'],cells['Y']+1)['Damaged']) :
            i+=1            
        if(searchCellSameCoor(cells['X']-1,cells['Y'])['Damaged']) :
            i+=1        
        if(searchCellSameCoor(cells['X'],cells['Y']-1)['Damaged']) :            
            i+=1
        return i

    def aroundHit(cells) :
        return searchCellSameCoor(cells['X']+1,cells['Y'])['Damaged'] or searchCellSameCoor(cells['X'],cells['Y']+1)['Damaged'] or searchCellSameCoor(cells['X']-1,cells['Y'])['Damaged'] or searchCellSameCoor(cells['X'],cells['Y']-1)['Damaged']
    targets = []
    for cell in opponent_map:
        if (not (cell['Damaged'])) and (not (cell['Missed'])) and ((cell['X']+cell['Y']) % 2 == 0):
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)
    if not targets :
        for cell in opponent_map :
            if (aroundHit2(cell) >= 2 ) and (not (cell['Damaged'])) and (not (cell['Missed'])) :
                valid_cell = cell['X'], cell['Y']
                targets.append(valid_cell)
    if not targets :
        for cell in opponent_map :
            if (aroundHit(cell)) and (not (cell['Damaged'])) and (not (cell['Missed'])) and ((cell['X']+cell['Y']) % 2 != 0) :
                valid_cell = cell['X'], cell['Y']
                targets.append(valid_cell)
    target = choice(targets)
    output_shot(*target)
    return


def loadPlacingMap() :
    file = open("Place.txt","r")
    listShips = []
    x = file.readline().strip('\n').strip('\t')
    while (x != "END") :
        tempShips = []
        while (x != "#") :
            tempShips.append(x)
            x = file.readline().strip('\n').strip('\t')
        listShips.append(tempShips)
        x = file.readline().strip('\n').strip('\t')
    file.close()
    return listShips


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west
    list_ships = loadPlacingMap()
    ships = choice(list_ships)
    # ships = ['Battleship 1 0 north',
    #          'Carrier 3 1 East',
    #          'Cruiser 4 2 north',
    #          'Destroyer 7 3 north',
    #          'Submarine 1 8 East'
    #          ]
    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)

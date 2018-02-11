import argparse
import json
import os
from random import choice

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0
data_file = "data.txt"


def main(player_key):
    #create initial file external
    with open(os.path.join("../..", data_file), 'w') as f:
        f.write('{},{},{}'.format(0,0,0))

    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)
    last_cell_x
    last_cell_x
    with open(os.path.join("../..",data_file), 'r') as f:
        last_cell_x, last_cell_y, last_state = f_in.read().split(',')
        last_cell_x = int(last_cell_x)
        last_cell_y = int(last_cell_y)

    for cell in opponent_map:
        if cell['X']==last_cell_x and cell['Y']==last_cell_y:
            if not cell['Damaged'] and not cell['Missed']:
                break
            
    
    #last state tidak kena, tembak random dengan pola checkerboard 
    if last_state==0:
        targets = []
        for cell in opponent_map:
            if not cell['Damaged'] and not cell['Missed']:
                if (cell['X']+cell['Y'])%2==0:
                    valid_cell = cell['X'], cell['Y']
                    targets.append(valid_cell)
        target = choice(targets)
    #last state kena
    elif last_state==1:
        cell_kiri
        cell_atas
        cell_kanan

        for cell in opponent_map:
            if last_cell_x>0 and cell['X']==last_cell_x-1 and cell['Y']==last_cell_y:
                cell_kiri = cell
            elif last_cell_x<9 and cell['X']==last_cell_x+1 and cell['Y']==last_cell_y:
                cell_kanan = cell
            elif last_cell_x<9 and cell['X']==last_cell_x and cell['Y']==last_cell_y+1:
                cell_atas = cell

        if not cell_kiri['Damaged'] and not cell_kiri['Missed']:
            valid_cell = cell_kiri['X'], cell_kiri['Y']
        elif not cell_atas['Damaged'] and not cell_atas['Missed']:
            valid_cell = cell_atas['X'], cell_atas['Y']
        elif not cell_kanan['Damaged'] and not cell_kanan['Missed']:
            valid_cell = cell_kanan['X'], cell_kanan['Y']
        else:







    with open(os.path.join("../..",data_file), 'w') as f_in:
        f_in.write('{},{},{}'.format(cell['X'],cell['Y'],last_state))
    
    output_shot(*target)
    return



def output_shot(x, y):
    move = 1  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    ships = ['Battleship 1 0 north',
             'Carrier 3 1 East',
             'Cruiser 4 2 north',
             'Destroyer 7 3 north',
             'Submarine 1 8 East'
             ]

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

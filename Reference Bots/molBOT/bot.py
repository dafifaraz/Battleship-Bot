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
stack_file = "stack.txt"


def main(player_key):
    #create initial external file
    with open(os.path.join("../..", data_file), 'w') as f:
        f.write('{},{},{}'.format(0,0,"hunt"))
    with open(os.path.join("../..", stack_file), 'w') as f:
        f.write("")
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
    with open(os.path.join("../..",data_file), 'r') as f:
        last_cell_x, last_cell_y, last_state = f_in.read().split(',')
        last_cell_x = int(last_cell_x)
        last_cell_y = int(last_cell_y)

    #get last cell
    last_cell
    for cell in opponent_map:
        if cell['X']==last_cell_x and cell['Y']==last_cell_y:
            last_cell = cell
            break

    #load stack
    stack = []
    with open(os.path.join("../..", stack_file), 'r') as f:
        for line in f_in:
        x,y = line[:-1].split(',')
        x = int(x)
        y = int(y)
        stack.append((x,y))

    #handling if last state hit
    if last_state=="hunt" and last_cell['Damaged']:
        last_state="target"
        for cell in opponent_map:
            if not cell['Damaged'] and not cell['Missed']:
                if cell['X']==last_cell_x+1 and cell['Y']==last_cell_y:
                    stack.append((cell['X'],cell['Y']))
                if cell['X']==last_cell_x-1 and cell['Y']==last_cell_y:
                    stack.append((cell['X'],cell['Y']))
                if cell['X']==last_cell_x and cell['Y']==last_cell_y+1:
                    stack.append((cell['X'],cell['Y']))
                if cell['X']==last_cell_x and cell['Y']==last_cell_y-1:
                    stack.append((cell['X'],cell['Y']))
    if last_state="target" and not last_cell['Damaged']:
        for cell in opponent_map:
            if not cell['Damaged'] and not cell['Missed']:
                if cell['X']==last_cell_x+1 and cell['Y']==last_cell_y:
                    stack.append((cell['X'],cell['Y']))
                if cell['X']==last_cell_x-1 and cell['Y']==last_cell_y:
                    stack.append((cell['X'],cell['Y']))
                if cell['X']==last_cell_x and cell['Y']==last_cell_y+1:
                    stack.append((cell['X'],cell['Y']))
                if cell['X']==last_cell_x and cell['Y']==last_cell_y-1:
                    stack.append((cell['X'],cell['Y']))
    
    if stack==[]:
        last_state = "hunt"

    #hunt mode
    if last_state=="hunt":
        targets = []
        for cell in opponent_map:
            if not cell['Damaged'] and not cell['Missed']:
                    valid_cell = cell['X'], cell['Y']
                    targets.append(valid_cell)
        target = choice(targets)
        with open(os.path.join("../..",data_file), 'w') as f:
            f.write("{},{},{}".format(target[0],target[1],"hunt"))
        output_shot(*target)
    #target mode
    elif last_state=="target":
        target = stack[0]
        stack = stack[1:]
        with open(os.path.join("../..",data_file), 'w') as f:
            f.write("{},{},{}".format(target[0],target[1],"target"))
        output_shot(*target)    

    #rewrite stack
    with open(os.path.join("../..",stack_file), 'w') as f:
        for s in stack:
            f.write("{},{}\n".format(*s))


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

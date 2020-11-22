# Name: forest fires
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
import numpy as np
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, randomise2d
import capyle.utils as utils

def transition_function(grid, neighbourstates, neighbourcounts):
    """Function to apply the transition rules
    and return the new grid"""
    # dead = state == 0, live = state == 1
    # unpack state counts for state 0 and state 1
    dead_neighbours, live_neighbours = neighbourcounts
    # create boolean arrays for the birth & survival rules
    # if 3 live neighbours and is dead -> cell born
    birth = (live_neighbours == 3) & (grid == 0)
    # if 2 or 3 live neighbours and is alive -> survives
    survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    # Set all cells to 0 (dead)
    grid[:, :] = 0
    # Set cells to 1 where either cell is born or survives
    grid[birth | survive] = 1
    return grid

def aRGB(x,y,z):
    return (x/255),(y/255),(z/255)

# cell states
CHAPARRAL = 0
FOREST = 1
LAKE = 2
CANYON = 3
BURNING = 4
BURNT_ALREADY = 5
BURNING_START = 6
BURNING_ENDING = 7
GRID_SIZE = 100
global start_grid

start_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
start_grid[60:80, 30:50] = FOREST
start_grid[20:30, 10:15] = LAKE
start_grid[10:60, 60:90] = CANYON
start_grid[0, GRID_SIZE-1] = BURNING  # initial fire right upper corner


def setup(args):
    """Set up the config object used to interact with the GUI"""
    config_path = args[0]
    config = utils.load(config_path)
    # -- THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED --
    config.title = "Forest Fire"
    config.dimensions = 2
    # config.states = (0, 1)
    # -------------------------------------------------------------------------
    config.states = (CHAPARRAL, FOREST, LAKE, CANYON, BURNING,
                     BURNT_ALREADY, BURNING_START, BURNING_ENDING)
    # ---- Override the defaults below (these may be changed at anytime) ----
    # green = aRGB(180,238,180)
    # fire = aRGB(178,34,34)
    # config.state_colors = [green,fire]#[(180,238,180),(178,34,34)]
    # config.num_generations = 150
    config.state_colors = \
        [
            (0.7, 0.7, 0.1),  # chaparral
            (0, 0.6, 0),  # forrest
            (0, 0.5, 1),  # lake
            (1, 0.6, 0.1),  # canyon
            (1, 0, 0),  # burning
            (0.25, 0.25, 0.25),  # burnt already
            (1, 0.7, 0),  # burn start
            (0.8, 0, 0.2)  # burning end
        ]



    config.grid_dims = (GRID_SIZE,GRID_SIZE)

    config.set_initial_grid(start_grid)
    config.wrap = False
    # ----------------------------------------------------------------------

    # the GUI calls this to pass the user defined config
    # into the main system with an extra argument
    # do not change
    if len(args) == 2:
        config.save()
        sys.exit()
    return config



def main():
    """ Main function that sets up, runs and saves CA"""
    # Get the config object from set up
    config = setup(sys.argv[1:])

    # Create grid object using parameters from config + transition function
    grid = Grid2D(config, transition_function)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # Save updated config to file
    config.save()
    # Save timeline to file
    utils.save(timeline, config.timeline_path)

if __name__ == "__main__":
    main()

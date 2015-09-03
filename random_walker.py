# general imports
import logging
import signal
import sys
import numpy as np
import time

# minecraft imports
import mcpi.minecraft as minecraft

# object filesave functionality
import dill

# websocket functionality
from websocket import create_connection
import json

# local project imports
from qtron import Qtron
import gamewindow
import aid
import actionutils
from prepareworld import create_pasture
from counterupdaters import *


def init_logging():
    """ configures logging"""

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
    #logging.disable(logging.DEBUG) # uncomment to block debug log messages

def signal_handler(signal, frame):
    """ handles ctrl-c more..umm..gracefully"""

    print "thanks for playing"
    sys.exit(0)

########################
# SETTINGS
########################

def init_config():
    config = {
        'frame_size': 50, # RGB matrix captured will be a square with side frame_size (requires even number)
        'walk_stride': 0.25, # duration in seconds for each key press when walking
        'look_angle': 150, # how many pixels to move mouse when looking around
        'load_training_data': False, # set to True to load Q-tron weights from file
        'number_of_episodes': 200, # how many training episodes we should run (1 episode = 1 flower picked)
        'graph_server': False, # if True, sends runtimedata to websocket server
        'episodes_per_round': 20 # rounds are convenient to measure performance
        }
    config['number_of_rounds'] = config['number_of_episodes'] / config['episodes_per_round']
    return config

########################
# Q-LEARNER v3
########################

def init_parameters():
    # NOTE: epsilon will decrease 0.1 every 20 rounds, so 100 rounds are needed to decrease it
    #       to 0.1 which means it will then exploit 90% of the time
    ### PARAMETERS (may need tweaks and also functions to change them as training progresses)
    parameters = {
        'alpha' : 0.1, # learning rate
        'epsilon' : 0.6, # policy (exploration/exploitation): higher value, more exploration
        'gamma' : 0.9, # discount factor: close to zero = immediate rewards, close to one more longsighted
        'chop_prob': 0.8 # if enough red, 80% prob of chop
    }
    return parameters

def create_actions(frame_size, parameters):
    """ creates dictionary of available actions and their respective Qtrons """

    actions = {}
    size = 3 * frame_size**2 # for 20x20 matrix with RGB pixels, size is 1200

    actions['forward']  = Qtron(size, parameters)
    actions['backward'] = Qtron(size, parameters)
    actions['left'] = Qtron(size, parameters)
    actions['right'] = Qtron(size, parameters)
    actions['look_left'] = Qtron(size, parameters)
    actions['look_right'] = Qtron(size, parameters)
    actions['chop'] = Qtron(size, parameters)

    return actions

def init_counters():
    count_dict = {
        'flowercount': 0, # how many flowers we've picked, should be equal to number_of_episodes when done
        'start_time': time.time(), # starting time
        'end_time': 0,
        'actioncount': 0, # +1 for each action taken
        'roundcount': 0, # +1 every config['episodes_per_round'] episode

        'actions_per_episode': [],
        'times_per_episode': [],

        'actions_per_round': [],
        'times_per_round': []
    }

    return count_dict

def run_episode(config, parameters, actions, counters, ws, gw, mc, episode):

    logging.debug("starting new episode")

    flower_picked = False # can actually skip this and use reward value for while loop, but this makes it easier to see what's going on.
    reward = 0

    # reset action for current episode
    action = None

    #episode action count
    ep_actioncount = 0

    # episode will continue until a flower is picked
    while not flower_picked:

        #select random action
        action = np.random.choice(actions.keys())
        logging.debug("ACTION:  %s" % (action))

        # reward is 10 if flower was picked else 0
        reward = actionutils.take_action(action, config['walk_stride'], config['look_angle'], mc)

        # increase number of actions taken
        counters['actioncount'] += 1

        # allow action animation to finish before observing new state
        time.sleep(0.8)

        # send q-value to websocket api server if that setting is enabled
        message = { 'action': action, 'q_value': actions[action].value, 'step': counters['actioncount'], 'episode': episode, 'round': counters['roundcount'] }
        if config['graph_server']: ws.send(json.dumps(message))

        # episode is over if flower was picked
        if reward != 0:
            flower_picked = True
            counters['flowercount'] += 1

        ep_actioncount += 1
        logging.debug("actions taken this episode: %s" % (ep_actioncount))

        # reset action before next step
        action = None


def update_parameters(parameters):
    """ update parameters between rounds """

    # decrease explore/exploit probability every round
    if parameters['epsilon'] >= 0.2:
        parameters['epsilon'] += -0.1

def save_qtrons_to_file(qtrons, parameters, counters, config):
    """ saves all Qtrons to file so we can analyze them """

    filename = "./data/qtrons_started%s_round%s_time%s.pk1" % (counters['start_time'],counters['roundcount'],time.time())

    with open(filename, 'wb') as f:
        dill.dump(parameters, f)
        dill.dump(qtrons, f)
        dill.dump(config, f)

def load_actions_from_file():
    """ loads Qtrons from previous file, please check that file load_qtrons.pk1 exists
    in data directory """

    with open('./data/load_qtrons.pk1', 'rb') as f:
        parameters = dill.load(f)
        actions = dill.load(f)
        config = dill.load(f)

    return parameters, actions, config

def run_random_walker(config, ws, gw, mc):

    if config['load_training_data']:
        #load training data, both parameters and qtrons
        parameters, actions, config = load_actions_from_file()
    else:
        # init learning parameters
        parameters = init_parameters()
        # create actions
        actions = create_actions(config['frame_size'], parameters)

    # init counters (we have lots of 'em)
    counters = init_counters()

    # init first pasture
    create_pasture()
    print "please hold while we create our first pasture"
    time.sleep(5) # allow pasture to complete
    print "pasture complete. lets pick some flowers!"

    # terminal state for episode is a picked flower
    for episode in xrange(0, config['number_of_episodes']):

        logging.debug("current round: %s/%s" % (counters['roundcount'],config['number_of_rounds']))
        logging.debug("current episode: %s/%s" % (episode,config['number_of_episodes']))

        # run the episode!
        run_episode(config, parameters, actions, counters, ws, gw, mc, episode)

        # every episode, update episode counters
        update_episode_counters(counters)

        logging.debug("last episode used %s actions" % (counters['actions_per_episode'][len(counters['actions_per_episode'])-1]))

        # every round we update round counters and parameters
        if (episode+1) % config['episodes_per_round'] == 0 and episode != 0:  # cant handle episode_per_round == 1 but we dont care about that
            update_round_counters(counters)
            update_parameters(parameters)

            logging.debug("last round used %s actions" % (counters['actions_per_round'][len(counters['actions_per_round'])-1]))

            # save qtrons every new round in case of crash or death
            save_qtrons_to_file(actions, parameters, counters, config)

            # create new pasture for the next round unless we are on the last episode
            if episode != config['number_of_episodes'] - 1:
                create_pasture()
                print "round complete. creating new pasture for the next round, please hold..."
                time.sleep(5) # allow pasture to be created
                print "new pasture generated. prepare for next round!"

    # when all episodes are done, save all runtimes to file
    finished_save_counters_to_file(counters)

    # also save qtrons so we can check their values and weights
    save_qtrons_to_file(actions, parameters, counters, config)

    # goodbye message, and final check that flowercount and nbr of episodes are equal
    print "Congrats! You picked %s flowers in %s steps!" % (counters['flowercount'], counters['actioncount'])
    if counters['flowercount'] == config['number_of_episodes']:
        print "Which is good, because there were %s episodes" % (config['number_of_episodes'])
    else:
        print "But unfortunately, something went wrong, as there were %s episodes" % (config['number_of_episodes'])


########################
# MAIN
########################

def main():
    init_logging()
    # nice exit via ctrl-c
    signal.signal(signal.SIGINT, signal_handler)

    print "Welcome! Let's do some random walking shall we?"

    # initialize runtime configuration
    config = init_config()

    # create game window object and tell it the size our screenshots will have
    gw = gamewindow.GameWindow(config['frame_size'])

    # initiate connection to minecraft
    mc = minecraft.Minecraft.create()

    # save current time
    main_start_time = time.time()

    # connect to api server
    if config['graph_server']:
        ws = create_connection("ws://localhost:8080")
    else:
        ws="empty"

    # run q-learner
    run_random_walker(config, ws, gw, mc)

    # save time data
    main_run_time = time.time() - main_start_time

    print "Random walker has completed %s episodes in %s seconds" % (config['number_of_episodes'], main_run_time)
    print "That means an average of %s seconds per episode (20 flowers)" % (main_run_time / config['number_of_episodes'])

    # close connection to api server
    if config['graph_server']: ws.close()

if __name__ == "__main__":
    main()






















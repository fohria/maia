import logging
import json
import time
import numpy as np
from websocket import create_connection
import json

def init_parameters():
    parameters = {
        'alpha' : 0.1, # learning rate (wikipedia page for q-learning states this may be good..)
        'epsilon' : 0.6, # policy (exploration/exploitation): higher value, more exploration
        'gamma' : 0.95, # discount factor: close to zero = immediate rewards, close to one more longsighted
    }

    return parameters

def init_actions():
    actions = {}

    actions['forward'] = 0
    actions['backward'] = 0
    actions['left'] = 0
    actions['right'] = 0
    actions['look_left'] = 0
    actions['look_right'] = 0
    actions['chop'] = 0

    return actions

def run_episode(actions, episode, ws):

    for step in range(0,10):
        # select random action
        action = np.random.choice(actions.keys())
        # update its qvalue
        actions[action] = np.random.uniform(0,1)
        # send update to websocket server
        message = { 'action': action, 'q_value': actions[action], 'step': step, 'episode': episode }
        ws.send(json.dumps(message))

    return actions

def main():
    number_of_episodes = 20
    stepcount = 0

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
    #logging.disable(logging.DEBUG) # uncomment to block debug log messages

    logging.debug("q value generator initiating...")

    parameters = init_parameters()
    actions = init_actions()

    logging.debug("values initialized, exporting...")

    # connect to websocket server
    ws = create_connection("ws://localhost:8080")
    #ws.send(json.dumps(actions))

    logging.debug("exporting done. starting simulation...")

    for i in range(0, number_of_episodes):
        logging.debug("starting episode %s" % (i))
        run_episode(actions, i, ws)
        logging.debug("new action values: %s" % (actions))
        logging.debug("sleeping for three seconds before we go again...")
        time.sleep(3)

    ws.close()
    logging.debug("all done, byeeeeeee!")

if __name__ == "__main__":
    main()

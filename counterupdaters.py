import logging
import time
import numpy as np

def update_round_counters(counters):
    """ saves metrics for the last round """

    # add runtime for the last round
    current_time = time.time()
    if len(counters['times_per_round']) == 0:
        counters['times_per_round'].append(current_time - counters['start_time'])
    else:
        round_time = current_time - counters['start_time'] - np.sum(counters['times_per_round'])
        counters['times_per_round'].append(round_time)
        #counters['times_per_round'].append(round_time - 5) # -5 to compensate for sleep during pasture creation

    # add number of actions for last round
    if len(counters['actions_per_round']) == 0:
        counters['actions_per_round'].append(counters['actioncount'])
    else:
        nbr_of_actions = counters['actioncount'] - np.sum(counters['actions_per_round'])
        counters['actions_per_round'].append(nbr_of_actions)

    # update how many rounds we've run
    counters['roundcount'] += 1

    # now save counters to file before moving on
    round_save_counters_to_file(counters)

def update_episode_counters(counters):
    """ updates episode specific time counters """

    # add runtime for the last episode
    current_time = time.time()
    if len(counters['times_per_episode']) == 0:
        counters['times_per_episode'].append(current_time - counters['start_time'])
    else:
        episode_time = current_time - counters['start_time'] - np.sum(counters['times_per_episode'])
        counters['times_per_episode'].append(episode_time)

    # add number of actions for last episode
    if len(counters['actions_per_episode']) == 0:
        counters['actions_per_episode'].append(counters['actioncount'])
    else:
        nbr_of_actions = counters['actioncount'] - np.sum(counters['actions_per_episode'])
        counters['actions_per_episode'].append(nbr_of_actions)

def finished_save_counters_to_file(counters):
    """ saves all counters to file so we can analyze them """

    end_time = time.time()
    total_time = end_time - counters['start_time']
    counters['end_time'] = end_time

    logging.debug("total time elapsed was: %s" % (total_time))

    filename = "./data/finished_counters_start%s.csv" % (counters['start_time'])
    with open(filename, 'wb') as f:
        f.write('flowercount,start_time,end_time,actioncount,roundcount,actions_per_episode,times_per_episode,actions_per_round,times_per_round')

    with open(filename, 'ab') as f:
        f.write('\n%s,%s,%s,%s,%s,%s,%s,%s,%s' % (counters['flowercount'],counters['start_time'],counters['end_time'],counters['actioncount'],counters['roundcount'],counters['actions_per_episode'][0],counters['times_per_episode'][0],counters['actions_per_round'][0],counters['times_per_round'][0]))

    with open(filename, 'ab') as f:
        for x in xrange(1,len(counters['actions_per_round'])):
            f.write('\nna,na,na,na,na,%s,%s,%s,%s' % (counters['actions_per_episode'][x],counters['times_per_episode'][x],counters['actions_per_round'][x],counters['times_per_round'][x]))

    with open(filename, 'ab') as f:
        for x in xrange(len(counters['actions_per_round']),len(counters['actions_per_episode'])):
            f.write('\nna,na,na,na,na,%s,%s,na,na' % (counters['actions_per_episode'][x],counters['times_per_episode'][x]))

def round_save_counters_to_file(counters):
    """ saves all counters to file so we can analyze them """

    end_time = time.time()
    total_time = end_time - counters['start_time']

    filename = "./data/round_counters_start%s_roundnbr%s.csv" % (counters['start_time'],counters['roundcount'])
    with open(filename, 'wb') as f:
        f.write('flowercount,start_time,end_time,actioncount,roundcount,actions_per_episode,times_per_episode,actions_per_round,times_per_round')

    with open(filename, 'ab') as f:
        f.write('\n%s,%s,%s,%s,%s,%s,%s,%s,%s' % (counters['flowercount'],counters['start_time'],end_time,counters['actioncount'],counters['roundcount'],counters['actions_per_episode'][0],counters['times_per_episode'][0],counters['actions_per_round'][0],counters['times_per_round'][0]))

    with open(filename, 'ab') as f:
        for x in xrange(1,len(counters['actions_per_round'])):
            f.write('\nna,na,na,na,na,%s,%s,%s,%s' % (counters['actions_per_episode'][x],counters['times_per_episode'][x],counters['actions_per_round'][x],counters['times_per_round'][x]))

    with open(filename, 'ab') as f:
        for x in xrange(len(counters['actions_per_round']),len(counters['actions_per_episode'])):
            f.write('\nna,na,na,na,na,%s,%s,na,na' % (counters['actions_per_episode'][x],counters['times_per_episode'][x]))

import logging
import numpy as np
import time #only used for debugging purposes

class Qtron(object):

    def __init__(self, size, parameters):
        """ parameters should be a dictionary with float values for keys alpha, epsilon and gamma
            size is how big the input pixel frame is, so with a 20x20 RGB pixel frame size is 20*20*3 """

        self.weights = self.init_weights(size)
        self.alpha = parameters['alpha']
        self.epsilon = parameters['epsilon']
        self.gamma = parameters['gamma']
        self.value = 0.0 #np.random.random()

    def init_weights(self, size):
        """ creates random weights between -0.5 and 0.5 for all inputs and the bias added in forward_pass()"""

        w = np.random.uniform(-0.5, 0.5, size + 1) # creates array with length size
        return w

    def get_max_q(self, actions, q2_state):
        """ iterates over the qtrons in the 'actions' dictionary to find highest q-value """

        action_values = [ qtron.forward_pass(q2_state) for qtron in actions.values() ]

        maxQ = max(action_values)

        return maxQ

    def update(self, states, reward, actions):
        """ updates qtron value """

        # this first self.value assign is redundant in all steps except first time action is taken
        self.value = self.forward_pass(states[0])
        #logging.debug("q-tron value is now %s" % (self.value))

        # get maxQ based on the state we observed after action was taken
        # maxQ is potential future reward
        maxQ = self.get_max_q(actions, states[1])
        #logging.debug("maxQ is: %s" % (maxQ))

        # update weights of this qtron with backpropagation
        self.back_propagate(reward, maxQ)

        # update qtron value with the new weights
        self.value = self.forward_pass(states[0])
        #logging.debug("new qtron value is: %s" % (self.value))


    def sigmoid(self, x):
        """ returns the sigmoid value of input 'x' """

        #logging.debug("sigmoid received %s as input" % (x))
        return 1.0 / ( 1.0 + np.exp(-x) )

    def forward_pass(self, state):
        """ calculates q-value for input 'state' """

        biased_state = np.copy(state) # creates a copy of state
        biased_state = np.append(biased_state, 1) # adds the bias

        return self.sigmoid( np.dot(self.weights, biased_state) )

    def back_propagate(self, reward, maxQ):
        """ computes error gradient and backprops it to update weights """

        error = self.alpha * (reward + self.gamma*maxQ - self.value)
        #logging.debug("error is now %s" % (error))

        # sigmoid derivate is sigmoid(x) * (1 - sigmoid(x) )
        dsig = self.value * (1 - self.value)

        gradient = error * dsig
        #logging.debug("gradient is now: %s" % (gradient))

        self.weigths = np.add( self.weights, np.multiply(gradient, self.weights) )
        # self.weights = [gradient * w + w for w in self.weights]

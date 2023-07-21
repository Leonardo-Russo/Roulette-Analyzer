import numpy as np

class lobby:

    def __init__(self, name, history, update = 0, after = 0):
        self.name = name
        self.history = history
        self.update = update
        self.after_dozens = after
        self.after_colors = after
        self.after_evorodd = after

    def summary(self, N_max):

        if np.size(self.history) <= (N_max-1):
            history = self.history
        else:
            history = self.history[0:N_max]

        hstr = str(history).replace('[', '').replace(']', '')

        return '{} [{}]:\n{}\n'.format(self.name, np.size(history), hstr)


class setting:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        
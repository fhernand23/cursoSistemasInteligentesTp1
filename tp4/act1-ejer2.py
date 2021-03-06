#######################################################################
# Copyright (C)                                                       #
# 2016-2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)             #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# windygridworld definition
# world height
WORLD_HEIGHT = 7
# world width
WORLD_WIDTH = 10
# wind strength for each column
WIND = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

# possible actions
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3
ACTION_UP_LEFT = 4
ACTION_UP_RIGHT = 5
ACTION_DOWN_LEFT = 6
ACTION_DOWN_RIGHT = 7
ACTION_WAIT = 8

# probability for exploration - learning rate
EPSILON = 0.1
# Step size
ALPHA = 0.6
# discount factor - importance of future rewards
DISCOUNT_FACTOR=1.0

# reward for each step
REWARD = -1.0

START = [3, 0]
GOAL = [3, 7]
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT,
           ACTION_UP_LEFT, ACTION_UP_RIGHT, ACTION_DOWN_LEFT, ACTION_DOWN_RIGHT, ACTION_WAIT]

def step(state, action):
    i, j = state
    if action == ACTION_UP:
        return [max(i - 1 - WIND[j], 0), j]
    elif action == ACTION_DOWN:
        return [max(min(i + 1 - WIND[j], WORLD_HEIGHT - 1), 0), j]
    elif action == ACTION_LEFT:
        return [max(i - WIND[j], 0), max(j - 1, 0)]
    elif action == ACTION_RIGHT:
        return [max(i - WIND[j], 0), min(j + 1, WORLD_WIDTH - 1)]
    elif action == ACTION_UP_LEFT:
        return [max(i - 1 - WIND[j], 0), max(j - 1, 0)]
    elif action == ACTION_UP_RIGHT:
        return [max(i - 1 - WIND[j], 0), min(j + 1, WORLD_WIDTH - 1)]
    elif action == ACTION_DOWN_LEFT:
        return [max(min(i + 1 - WIND[j], WORLD_HEIGHT - 1), 0), max(j - 1, 0)]
    elif action == ACTION_DOWN_RIGHT:
        return [max(min(i + 1 - WIND[j], WORLD_HEIGHT - 1), 0), min(j + 1, WORLD_WIDTH - 1)]
    elif action == ACTION_WAIT:
        return [max(i - WIND[j], 0), j]
    else:
        assert False

# play for an episode
def episode(q_value):
    # track the total time steps in this episode
    time = 0

    # initialize state
    state = START

    # choose an action based on epsilon-greedy algorithm
    if np.random.binomial(1, EPSILON) == 1:
        action = np.random.choice(ACTIONS)
    else:
        values_ = q_value[state[0], state[1], :]
        action = np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])

    # keep going until get to the goal state
    while state != GOAL:
        next_state = step(state, action)
        if np.random.binomial(1, EPSILON) == 1:
            next_action = np.random.choice(ACTIONS)
        else:
            values_ = q_value[next_state[0], next_state[1], :]
            next_action = np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])

        # Q-Learning algorithm: Off-policy TD control.
        # Finds the optimal greedy policy while improving following an epsilon-greedy policy
        q_value[state[0], state[1], action] += ALPHA * (
                REWARD + DISCOUNT_FACTOR * np.max(q_value[next_state[0], next_state[1], :]) - q_value[state[0], state[1], action])

        state = next_state
        action = next_action
        time += 1
    return time

def run_qlearning_1_2(num_episodes):
    q_value = np.zeros((WORLD_HEIGHT, WORLD_WIDTH, 9))

    steps = []
    ep = 0
    while ep < num_episodes:
        steps.append(episode(q_value))
        # time = episode(q_value)
        # episodes.extend([ep] * time)
        ep += 1

    steps = np.add.accumulate(steps)

    plt.plot(steps, np.arange(1, len(steps) + 1))
    plt.xlabel('Time steps')
    plt.ylabel('Episodes')

    plt.savefig('./images/figure_1_2.png')
    plt.close()

    # display the optimal policy
    optimal_policy = []
    for i in range(0, WORLD_HEIGHT):
        optimal_policy.append([])
        for j in range(0, WORLD_WIDTH):
            if [i, j] == GOAL:
                optimal_policy[-1].append('G ')
                continue
            bestAction = np.argmax(q_value[i, j, :])
            if bestAction == ACTION_UP:
                optimal_policy[-1].append('˄ ')
            elif bestAction == ACTION_DOWN:
                optimal_policy[-1].append('˅ ')
            elif bestAction == ACTION_LEFT:
                optimal_policy[-1].append('< ')
            elif bestAction == ACTION_RIGHT:
                optimal_policy[-1].append('> ')
            elif bestAction == ACTION_WAIT:
                optimal_policy[-1].append('= ')
            elif bestAction == ACTION_UP_LEFT:
                optimal_policy[-1].append('˄<')
            elif bestAction == ACTION_UP_RIGHT:
                optimal_policy[-1].append('˄>')
            elif bestAction == ACTION_DOWN_LEFT:
                optimal_policy[-1].append('˅<')
            elif bestAction == ACTION_DOWN_RIGHT:
                optimal_policy[-1].append('˅>')
    print('Optimal policy is:')
    for row in optimal_policy:
        print(row)
    print('Wind strength for each column:\n{}'.format(['0'+str(w) for w in WIND]))

# Train the model
print("Training model")
# run 500 episodes
run_qlearning_1_2(500)
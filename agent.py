import random
from collections import deque

import pygame as pg
import numpy as np
import torch

from game import GameScreenRender
from model import Linear, QTrainer

# Parameters
BATCH_SIZE = 100
LR = 0.001
MAX_MEMORY = 100000
MAX_EPSILON = 100
STATE_LEN = 9
GAMMA = 0.9


class Agent():
    def __init__(self):
        self.epsilon = 0
        self.num_games = 0
        self.gamma = GAMMA
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear(STATE_LEN, 4*STATE_LEN, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_action(self, state):
        self.epsilon = MAX_EPSILON - self.num_games
        final_move = [0, 0]

        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,1)
            final_move[move] = 1
        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def train_short_memory(self, state, action, reward, new_state, done):
        self.trainer.train_step(state, action, reward, new_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def remember(self, state, action, reward, new_state, done):
        self.memory.append((state, action, reward, new_state, done))

    def train(self, game):
        plot_scores = []
        plot_mean_scores = []
        self.total_score = 0
        self.best_score = 0
        
        while True:
            [exit() for event in pg.event.get() if event.type==pg.QUIT]
            # Get current state
            state = np.array(game.get_state(), dtype=float)

            # Get move based on current state
            action = self.get_action(state)

            # Perform action  
            reward, done, score = game.frame_step(action) 

            print(reward)

            # Get new state
            new_state = np.array(game.get_state(), dtype=float)

            # Train short-term memory
            self.train_short_memory(state, action, reward, new_state, done)

            # Remember
            agent.remember(state, action, reward, new_state, done)

            if done:
                # Train long-term memory and plot result
                game.reset()
                agent.num_games += 1
                agent.train_long_memory()

                if score > self.best_score:
                    self.best_score = score
                    agent.model.save()

                print('Game: ', agent.num_games, 'Score: ', score, 'Record: ', self.best_score)


if __name__=="__main__":
    agent = Agent()
    game = GameScreenRender()
    agent.train(game)
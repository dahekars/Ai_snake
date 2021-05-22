import torch 
import random
import numpy as np
from game1 import SnakeGame, Direction, Point
from collections import deque

MAX_memory = 100_000
Batch_size = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_memory)


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x -20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y -20)
        point_d = Point(head.x, head.y + 20)
        
    def remember(self, state, action, reward, next_state, done):
        pass
    def train_long_memory(self):
        pass
    def train_short_memory(self):
        pass
    def get_action(self, state):
         pass


def train():
    plat_score = []
    plot_mean_score = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame()
    while True:
        state_old = agent.get_state(game)
        final_moves = agent.get_action(state_old)
        reward, done, score = game.play_step(final_moves)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_moves, reward, state_new, done)
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
            
            print("Game", agent.n_games, "Score", score, "Record:", record)


if __name__ == "__main__":
    train()


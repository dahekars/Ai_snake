import torch 
import random
import numpy as np
from game1 import SnakeGame, Direction, Point
from collections import deque
from model import Linear_Qnet, Qtrain
from helper import plot

MAX_memory = 100_000
Batch_size = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_memory)
        self.model = Linear_Qnet(11, 256, 3)
        self.trainer = Qtrain(self.model, lr = LR, gamma = self.gamma)


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x -20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y -20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            #danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_u and game.is_collision(point_u)),

            #danger RIGHT
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            #danger LEFT
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u, 
            dir_d, 

            #Food location
            game.food.x < game.head.x, 
            game.food.x > game.head.x, 
            game.food.y < game.head.y,
            game.food.y > game.head.y
        ]

        return np.array(state, dtype=int) 

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def train_long_memory(self):
        if len(self.memory)< Batch_size:
            mini_sample = random.sample(self.memory, Batch_size)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, next_state, done in mini_sample: ##for test


    def train_short_memory(self,state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move


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
                agent.model.save()
            print("Game", agent.n_games, "Score", score, "Record:", record)
            plat_score.append(score)
            total_score += score
            mean_scores = total_score/agent.n_games
            plot_mean_score .append(mean_scores)
            plot(plat_score, plot_mean_score)

if __name__ == "__main__":
    train()


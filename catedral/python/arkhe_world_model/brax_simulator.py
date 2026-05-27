#!/usr/bin/env python3
import numpy as np

class SimulationConfig:
    pass

class ArkheBraxSimulator:
    def __init__(self, scene="pendulum"):
        self.scene = scene

    def reset(self, seed=42):
        return {"x": np.zeros(3), "qd": np.zeros(6)}

    def step(self, state, action):
        state["x"] += action[:3]
        state["qd"][:3] += action[3:6]
        return state

    def get_world_embedding(self, state):
        return np.concatenate((state["x"], state["qd"], np.zeros(256 - 9)))

    def get_trajectory_embedding(self, window=5):
        return np.zeros(256)

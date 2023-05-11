from custom_env import CustomEnv

import os

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

env = CustomEnv(training=True, step_size=14)
monitor_env = Monitor(env)

log_path = os.path.join("Training", "Logs")
model = PPO("MlpPolicy", monitor_env, verbose=1, tensorboard_log=log_path)
model.learn(total_timesteps=int(1000))

model.save('Model')
evaluate_policy(model, monitor_env, n_eval_episodes=10)
print("done")
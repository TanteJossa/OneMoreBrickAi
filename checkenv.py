from stable_baselines3.common.env_checker import check_env
from custom_env import CustomEnv

env = CustomEnv()

episodes = 50
# It will check your custom environment and output additional warnings if needed
for episode in range(episodes):
	done = False
	obs = env.reset()
	while not done:#not done:
		random_action = env.action_space.sample()
		print("action",random_action)
		obs, reward, done, info = env.step(random_action)
		print('reward',reward)
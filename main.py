import os
import sys
import pickle
import pandas
import utils

if "SUMO_HOME" in os.environ:
  tools = os.path.join(os.environ["SUMO_HOME"], "tools")
  sys.path.append(tools)
else:
  sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumo_rl import SumoEnvironment
from sumo_rl.agents import QLAgent
from sumo_rl.exploration import EpsilonGreedy

if __name__ == "__main__":
  scenario = utils.Scenario("4x4")

  env = SumoEnvironment(
    net_file=scenario.network_file(),
    route_file=scenario.route_file(),
    use_gui=False,
    num_seconds=scenario.config.sumo.seconds,
    min_green=scenario.config.sumo.min_green,
    delta_time=scenario.config.sumo.delta_time,
  )

  for run in range(scenario.config.training.runs):
    initial_states = env.reset()
    ql_agents = {
      ts: QLAgent(
        starting_state=env.encode(initial_states[ts], ts),
        state_space=env.observation_space,
        action_space=env.action_space,
        alpha=scenario.config.agent.alpha,
        gamma=scenario.config.agent.gamma,
        exploration_strategy=EpsilonGreedy(
          initial_epsilon=scenario.config.agent.initial_epsilon,
          min_epsilon=scenario.config.agent.min_epsilon,
          decay=scenario.config.agent.decay),
      )
      for ts in env.ts_ids
    }

    for episode in range(scenario.config.training.episodes):
      if episode != 0:
        initial_states = env.reset()
        for ts in initial_states.keys():
          ql_agents[ts].state = env.encode(initial_states[ts], ts)

      done = {"__all__": False}
      while not done["__all__"]:
        actions = {ts: ql_agents[ts].act() for ts in ql_agents.keys()}
        s, r, done, info = env.step(action=actions)
        for agent_id in s.keys():
          ql_agents[agent_id].learn(next_state=env.encode(s[agent_id], agent_id), reward=r[agent_id])

      path = scenario.metrics_file(run, episode)
      pandas.DataFrame(env.metrics).to_csv(path, index=False)
      for ts, agent in ql_agents.items():
        path = scenario.agents_file(run, episode, ts)
        with open(path, "wb") as file:
          pickle.dump(agent.q_table, file)
  env.close()

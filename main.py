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

RECICLE=True

from sumo_rl import SumoEnvironment
from sumo_rl.agents import QLAgent
from sumo_rl.exploration import EpsilonGreedy

if __name__ == "__main__":
  scenario = utils.Scenario("nuovo")

  env = scenario.new_sumo_environment()
  for run in range(scenario.config.training.runs):
    initial_states = env.reset()
    ql_agents = {}
    for ts in env.ts_ids:
      if RECICLE:
        ql_agents[ts] = scenario.load_or_new_agent(env, run, ts, initial_states[ts])
      else:
        ql_agents[ts] = scenario.new_agent(env, ts, initial_states[ts])

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
    for ts, agent in ql_agents.items():
      path = scenario.agents_file(run, None, ts)
      with open(path, "wb") as file:
        pickle.dump(agent.q_table, file)
  env.close()

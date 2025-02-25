import os
import sys
import pickle
import pandas
import utils
import argparse

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
  cli = argparse.ArgumentParser(sys.argv[0])
  cli.add_argument('-s', '--scenario', type=str, default='prism2', choices=['4x4', 'prism2', 'fiore'])
  cli.add_argument('-f', '--fixed', action="store_true", default=False)
  cli_args = cli.parse_args(sys.argv[1:])
  scenario = utils.Scenario(cli_args.scenario)

  env = scenario.new_sumo_environment(cli_args.fixed)
  for run in range(scenario.config.training.runs):
    initial_states = env.reset()
    ql_agents = {}
    if not cli_args.fixed:
      for ts in env.ts_ids:
        if RECICLE:
          ql_agents[ts] = scenario.load_or_new_agent(env, run, ts, initial_states[ts])
        else:
          ql_agents[ts] = scenario.new_agent(env, ts, initial_states[ts])

    for episode in range(scenario.config.training.episodes):
      if episode != 0:
        env.sumo_seed = int(env.sumo_seed) + 1
        initial_states = env.reset()
        if not cli_args.fixed:
          for ts in initial_states.keys():
            ql_agents[ts].state = env.encode(initial_states[ts], ts)

      done = {"__all__": False}
      while not done["__all__"]:
        if not cli_args.fixed:
          actions = {ts: ql_agents[ts].act() for ts in ql_agents.keys()}
          s, r, done, info = env.step(action=actions)
          for agent_id in s.keys():
            ql_agents[agent_id].learn(next_state=env.encode(s[agent_id], agent_id), reward=r[agent_id])
        else:
          s, r, done, info = env.step(action={})

      path = scenario.metrics_file(run, episode)
      pandas.DataFrame(env.metrics).to_csv(path, index=False)
      if not cli_args.fixed:
        for ts, agent in ql_agents.items():
          path = scenario.agents_file(run, episode, ts)
          with open(path, "wb") as file:
            pickle.dump(agent.q_table, file)
    if not cli_args.fixed:
      for ts, agent in ql_agents.items():
        path = scenario.agents_file(run, None, ts)
        with open(path, "wb") as file:
          pickle.dump(agent.q_table, file)
  env.close()

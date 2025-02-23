import os
import yaml

class SumoConfig:
  def __init__(self, data: dict):
    self.seconds: int = data['seconds']
    self.min_green: int = data['min_green']
    self.delta_time: int = data['delta_time']

class AgentConfig:
  def __init__(self, data: dict):
    self.alpha: float = data['alpha']
    self.gamma: float = data['gamma']
    self.initial_epsilon: float = data['initial_epsilon']
    self.min_epsilon: float = data['min_epsilon']
    self.decay: int = data['decay']

class TrainingConfig:
  def __init__(self, data: dict):
    self.runs: int = data['runs']
    self.episodes: int = data['episodes']

class Config:
  def __init__(self, data: dict):
    self.sumo: SumoConfig = SumoConfig(data['sumo'])
    self.agent: AgentConfig = AgentConfig(data['agent'])
    self.training: TrainingConfig = TrainingConfig(data['training'])
  
  @staticmethod
  def from_file(filepath: str):
    with open(filepath, "r") as file:
      return Config(yaml.load(file, Loader=yaml.Loader))

class Scenario:
  def __init__(self, name: str) -> None:
    self.name = name
    self.config = Config.from_file(self.config_file())

  def ensure_dir(self, dir: str) -> str:
    if not os.path.exists(dir):
      os.makedirs(dir)
    return dir

  def config_file(self, ) -> str:
    return './scenarios/%s/config.yml' % self.name

  def agents_dir(self, run: int, episode: int) -> str:
    return self.ensure_dir("./outputs/%s/agents/%s/%s" % (self.name, run, episode))

  def agents_file(self, run: int, episode: int, agent: int) -> str:
    return "./%s/%s.pickle" % (self.agents_dir(run, episode), agent)

  def metrics_dir(self, run: int) -> str:
    return self.ensure_dir("./outputs/%s/metrics/%s" % (self.name, run))

  def metrics_file(self, run: int, episode: int) -> str:
    return "./%s/%s.csv" % (self.metrics_dir(run), episode)

  def plots_dir(self, run: int) -> str:
    return self.ensure_dir("./outputs/%s/plots/%s" % (self.name, run))

  def plots_file(self, run: int, episode: int|None) -> str:
    if episode is None:
      return "./%s/summary.png" % (self.plots_dir(run))
    return "./%s/%s.png" % (self.plots_dir(run), episode)

  def network_file(self, ) -> str:
    return "./scenarios/%s/network.net.xml" % self.name

  def route_file(self, ) -> str:
    return "./scenarios/%s/routes.rou.xml" % self.name

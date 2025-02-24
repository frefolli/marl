import pandas
import matplotlib.pyplot
import utils

def load_metrics(scenario: utils.Scenario) -> dict[int, dict[int, pandas.DataFrame]]:
  metrics = {}
  for run in range(scenario.config.training.runs):
    metrics[run] = {}
    for episode in range(scenario.config.training.episodes):
      metrics[run][episode] = pandas.read_csv(scenario.metrics_file(run, episode))
  return metrics

def plot_single_metrics(metrics: dict[int, dict[int, pandas.DataFrame]], metric: str):
  for run in metrics:
    for episode in metrics[run]:
      df = metrics[run][episode]
      figure = matplotlib.pyplot.figure(figsize=(20, 10))
      matplotlib.pyplot.plot(df['step'], df[metric], marker='o')
      matplotlib.pyplot.title('Metric %s for run %s / episode %s' % (metric, run, episode))
      matplotlib.pyplot.savefig(scenario.plots_file(run, episode))

def plot_summary_metrics(metrics: dict[int, dict[int, pandas.DataFrame]], metric: str):
  for run in metrics:
    figure = matplotlib.pyplot.figure(figsize=(20, 10))
    Ys = []
    for episode in metrics[run]:
      df = metrics[run][episode]
      Ys += list(df[metric])
    Xs = [_ for _ in range(len(Ys))]
    matplotlib.pyplot.plot(Xs, Ys, marker='o')
    matplotlib.pyplot.title('Metric %s for run %s' % (metric, run))
    matplotlib.pyplot.savefig(scenario.plots_file(run, None))

if __name__ == "__main__":
  metric='system_mean_waiting_time'
  scenario = utils.Scenario('nuovo')
  metrics = load_metrics(scenario)
  plot_single_metrics(metrics, metric)
  plot_summary_metrics(metrics, metric)

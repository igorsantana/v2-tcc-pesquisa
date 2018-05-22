import types

class Config:
  def __init__(self, args):
    self.args = args
    self.dataset      = args.dataset[0].split('=')[1]
    self.baseline     = args.baseline[0].split('=')[1]
    self.config       = args.config[0].split('=')[1]
    self.recommender  = args.recommender[0].split('=')[1]
    if isinstance(args.metrics, str):
      self.metrics = args.metrics.split(',')
    else:
      self.metrics = args.metrics[0].split('=')[1].split(',')

  def get_dataset(self):
    return self.dataset
  def get_baseline(self):
    return self.baseline
  def get_config(self):
    return self.config
  def get_recommender(self):
    return self.recommender
  def get_metrics(self):
    return self.metrics
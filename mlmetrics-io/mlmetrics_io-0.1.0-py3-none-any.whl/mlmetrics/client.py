import os
from urllib import request
import json
import pandas as pd

class Metrics:
  def __init__(self, payload=None):
    self.payload = payload

  def metrics(self):
    return pd.DataFrame(self.payload["metrics"])

  def parameters(self):
    return pd.DataFrame(self.payload["parameters"])

  def attributes(self):
    return pd.DataFrame(self.payload["attributes"])
  
  def plot(self):
    # TODO: Per metrics, key - generate a plot with run_id as series.
    pass

  def save(self, filename):
    with open(filename, "w") as f:
      json.dump(self.payload, f)

  def load(self, filename):
    with open(filename, "r") as f:
      self.payload = json.load(f)


class Client:
  def __init__(self, token=None, url=None):
    if url:
      self.url = url
    else:
      self.url = os.environ.get("MLMETRICS_API_URL", "https://www.mlmetrics.io/api")

    if token:
      self.token = token
    else:
      self.token = os.environ.get("MLMETRICS_TOKEN")

  def runs(self, run_ids):
    request_url=self.url + '/runs/get?run_ids=' + ",".join(run_ids)
    req = request.Request(request_url, method="GET")
    req.add_header('Authorization', 'Bearer ' + self.token)
    r = request.urlopen(req)
    content = r.read()
    return Metrics(json.loads(content))

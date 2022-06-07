def create(values = None):
  # "device": {
  #   "id": ...
  #   "type": ...
  # }
  record = {
    "sampleId": None,
    "analysisName": None,
    "analysisCenter": None,
    "analysisCenterSampleId":None,
    "qcFailed": None,
    "device": None,
    "calls": []
  }
  if values!=None:
    record.update(values)
  return record

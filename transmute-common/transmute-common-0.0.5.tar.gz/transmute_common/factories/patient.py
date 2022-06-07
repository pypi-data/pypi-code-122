def create(values = None):
  # "name": {
  #   "text": ...
  #   "family": ...
  #   "given": ...
  #   "prefix": ...
  #   "suffix": ...
  # }
  record = {
    "patientId": None,
    "name": None,
    "managingOrganization": None,
    "sex": None,
    "race": None,
    "ethnicity": None,
    "dateOfBirth": None
  }
  if values!=None:
    record.update(values)
  return record
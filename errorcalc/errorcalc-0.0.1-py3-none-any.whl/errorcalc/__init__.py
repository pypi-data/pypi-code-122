def errpred(val_1,val_2):
  import numpy as np
  from sklearn import metrics
  print('Mean absolute error',metrics.mean_absolute_error(val_1,val_2))
  print('Mean squared error',metrics.mean_squared_error(val_1,val_2))
  print('Root mean squared error',np.sqrt(metrics.mean_squared_error(val_1,val_2)))

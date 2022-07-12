import pandas as pd
from math import sqrt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import ensemble

df = pd.read_csv("Clean_Data_CSV.csv")

x = df[["Case Percentage", "% with Bachelor's", "Percent Democrat"]]
y = df['Vaccinated']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
parameters = {'loss':'absolute_error', 'random_state':42, 'max_depth':1}
GBM_regressor = ensemble.GradientBoostingRegressor(**parameters)
GBM_regressor.fit(x_train, y_train)


sample=x_test.loc[list(y_test.index)[-1]]
predictions = GBM_regressor.predict(x_test)
predictions_train = GBM_regressor.predict(x_train)
sample_pred = list(predictions)[-1]
print('----- Sample case -----')
print("Case Percentage:",sample[0])
print("% with Bachelor's:",sample[1])
print("Percent Democrat:",sample[2])
print('Predicted Vaccination Rate:', round(float(sample_pred), 3))
print('-----------------------\n')

print("\n--------------TEST DATA SCORES-----------------")
mae = metrics.mean_absolute_error(y_test, predictions)
mse = metrics.mean_squared_error(y_test, predictions)
print('    Mean absolute error (MAE):', mae)
print('    Root mean squared error (RMSE):', sqrt(mse)) 
print('    R-squared score:', metrics.r2_score(y_test, predictions))



print("\n--------------TRAINING DATA SCORES-----------------")
mae = metrics.mean_absolute_error(y_train, predictions_train)
mse = metrics.mean_squared_error(y_train, predictions_train)
print('    Mean absolute error (MAE):', mae)
print('    Root mean squared error (RMSE):', sqrt(mse))
print('    R-squared score:', metrics.r2_score(y_train, predictions_train))


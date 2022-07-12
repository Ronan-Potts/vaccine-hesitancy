import pandas as pd
from math import sqrt
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split

df = pd.read_csv('Clean_Data_CSV.csv')

predictors = df[["Case Percentage", "% with Bachelor's", "Percent Democrat", "Number of Cases", "Population"]]
predicted = df['Vaccinated']

predictors_train, predictors_test, predicted_train, predicted_test = train_test_split(predictors, predicted, test_size=0.2, random_state=42)
regr = linear_model.LinearRegression().fit(predictors_train, predicted_train)



sample = predictors_test.loc[list(predictors_test.index)[-1]]
new_df = pd.DataFrame([sample], columns=["Case Percentage", "% with Bachelor's", "Percent Democrat", "Number of Cases", "Population"])
sample_pred = regr.predict(new_df)
print('----- Sample case -----')
print("Case Percentage:",sample[0])
print("% with Bachelor's:",sample[1])
print("Percent Democrat:",sample[2])
print('Predicted Vaccination Rate:', round(float(sample_pred), 3))
print('-----------------------')

# The coefficients
print('Coefficients:')
print(regr.coef_)
# Use the model to predict vaccination rate from predictors_test
predicted_pred = regr.predict(predictors_test)
# Root mean squared error
mae = metrics.mean_absolute_error(predicted_test, predicted_pred)
print('Mean absolute error (MAE):', mae)
# R-squared score: 1 is perfect prediction
print('R-squared score:', metrics.r2_score(predicted_test, predicted_pred))

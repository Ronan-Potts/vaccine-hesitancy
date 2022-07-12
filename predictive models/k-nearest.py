import pandas as pd
from math import sqrt
from sklearn import metrics
from sklearn import neighbors
from sklearn.model_selection import train_test_split

df = pd.read_csv('Clean_Data_CSV.csv')

predictors = df[["Case Percentage", "% with Bachelor's", "Percent Democrat"]]
predicted = df['Vaccinated']

predictors_train, predictors_test, predicted_train, predicted_test = train_test_split(predictors, predicted, test_size=0.2, random_state=42)
neigh = neighbors.KNeighborsRegressor(n_neighbors=46).fit(predictors_train, predicted_train)

# Let's create one sample and predict the number of comments
sample = [0.2, 0.4, 0.8]        # a sample with 1000 likes and 100 dislikes
sample_pred = neigh.predict([sample])
print('----- Sample case -----')
print("Case Percentage:",sample[0])
print("% with Bachelor's:",sample[1])
print("Percent Democrat:",sample[2])
print('Predicted Vaccination Rate:', round(float(sample_pred), 2))
print('-----------------------')

# Use the model to predict X_test
predicted_pred = neigh.predict(predictors_test)
# Root mean squared error
mse = metrics.mean_squared_error(predicted_test, predicted_pred)
print('Root mean squared error (RMSE):', sqrt(mse))
# R-squared score: 1 is perfect prediction
print('R-squared score:', metrics.r2_score(predicted_test, predicted_pred))

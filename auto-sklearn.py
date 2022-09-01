import numpy as numpy
import pandas as pd
from pprint import pprint

from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from autosklearn.regression import AutoSklearnRegressor


df = pd.read_pickle("mid_concrete.pkl")  
df.drop(['point', 'anchor', 'channel'], axis=1,inplace=True)
features = ['power', 'pdda_input_real_1', 'pdda_input_real_2', 'pdda_input_imag_2', 'pdda_input_real_3', 'pdda_input_imag_3', 'pdda_input_real_4', 'pdda_input_imag_4',
           'pdda_input_real_5', 'pdda_input_imag_5']
targets = ['x_tag', 'y_tag', 'z_tag']
X = df[features].values
y = df[targets].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

automl = AutoSklearnRegressor(
    time_left_for_this_task=120,
    per_run_time_limit=30,
    tmp_folder='/auto-sklearn/',
)
automl.fit(X_train, y_train, dataset_name='libra')

print(automl.leaderboard())

############################################################################
# Print the final ensemble constructed by auto-sklearn
# ====================================================

pprint(automl.show_models(), indent=4)

###########################################################################
# Get the Score of the final ensemble
# ===================================

predictions = automl.predict(X_test)
print("R2 score:", r2_score(y_test, predictions))

###########################################################################
# Get the configuration space
# ===========================

# The configuration space is reduced, i.e. no SVM.
print(automl.get_configuration_space(X_train, y_train))

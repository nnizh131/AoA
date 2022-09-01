import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import autokeras as ak
from tensorflow.keras.models import load_model
import os

params = {
    'file_path': "mid_concrete.pkl",
    'save_path': "model_autokeras",
    'test_size': 0.33,
    'random_state': 42,
    'trials': 1,
    'max_model_size': 600000, #Maximum number of scalars in the parameters of a model
    'batch_size': 32,
    'epochs': 2
}

def prepare_data():
    print(os.getcwd())
    df = pd.read_pickle(params['file_path'])  
    df.drop(['point', 'anchor', 'channel'], axis=1,inplace=True)
    features = ['power', 'pdda_input_real_1', 'pdda_input_real_2', 'pdda_input_imag_2', 'pdda_input_real_3', 'pdda_input_imag_3',    'pdda_input_real_4',
                'pdda_input_imag_4', 'pdda_input_real_5', 'pdda_input_imag_5']
    targets = ['x_tag', 'y_tag', 'z_tag']
    X = df[features].values
    y = df[targets].values
    return train_test_split(X, y, test_size=params['test_size'], random_state=params['random_state'])


def model():
    input_node = ak.StructuredDataInput()
    output_node = ak.Normalization()(input_node)
    # output_node = ak.CategoricalToNumerical()(input_node)
    output_node = ak.DenseBlock()(output_node)
    output_node = ak.RegressionHead(output_dim=3, loss="mean_absolute_error")(output_node)
    reg = ak.AutoModel(
        inputs=input_node, 
        outputs=output_node, 
        max_trials=params['trials'], 
        overwrite=True,
        tuner='greedy',
        max_model_size=params['max_model_size']
    )
    
    return reg

def train(automodel, X_train, y_train):
    automodel.fit(X_train, y_train, batch_size=params['batch_size'], epochs=params['epochs'])
    best_model = automodel.export_model()
    try:
        best_model.save(params['save_path'], save_format="tf")
        print("Model successfully saved.")
        print(best_model.summary())
    except Exception:
        print(Exception)

def evaluate(X_test, y_test):
    try:
        loaded_model = load_model(params['save_path'], custom_objects=ak.CUSTOM_OBJECTS)
    except Exception:
        print(Exception)
    print(loaded_model.evaluate(X_test, y_test))

if __name__ == "__main__":
    X_train, y_train, X_test, y_test = prepare_data()
    automodel = model()
    print(automodel)
    train(automodel, X_train, y_train)
    # evaluate(X_test, y_test)








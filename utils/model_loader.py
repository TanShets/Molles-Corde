import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.metrics import categorical_accuracy, Accuracy, CategoricalAccuracy, SparseCategoricalAccuracy
import sys
sys.path.append('../molles_corde')
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def accuracy(Y_true, Y_pred):
    m = CategoricalAccuracy()
    m.update_state(Y_true, Y_pred)
    return m.result().numpy()

def get_model(name):
    addr = BASE_DIR.__str__().replace("\\", '/')
    linker = {
        'chd': addr + '/Models/CHDdata.h5',
        'cvd': addr + '/Models/CVD.h5',
        'hypertension': addr + '/Models/model1_hypertension.h5',
        'arrhythmia': addr + '/Models/Arrhythmia2.h5',
        'general': addr + '/Models/model3.h5'
    }
    
    if linker.get(name, None) is None:
        return None
    else:
        return load_model(linker.get(name))

def normalize_input(X, name):
    # Assumption: X is a dataframe
    addr = addr = BASE_DIR.__str__().replace("\\", '/')
    if name == 'chd':
        fp = open(addr + '/Models/CHDdata/col_names.txt', 'r')
        line = list(fp.readline().strip().split(','))
        fp.close()
        X_min = np.load(addr + '/Models/CHDdata/min.npy')
        X_max = np.load(addr + '/Models/CHDdata/max.npy')
        X[line] = (X[line] - X_min) / (X_max - X_min)
    elif name == 'cvd':
        line = np.load(addr + '/Models/CVD/labels6.npy').tolist()
        X_min = np.load(addr + '/Models/CVD/min6.npy')
        X_max = np.load(addr + '/Models/CVD/max6.npy')
        X[line] = (X[line] - X_min) / (X_max - X_min)
    elif name == 'hypertension':
        pass
    elif name == 'arrhythmia':
        line = np.load(addr + '/Models/Arrhythmia/labels.npy').tolist()[:-1]
        X_min = np.load(addr + '/Models/Arrhythmia/min.npy')
        X_max = np.load(addr + '/Models/Arrhythmia/max.npy')
        X[line] = (X[line] - X_min) / (X_max - X_min)
    elif name == 'general':
        X_min = np.load(addr + '/Models/gen_model_2/gen_min.npy')[:8]
        X_max = np.load(addr + '/Models/gen_model_2/gen_max.npy')[:8]
        X = (X - X_min) / (X_max - X_min)
    
    return np.array(X)

def get_model_result(X, name):
    X_in = normalize_input(X, name)
    model = get_model(name)
    # print(model.summary())
    if model is None:
        return None
    # print(model.predict(aaa))
    # print(model.predict(X_in))
    return model.predict(X_in)
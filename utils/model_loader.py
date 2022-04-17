import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import sys
sys.path.append('../molles_corde')
from settings import BASE_DIR

def get_model(name):
    addr = BASE_DIR.__str__().replace("\\", '/')
    linker = {
        'chd': addr + '/Models/CHDdata.h5',
        'cvd': addr + '/Models/CVD.h5',
        'hypertension': addr + '/Models/model1_hypertension.h5',
        'arrhythmia': addr + '/Models/Arrhythmia2.h5',
        'general': addr + '/Models/gen_model_2/model2.h5'
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
        X_min = np.load(addr + '/Models/Arrhythmia/min.npy')
        X_max = np.load(addr + '/Models/Arrhythmia/max.npy')
        X = (X - X_min) / (X_max - X_min)
    return np.array(X)

def get_model_result(X, name):
    X_in = normalize_input(X, name)
    model = get_model(name)
    if model is None:
        return None
    
    return model.predict(X)
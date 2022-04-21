from django.shortcuts import render, redirect
import sys
sys.path.append('../utils')
from utils import model_loader
import numpy as np
import pandas as pd
import copy, io

def process_Hyp(data):
    X = dict()
    names1 = [
        'masl', 'sex', 'age', 'systolic_bp', 'diastolic_bp', 'weight', 'height', 'bmi', 
        'diabetes_mellitus', 'cv_diseases', 'smoke', 'physical_activity', 'sist_old', 
        'diast_old', 'sist_new', 'diast_new', 'BMI_cat'
    ]

    names2 = [
        'masl', 'sex', 'age_years', 'systolic_bp', 'diastolic_bp', 'weight_kg', 'height_cm', 'body_mass_index', 
        'diabetes_mellitus', 'cv_diseases', 'smoking', 'physical_activity', 'sist_old', 
        'diast_old', 'sist_new', 'diast_new', 'BMI_cat'
    ]
    
    for i in range(len(names1)):
        X[names2[i]] = data[names1[i]]
    X['height_cm'] *= 100
    X = pd.DataFrame(X)
    return model_loader.get_model_result(X, 'hypertension')

def process_Arr(data):
    X = dict()
    names = [
        'age', 'height', 'weight', 'qrs_duration', 'p-r_interval', 'q-t_interval', 
        't_interval', 'p_interval', 'qrs', 'T', 'P', 'QRST', 'J', 'heart_rate', 'Q wave', 
        'R wave', 'S wave', "R' wave", "S' wave", 'no_of_deflections', 'Ragged R wave', 
        'Diphasic Derivation of R wave', 'Ragged P wave', 'Diphasic Derivation of P wave', 
        'Ragged T wave', 'Diphasic Derivation of T wave', 'JJ wave Amp', 'Q wave Amp', 
        'R wave Amp', 'S wave Amp', "R' wave Amp", "S' wave Amp", 'P wave Amp', 'T wave Amp', 
        'QRSA', 'QRSTA', 'sex'
    ]
    
    for i in names:
        X[i] = data[i]
    X = pd.DataFrame(X)
    return model_loader.get_model_result(X, 'arrhythmia')

def process_CHD(data):
    X = dict()
    names1 = [
        'systolic_bp', 'tobacco_consumed', 'ldl', 'adiposity', 'famhist', 'typea', 
        'bmi', 'alcohol_consumed', 'age'
    ]
    names2 = [
        'sbp', 'tobacco', 'ldl', 'adiposity', 'famhist', 'typea', 
        'obesity', 'alcohol', 'age'
    ]
    
    for i in range(len(names1)):
        X[names2[i]] = data[names1[i]]
    
    X = pd.DataFrame(X)
    return model_loader.get_model_result(X, 'chd')

def process_CVD(data):
    X = dict()
    names1 = [
        'age', 'sex', 'height', 'weight', 'systolic_bp', 'diastolic_bp', 'cholesterol', 'gluc',
        'smoke', 'alcohol', 'physical_activity'
    ]
    names2 = [
        'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
        'smoke', 'alco', 'active'
    ]
    
    for i in range(len(names1)):
        X[names2[i]] = data[names1[i]]
    
    X = pd.DataFrame(X)
    return model_loader.get_model_result(X, 'cvd')

def DiagnosisHome(request):
    context = {
        'title': 'Home',
        'isComplete': False
    }
    if request.method != 'POST':
        return render(request, 'diagnosis/diagnosis_home.html', context)
    elif int(request.POST.get('id')) == 1:
        X = dict()
        X['age'] = [float(request.POST.get('age', 21))]
        X['bmi'] = [float(request.POST.get('weight')) / (float(request.POST.get('height'))**2)]
        X['sex'] = [int(request.POST.get('sex'))]
        X['smoke'] = [int(request.POST.get('smoke'))]
        X['alcohol'] = [int(request.POST.get('alcohol'))]
        X['physical_activity'] = [int(request.POST.get('physical_activity'))]
        X['heart_rate'] = [float(request.POST.get('heart_rate'))]
        X['cholesterol'] = [int(request.POST.get('cholesterol', 0))]
        x = X
        X = pd.DataFrame(X)
        print(X)
        Y = model_loader.get_model_result(X, 'general')
        print(Y)
        outputs = [0, 0, 0, 0]
        needsRunning = [False, False, False, False]
        names = ['diagnosis-hyp', 'diagnosis-arr', 'diagnosis-chd', 'diagnosis-cvd']
        for i in range(Y.shape[1]):
            if Y[0, i] >= 0.2:
                needsRunning[i] = True
        request.session['X'] = x
        request.session['X']['weight'] = [float(request.POST.get('weight'))]
        request.session['X']['height'] = [float(request.POST.get('height'))]
        request.session['outputs'] = outputs
        request.session['needsRunning'] = needsRunning
        request.session['names'] = names
        request.session.modified = True
        
        for i in range(len(needsRunning)):
            if needsRunning[i]:
                return redirect(names[i])
        print(request.session['outputs'])
        del request.session['outputs']
        del request.session['needsRunning']
        del request.session['X']
        request.session.modified = True
        return render(request, 'diagnosis/diagnosis_home.html', context)
    else:
        fp = request.FILES['file']
        data = pd.read_csv(io.StringIO(fp.read().decode('utf-8')), delimiter = ',')
        data = data.drop('Unnamed: 0', axis = 1)
        X = dict()
        X['age'] = data['age']
        X['bmi'] = data['bmi']
        X['sex'] = data['sex']
        X['smoke'] = data['smoke']
        X['alcohol'] = data['alcohol']
        X['physical_activity'] = data['physical_activity']
        X['heart_rate'] = data['heart_rate']
        X['cholesterol'] = data['cholesterol']
        # X['systolic_bp'] = data['systolic_bp']
        x = X
        X = pd.DataFrame(X)
        # Y = model_loader.get_model_result(X, 'general')
        Y = model_loader.get_model_result(X, 'general')
        indices = [[] for _ in range(4)]
        for i in range(Y.shape[0]):
            for j in range(Y.shape[1]):
                if Y[i, j] >= 0.2:
                    indices[j].append(i)
        Ys = []
        if len(indices[0]) > 0:
            Y_1 = process_Hyp(data.iloc[indices[0]])
            Ys.append(Y_1)
            Y[indices[0], 0] = Y_1.reshape(Y_1.shape[0])
        
        if len(indices[1]) > 0:
            Y_2 = process_Arr(data.iloc[indices[1]])
            Ys.append(Y_2)
            Y[indices[1], 1] = Y_2.reshape(Y_2.shape[0])
        
        if len(indices[2]) > 0:
            Y_3 = process_CHD(data.iloc[indices[2]])
            Ys.append(Y_3)
            Y[indices[2], 2] = Y_3.reshape(Y_3.shape[0])
        
        if len(indices[3]) > 0:
            Y_4 = process_CVD(data.iloc[indices[3]])
            Ys.append(Y_4)
            Y[indices[3], 3] = Y_4.reshape(Y_4.shape[0])
        # print(Y_1 is None, Y_2 is None, Y_3 is None, Y_4 is None)

        for i in range(len(indices)):
            for j in range(len(indices[i])):
                # if Ys[i] is None or Y is None or Y[indices[i]] is None:
                    # print(i, j)
                    # print(Ys[i], Y[indices[i]])
                Y[indices[i][j], i] = Ys[i][j]

        print(model_loader.accuracy(data[['hyp', 'arrhythmia', 'chd', 'cvd']].to_numpy(), Y))
        return redirect('diagnosis-home')

def DiagnosisCVD(request):
    context = {
        'title': 'CHD Diagnosis',
        'isComplete': False
    }
    if request.method != 'POST':
        return render(request, 'diagnosis/diagnosis_cvd.html', context)
    else:
        if 'X' in request.session:
            stored_vals = request.session['X']
        else:
            print('Session did not move here:')
            return render(request, 'diagnosis/diagnosis_cvd.html', context)
        X = dict()
        X['age'] = stored_vals['age']
        X['gender'] = stored_vals['sex']
        X['height'] = stored_vals['height']
        X['weight'] = stored_vals['weight']
        X['ap_hi'] = [float(request.POST.get('ap_hi'))]
        X['ap_lo'] = [float(request.POST.get('ap_lo'))]
        X['cholesterol'] = stored_vals['cholesterol']
        X['gluc'] = [float(request.POST.get('gluc'))]
        X['smoke'] = stored_vals['smoke']
        X['alco'] = stored_vals['alcohol']
        X['active'] = stored_vals['physical_activity']
        X = pd.DataFrame(X)
        print(X)
        Y = model_loader.get_model_result(X, 'cvd')
        request.session['outputs'][3] = Y[0, 0]
        request.session['needsRunning'][3] = False
        request.session.modified = True
        print(request.session['outputs'])
        del request.session['outputs']
        del request.session['needsRunning']
        del request.session['X']
        request.session.modified = True
        return redirect('diagnosis-home')

def DiagnosisArrhymthmia(request):
    context = {
        'title': 'Arrhythmia',
        'isComplete': False
    }
    if request.method != 'POST':
        return render(request, 'diagnosis/diagnosis_arr.html', context)
    else:
        if 'X' in request.session:
            stored_vals = request.session['X']
        else:
            print('Session did not move here:')
            return render(request, 'diagnosis/diagnosis_arr.html', context)
        X = dict()
        X['age'] = stored_vals['age']
        X['height'] = stored_vals['height']
        X['weight'] = stored_vals['weight']
        
        names = [
            'qrs_duration', 'p-r_interval', 'q-t_interval', 't_interval', 'p_interval', 'qrs', 'T', 'P', 'QRST','J'
        ]
        for i in names:
            X[i] = [float(request.POST.get(i))]
        
        X['heart_rate'] = stored_vals['heart_rate']
        
        names = [
            'Q wave', 'R wave', 'S wave', "R' wave", "S' wave"
        ]
        for i in names:
            X[i] = [float(request.POST.get(i))]
        
        X['no_of_deflections'] = [float(request.POST.get('no_of_deflections'))]
        names = [    
            'Ragged R wave', 'Diphasic Derivation of R wave',
            'Ragged P wave', 'Diphasic Derivation of P wave', 'Ragged T wave',
            'Diphasic Derivation of T wave', 'JJ wave Amp', 'Q wave Amp',
            'R wave Amp', 'S wave Amp', "R' wave Amp", "S' wave Amp", 'P wave Amp',
            'T wave Amp', 'QRSA', 'QRSTA'
        ]
        for i in names:
            X[i] = [float(request.POST.get(i))]
        X['sex'] = stored_vals['sex']
        X = pd.DataFrame(X)
        Y = model_loader.get_model_result(X, 'arrhythmia')
        request.session['outputs'][1] = Y[0, 0]
        request.session['needsRunning'][1] = False
        request.session.modified = True
        for i in range(2, len(request.session['needsRunning'])):
            if request.session['needsRunning'][i]:
                return redirect(request.session['names'][i])
        
        print(request.session['outputs'])
        del request.session['outputs']
        del request.session['needsRunning']
        del request.session['X']
        request.session.modified = True
        return redirect('diagnosis-home')

def DiagnosisHyp(request):
    context = {
        'title': 'Hypertension',
        'isComplete': False
    }
    if request.method != 'POST':
        return render(request, 'diagnosis/diagnosis_hyp.html', context)
    else:
        if 'X' in request.session:
            stored_vals = request.session['X']
        else:
            print('Session did not move here:')
            return render(request, 'diagnosis/diagnosis_hyp.html', context)
        X = dict()
        X['masl'] = [float(request.POST.get('masl'))]
        X['sex'] = abs(stored_vals['sex'] - 1)
        X['age_years'] = stored_vals['age']
        X['systolic_bp'] = [float(request.POST.get('systolic_bp'))]
        X['diastolic_bp'] = [float(request.POST.get('diastolic_bp'))]
        X['weight_kg'] = stored_vals['weight']
        X['height_cm'] = [i * 100 for i in stored_vals['height']]
        X['body_mass_index'] = stored_vals['bmi']
        X['diabetes_mellitus'] = [float(request.POST.get('diabetes_mellitus'))]
        X['cv_diseases'] = [float(request.POST.get('cv_diseases'))]
        X['smoking'] = stored_vals['smoke']
        X['physical_activity'] = stored_vals['physical_activity']
        X['sist_old'] = [float(request.POST.get('sist_old'))]
        X['diast_old'] = [float(request.POST.get('diast_old'))]
        X['sist_new'] = [float(request.POST.get('sist_new'))]
        X['diast_new'] = [float(request.POST.get('diast_new'))]
        X['BMI_cat'] = [int(request.POST.get('BMI_cat'))]
        print(X)
        X = pd.DataFrame(X)
        print(X)
        Y = model_loader.get_model_result(X, 'hypertension')
        print(Y)

        request.session['outputs'][0] = Y[0, 0]
        request.session['needsRunning'][0] = False
        request.session.modified = True

        for i in range(1, len(request.session['needsRunning'])):
            if request.session['needsRunning'][i]:
                return redirect(request.session['names'][i])
        print(request.session['outputs'])
        del request.session['outputs']
        del request.session['needsRunning']
        del request.session['X']
        request.session.modified = True
        return redirect('diagnosis-home')
        # return render(request, 'diagnosis/diagnosis_hyp.html', context)

def DiagnosisCHD(request):
    context = {
        'title': 'CHD Diagnosis',
        'isComplete': False
    }
    if request.method != 'POST':
        return render(request, 'diagnosis/diagnosis_chd.html', context)
    else:
        if 'X' in request.session:
            stored_vals = request.session['X']
        else:
            print('Session did not move here:')
            return render(request, 'diagnosis/diagnosis_chd.html', context)
        X = dict()
        X['sbp'] = [float(request.POST.get('sbp'))]
        X['tobacco'] = [float(request.POST.get('tobacco'))]
        X['ldl'] = [float(request.POST.get('ldl'))]
        X['adiposity'] = [float(request.POST.get('adiposity'))]
        X['famhist'] = [int(request.POST.get('famhist'))]
        X['typea'] = [float(request.POST.get('typea'))]
        X['obesity'] = stored_vals['bmi']
        X['alcohol'] = [float(request.POST.get('alcohol'))]
        X['age'] = stored_vals['age']
        X = pd.DataFrame(X)
        print(X)
        Y = model_loader.get_model_result(X, 'chd')
        request.session['outputs'][2] = Y[0, 0]
        request.session['needsRunning'][2] = False
        request.session.modified = True
        # print(Y)
        # return render(request, 'diagnosis/diagnosis_cvd.html', context)
        for i in range(3, len(request.session['needsRunning'])):
            if request.session['needsRunning'][i]:
                return redirect(request.session['names'][i])
        print(request.session['outputs'])
        del request.session['outputs']
        del request.session['needsRunning']
        del request.session['X']
        request.session.modified = True
        return redirect('diagnosis-home')

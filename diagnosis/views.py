from django.shortcuts import render, redirect
import sys
sys.path.append('../utils')
from utils import model_loader
import numpy as np
import pandas as pd
import copy

def DiagnosisHome(request):
    context = {
        'title': 'Home',
        'isComplete': False
    }
    if request.method != 'POST':
        return render(request, 'diagnosis/diagnosis_home.html', context)
    else:
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
        X['sex'] = stored_vals['sex']
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

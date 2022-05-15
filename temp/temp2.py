import numpy as np
import pandas as pd

data = pd.read_csv('C:/Users/Narendra Shetty/Downloads/overall_data.csv')
print("Arr")
row = data.iloc[[12456]]
print(row[['age', 'weight', 'height', 'sex', 'smoke', 'alcohol', 'physical_activity', 'heart_rate', 'cholesterol']])
print(row[['systolic_bp', 'tobacco_consumed', 'ldl', 'adiposity', 'famhist', 'typea', 'alcohol_consumed']])
print()
print(row[[
    'qrs_duration', 'p-r_interval', 'q-t_interval', 
    't_interval', 'p_interval', 'qrs']])
print(row[['T', 'P', 'QRST', 'J', 'Q wave', 
    'R wave', 'S wave', "R' wave"]])
print(row[["S' wave", 'no_of_deflections', 'Ragged R wave', 
    'Diphasic Derivation of R wave', 'Ragged P wave']])
print(row[['Diphasic Derivation of P wave', 
    'Ragged T wave', 'Diphasic Derivation of T wave']])
print(row[['JJ wave Amp', 'Q wave Amp', 
    'R wave Amp', 'S wave Amp', "R' wave Amp", "S' wave Amp", 'P wave Amp', 'T wave Amp', 
    'QRSA', 'QRSTA'
]])
print()
print(row[['systolic_bp', 'diastolic_bp', 'gluc']])
print()
print(row[['masl', 'sex', 'age', 'systolic_bp', 'diastolic_bp', 'weight', 'height', 'bmi', 
        'diabetes_mellitus', 'cv_diseases']])
print(row[['smoke', 'physical_activity', 'sist_old', 'diast_old', 'sist_new', 'diast_new', 'BMI_cat']])
# print("Arrhythmia")
# row = data.iloc[[16524]]
# print(row[['age', 'weight', 'height', 'sex', 'smoke', 'alcohol', 'physical_activity', 'heart_rate', 'cholesterol']])
# print(row[[
#     'qrs_duration', 'p-r_interval', 'q-t_interval', 
#     't_interval', 'p_interval', 'qrs', 'T', 'P', 'QRST', 'J', 'Q wave', 
#     'R wave', 'S wave', "R' wave"]])
# print(row[["S' wave", 'no_of_deflections', 'Ragged R wave', 
#     'Diphasic Derivation of R wave', 'Ragged P wave', 'Diphasic Derivation of P wave', 
#     'Ragged T wave', 'Diphasic Derivation of T wave']])
# print(row[['JJ wave Amp', 'Q wave Amp', 
#     'R wave Amp', 'S wave Amp', "R' wave Amp", "S' wave Amp", 'P wave Amp', 'T wave Amp', 
#     'QRSA', 'QRSTA'
# ]])


# print("CVD")
# row = data.iloc[[23557]]
# # print(row[['systolic_bp', 'diastolic_bp', 'gluc']])

# print("Hyp")
# row = data.iloc[[29035]]
# print(row[['age', 'weight', 'height', 'sex', 'smoke', 'alcohol', 'physical_activity', 'heart_rate', 'cholesterol']])
# print(row[['masl', 'sex', 'age', 'systolic_bp', 'diastolic_bp', 'weight', 'height', 'bmi', 
#         'diabetes_mellitus', 'cv_diseases']])
# print(row[['smoke', 'physical_activity', 'sist_old', 'diast_old', 'sist_new', 'diast_new', 'BMI_cat']])
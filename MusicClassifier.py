import librosa,librosa.display
import numpy as np
import os
from Utils import *
import pandas as pd
from glob import glob
from sklearn.preprocessing import StandardScaler,quantile_transform,LabelEncoder
from sklearn.model_selection import train_test_split
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

X = pd.read_csv('./X.csv')

def audio_process(path):
    df = pd.DataFrame(columns=[
    'chroma_stft_mean', 'chroma_stft_var', 'rms_mean', 'rms_var',
    'spectral_centroid_mean', 'spectral_centroid_var', 'spectral_bandwidth_mean',
    'spectral_bandwidth_var', 'rolloff_mean', 'rolloff_var', 'zero_crossing_rate_mean',
    'zero_crossing_rate_var', 'harmony_mean', 'harmony_var', 'perceptr_mean',
    'perceptr_var', 'tempo', 'mfcc1_mean', 'mfcc1_var', 'mfcc2_mean', 'mfcc2_var',
    'mfcc3_mean', 'mfcc3_var', 'mfcc4_mean', 'mfcc4_var', 'mfcc5_mean', 'mfcc5_var',
    'mfcc6_mean', 'mfcc6_var', 'mfcc7_mean', 'mfcc7_var', 'mfcc8_mean', 'mfcc8_var',
    'mfcc9_mean', 'mfcc9_var', 'mfcc10_mean', 'mfcc10_var', 'mfcc11_mean', 'mfcc11_var',
    'mfcc12_mean', 'mfcc12_var', 'mfcc13_mean', 'mfcc13_var', 'mfcc14_mean', 'mfcc14_var',
    'mfcc15_mean', 'mfcc15_var', 'mfcc16_mean', 'mfcc16_var', 'mfcc17_mean', 'mfcc17_var',
    'mfcc18_mean', 'mfcc18_var', 'mfcc19_mean', 'mfcc19_var', 'mfcc20_mean', 'mfcc20_var'
])
    signal,sr = librosa.load(path,sr=SR)
    chromagram = librosa.feature.chroma_stft(y=signal, sr=SR, hop_length=HOP_LENGTH)
    rms = librosa.feature.rms(y=signal)
    spec_cent = librosa.feature.spectral_centroid(y=signal)
    spec_band = librosa.feature.spectral_bandwidth(y=signal, sr=SR)
    spec_roll = librosa.feature.spectral_rolloff(y=signal, sr=SR)
    zero_crossing = librosa.feature.zero_crossing_rate(y=signal)
    harmony, perceptr = librosa.effects.hpss(y=signal)
    tempo, _ = librosa.beat.beat_track(y=signal, sr=SR)
    mfcc = librosa.feature.mfcc(y=signal, sr=SR, n_mfcc=N_MFCC, hop_length=HOP_LENGTH)

    features = {
        'chroma_stft_mean': np.mean(chromagram),
        'chroma_stft_var': np.var(chromagram),
        'rms_mean': np.mean(rms),
        'rms_var': np.var(rms),
        'spectral_centroid_mean': np.mean(spec_cent),
        'spectral_centroid_var': np.var(spec_cent),
        'spectral_bandwidth_mean': np.mean(spec_band),
        'spectral_bandwidth_var': np.var(spec_band),
        'rolloff_mean': np.mean(spec_roll),
        'rolloff_var': np.var(spec_roll),
        'zero_crossing_rate_mean': np.mean(zero_crossing),
        'zero_crossing_rate_var': np.var(zero_crossing),
        'harmony_mean': np.mean(harmony),
        'harmony_var': np.var(harmony),
        'perceptr_mean': np.mean(perceptr),
        'perceptr_var': np.var(perceptr),
        'tempo': tempo,
    }
    for x in range(20):
        features[f'mfcc{x+1}_mean'] = np.mean(mfcc[x, :])
        features[f'mfcc{x+1}_var'] = np.var(mfcc[x, :])

    #label_mapping
    mapping = {'blues': 0,
    'classical': 1,
    'country': 2,
    'disco': 3,
    'hiphop': 4,
    'jazz': 5,
    'metal': 6,
    'pop': 7,
    'reggae': 8,
    'rock': 9}
    
    #preprocessing data
    df = pd.concat([df, pd.DataFrame(features, index=[0])], ignore_index=True)
    df_sc = pd.concat([X.drop('Unnamed: 0',axis='columns'),df],ignore_index=True)
    
    sc = StandardScaler()
    X_sc = sc.fit_transform(df_sc)
    X_pp = X_sc[-1].reshape(1,-1)

    #load_model and classification
    with open('rfc_model','rb') as f:
        rfc_model = pickle.load(f)
    with open('knn_model','rb') as f:
        knn_model = pickle.load(f)
    with open('lrc_model','rb') as f:
        lrc_model = pickle.load(f)
    encoded_label_r = rfc_model.predict(X_pp)
    encoded_label_k = knn_model.predict(X_pp)
    encoded_label_l = lrc_model.predict(X_pp)
    return [{v: k for k, v in mapping.items()}.get(encoded_label_r.item()),
{v: k for k, v in mapping.items()}.get(encoded_label_k.item()),
{v: k for k, v in mapping.items()}.get(encoded_label_l.item())]






    
    

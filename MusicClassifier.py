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

def audio_process(path):
    df = pd.DataFrame(columns=['chroma_stft_mean', 'chroma_stft_var', 'rms_mean', 'rms_var',
       'spectral_centroid_mean', 'spectral_centroid_var',
       'spectral_bandwidth_mean', 'spectral_bandwidth_var', 'rolloff_mean',
       'rolloff_var', 'zero_crossing_rate_mean', 'zero_crossing_rate_var',
       'harmony_mean', 'harmony_var', 'perceptr_mean', 'perceptr_var', 'tempo',
       'mfcc1_mean', 'mfcc1_var', 'mfcc2_mean', 'mfcc2_var', 'mfcc3_mean',
       'mfcc3_var', 'mfcc4_mean', 'mfcc4_var', 'mfcc5_mean', 'mfcc5_var',
       'mfcc6_mean', 'mfcc6_var', 'mfcc7_mean', 'mfcc7_var', 'mfcc8_mean',
       'mfcc8_var', 'mfcc9_mean', 'mfcc9_var', 'mfcc10_mean', 'mfcc10_var',
       'mfcc11_mean', 'mfcc11_var', 'mfcc12_mean', 'mfcc12_var', 'mfcc13_mean',
       'mfcc13_var', 'mfcc14_mean', 'mfcc14_var', 'mfcc15_mean', 'mfcc15_var',
       'mfcc16_mean', 'mfcc16_var', 'mfcc17_mean', 'mfcc17_var', 'mfcc18_mean',
       'mfcc18_var', 'mfcc19_mean', 'mfcc19_var', 'mfcc20_mean', 'mfcc20_var'])
    signal, sr = librosa.load(path,
                                sr=SR)
    mfcc = librosa.feature.mfcc(y=signal,
                                sr=SR,
                                n_mfcc=N_MFCC,
                                hop_length=HOP_LENGTH)
    chroma_stft = librosa.feature.chroma_stft(y=signal,
                                            sr=SR,
                                            hop_length=HOP_LENGTH)
    rms = librosa.feature.rms(y=signal,
                            hop_length=HOP_LENGTH)
    spectral_centroid = librosa.feature.spectral_centroid(y=signal,
                                                        sr=SR,
                                                        hop_length=HOP_LENGTH)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=signal,
                                                        sr=SR,
                                                        hop_length=HOP_LENGTH)
    rolloff = librosa.feature.spectral_rolloff(y=signal,
                                    sr=SR,
                                    hop_length=HOP_LENGTH) 
    tempo = librosa.feature.tempo(y=signal)
    zero_crossing_rate = librosa.zero_crossings(y=signal)
    harmony, perceptr = librosa.effects.hpss(y=signal)
    mfcc = librosa.feature.mfcc(y=signal,
                            sr=SR,
                            n_mfcc=N_MFCC,
                            hop_length=HOP_LENGTH)

    df['chroma_stft_mean']= [np.mean(chroma_stft)]
    df['chroma_stft_var']= [np.var(chroma_stft)]
    df['rms_mean']= [np.mean(rms)]
    df['rms_var']= [np.var(rms)]
    df['spectral_centroid_mean']= [np.mean(spectral_centroid)]
    df['spectral_centroid_var']= [np.var(spectral_centroid)]
    df['spectral_bandwidth_mean']= [np.mean(spectral_bandwidth)]
    df['spectral_bandwidth_var']= [np.var(spectral_bandwidth)]
    df['rolloff_mean']= [np.mean(rolloff)]
    df['rolloff_var']= [np.var(rolloff)]
    df['zero_crossing_rate_mean']= [np.mean(zero_crossing_rate)]
    df['zero_crossing_rate_var']= [np.var(zero_crossing_rate)]
    df['harmony_mean']= [np.mean(harmony)]
    df['harmony_var']=[np.var(harmony)]
    df['perceptr_mean']= [np.mean(perceptr)]
    df['perceptr_var']= [np.var(perceptr)]
    df['tempo']= tempo
    for x in range(20):
        feat1 = "mfcc" + str(x+1) + "_mean"
        feat2 = "mfcc" + str(x+1) + "_var"
        df[feat1] = [mfcc[:,x].mean()]
        df[feat2] = [mfcc[:,x].var()]

    #Using quantile tranformation and stantard scaler for X
    sc = StandardScaler()
    X_sc = sc.fit_transform(df.values.reshape(-1,1))
    X_pp = quantile_transform(X_sc)

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
    #load_model and predict
    with open('model_30','rb') as f:
        model = pickle.load(f)
    encoded_label = model.predict(X_pp.reshape(1,-1))
    return {v: k for k, v in mapping.items()}.get(encoded_label.item())






    
    

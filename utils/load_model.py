import pickle

def svd_model():
    pickled_model = pickle.load(open('trainedmodels/svd100_30_0005_04.pkl', 'rb'))
    return pickled_model
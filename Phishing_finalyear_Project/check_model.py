import pickle

model = pickle.load(open("model.pkl","rb"))

print("Classes:")
print(model.classes_)

print("Feature count:")
print(model.n_features_in_)
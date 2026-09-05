import pickle

model = pickle.load(open("model.pkl","rb"))

print("MODEL TYPE:")
print(type(model))

print("\nCLASSES:")
print(model.classes_)

print("\nFEATURE COUNT:")
print(model.n_features_in_)
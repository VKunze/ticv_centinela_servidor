from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

X = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
y = iris_data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1,
                                                    test_size=0.2)
sc_X = StandardScaler()
X_trainscaled = sc_X.fit_transform(X_train)
X_testscaled = sc_X.transform(X_test)

clf = MLPClassifier(hidden_layer_sizes=(256, 128, 64, 32), activation="relu",
                    random_state=1).fit(X_trainscaled, y_train)
y_pred = clf.predict(X_testscaled)
print(clf.score(X_testscaled, y_test))

fig = plot_confusion_matrix(clf, X_testscaled, y_test,
                            display_labels=["Setosa", "Versicolor",
                                            "Virginica"])
fig.figure_.suptitle("Confusion Matrix for Iris Dataset")
plt.show()

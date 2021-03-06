import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix

# import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target
class_names = iris.target_names

# Split the data into a training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Run classifier, using a model that is too regularized ( C too low)
# to see the impact on the results
classifier = svm.SVC(kernel='linear', C=0.01).fit(X_train, y_train)

np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
title_options = [("Confusion matrix, without normalization", None),
			  ("Normalizaed confusion matrix", 'true')]
count = 0
for title, normalize in title_options:
    disp = plot_confusion_matrix(classifier, X_test, y_test,display_labels=class_names,
			cmap=plt.cm.Blues, normalize = normalize)
    disp.ax_.set_title(title)
    print(title)
    print(disp.confusion_matrix)
    plt.show()
    plt.savefig("confusion_matrix"+str(count)+".png")
    count += 1

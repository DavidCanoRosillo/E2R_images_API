import pandas as pd
import numpy as np

df = pd.read_csv('/Users/dcr/uni/beca/demo/final_results.csv')

def acc(test = 'MPNET'):
    max_acc = 0
    max_threshold = 0

    for threshold in np.arange(df[test].min(), df[test].max(), 0.01):
        correct = 0
        total = 0
        for index, row in df.iterrows():
            if row['id_imagen'] == row['id_description']:
                if row[test] < threshold:
                    correct += 1
            else:
                if row[test] > threshold:
                    correct += 1
            total += 1
        if (correct / total) > max_acc:
            max_acc = (correct / total)
            max_threshold = threshold

    print(f"Threshold {max_threshold}={max_acc * 100}")

def positives(test = 'MPNET'):
    correct = 0
    total = 0
    threshold = 0.2
    for index, row in df.iterrows():
        if row[test] >= threshold: # 0.4
            if row['id_imagen'] == row['id_description']:
                correct += 1
            total += 1

    print(f"Threshold {threshold}={(correct / total) * 100}")
    print(f"{correct} correct out of {total} over {threshold}.")
    print(f"Total items tested {len(df)}")

test = 'CLIP'
threshold = 0.1
true_positive, false_positive, true_negative, false_negative = 0, 0, 0, 0
y_true = []
y_pred = []

import matplotlib.pyplot as plt
import numpy
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score

#for threshold in np.arange(df[test].min(), df[test].max(), 0.01):
threshold = 0.2434956976771353
if True:
    y_true = []
    y_pred = []
    for index, row in df.iterrows():
        if row['id_imagen'] == row['id_description']: # label = true
            y_true.append(1)
            if row[test] >= threshold: # pred = true
                true_positive += 1 
                y_pred.append(1)
            else: # pred = false
                false_negative += 1 
                y_pred.append(0)
        else: # label = false
            y_true.append(0)
            if row[test] < threshold: # pred = false
                true_negative += 1
                y_pred.append(0)
            else:  # pred = true
                false_positive += 1 
                y_pred.append(1)
    print('threshold:', threshold, "Acc", accuracy_score(y_true, y_pred))

total = false_negative + false_positive + true_negative + true_positive
print(false_negative, false_positive, true_negative, true_positive, total)

import matplotlib.pyplot as plt
import numpy
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score

cm = confusion_matrix(y_true, y_pred)
print("Acc", (cm[0][0] + cm[1][1]) / (cm[0][1] + cm[1][0] + cm[0][0] + cm[1][1]))
print("Acc", accuracy_score(y_true, y_pred))
#cm = cm / total
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()
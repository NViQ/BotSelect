import pandas as pd

def process_score(score):
    if score > 77:
        return "correct"
    elif score >= 29 and score <= 77:
        return "reask"
    else:
        return "operator"


def calculate_accuracy(data):
    correct_predictions = 0

    for row in data:
        score = row['Score']
        predicted_action = process_score(score)
        actual_action = row['Action']

        if predicted_action == actual_action:
            correct_predictions += 1

    accuracy = correct_predictions / len(data) * 100
    return accuracy

df = pd.read_csv('table.csv')
data = df.to_dict(orient='records')

accuracy = calculate_accuracy(data)
print("Точность алгоритма: {:.2f}%".format(accuracy))


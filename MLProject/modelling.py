import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import os
import warnings
import sys
 
if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)
 
    file_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_balita_preprocessing.csv")
    data = pd.read_csv(file_path)
 
    X_train, X_test, y_train, y_test = train_test_split(
    data.drop("Status Gizi", axis=1),
    data["Status Gizi"],
    random_state=42,
    test_size=0.2
    )
    input_example = X_train[0:5]
    n_estimators = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 20
 
    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
        model.fit(X_train, y_train)
 
        predicted_qualities = model.predict(X_test)
 
        mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        input_example=input_example
        )
        model.fit(X_train, y_train)
        # Log metrics
        accuracy = model.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)
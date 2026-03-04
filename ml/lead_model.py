import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def train_lead_model(df):

    df_model = df.copy()

    cat_cols = df_model.select_dtypes(include="object").columns

    for col in cat_cols:
        encoder = LabelEncoder()
        df_model[col] = encoder.fit_transform(df_model[col])

    X = df_model.drop(["y","customer"],axis=1)

    y = df_model["customer"]

    X_train,X_test,y_train,y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        random_state=42
    )

    model.fit(X_train,y_train)

    preds = model.predict(X_test)

    accuracy = accuracy_score(y_test,preds)

    importance = pd.DataFrame({
        "Feature":X.columns,
        "Importance":model.feature_importances_
    }).sort_values(by="Importance",ascending=False)

    return model, accuracy, importance
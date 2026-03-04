import pandas as pd

def load_data():

    df = pd.read_csv("data/marketing_funnel.csv", sep=";")

    df["visitor"] = 1

    df["lead"] = df["contact"].apply(
        lambda x: 1 if x != "unknown" else 0
    )

    df["customer"] = df["y"].map({
        "yes":1,
        "no":0
    })

    return df
import pandas as pd

def funnel_metrics(df):

    visitors = df["visitor"].sum()

    leads = df["lead"].sum()

    customers = df["customer"].sum()

    v_to_l = round((leads/visitors)*100,2)

    l_to_c = round((customers/leads)*100,2)

    overall = round((customers/visitors)*100,2)

    return visitors, leads, customers, v_to_l, l_to_c, overall


def dropoff_data(df):

    data = pd.DataFrame({
        "Stage":["Visitors","Leads","Customers"],
        "Count":[
            df["visitor"].sum(),
            df["lead"].sum(),
            df["customer"].sum()
        ]
    })

    return data


def channel_performance(df):

    result = df.groupby("contact")["customer"].mean().reset_index()

    result["conversion_rate"] = result["customer"]*100

    return result


def campaign_performance(df):

    result = df.groupby("campaign")["customer"].mean().reset_index()

    result["conversion_rate"] = result["customer"]*100

    return result


def monthly_conversion(df):

    df["month_num"] = pd.to_datetime(
        df["month"], format="%b"
    ).dt.month

    trend = df.groupby("month_num")["customer"].mean().reset_index()

    trend["conversion_rate"] = trend["customer"]*100

    return trend
import plotly.express as px


def funnel_chart(data):

    fig = px.funnel(
        data,
        x="Count",
        y="Stage",
        title="Marketing Funnel"
    )

    return fig


def channel_chart(data):

    fig = px.bar(
        data,
        x="contact",
        y="conversion_rate",
        color="contact",
        title="Conversion Rate by Channel"
    )

    return fig


def campaign_chart(data):

    fig = px.line(
        data,
        x="campaign",
        y="conversion_rate",
        markers=True,
        title="Campaign Conversion Trend"
    )

    return fig


def conversion_trend(data):

    fig = px.line(
        data,
        x="month_num",
        y="conversion_rate",
        markers=True,
        title="Monthly Conversion Trend"
    )

    return fig
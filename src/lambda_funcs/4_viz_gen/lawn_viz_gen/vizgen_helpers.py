import pandas as pd
import plotly.express as px
import plotly.offline as offline

day_names = "Mon Tue Wed Thu Fri Sat Sun".split()
hour_bin_names = "Midnight-4a 4a-8a 8a-Noon Noon-4p 4p-8p 8p-Midnight".split()


def make_uptime_heatmap(df):
    grouped_uptime = group_day_hour_uptime(df)
    div_uptime_heatmap = make_uptime_plotly_div(grouped_uptime)
    return div_uptime_heatmap


def make_uptime_plotly_fig(grouped_uptime):
    print("Creating uptime heatmap json...")

    px.defaults.color_continuous_scale = px.colors.sequential.Teal

    fig = px.imshow(
        grouped_uptime * 100,
        labels=dict(x="Days of Week", y="Times of Day", color="Uptime %"),
        x=day_names,
        y=hour_bin_names,
    )

    fig.update_xaxes(side="top")

    print("Created uptime heatmap json.")

    return fig


def group_day_hour_uptime(df):
    df["utc_time"] = pd.to_datetime(df.utc_time, utc=True)
    df = df.set_index("utc_time").tz_convert("US/Eastern", axis=0)
    day_ints = list(range(7))

    days_of_week = dict(zip(day_ints, day_names))
    df["day_of_week"] = df.index.dayofweek.map(days_of_week)

    df["binned_hour"] = pd.cut(
        df.index.hour, [-1, 4, 8, 12, 16, 20, 25], labels=hour_bin_names
    )

    grouped_uptime = (
        df.groupby(["binned_hour", "day_of_week"])
        .lawn_open.mean()
        .unstack()[day_names]
    )

    return grouped_uptime

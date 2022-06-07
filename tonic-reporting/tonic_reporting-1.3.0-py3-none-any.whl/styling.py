class Colors:
    REAL = "mediumpurple"
    SYNTH = "mediumturquoise"
    ALPHA = 0.5


class PlotsSizes:
    LARGE_FIGURE = (16, 10)
    XTRA_LARGE_FIGURE = (20, 10)


class Labels:
    REAL = "Real"
    SYNTH = "Synth"


class FontSizes:
    DEFAULT = 14
    LARGE = 16

def format_stats_data(df):
    format_kwargs = {col: "{:.2%}" for col in df.columns if "p-value" in col}
    return df.style.format(format_kwargs)

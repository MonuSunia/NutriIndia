import pandas as pd


def dataframe_to_csv(df: pd.DataFrame):

    return df.to_csv(index=False).encode("utf-8")
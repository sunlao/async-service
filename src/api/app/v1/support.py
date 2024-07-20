from fastapi.encoders import jsonable_encoder
from pandas import json_normalize


def html_table(p_rows):
    rows_json = jsonable_encoder(p_rows)
    rows_df = json_normalize(rows_json)
    rows_df.rename(columns=lambda s: s.replace(".", " "), inplace=True)
    rows_df.rename(columns=lambda s: s.replace("_", " "), inplace=True)

    try:
        drop1_df = rows_df.drop(columns="score")
    except KeyError:
        drop1_df = rows_df
    try:
        drop2_df = drop1_df.drop(columns="args")
    except KeyError:
        drop2_df = drop1_df
    drop2_df.columns = drop2_df.columns.str.upper()

    try:
        sort_df = drop2_df.sort_values(by=["ENQUEUE TIME"], ascending=False)
    except KeyError:
        sort_df = drop2_df

    return sort_df.to_html(index=False)

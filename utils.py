import pandas as pd
import numpy as np


def start_notebook():
    pd.set_option("display.max_columns", None)
    return


def calculate_percentage_of_group(
    df, id_column, indicator_column, group_interest, new_column_name
):
    df = df[[id_column, indicator_column]]
    cols_to_group = [id_column, indicator_column]
    df_grouped = df.groupby(cols_to_group, as_index=False).size()
    df_grouped[new_column_name] = (
        100
        * df_grouped["size"]
        / df_grouped.groupby([id_column])["size"].transform("sum")
    )
    df_grouped = df_grouped[df_grouped[indicator_column] == group_interest]
    return df_grouped


def apply_func_perc(
    final_df,
    origin_df,
    f_to_apply,
    unique_key,
    indicator_column,
    group_interest,
    new_column_name,
):
    """
    Parameters:

        final_df : the dataframe that joins all the final data,
        origin_df : dataframe with all columns, the origin
        f_to_apply : the function that is applied
        unique_key : the join key
        indicator_column : the column with the indicator
        group_interest : the group indicator that i want to filter
        new_column_name : the new name of the column on the final_df

    returns :
        the final_df enriched
    """
    tmp_df = f_to_apply(
        df=origin_df,
        id_column=unique_key,
        indicator_column=indicator_column,
        group_interest=group_interest,
        new_column_name=new_column_name,
    )
    final_df = final_df.merge(
        tmp_df[[unique_key, new_column_name]], how="left", on=unique_key
    )

    return final_df


def calculate_sum_of_group(df, id_column, indicator_column, new_column_name):
    df = df[[id_column, indicator_column]]
    df = df.groupby(id_column, as_index=False).agg(np.sum)
    df = df.rename(columns={indicator_column: new_column_name})

    return df


def apply_func_sum(
    final_df, origin_df, f_to_apply, unique_key, indicator_column, new_column_name
):

    tmp_df = f_to_apply(origin_df, unique_key, indicator_column, new_column_name)
    final_df = final_df.merge(tmp_df, how="left", on=unique_key)

    return final_df

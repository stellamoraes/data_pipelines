import json
import logging
from datetime import datetime

import requests
import pandas as pd
import pytz

BRAZIL_TIMEZONE = pytz.timezone("America/Sao_Paulo")

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Main role responsible for extracting, transforming and loading data into a csv file.
    """
    logger.info("Extracting data")
    carts_data = extract_fake_store_api_data(endpoint="carts")
    product_data = extract_fake_store_api_data(endpoint="products")

    logger.info("Starting data transformation...")
    df_carts = pd.json_normalize(
        data=carts_data,
        meta=["id", "userId", "date"],
        record_path="products",
        errors="raise",
    )

    df_product = pd.json_normalize(data=product_data)
    df_product = df_product[["id", "category"]]

    df = df_carts.merge(df_product, left_on="productId", right_on="id")

    df = transform_datetime_column(df, columns=["date"])
    df = applies_aggregation_operations(df)

    df["processing_date"] = datetime.now(BRAZIL_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    df = df.rename(columns={
        "category": "most_relevant_category",
        "userId":"user_id"
        })
    df = df.drop(["sum_product_quantity"], axis=1)

    logger.info("Loading data...")
    persist_file(df=df, file_name="fake_store_analytics", file_format="csv")


def extract_fake_store_api_data(endpoint: str) -> list:
    """
    Function responsible for making requests to the Fake Store API and extract data.
    
    Parameters:
    - endpoint (str): Name of the endpoint to be used in the request.
    
    Returns:
    - list:  List containing dictionaries with data extracted from API.
    """
    api_url = f"https://fakestoreapi.com/{endpoint}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = json.loads(response.text)
        logger.info(
            f"API request to URL: {api_url} and data extraction was successfully completed"
        )
    else:
        logger.error(f"API request error: Status Code {response.status_code}")
        data = []
    
    return data


def transform_datetime_column(
    df: pd.DataFrame,
    columns: list,
    timezone: str = BRAZIL_TIMEZONE,
    date_format: str = "%Y-%m-%d %H:%M:%S",
) -> pd.DataFrame:
    """
    Function responsible for correcting the time zone to America/Sao_Paulo and
    adjusting datetime format.

    Parameters:
    - df(pd.DataFrame): Dataframe with date column in the format '%Y-%m-%dT%H:%M:%S.%fZ'.

    Returns:
    - pd.DataFrame: Dataframe with date column in 'yyyy-mm-dd hh:mm:ss' format with Brazil time zone.
    """
    for column in columns:
        df[column] = pd.to_datetime(df[column], utc=True)
        df[column] = df[column].dt.tz_convert(timezone).dt.strftime(date_format)

    return df


def applies_aggregation_operations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function responsible for transform data to answer the following questions:
    1) What was the last date the customer added products to the cart?
    - To answer this question, grouped the data by user ID and created a new column
    (last_date_add_to_cart) with the last date (max) on which products were added to the cart.

    2) Which category did the customer add the most products to the cart?
    - To answer this question, grouped the data by user ID and product category name, then
    sum the number of products added to the cart. At the end, a new grouping of the data
    from the dataframe is made by user ID and using aggregation to keep in the dataframe records
    with most products per category.

    Parameters:
    - df(pd.DataFrame): Dataframe containing userId, category, date and quantinty columns.

    Returns:
    - pd.DataFrame: Dataframe with analytical data and granularity by user ID.
    """
    df["last_date_add_to_cart"] = df.groupby("userId")["date"].transform("max")
    df["sum_product_quantity"] = df.groupby(["userId", "category"])[
        "quantity"
    ].transform("sum")

    df = df.groupby(["userId"]).agg(
        {
            "category": "first",
            "last_date_add_to_cart": "first",
            "sum_product_quantity": "max",
        }
    )

    return df


def persist_file(df: pd.DataFrame, file_name: str, file_format: str) -> None:
    """
    Function responsible for receiving the dataset with the transformed data
    and persisting it in a file.
    
    Parameters:
    - df (pd.DataFrame): Final dataframe containing the transformed data.
    - file_name (str): Name of the file to be persisted in the directory.
    - file_format (str): File format to persist data.
    """
    assert file_format in ["csv", "json", "parquet"]

    if file_format == "parquet":
        df.to_parquet(f"{file_name}.parquet", engine="fastparquet", compression=None)
    elif file_format == "csv":
        df.to_csv(f"{file_name}.csv")
    elif file_format == "json":
        with open(f"{file_name}.json", "w") as file:
            file.write(json.dumps(df.to_dict()))

    logger.info("Data successfully persisted!")


if __name__ == "__main__":
    main()
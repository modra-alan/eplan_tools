from typing import Any
import pandas as pd
from enums import PartHeader
from api_controller import APIController
import time
import json

OUTPUT_FILE = "outputs/PartData.json"


def main():
    df = pd.read_excel("inputs/Parts.xlsx")

    # set columns to value of second row
    df.columns = df.iloc[0]

    column_map = map_columns_to_enum(df)

    api_controller = APIController()

    api_part_data: dict[str, list[dict[str, Any]]] = {}

    prev_query = ""
    prev_partno = ""
    for row in df.values[1:]:
        part_num = row[column_map[PartHeader.Type_number]]
        query = str(part_num).split("-")[0]
        if query == prev_query:
            if prev_partno in api_part_data:
                api_part_data[part_num] = api_part_data[prev_partno]
            print(f"Skipping {query} as it was already queried")
            continue
        else:
            prev_query = query
            prev_partno = part_num
        print(f"Searching api for {query}")
        api_response = api_controller.get_parts(query)
        if "data" in api_response and isinstance(api_response["data"], list):
            api_part_data[part_num] = api_response["data"]
        elif "message" in api_response:
            print(
                f"Unusable value from api for query {query}:",
                api_response["message"],
            )
        time.sleep(1)
    if not api_part_data:
        print("No data found")
        return
    print(f"API returned results for {len(api_part_data)} / {len(df)} parts:")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(api_part_data, f, indent=4)


def map_columns_to_enum(df: pd.DataFrame) -> dict[PartHeader, int]:
    """Searches for each enum in column names and maps the column index to the enum value

    Args:
        df (pd.DataFrame): Dataframe to map

    Returns:
        dict[PartHeader, int]: Dictionary with enum as key and column index as value
    """
    result = {}
    for enum in PartHeader:
        if index := df.columns.get_loc(enum.value):
            if type(index) != int:
                raise TypeError(f"Expected int, got {type(index)}")
            result[enum] = index
    return result


if __name__ == "__main__":
    main()

import io
import json
import os

import pandas as pd
from flask import Flask, jsonify, request

# this api serves only for one data file and is tailored for task
# in ideal world, is better to use json only here but pandas has a good methods to handle frames
# if I want to go deeper I will add a method to check if each data column / row has correct format

app = Flask(__name__)

WORKDIR = os.path.join(os.getcwd(), "data")


def table_name_to_file_path(table_name: str) -> str:
    return os.path.join(WORKDIR, f"{table_name}.csv")


@app.route("/table/<table_name>", methods=["PUT"])
def create_or_add_table(table_name: str):
    # check if its csv
    file_path = table_name_to_file_path(table_name=table_name)
    data = request.json
    in_df = pd.read_json(io.StringIO(data))
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if (df.columns.tolist() == in_df.columns.tolist()) & (df.dtypes.tolist() == in_df.dtypes.tolist()):
            df = pd.concat([df, in_df], ignore_index=True)
            df.drop_duplicates().to_csv(file_path, index=False)
            return jsonify({"info": f"New rows were added, duplicates were dropped."})
        else:
            return jsonify({"info": "Column names or types do not match."}), 400  # add some stats
    else:
        in_df.to_csv(file_path, index=False)
        return jsonify({"info": "Created a new data table."})


@app.route("/table/<table_name>", methods=["GET"])
def query_table(table_name: str):
    file_path = table_name_to_file_path(table_name=table_name)
    try:
        data = pd.read_csv(file_path).to_dict(orient="records")
    except FileNotFoundError:
        return jsonify({"error": "Table hasn't been initialised."}), 404
    return jsonify(data)


@app.route("/table/<table_name>", methods=["DELETE"])
def delete_table(table_name: str):
    file_path = table_name_to_file_path(table_name=table_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"info": f"{file_path} has been deleted."}), 200
    else:
        return jsonify({"error": f"{file_path} does not exist."}), 404


app.run()

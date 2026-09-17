# Create a Flask API that reads sales_data.csv file and returns total revenue
# the API should have an endpoint /total_revenue that returns the total revenue as a JSON response
# the structure of the sales_data.csv file is as follows:
# order_id,product,region,sales,order_date
# 1001,Monitor,South,1306,2024-12-26
# the total revenue can be calculated by summing up the sales column
# convert the total revenue to an integer and return it as a JSON response.
# Additionally, create another endpoint /highest_region that returns the region 
# with the highest sales along with the total sales for that region as a JSON response.

from flask import Flask, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = os.path.join(os.path.dirname(__file__), "sales_data.csv")


def read_sales_data():
    sales = []
    if not os.path.exists(CSV_FILE):
        return sales

    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                sales.append(float(row["sales"]))
            except (TypeError, ValueError):
                continue
    return sales


@app.route("/total_revenue", methods=["GET"])
def total_revenue():
    sales = read_sales_data()
    total = sum(sales)
    return jsonify({"total_revenue": int(total)})


@app.route("/highest_region", methods=["GET"])
def highest_region():
    if not os.path.exists(CSV_FILE):
        return jsonify({"region": None, "total_sales": 0})

    region_totals = {}
    with open(CSV_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            region = row.get("region", "")
            try:
                sales_value = float(row["sales"])
            except (TypeError, ValueError):
                continue
            region_totals[region] = region_totals.get(region, 0) + sales_value

    if not region_totals:
        return jsonify({"region": None, "total_sales": 0})

    highest_region = max(region_totals, key=region_totals.get)
    highest_sales = int(region_totals[highest_region])
    return jsonify({"region": highest_region, "total_sales": highest_sales})


if __name__ == "__main__":
    app.run(debug=True)

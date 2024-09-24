import csv
import json
import os
import pandas as pd

default_theta = {
    "theta0": 0,
    "theta1": 0,
    "maxMileage": None,
    "minMileage": None
}

def jsonChecker() :
    try:
        with open("theta.json", "w") as file:
            json.dump(default_theta, file, indent=4)

        print("theta.json was created or reset with default values.")

    except Exception as e:
            print(f"An error occurred while creating or resetting theta.json: {e}")

def dataChecker():
    try:
        if not os.path.exists("data.csv"):
            print("data.csv does not exist.")
            return False

        with open("data.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) == 0:
                print("data.csv is empty")
                return False

            header = rows[0]
            expected_header = ["km", "price"]
            if header != expected_header:
                print("data.csv has an invalid header or no header at all")
                return False

            if len(rows) < 2:
                print("data.csv needs minimum one data point")
                return False

            for i, row in enumerate(rows[1:], start=2):
                if len(row) != 2:
                    print(f"Invalid row {i} in data.csv. Each datapoint should have 2 values")
                    return False

                try:
                    km = float(row[0])
                    price = float(row[1])
                except ValueError:
                    print(f"Invalid data in row {i}. Both 'km' and 'price' should be numeric")
                    return False

            return True

    except Exception as e:
        print(f"An error occurred while checking data.csv: {e}")
        return False


def fillMaxAndMin() :
    try:
        with open("data.csv", "r") as file:
            reader = csv.DictReader(file)
            kms = [int(row["km"]) for row in reader]

            if kms:
                least = min(kms)
                highest = max(kms)
            else:
                print("No data found in data.csv")
                return

    except FileNotFoundError:
        print("data.csv not found.")
        return

    except Exception as e:
        print(f"An error occurred while processing data.csv: {e}")
        return

    try:
        with open("theta.json", "r") as jsonFile:
            content = json.load(jsonFile)

        content["maxMileage"] = highest
        content["minMileage"] = least

        with open("theta.json", "w") as jsonFile:
            json.dump(content, jsonFile, indent=4)

        print("Data limits are updated")

    except FileNotFoundError:
        print("theta.json not found")
        return

    except Exception as e:
        print(f"An error occurred while processing data.csv: {e}")
        return

class   calculations:
    def __init__(self):
        self.rate = 0.1
        self.theta0 = 0
        self.theta1 = 0
        self.data = pd.read_csv("data.csv").values.tolist()
        self.mileages = [row[0] for row in self.data]
        self.prices = [row[1] for row in self.data]
        self.samples = len(self.data)

        # Needed for scaling
        self.averageMileage = sum(self.mileages) / len(self.mileages)
        self.mileageDev = (sum((mileage - self.averageMileage) ** 2 for mileage in self.mileages) / len(self.mileages)) ** 0.5

        # Scalers
        self.scaled_mileages = [(mileage - self.averageMileage) / self.mileageDev for mileage in self.mileages]


def main() :
    if dataChecker() == False:
        return

    jsonChecker()
    fillMaxAndMin()

    calc = calculations()

if __name__ == '__main__' :
    main()

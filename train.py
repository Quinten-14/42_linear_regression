import csv
import json

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


def main() :
    fillMaxAndMin()

if __name__ == '__main__' :
    main()

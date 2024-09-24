import json
import sys

def getThetas():
    try:
        with open("theta.json", "r") as file:
            theta = json.load(file)
    except FileNotFoundError:
        print("The file theta.json does not exist.")
        sys.exit(1)

    return theta["theta0"], theta["theta1"]

def getEdges():
    try:
        with open("theta.json", "r") as file:
            content = json.load(file)
    except FileNotFoundError:
        print("The file theta.json does not exist.")
        sys.exit(1)

    return content["minMileage"], content["maxMileage"]


def scaler(x):
        min_km, max_km = getEdges()

        if min_km is None or max_km is None:
            print("Unable to scale the value as min/max km are not available.")
            return None
        
        scaledValue = (x - min_km) / (max_km - min_km)
        return scaledValue

def estimatePrice():
    if len(sys.argv) != 1:
        print("Usage: python estimatePrice.py")
        sys.exit(1)

    while (1):
        mileage_input = input("Which mileage is on your car ? ")
        if not mileage_input:
            break
        if not mileage_input.isdigit():
            print("Please enter a number")
            continue
        if int(mileage_input) < 0:
            print("Please enter a positive number")
            continue

        try:
            float_mileage = float(mileage_input)
        except ValueError:
            print("Please enter a number")
            continue


        theta0, theta1 = getThetas()
        mileage = scaler(float_mileage)
        price = theta0 + (theta1 * mileage)
        if price < 0:
            print("It is not worth to sell your car. The estimated price is under 0 euros.")
            return
        else:
            print("The estimated price is: ", str(int(price)) + " euros")
            return

if __name__ == "__main__":
    estimatePrice()

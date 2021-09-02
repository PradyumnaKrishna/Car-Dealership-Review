import sys

def main(dict):
    fields = ["id", "name", "dealership", "review", "purchase",
              "another", "purchase_date", "car_make", "car_model", "car_year"]
    
    doc = {}
    for field in fields:
        if field in dict["review"]:
            doc[field] = dict["review"][field]

    return {"doc": doc}

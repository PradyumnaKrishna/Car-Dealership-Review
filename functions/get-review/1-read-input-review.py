import sys


def main(dict):
    dealerId = dict.get("dealerId", None)

    if dealerId:
        return {
            "query": {
                "selector": {
                    "dealership": int(dealerId)
                },
                "use_index": "dealership_index"
            }
        }
        
    return {
        "query": {
            "selector": {
                "id": {
                    "$exists": True
                }
            }
        }
    }

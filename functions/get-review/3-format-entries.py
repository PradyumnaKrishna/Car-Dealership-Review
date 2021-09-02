def main(dict):
    # Check for errors
    if dict.get("error", None):
        return {"error": {"status": 500, "msg": "Something went wrong on the server", "params": dict}}
    
    elif dict["docs"] == []:
        return {"error": {"status": 404, "msg": "DealerId does not exist"}}

    docs = [entry(doc) for doc in dict["docs"]]
    return {"entries": docs}


def entry(doc):
    doc.pop("_id")
    doc.pop("_rev")
    return doc

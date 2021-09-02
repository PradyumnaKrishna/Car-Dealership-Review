import json
import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings

from .models import CarDealer, DealerReview


def get_request(url, **kwargs):
    """ generic get request """
    print(kwargs)
    print(f"GET from {url} ")
    try:
        # Call to NLU
        if "apikey" in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(
                url,
                headers={"Content-Type": "application/json"},
                params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"])
            )

        # Call to Cloudant DB
        else:
            response = requests.get(url, headers={"Content-Type": "application/json"}, params=kwargs)
    except Exception:
        print("Network exception occurred")

    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(f"POST to {url}")
    try:
        # Post review to Cloudant DB
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=json_payload)
    except Exception:
        print("Network exception occurred")
        return None

    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = response.json()
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `dealer` object
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                zip=dealer["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []

    json_result = get_request(url, **kwargs)
    if json_result:
        reviews = json_result.get("entries", [])

        for review in reviews:
            # Create a DealerReview object with values in `review` object
            review_obj = DealerReview(
                review["name"],
                review["dealership"],
                review["review"],
                review["purchase"],
                review["id"]
            )

            # Populate optional fields of DealerReview object
            if "purchase_date" in review:
                review_obj.purchase_date = review["purchase_date"]
            if "car_make" in review:
                review_obj.car_make = review["car_make"]
            if "car_model" in review:
                review_obj.car_model = review["car_model"]
            if "car_year" in review:
                review_obj.car_year = review["car_year"]

            # Analyze sentiment of the review
            review_obj.sentiment = analyze_review_sentiment(review_obj.review)
            results.append(review_obj)
            print(review)
        return results


def analyze_review_sentiment(text):
    """ Analyze review tone using IBM NLU service """
    url = f"{settings.NLU_API_ENDPOINT}/v1/analyze"

    params = {
        "apikey": settings.NLU_API_KEY,
        "text": text,
        "version": "2021-08-01",
        "features": "sentiment",
        "return_analyzed_text": False,
        "language": "en",
    }

    response = get_request(url, **params)

    if "sentiment" in response:
        return response["sentiment"]["document"]["label"]

    return ""

from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .models import Dealership, CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Handle user login."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"

    return JsonResponse(response_data)


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration_view(request):
    """Handle user registration."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data.get("email", "")

    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("%s is a new user", username)

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "error": "Already Registered"})


def get_dealerships(request, state="All"):
    """Fetch dealerships from backend service."""
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealers(request):
    """Fetch dealerships from local DB."""
    dealers = Dealership.objects.all()
    results = [
        {
            "id": dealer.id,
            "full_name": dealer.full_name,
            "city": dealer.city,
            "address": dealer.address,
            "zip": dealer.zip,
            "state": dealer.state,
        }
        for dealer in dealers
    ]
    return JsonResponse({"status": 200, "dealers": results})


def get_dealer_details(request, dealer_id):
    """Fetch dealer details from backend service."""
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    """Submit a review."""
    if request.method != "POST":
        return JsonResponse(
            {"status": 405, "message": "Method not allowed"},
            status=405,
        )

    if request.user.is_anonymous:
        return JsonResponse(
            {"status": 403, "message": "Unauthorized"},
            status=403,
        )

    try:
        data = json.loads(request.body)
        required_fields = [
            "name",
            "dealership",
            "review",
            "purchase",
            "purchase_date",
            "car_make",
            "car_model",
            "car_year",
        ]

        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return JsonResponse(
                    {
                        "status": 400,
                        "message": f"Missing or empty field: {field}",
                    },
                    status=400,
                )

        post_review(data)
        return JsonResponse(
            {"status": 200, "message": "Review posted successfully"}
        )

    except Exception as e:
        return JsonResponse(
            {
                "status": 500,
                "message": f"Error in posting review: {str(e)}",
            },
            status=500,
        )


def get_dealer_reviews(request, dealer_id):
    """Fetch dealer reviews and analyze sentiment."""
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            review_detail["sentiment"] = response.get("sentiment")

        return JsonResponse({"status": 200, "reviews": reviews})

    return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def get_cars(request):
    """Fetch car models and makes."""
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})

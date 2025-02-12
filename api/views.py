from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings



# Function to fetch nutrition data from Nutritionix API
def fetch_nutrition_data(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": settings.NUTRITIONIX_APP_ID,
        "x-app-key": settings.NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json",
    }
    data = {"query": food_item}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


# View to handle meal data input
@csrf_exempt
def meal_data(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Meal data endpoint"})

    elif request.method == 'POST':
        try:
            # Parse the incoming JSON data
            body = json.loads(request.body)
            food_item = body.get("meal", "")
            print("Printing food item:", food_item)

            # Fetch nutrition data for the food item
            nutrition_data = fetch_nutrition_data(food_item)

            # Return the nutrition data as a response
            return JsonResponse(nutrition_data, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


# View to aggregate daily nutrient totals (placeholder)
@csrf_exempt
def nutrition_summary(request):
    if request.method == 'GET':
        # Placeholder response for daily nutrient aggregation
        # Replace this with actual logic for aggregating nutrients from stored meals
        sample_summary = {
            "calories": 1500,
            "protein": 50,
            "carbohydrates": 200,
            "fats": 60,
            "vitamins": {"Vitamin A": 50, "Vitamin C": 30},
        }
        return JsonResponse(sample_summary, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# View to provide food suggestions based on nutrient deficiencies (placeholder)
@csrf_exempt
def suggestions(request):
    if request.method == 'GET':
        # Placeholder response for food suggestions
        # Replace this with actual logic to calculate deficiencies and suggest foods
        sample_suggestions = [
            {"food": "Spinach", "nutrient": "Vitamin A", "amount_per_serving": 100},
            {"food": "Chicken Breast", "nutrient": "Protein", "amount_per_serving": 30},
        ]
        return JsonResponse(sample_suggestions, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

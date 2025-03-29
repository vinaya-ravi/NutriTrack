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


# View to provide food suggestions based on nutrient deficiencies
@csrf_exempt
def suggestions(request):
    if request.method == 'GET':
        try:
            # Example of daily recommended values (can be dynamic based on user profile)
            recommended_values = {
                "calories": 2000,
                "protein": 75,
                "carbohydrates": 300,
                "fats": 70,
                "Vitamin A": 100,
                "Vitamin C": 90,
            }

            # Example of current daily intake (replace with real aggregated data)
            current_intake = {
                "calories": 1500,
                "protein": 50,
                "carbohydrates": 200,
                "fats": 60,
                "Vitamin A": 50,
                "Vitamin C": 30,
            }

            # Calculate deficiencies
            deficiencies = {
                nutrient: recommended_values[nutrient] - current_intake.get(nutrient, 0)
                for nutrient in recommended_values
                if recommended_values[nutrient] > current_intake.get(nutrient, 0)
            }

            # Fetch food suggestions for deficiencies using Nutritionix API
            suggestions = []
            for nutrient, deficiency in deficiencies.items():
                url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
                headers = {
                    "x-app-id": settings.NUTRITIONIX_APP_ID,
                    "x-app-key": settings.NUTRITIONIX_APP_KEY,
                    "Content-Type": "application/json",
                }
                query = f"foods high in {nutrient}"
                response = requests.post(url, json={"query": query}, headers=headers)

                if response.status_code == 200:
                    foods = response.json().get("foods", [])
                    for food in foods[:3]:  # Limit to top 3 suggestions per nutrient
                        suggestions.append({
                            "food_name": food["food_name"],
                            "nutrient": nutrient,
                            "amount_per_serving": food.get("nf_calories", None),
                        })

            return JsonResponse(suggestions, safe=False, status=200)

        except Exception as e:
            return HttpResponseBadRequest(str(e))

    return JsonResponse({"error": "Invalid request method"}, status=405)

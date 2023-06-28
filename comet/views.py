import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .comet import get_user, login, map_freelancer
from .models import Freelancer, User
from .serializers import FreelancerDetailSerializer


@csrf_exempt
def auth(request):
    if request.method != 'POST':
        return JsonResponse({"error": "method not allowed"}, status=405)
    else:
        if request.content_type != 'application/json':
            payload = {
                "error": "invalid content type. expected application/json."}
            return JsonResponse(payload, status=400)

        try:
            body = json.loads(request.body)

            email = body.get('username')
            password = body.get('password')

            if (email is None or password is None):
                payload = {"error": "provide username and password."}
                return JsonResponse(payload, status=400)

        except json.JSONDecodeError:
            payload = {"error": "invalid json payload."}
            return JsonResponse(payload, status=400)

        # Check if provided login credentials are valid. If it is, logic flows and creates a user with empty freelancer.
        # We do this because we dont want to try to access invalid credentials in /pull.
        # It slows down /auth process a lot but saves more time later.
        login_response = login(email=email, password=password)

        if 'error' in login_response:
            return JsonResponse({'error': login_response['error']}, status=400)

        try:
            user = User.objects.get(email=email)
            user.password = password
            user.save()

        except User.DoesNotExist:
            user = User(email=email, password=password)
            user.save()

        response_payload = {
            'id': user.id,
        }

        return JsonResponse(response_payload, status=200)


@csrf_exempt
def pull(request):
    if request.method != 'POST':
        return JsonResponse({"error": "method not allowed"}, status=405)

    if request.content_type != 'application/json':
        payload = {"error": "invalid content type. expected application/json."}
        return JsonResponse(payload, status=400)

    try:
        # Check if provided request body is valid.
        body = json.loads(request.body)
        user_id = body.get('id')

        if user_id is None:
            payload = {"error": "id required."}
            return JsonResponse(payload, status=400)

    except json.JSONDecodeError:
        payload = {"error": "invalid json payload."}
        return JsonResponse(payload, status=400)

    try:
        # Get user from the DB with provided user id.  
        user = User.objects.get(id=user_id)
        freelancer_data = get_user(email=user.email, password=user.password)

        if 'error' in freelancer_data:
            return JsonResponse({'error': freelancer_data['error']}, status=400)

        # Map freelancer makes the response body uniformat with the Freelancer model and saves to DB as related to the User model.
        map_freelancer(user=user, response=freelancer_data)

        # After saving to DB, we call it from DB and serialize it for response. 
        freelancer = Freelancer.objects.get(user_id=user_id)
        serialized_freelancer = FreelancerDetailSerializer(freelancer)

        return JsonResponse(serialized_freelancer.data, status=200)

    except User.DoesNotExist:
        return JsonResponse({'error': 'user not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

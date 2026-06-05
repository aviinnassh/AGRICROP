from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from django.http import HttpResponse, JsonResponse
from .models import crop, crop_recommed, CropModel, Fertilizer, fertilizer_recommed
import numpy as np
import pickle as p
import os
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages


# ------------------------------- Home ---------------------------------
def Index(request):
    if not request.user.is_authenticated:
        return render(request, 'base.html')
        
    recent_recommend = crop_recommed.objects.all().order_by('-cr_id')[:4]
    return render(request, 'index.html', {'recent_recommend': recent_recommend})


# ------------------------------- Auth ---------------------------------
def login_view(request):
    if request.method == 'POST':
        login_id = request.POST.get('username')
        p = request.POST.get('password')
        
        # Check if the user entered an email address
        if '@' in login_id:
            user_obj = User.objects.filter(email=login_id).first()
            if user_obj:
                u = user_obj.username
            else:
                u = login_id
        else:
            u = login_id
            
        user = authenticate(request, username=u, password=p)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username/email or password.')
            return render(request, 'base.html', {'login_error': True})
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        c = request.POST.get('confirm_password')
        
        if p != c:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'base.html', {'register_error': True})
            
        if User.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'base.html', {'register_error': True})
            
        user = User.objects.create_user(username=u, email=e, password=p)
        auth_login(request, user)
        return redirect('home')
    return redirect('home')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

# ------------------------------- Crop ---------------------------------
def Crop(request):
    crops = crop.objects.all()
    return render(request, 'crop.html', {"crops": crops})


def Crop_details(request, crop_name):
    crop_details = get_object_or_404(crop, crop_name=crop_name)
    return render(request, 'crop_details.html', {"crop_details": crop_details})


# ------------------------------- Recommendation ---------------------------------
def Crop_recommend(request):
    if request.method == 'POST':
        model, encoder, accuracy = Recommendation('Crop_Recommendation.pkl')
        result = predict_data(model, encoder, request)
        crops_to_fetch = [c.strip().lower() for c in result.cr_crop.split(" or ")]
        result_crop_data = list(crop.objects.filter(crop_name__in=crops_to_fetch))

        return render(request, 'crop_recommend_view.html', {
            'result': result,
            'result_crop_data': result_crop_data
        })

    return render(request, 'crop_recommend.html')

# ------------------------------- Fertilizer ---------------------------------
GLOBAL_FERTILIZER_MODEL = None

def Fertilizer_suggest(request):
    crops = crop.objects.all()
    if request.method == 'POST':
        t = float(request.POST.get('temperature', 0))
        h = float(request.POST.get('humidity', 0))
        m = float(request.POST.get('moisture', 0))
        soil = request.POST.get('soil_type', 'Sandy')
        crop_type = request.POST.get('crop_type', 'Maize')
        n = int(request.POST.get('nitrogen', 0))
        phos = int(request.POST.get('phosphorous', 0))
        k = int(request.POST.get('potassium', 0))
        
        try:
            global GLOBAL_FERTILIZER_MODEL
            if GLOBAL_FERTILIZER_MODEL is None:
                file_path = os.path.join('CropRecommendationApp', 'Model', 'Fertilizer_Recommendation.pkl')
                with open(file_path, 'rb') as f:
                    GLOBAL_FERTILIZER_MODEL = p.load(f)
            
            model, soil_encoder, crop_encoder, fertilizer_encoder = GLOBAL_FERTILIZER_MODEL
                
            soil_encoded = soil_encoder.transform([soil])[0]
            
            # Handle crops that are not in the ML dataset
            if crop_type in crop_encoder.classes_:
                crop_encoded = crop_encoder.transform([crop_type])[0]
            else:
                # Fallback to a generic crop type (e.g., encoded 0 or 'Wheat') so the model doesn't crash
                # The model prediction relies heavily on NPK and Soil Type anyway
                crop_encoded = 0
            
            # Predict
            pred = model.predict(np.array([[t, h, m, soil_encoded, crop_encoded, n, k, phos]]))
            recommendation = fertilizer_encoder.inverse_transform(pred)[0]
            
            try:
                fert_obj = Fertilizer.objects.get(name=recommendation)
                details = fert_obj.description
            except Fertilizer.DoesNotExist:
                details = "A specialized fertilizer recommended by our AI based on your specific soil and environmental conditions."
            
            # Save history to database if the user is authenticated (or just save the name)
            farmer_name = request.user.username if request.user.is_authenticated else "Guest"
            history = fertilizer_recommed(
                fr_farmername=farmer_name,
                fr_crop=crop_type,
                fr_soil=soil,
                fr_nitrogen=n,
                fr_phosphorous=phos,
                fr_potassium=k,
                fr_temperature=t,
                fr_humidity=h,
                fr_moisture=m,
                fr_fertilizer=recommendation
            )
            history.save()
            
        except Exception as e:
            recommendation = "Error"
            details = f"Could not generate prediction. Make sure all inputs are valid. ({e})"
            
        image_name = recommendation.replace(" ", "_").replace("-", "_").lower() + ".png"
        
        result = {
            'crop': crop_type,
            'nitrogen': n,
            'phosphorous': phos,
            'potassium': k,
            'recommendation': recommendation,
            'details': details,
            'image_name': image_name
        }
        
        return render(request, 'fertilizer_result.html', {'result': result})
        
    return render(request, 'fertilizer_suggest.html', {'crops': crops})

# ------------------------------- Disease Detection ---------------------------------
import random

def Disease_detect(request):
    if request.method == 'POST':
        # Simulate an image upload and AI detection process
        image_file = request.FILES.get('leaf_image')
        crop_type = request.POST.get('crop_type', 'Unknown')
        
        # Mock ML results for demonstration
        possible_diseases = [
            {"name": "Healthy", "confidence": "98.2%", "status": "success", "desc": "Your plant is completely healthy! Keep up the good work with watering and fertilization.", "action": "No action needed."},
            {"name": "Early Blight", "confidence": "91.5%", "status": "warning", "desc": "We detected early blight. It's a fungal disease that affects the lower leaves first.", "action": "Apply a copper-based fungicide and ensure proper spacing between plants for airflow."},
            {"name": "Rust Disease", "confidence": "87.4%", "status": "warning", "desc": "Rust fungus detected. It appears as orange or brown pustules on the undersides of leaves.", "action": "Remove affected leaves and apply neem oil or sulfur fungicides."},
            {"name": "Powdery Mildew", "confidence": "94.1%", "status": "warning", "desc": "Fungal disease that looks like white powder on leaves.", "action": "Increase air circulation, avoid overhead watering, and apply potassium bicarbonate."}
        ]
        
        # Select a random mock result
        result = random.choice(possible_diseases)
        result['crop'] = crop_type
        
        # To simulate the uploaded image being shown, we'll just pass a flag
        result['has_image'] = True if image_file else False
        
        return render(request, 'disease_result.html', {'result': result})
        
    return render(request, 'disease_detect.html')

# ------------------------------- Load ML Model ---------------------------------
GLOBAL_CROP_MODEL = None

def Recommendation(recommend_file):
    global GLOBAL_CROP_MODEL
    if GLOBAL_CROP_MODEL is None:
        file_path = os.path.join('CropRecommendationApp', 'Model', recommend_file)
        with open(file_path, 'rb') as f:
            GLOBAL_CROP_MODEL = p.load(f)
    return GLOBAL_CROP_MODEL


# ------------------------------- Prediction Logic ---------------------------------
def predict_data(model, encoder, request):
    if request.user.is_authenticated:
        farmer_name = request.user.username
    else:
        farmer_name = request.POST.get('farmer_name')
        
    soil_nitrogen = int(request.POST.get('soil_nitrogen'))
    soil_phosphorous = int(request.POST.get('soil_phosphorous'))
    soil_potassium = int(request.POST.get('soil_potassium'))
    soil_temperature = float(request.POST.get('soil_temperature'))
    relative_humidity = float(request.POST.get('relative_humidity'))
    soil_ph = float(request.POST.get('soil_ph'))
    rainfall = float(request.POST.get('rainfall'))

    predict_details = [soil_nitrogen, soil_phosphorous, soil_potassium,
                       soil_temperature, relative_humidity, soil_ph, rainfall]
    
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(np.array([predict_details]))[0]
        top2_indices = np.argsort(probabilities)[-2:][::-1]
        
        prob1 = probabilities[top2_indices[0]]
        prob2 = probabilities[top2_indices[1]]
        
        # Calculate an independent match percentage.
        # Anchor the top crop to a ~99% match, and scale the second crop relative to it.
        match1 = 99.5
        match2 = (prob2 / prob1) * match1 if prob1 > 0 else 0
        
        crop1 = encoder.inverse_transform([top2_indices[0]])[0]
        crop2 = encoder.inverse_transform([top2_indices[1]])[0]
        
        # Condition: suggest both if the second crop's match percentage is >= 80%
        if match2 >= 80.0:
            recommend_crop = f"{crop1} or {crop2}"
        else:
            recommend_crop = crop1
    else:
        encoded_pred = model.predict(np.array([predict_details]))
        recommend_crop = encoder.inverse_transform(encoded_pred)[0]

    data = crop_recommed(
        cr_farmername=farmer_name,
        cr_nitrogen=soil_nitrogen,
        cr_phosphorous=soil_phosphorous,
        cr_potassium=soil_potassium,
        cr_ph=soil_ph,
        cr_temperature=soil_temperature,
        cr_humidity=relative_humidity,
        cr_rainfall=rainfall,
        cr_crop=recommend_crop
    )
    data.save()

    return data
# ------------------------------- Error Pages ---------------------------------
def Error_404(request, exception):
    return render(request, '404.html')


def Error_500(request):
    return render(request, '500.html')

# ------------------------------- Dashboard ---------------------------------
def Dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    import json
    
    # Filter by user's username
    user_crops = crop_recommed.objects.filter(cr_farmername=request.user.username)
    
    # Soil Health Data (Averages for the user)
    soil_data = user_crops.aggregate(
        avg_n=Avg('cr_nitrogen'),
        avg_p=Avg('cr_phosphorous'),
        avg_k=Avg('cr_potassium'),
        avg_ph=Avg('cr_ph')
    )
    
    # Handle case where user has no records
    if not soil_data['avg_n']:
        soil_data = {'avg_n': 0, 'avg_p': 0, 'avg_k': 0, 'avg_ph': 0}
    
    # Mock Disease History (since there's no model for this)
    disease_data = {
        'labels': ['Leaf Blight', 'Rust', 'Powdery Mildew', 'Root Rot', 'Healthy'],
        'data': [15, 10, 5, 8, 62]
    }
    
    # Mock Yield Reports (Tons per Hectare over years)
    yield_data = {
        'labels': ['2021', '2022', '2023', '2024', '2025'],
        'data': [2.4, 2.8, 2.6, 3.2, 3.5]
    }
    
    # Weather Data (Averages per Recommended Crop for the user)
    weather_stats = user_crops.values('cr_crop').annotate(
        avg_temp=Avg('cr_temperature'),
        avg_hum=Avg('cr_humidity'),
        avg_rain=Avg('cr_rainfall')
    ).order_by('-avg_rain')[:5]
    
    weather_labels = [w['cr_crop'] for w in weather_stats]
    weather_temp = [round(w['avg_temp'], 1) if w['avg_temp'] else 0 for w in weather_stats]
    weather_rain = [round(w['avg_rain'], 1) if w['avg_rain'] else 0 for w in weather_stats]

    context = {
        'soil_data': json.dumps(soil_data),
        'disease_data': json.dumps(disease_data),
        'yield_data': json.dumps(yield_data),
        'weather_labels': json.dumps(weather_labels),
        'weather_temp': json.dumps(weather_temp),
        'weather_rain': json.dumps(weather_rain),
    }
    return render(request, 'dashboard.html', context)


# ------------------------------- Dashboard API ---------------------------------
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_predict_dashboard(request):
    import json
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            n = int(data.get('n', 0))
            p_val = int(data.get('p', 0))
            k = int(data.get('k', 0))
            temp = float(data.get('temp', 0))
            humidity = float(data.get('humidity', 0))
            ph = float(data.get('ph', 0))
            rainfall = float(data.get('rainfall', 0))
            moisture = float(data.get('moisture', 0))
            soil_type = data.get('soil', 'Sandy')
            crop_type = data.get('crop', 'Maize')

            # Predict Crop
            crop_model, crop_encoder, _ = Recommendation('Crop_Recommendation.pkl')
            try:
                encoded_crop_pred = crop_model.predict(np.array([[n, p_val, k, temp, humidity, ph, rainfall]]))
                recommend_crop = crop_encoder.inverse_transform(encoded_crop_pred)[0]
            except Exception as e:
                recommend_crop = "Unknown"

            # Predict Fertilizer
            global GLOBAL_FERTILIZER_MODEL
            if GLOBAL_FERTILIZER_MODEL is None:
                file_path = os.path.join('CropRecommendationApp', 'Model', 'Fertilizer_Recommendation.pkl')
                with open(file_path, 'rb') as f:
                    GLOBAL_FERTILIZER_MODEL = p.load(f)
            fert_model, soil_encoder, fert_crop_encoder, fertilizer_encoder = GLOBAL_FERTILIZER_MODEL
            
            try:
                soil_encoded = soil_encoder.transform([soil_type])[0]
                # Use the freshly predicted crop for the fertilizer model!
                if recommend_crop in fert_crop_encoder.classes_:
                    crop_encoded = fert_crop_encoder.transform([recommend_crop])[0]
                else:
                    crop_encoded = 0
                fert_pred = fert_model.predict(np.array([[temp, humidity, moisture, soil_encoded, crop_encoded, n, k, p_val]]))
                recommend_fertilizer = fertilizer_encoder.inverse_transform(fert_pred)[0]
            except Exception as e:
                recommend_fertilizer = "Balanced NPK"

            return JsonResponse({
                'predicted_crop': recommend_crop,
                'predicted_fertilizer': recommend_fertilizer
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# ------------------------------- Admin Page ---------------------------------
def Admin(request):
    return render(request, 'AGRICROP/admin/signin.html')
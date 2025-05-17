from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from .models import User, Challenge
from .decorators import admin_required
from .models import ChallengeResult
from django.shortcuts import render, redirect, get_object_or_404
from .models import Challenge, ChallengeResult
from django.utils.dateparse import parse_datetime



import joblib
import os
import pickle
import pandas as pd
import numpy as np
import ast
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import User, Challenge, ChallengeResult
from .decorators import admin_required
import joblib
import os
import pickle
import pandas as pd
import numpy as np
import ast

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Challenge, ChallengeResult

# /////////////////////////////////////////////////////////////////////////////////
# user authentication and authorization and insights PAGE
# Home Page View for Users
def home(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        username = user.username  # Get the username from the User model
        points = user.points  # Get the points (assuming 'points' is a field in the User model)
        
        # Pass the username and points to the template
        return render(request, 'html/user/home.html', {'username': username, 'points': points})
    else:
        # If the user is not logged in, redirect to the login page
        return redirect('login')

# Admin Home View
def home_admin(request):
    return render(request, 'html/admin/home_admin.html')


# Custom Login View (Removed Django Auth)
def login_view(request):
    return render(request, 'html/both/login.html')


# Custom Signup View (Removed Django Auth)
def signup_view(request):
    return render(request, 'html/both/signup.html')

# Custom Login Authentication
def login_authentication(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('pass')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):  # This will check the hashed password
                request.session['user_id'] = user.id
                request.session['user_type'] = user.user_type
                if user.user_type == 'admin':
                    return redirect('home_admin')  # For admin
                else:
                    return redirect('home')  # For regular user
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, 'html/both/login.html', {'messages': messages.get_messages(request)})


def signup_process(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('mail')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confpass')

        if not all([username, email, password, confirm_password]):
            messages.error(request, "All fields are required")
            return redirect('signup')
        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('signup')
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        try:
            user = User(username=username, email=email, user_type='user')
            user.set_password(password)  # Hash the password before saving
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('signup')
    return redirect('signup')


# Custom Logout View
def logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('login')


# admin insight page gives insight about the data given by our client
@admin_required
def insights_admin(request):
    return render(request, 'html/admin/insights_admin.html')


def logout_view(request):
    logout(request)
    return redirect('login')  # or 'login' depending on your flow




















# ///////////////////////////////////////////////////////////////////////////////
# challenge handling in user and admin pages
# User Challenge Listing Page (active challenges only)
def challenge(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Only show challenges that are still ongoing (is_ended=False)
    challenges = Challenge.objects.filter(is_ended=False)
    return render(request, 'html/user/challenge.html', {'challenges': challenges})

# Admin: End Challenge Page (active challenges only)
def end_challenge_page(request):
    challenges = Challenge.objects.all()
    return render(request, 'html/admin/end_challenge.html', {'challenges': challenges})

# Admin: End Challenge Logic
@admin_required
def end_challenge(request, challenge_id):
    try:
        challenge = Challenge.objects.get(id=challenge_id)
        
        if challenge.is_ended:
            return redirect('end_challenge_page')
        
        challenge.is_ended = True
        challenge.save()

        top_users = ChallengeResult.objects.filter(challenge=challenge).order_by('-accuracy')[:3]
        reward_distribution = [1.0, 0.75, 0.5]

        for idx, result in enumerate(top_users):
            reward_points = challenge.points * reward_distribution[idx]
            result.user.points += int(reward_points)
            result.user.save()

        return redirect('end_challenge_page')

    except Challenge.DoesNotExist:
        return redirect('end_challenge_page')

def submit_prediction(request, challenge_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        challenge = get_object_or_404(Challenge, id=challenge_id)

        # Block updates if already submitted
        if ChallengeResult.objects.filter(user=user, challenge=challenge).exists():
            return redirect('challenge')

        user_prediction = float(request.POST.get('prediction'))
        expected_result = challenge.expected_result
        accuracy = compute_accuracy(user_prediction, expected_result)

        # Create only if not already submitted
        ChallengeResult.objects.create(
            user=user,
            challenge=challenge,
            accuracy=accuracy
        )

        return redirect('all_challenges_scoreboard')

    return redirect('challenge_detail', challenge_id=challenge_id)

# View All Challenges Scoreboard
def all_challenges_scoreboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    challenges = Challenge.objects.all()
    challenge_results = {}

    for challenge in challenges:
        results = ChallengeResult.objects.filter(challenge=challenge).select_related('user').order_by('-accuracy')
        challenge_results[challenge] = results

    return render(request, 'html/user/scoreboard.html', {
        'challenge_results': challenge_results
    })
# admin new challenge page allows admin to create new challenges for users gamification:

@admin_required
def new_challenge(request):
    if request.method == 'POST':
        try:
            # Get the form data
            title = request.POST.get('title')
            description = request.POST.get('description')
            expected_result = float(request.POST.get('expected_result'))
            end_time = request.POST.get('end_time')  # Assuming the end_time is passed in a valid datetime format
            points = int(request.POST.get('points'))  # Assuming points are passed as an integer

            # Parse end_time if it's in string format
            if end_time:
                end_time = parse_datetime(end_time)  # Converts string to datetime object

            # Create the Challenge instance with all fields
            Challenge.objects.create(
                title=title,
                description=description,
                expected_result=expected_result,
                end_time=end_time,
                points=points
            )
        except Exception as e:
            return redirect('new_challenge')

    return render(request, 'html/admin/new_challenge_admin.html')


# end challenge page allows admin to end the challenge and give points to the user:
@admin_required
def end_challenge(request, challenge_id):
    try:
        challenge = Challenge.objects.get(id=challenge_id)

        if challenge.is_ended:
            return redirect('end_challenge_page')

        # Mark the challenge as ended
        challenge.is_ended = True  
        challenge.save()

        # Reward top users
        top_users = ChallengeResult.objects.filter(challenge=challenge).order_by('-accuracy')[:3]
        reward_distribution = [1.0, 0.75, 0.5]
        for idx, result in enumerate(top_users):
            result.user.points += int(challenge.points * reward_distribution[idx])
            result.user.save()

        return redirect('end_challenge_page')

    except Challenge.DoesNotExist:
        return redirect('end_challenge_page')

    except Exception as e:
        return redirect('end_challenge_page')


def scoreboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    users = User.objects.filter(user_type='user').order_by('-points')
    return render(request, 'html/user/scoreboard.html' )


# Compute Prediction Accuracy
def compute_accuracy(predicted, actual):
    if actual == 0:
        return 0.0
    accuracy = 100 - (abs(predicted - actual) / actual) * 100
    if accuracy < 0 or accuracy > 100:
        return 0.0
    else:
        return accuracy












# ///////////////////////////////////////////////////////////////////////////
# prediction models

# Responsible for predicting the price of a product based on the given parameters (Dynamic Pricing Model):
# Utility Functions

Q_TABLE_PATH = os.path.join(settings.BASE_DIR, 'ml_model', 'trained_model_RL_2.pkl')
with open(Q_TABLE_PATH, 'rb') as f:
    q_table = pickle.load(f)

def hamming_distance(t1, t2):
    return sum(a != b for a, b in zip(t1, t2))

def safe_literal_eval_tuple_keys(q_table):
    parsed_keys = []
    for k in q_table.keys():
        try:
            parsed = ast.literal_eval(k)
            if isinstance(parsed, tuple) and len(parsed) == 6:
                parsed_keys.append((parsed, k))
        except (ValueError, SyntaxError):
            continue
    return parsed_keys

def predict_price(date, onpromotion, oil_price, current_price, family_encoded, store_type_encoded):
    dt = pd.to_datetime(date)
    day_of_week = dt.weekday()
    is_weekend = int(day_of_week >= 5)

    oil_bin = pd.cut([oil_price], bins=[0, 40, 60, 100], labels=[0, 1, 2])[0]
    if pd.isnull(oil_bin):
        return {
            "recommended_action": None,
            "action_meaning": "Oil price out of expected range.",
            "recommended_price": None
        }

    current_state = (day_of_week, int(onpromotion), is_weekend, int(oil_bin), int(family_encoded), int(store_type_encoded))
    state_str = str(current_state)

    if state_str in q_table:
        state_action = q_table[state_str]
    else:
        parsed_q_table_keys = safe_literal_eval_tuple_keys(q_table)
        if not parsed_q_table_keys:
            return {
                "recommended_action": None,
                "action_meaning": "No valid states in Q-table.",
                "recommended_price": None
            }

        closest_state = min(
            parsed_q_table_keys,
            key=lambda x: hamming_distance(current_state, x[0])
        )[1]
        state_action = q_table[closest_state]

    if isinstance(state_action, list):
        max_value = max(v for _, v in state_action)
        best_actions = [a for a, v in state_action if v == max_value]
    elif isinstance(state_action, dict):
        max_value = max(state_action.values())
        best_actions = [a for a, v in state_action.items() if v == max_value]
    else:
        return {
            "recommended_action": None,
            "action_meaning": "Unsupported state_action format.",
            "recommended_price": None
        }

    chosen_action = np.random.choice(best_actions)
    price_change = {0: -0.05, 1: 0.0, 2: 0.05}[chosen_action]
    new_price = current_price * (1 + price_change)

    return {
        "recommended_action": chosen_action,
        "action_meaning": {0: "Decrease 5%", 1: "Keep", 2: "Increase 5%"}[chosen_action],
        "recommended_price": round(new_price, 2)
    }

@admin_required
def predict_admin(request):
    if request.method == 'POST':
        try:
            date = request.POST.get('date')
            onpromotion = int(request.POST.get('onpromotion'))
            oil_price = float(request.POST.get('oil_price'))
            current_price = float(request.POST.get('current_price'))
            family = int(request.POST.get('product'))
            store_type = int(request.POST.get('store_type'))

            result = predict_price(date, onpromotion, oil_price, current_price, family, store_type)

            return render(request, 'html/admin/predict_admin.html', {
                'prediction': {
                    'recommended_price': result['recommended_price'],
                    'recommended_action': result.get('recommended_action'),
                    'action_meaning': result['action_meaning']
                }
            })

        except Exception as e:
            return render(request, 'html/admin/predict_admin.html', {
                'prediction': {
                    'recommended_price': None,
                    'action_meaning': f"Error during prediction: {e}"
                }
            })

    return render(request, 'html/admin/predict_admin.html')


# Responsible for predicting the demand of a product based on the given parameters(Demand Prediction Model):


# Load model, encoder, and features
with open(os.path.join(settings.BASE_DIR, 'ml_model', 'xgboost_model.pkl'), 'rb') as f:
    trained_model = pickle.load(f)

with open(os.path.join(settings.BASE_DIR, 'ml_model', 'binary_encoder.pkl'), 'rb') as f:
    binary_encoder = pickle.load(f)

model_features = [
    'store_nbr', 'onpromotion', 'cluster', 'dcoilwtico', 'day', 'month',
    'week', 'year', 'day_of_week', 'is_weekend', 'quarter', 'season',
    'Days_to_Thanksgiving', 'Days_to_Christmas', 'is_holiday', 'price',
    'lag_1_log_sales', 'lag_7_log_sales', 'lag_14_log_sales', 'lag_promo_1',
    'rolling_promo_7', 'rolling_7_log_sales', 'rolling_14_log_sales',
    'family_0', 'family_1', 'family_2', 'family_3', 'family_4', 'family_5',
    'city_0', 'city_1', 'city_2', 'city_3', 'city_4', 'holiday_type_0',
    'holiday_type_1', 'holiday_type_2', 'store_type_0', 'store_type_1',
    'store_type_2'
]

def predict_demand(user_input, model, binary_encoder, model_features):
    user_input['date'] = pd.to_datetime(user_input['date'])
    if user_input['date'] < pd.to_datetime('2017-01-01'):
        raise ValueError("Date must be after 2017.")

    user_input_df = pd.DataFrame([user_input])

    # Date features
    user_input_df['day'] = user_input_df['date'].dt.day
    user_input_df['month'] = user_input_df['date'].dt.month
    user_input_df['week'] = user_input_df['date'].dt.isocalendar().week
    user_input_df['year'] = user_input_df['date'].dt.year
    user_input_df['day_of_week'] = user_input_df['date'].dt.dayofweek
    user_input_df['is_weekend'] = user_input_df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    user_input_df['quarter'] = user_input_df['date'].dt.quarter
    user_input_df['season'] = user_input_df['month'].apply(
        lambda x: 0 if x in [2, 3] else 1 if x in [4, 5, 6] else 2 if x in [7, 8]
        else 3 if x in [9, 10, 11] else 4
    )

    # Holidays
    user_input_df['Days_to_Thanksgiving'] = (
        pd.to_datetime(user_input_df["year"].astype(str) + "-11-24") - user_input_df["date"]
    ).dt.days.astype(int)
    user_input_df['Days_to_Christmas'] = (
        pd.to_datetime(user_input_df["year"].astype(str) + "-12-24") - user_input_df["date"]
    ).dt.days.astype(int)
    user_input_df['is_holiday'] = 0
    user_input_df['holiday_type'] = 'Work Day'

    # Required dummy numeric inputs
    user_input_df['price'] = user_input.get('current_price', 0)
    user_input_df['onpromotion'] = user_input.get('onpromotion', 0)
    user_input_df['dcoilwtico'] = user_input.get('dcoilwtico', 0)
    user_input_df['store_nbr'] = user_input.get('store_nbr', 1)
    user_input_df['cluster'] = user_input.get('cluster', 3)

    # Zero-filling lag/rolling values
    for col in ['lag_1_log_sales', 'lag_7_log_sales', 'lag_14_log_sales',
                'lag_promo_1', 'rolling_promo_7', 'rolling_7_log_sales', 'rolling_14_log_sales']:
        user_input_df[col] = 0

    # Encode categorical
    categorical_cols = ['family', 'store_type', 'city', 'holiday_type']
    encoded_df = binary_encoder.transform(user_input_df[categorical_cols])
    user_input_df = pd.concat([user_input_df.drop(columns=categorical_cols), encoded_df], axis=1)

    # Ensure all expected columns exist
    for col in model_features:
        if col not in user_input_df.columns:
            user_input_df[col] = 0

    user_input_df = user_input_df[model_features]
    user_input_df = user_input_df.astype(float)

    # Predict
    log_demand_pred = model.predict(user_input_df)[0]
    demand_pred = np.expm1(log_demand_pred)
    if demand_pred <= 0:
        demand_pred = 1

    return int(demand_pred)

@admin_required
def demand_admin(request):
    if request.method == 'POST':
        
        user_input = {
            'onpromotion': request.POST.get('onpromotion'),
            'date': request.POST.get('date'),
            'dcoilwtico': request.POST.get('dcoilwtico'),
            'family': request.POST.get('family'),
            'city': request.POST.get('city'),
            'current_price': request.POST.get('current_price'),
            'store_type': request.POST.get('store_type'),
            'store_nbr': 1,
            'cluster': 3
        }

        prediction = predict_demand(user_input, trained_model, binary_encoder, model_features)

        return render(request, 'html/admin/demand_admin.html', {
            'prediction': {
                'units_sold': prediction
            }
        })
    return render(request, 'html/admin/demand_admin.html')

# Streamlit Dashboard
def streamlit_dashboard(request):
    return render(request, 'html/user/Dashboard.html')


# Leaderboard View
def leaderboard_view(request):
    users = User.objects.filter(user_type='user').order_by('-points')
    return render(request, 'html/admin/leaderboard.html', {'users': users})
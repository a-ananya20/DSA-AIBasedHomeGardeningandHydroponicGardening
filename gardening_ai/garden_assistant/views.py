import math
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings
from django.http import JsonResponse
import random
from django.shortcuts import render, redirect

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from collections import deque
from django.db.models import Q
from django.shortcuts import render
from .models import Plant, SoilType, Season, GardenType  # Make sure you import all these
from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_engine import get_bot_response
from django.views.decorators.csrf import csrf_exempt



def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

def harvesthub(request):
    return render(request, 'harvesthub.html')


def home_gardening(request):
    return render(request, 'home_gardening.html')

def hydroponic_gardening(request):
    return render(request, 'hydroponic_gardening.html')

def hydroponic_methods(request):
    return render(request, 'hydroponicmethods.html')

def hydroponic_layout(request):
    method = request.GET.get('method', '').lower()
    return render(request, 'hydroponiclayout.html', {'method': method})


def plant_recommend(request):
    return render(request, 'recommendation.html')




def bfs_planting(graph, start):
    queue = deque([start])
    visited = set()
    planting_positions = []

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            planting_positions.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

    return planting_positions


def dfs_planting(graph, start):
    stack = [start]
    visited = set()
    planting_positions = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            planting_positions.append(node)

            # Add neighbors in reverse order to maintain similar ordering
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return planting_positions




def recommend_plants_smart(request):
    soil_types = SoilType.objects.all()
    seasons = Season.objects.all()
    garden_types = GardenType.objects.all()

    plants = []
    selected_soil_name = ""
    selected_season_name = ""
    selected_garden_name = ""
    sunlight = ""  # ✅ Define it safely at the beginning

    if request.method == 'POST':
        soil_id = request.POST.get('soil_types')
        season_id = request.POST.get('seasons')
        garden_id = request.POST.get('garden_types')

        filters = Q()

        if garden_id:
            selected_garden = GardenType.objects.get(id=garden_id)
            selected_garden_name = selected_garden.name.strip().lower()

            if selected_garden_name == "indoor":
                sunlight = request.POST.get('sunlight', '').strip().lower()
                

                filters = Q(garden_types__id=garden_id) & Q(is_indoor_friendly=1)

                if sunlight:
                    sunlight_processed = sunlight.strip().lower()
                   
                    plants=Plant.objects.filter(sunlight_requirement__iexact=sunlight_processed)

            else:
                if soil_id:
                    selected_soil = SoilType.objects.get(id=soil_id)
                    selected_soil_name = selected_soil.name
                    filters |= Q(soil_types__id=soil_id)

                if season_id:
                    selected_season = Season.objects.get(id=season_id)
                    selected_season_name = selected_season.name
                    filters |= Q(seasons__id=season_id)

                filters |= Q(garden_types__id=garden_id)
                plants = Plant.objects.filter(filters).distinct()

    return render(request, 'recommendation.html', {
        'soil_types': soil_types,
        'seasons': seasons,
        'garden_types': garden_types,
        'plants': plants,
        'sunlight': sunlight,  # ✅ Now it's always defined
        'selected_soil': selected_soil_name,
        'selected_season': selected_season_name,
        'selected_garden': selected_garden_name.capitalize(),
    })






# Load model once globally
MODEL_PATH = os.path.join('garden_assistant', 'models', 'plant_disease_model.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# Class labels (in the order that appears in your dataset train folder)
class_names = ['Pepper Bacterial Spot', 'Pepper Healthy', 'Potato Late Blight', 'Potato Healthy', 
                'Tomato Leaf Mold','Tomato Healthy']

home_remedies = {
    "Pepper Bacterial Spot": "Spray a solution of baking soda (1 tsp), water (1 liter), and a few drops of mild soap. Avoid overhead watering.",
    "Pepper Healthy": "No action needed! Just ensure good sunlight and avoid overwatering.",
    "Potato Late Blight": "Use neem oil spray every few days. Remove affected leaves immediately.",
    "Potato Healthy": "Keep rotating crops and ensure well-drained soil.",
    "Tomato Leaf Mold": "Apply a mix of 1 tsp baking soda, 1 tsp oil, and 1 liter water. Spray on both sides of the leaves.",
    "Tomato Healthy": "Maintain air circulation around plants and water at the base.",
}


def predict_disease(request):
    if request.method == 'POST' and request.FILES.get('leaf_image'):
        image_file = request.FILES['leaf_image']
        fs = FileSystemStorage()
        file_path = fs.save(image_file.name, image_file)
        full_path = fs.path(file_path)

        # Preprocess image
        img = image.load_img(full_path, target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions)
        predicted_label = class_names[predicted_index]
        remedy = home_remedies.get(predicted_label, "No remedy available for this disease yet.")

        return render(request, 'result.html', {
            'prediction': predicted_label,
            'image_url': fs.url(file_path),
            'remedy': remedy
        })

    return render(request, 'predict.html')



def chatbot_page(request):
    return render(request, 'chatbot.html')



def gardening_chatbot(request):
     # Initialize session state
     if 'current_node' not in request.session:
         request.session['current_node'] = 'start'
 
     if 'chat_history' not in request.session:
         request.session['chat_history'] = []
 
     if request.method == "POST":
         user_message = request.POST.get("message")
         current_node = request.session['current_node']
 
         # 🔄 Get bot response (you must return options in {label: node} format from get_bot_response)
         bot_reply, next_node, options = get_bot_response(user_message, current_node)
 
         # Update current node
         request.session['current_node'] = next_node
 
         # Store chat history
         history = request.session['chat_history']
         history.append({
             "user": user_message,
             "bot": bot_reply,
             "options": list(options.keys()) if options else []  # just show the labels to frontend
         })
         request.session['chat_history'] = history
 
         # JSON response for frontend
         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({
                 "bot_reply": bot_reply,
                 "options": options,  # full {label: node} format
                 "next_node": next_node,
                 "chat_history": request.session['chat_history']
             })
 
         # fallback for non-AJAX
         return render(request, "chatbot.html", {
             "chat_history": request.session['chat_history']
         })
 
     # For GET requests
     return render(request, "chatbot.html", {
         "chat_history": request.session.get('chat_history', [])
     })





def garden_type_selection(request):
    return render(request, 'select_type.html')

def get_dimensions(request, garden_type):
    return render(request, 'enter_dimensions.html', {'garden_type': garden_type})



@csrf_exempt
def generate_layout(request):
    if request.method == "POST":
        garden_type = request.POST.get("garden_type")
        length = request.POST.get("length")
        width = request.POST.get("width")
        shelves = request.POST.get("shelves")
        beds = request.POST.get("beds")
        algorithm = request.POST.get("algorithm", "bfs") 

        traversal_func = dfs_planting if algorithm == 'dfs' else bfs_planting
       
        
        if garden_type == 'backyard':
            layout = generate_backyard_layout(int(length), int(width))
        elif garden_type =='terrace':
            layout = generate_terrace_layout(int(length), int(width))
        elif garden_type =='indoor':
            layout = generate_indoor_layout(int(length), int(width),int(shelves))
        elif garden_type =='raised':
            layout=generate_raised_bed_layout(int(beds),int(length),int(width),traversal_func)
        elif garden_type == 'farm':
            layout = generate_farm_layout(int(length), int(width),traversal_func) 
        
        # You can pass all inputs to the next screen (layout screen)
        context = {
            "garden_type": garden_type,
            "length": length,
            "width": width,
            "shelves": shelves,
            "beds": beds,
            "layout": layout,
            "algorithm":algorithm
        }
        return render(request, "layout_result.html", context)




def generate_backyard_layout(length, width):
    layout = []
    path_row = length // 2  # Middle row for walking path

    for i in range(int(length)):
        row = []
        for j in range(int(width)):
            # Corners → Shrubs/Trees
            if (i, j) in [(1, 1), (1, width-2), (length-2, 1), (length-2, width-2)]:
                row.append("🌳")
            # Compost spot → fixed (bottom right corner)
            elif i == length - 2 and j == width - 2:
                row.append("🪴")
            # Starting point (left edge of walking path)
            elif i == path_row and j == 0:
                row.append("🚶")
            # Walking path → horizontal midline (except entry point already handled)
            elif i == path_row:
                row.append("🚶")
            # Edges → Flower bed
            elif i == 0 or i == length - 1 or j == 0 or j == width - 1:
                row.append("🌼")
            # Center → Veggies
            else:
                row.append("🥕")
        layout.append(row)
    
    return layout


def generate_terrace_layout(length, width):
    grid = []

    # Hardcoded icons for simplicity
    icons = {
        "herb": "🌿",
        "veggie": "🥬",
        "climber": "🌵",
        "vertical": "🎋"
    }

    for i in range(length):
        row = []
        for j in range(width):
            if i == 0 or i == length - 1 or j == 0 or j == width - 1:
                row.append(icons["vertical"])  # edge zones
            elif (i + j) % 3 == 0:
                row.append(icons["herb"])
            elif (i + j) % 3 == 1:
                row.append(icons["veggie"])
            else:
                row.append(icons["climber"])
        grid.append(row)
    return grid


def generate_indoor_layout(length, width, shelves):
    layout = []
    for i in range(shelves):
        if i == 0:
            # Top shelf → bright light
            row = ["☀️"] * 3
        elif i == 1:
            # Middle shelf → moderate light
            row = ["🌤️"] * 3
        else:
            # Bottom and lower → shade
            row = ["🌑"] * 3
        layout.append(row)
    return layout




def generate_raised_bed_layout(beds, length, width,traversal_func):
    plant_icons = ["🌱", "🍅", "🌶️", "🥦", "🌿"]
    layout = []
    beds = int(beds)
    length = int(length)
    width = int(width)

    

    for _ in range(beds):
        # Step 1: Build graph for this bed
        graph = {}
        for r in range(length):
            for c in range(width):
                node = (r, c)
                neighbors = []
                if r > 0: neighbors.append((r - 1, c))
                if r < length - 1: neighbors.append((r + 1, c))
                if c > 0: neighbors.append((r, c - 1))
                if c < width - 1: neighbors.append((r, c + 1))
                graph[node] = neighbors

        # Step 2: Get planting order using selected algorithm
        planting_order = traversal_func(graph, (0, 0))  # Start from top-left corner
        bed = [[None for _ in range(width)] for _ in range(length)]

        # Step 3: Fill the bed using plant icons in BFS/DFS order
        icon_index = 0
        for (r, c) in planting_order:
            bed[r][c] = plant_icons[icon_index % len(plant_icons)]
            icon_index += 1

        layout.append(bed)

    return layout





def generate_farm_layout(length, width,traversal_func, plot_size=1):
    plant_icons = [
        "🌱",  "🍆", "🥕", "🥬", "🌽"]
    length = int(length)
    width = int(width)

    rows = length // plot_size
    cols = width // plot_size
    # Step 1: Build the graph from grid
    graph = {}
    for r in range(rows):
        for c in range(cols):
            node = (r, c)
            neighbors = []

            if r > 0: neighbors.append((r - 1, c))      # up
            if r < rows - 1: neighbors.append((r + 1, c))  # down
            if c > 0: neighbors.append((r, c - 1))      # left
            if c < cols - 1: neighbors.append((r, c + 1))  # right

            graph[node] = neighbors

    # Step 2: Get planting order using BFS
    planting_order = traversal_func(graph, (0, 0))  # start from top-left corner

    # Step 3: Fill layout using planting_order
    layout = [[None for _ in range(cols)] for _ in range(rows)]
    plant_index = 0

    for (r, c) in planting_order:
        layout[r][c] = plant_icons[plant_index % len(plant_icons)]
        plant_index += 1

    return layout

# chatbot for hydroponic gardening
def chat_home(request):
    """Render the chat interface."""
    return render(request, 'chat.html')

@csrf_exempt
def chat_message(request):
    """Handle incoming chat messages and return bot responses."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()
            
            # Basic response logic - This can be expanded with more sophisticated AI/ML
            response = get_bot_response(user_message)
            
            return JsonResponse({'response': response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_bot_responses(message):
    """Generate bot response based on user input."""
    # Basic keyword matching - This can be replaced with more sophisticated AI/ML models
    keywords = {
        'nutrient': 'For hydroponic nutrients, maintain pH between 5.5-6.5 and EC levels between 1.2-2.0 mS/cm. Essential nutrients include nitrogen, phosphorus, and potassium.',
        'ph': 'The ideal pH range for most hydroponic plants is between 5.5 and 6.5. Test your water daily and adjust as needed.',
        'light': 'Most hydroponic plants need 14-16 hours of light daily. LED grow lights are energy-efficient and provide the right spectrum.',
        'temperature': 'Maintain water temperature between 65-75°F (18-24°C) for optimal nutrient absorption.',
        'system': 'Common hydroponic systems include Deep Water Culture (DWC), Nutrient Film Technique (NFT), and Ebb and Flow. Each has its advantages.',
        'plant': 'Good starter plants include lettuce, herbs, and leafy greens. These grow well in hydroponic systems.',
        'water': 'Use clean, filtered water and change it every 1-2 weeks. Monitor water levels daily.',
        'problem': 'Common issues include nutrient deficiencies, pH imbalance, and algae growth. Regular monitoring helps prevent these problems.',
    }
    
    for key, response in keywords.items():
        if key in message:
            return response
    
    return "I can help you with questions about hydroponic nutrients, pH levels, lighting, temperature, system types, plant selection, water management, and common problems. What would you like to know more about?"

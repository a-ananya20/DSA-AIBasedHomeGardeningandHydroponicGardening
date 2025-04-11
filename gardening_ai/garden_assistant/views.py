import math
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings
from django.http import JsonResponse
import random
from django.shortcuts import render, redirect
from .forms import GardenForm
from .models import GardenLayout



def home(request):
    return render(request, 'home.html')


def home_gardening(request):
    return render(request, 'home_gardening.html')

def hydroponic_gardening(request):
    return render(request, 'hydroponic_gardening.html')

def garden_form(request):
    return render(request,'garden_form.html')

def plant_recommend(request):
    return render(request, 'recommendation.html')

from django.shortcuts import get_object_or_404

# def garden_layout(request, layout_id):
#     # layout = get_object_or_404(GardenLayout, id=layout_id)
#     return render(request, 'garden_layout.html', {'layout': layout})

def garden_layout(request):
    selected_soil = request.session.get("selected_soil", "")
    recommended_plants = request.session.get("recommended_plants", [])

    return render(request, "garden_layout.html", {
        "selected_soil": selected_soil,
        "recommended_plants": recommended_plants
    })






        
        


    


from django.shortcuts import render
from .forms import GardenForm

def optimize_garden_space(request):
    recommended_plants = {
        "sandy": ["Carrots", "Radishes", "Lettuce"],
        "clay": ["Cabbage", "Broccoli", "Brussels Sprouts"],
        "loamy": ["Tomatoes", "Peppers", "Cucumbers"],
        "mixed": ["Spinach", "Peas", "Beans"]
    }

    if request.method == "POST":
        

        # Get the selected soil type first
        soil_type = request.POST.get("soil_type")  # Default to 'sandy' if not provided
        available_plants = recommended_plants.get(soil_type, [])  # Get plants based on soil type

        # Initialize form with POST data
        form = GardenForm(request.POST)
        
        # ✅ Update the choices for selected_plants before validation
        form.fields["selected_plants"].choices = [(plant, plant) for plant in available_plants]

        if form.is_valid():
            selected_plants = form.cleaned_data["selected_plants"]  # Get selected plants

            return render(request, "garden_layout.html", {
                "selected_plants": selected_plants,
                "soil_type": soil_type
            })
        else:
            print("❌ Form errors:", form.errors)
    
    else:
        # Default form initialization (GET request)
        form = GardenForm()
        form.fields["selected_plants"].choices = [(plant, plant) for plant in recommended_plants[soil_type]]  # Default to 'sandy' plants

    return render(request, "garden_form.html", {"form": form, "recommended_plants": recommended_plants})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def optimize_garden(request):
    if request.method == "POST":
        data = json.loads(request.body)
        length = int(data.get("length"))
        width = int(data.get("width"))
        
        total_area = length * width
        return JsonResponse({"total_area": total_area})




class GardenGraph:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.graph = {}

        # Create nodes for each grid cell
        for i in range(length):
            for j in range(width):
                self.graph[(i, j)] = []

        # Connect adjacent nodes
        for i in range(length):
            for j in range(width):
                if i + 1 < length:  # Down
                    self.graph[(i, j)].append((i + 1, j))
                if j + 1 < width:  # Right
                    self.graph[(i, j)].append((i, j + 1))

    def get_graph(self):
        return self.graph



from collections import deque

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



def get_planting_recommendations(area, soil_type, planting_style):
    plant_options = {
        "sandy": ["Carrots", "Radishes", "Sweet Potatoes"],
        "clay": ["Broccoli", "Cabbage", "Pumpkins"],
        "loamy": ["Tomato", "Peppers", "Beans"],
        "mixed": ["Lettuce", "Spinach", "Cucumbers"]
    }

    # Ensure the soil type exists
    suggested_plants = plant_options.get(soil_type ,[])
    
    if not suggested_plants:
        print("No plants found for this soil type!")
    return {
        "suggested_plants": suggested_plants
    }



from django.shortcuts import render
from .models import Plant, SoilType, Season
from django.apps import apps


def recommend_plants_smart(request):
    soil_types = SoilType.objects.all()
    seasons = Season.objects.all()
    plants = []
    selected_soil_name=""
    selected_season_name=""

    if request.method == 'POST':
        soil_id = request.POST.get('soil_types')
        season_id = request.POST.get('seasons')
        prefix = request.POST.get('plant_prefix', '')
        
        if soil_id and season_id:
            soil_name = SoilType.objects.get(id=soil_id).name
            season_name = Season.objects.get(id=season_id).name
            selected_soil_name=soil_name
            selected_season_name=season_name
            app_config = apps.get_app_config('garden_assistant')

            key = (soil_name, season_name)
            recommended = app_config.recommend_map.get(key, [])

            if prefix:
                matching_names = set(app_config.trie.search_prefix(prefix))
                plants = [p for p in recommended if p.name in matching_names]
            else:
                plants = recommended
    print("SoilTypes:", soil_types)
    print("Seasons:", seasons)

    return render(request, 'recommendation.html', {
        'soil_types': soil_types,
        'seasons': seasons,
        'plants': plants,
        'selected_soil':selected_soil_name,
        'selected_season':selected_season_name
    })















import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

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








# garden_assistant/views.py




from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_engine import get_bot_response

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










































from django.shortcuts import render

def garden_type_selection(request):
    return render(request, 'select_type.html')

def get_dimensions(request, garden_type):
    return render(request, 'enter_dimensions.html', {'garden_type': garden_type})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def generate_layout(request):
    if request.method == "POST":
        garden_type = request.POST.get("garden_type")
        length = request.POST.get("length")
        width = request.POST.get("width")
        shelves = request.POST.get("shelves")
        beds = request.POST.get("beds")
        



        if garden_type == 'backyard':
            layout = generate_backyard_layout(int(length), int(width))
        elif garden_type =='terrace':
            layout = generate_terrace_layout(int(length), int(width))
        elif garden_type =='indoor':
            layout = generate_indoor_layout(int(length), int(width),int(shelves))
        elif garden_type =='raised':
            layout=generate_raised_bed_layout(int(beds),int(length),int(width))
        elif garden_type == 'farm':
            layout = generate_farm_layout(int(length), int(width)) 
        
            

        # You can pass all inputs to the next screen (layout screen)
        context = {
            "garden_type": garden_type,
            "length": length,
            "width": width,
            "shelves": shelves,
            "beds": beds,
            "layout": layout
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



import random

def generate_raised_bed_layout(beds, bed_length, bed_width):
    plant_icons = ["🌱", "🍅", "🌶️", "🥦", "🌿"]
    layout = []

    for _ in range(beds):
         # Step 1: Build graph for this bed
        graph = {}
        for r in range(bed_length):
            for c in range(bed_width):
                node = (r, c)
                neighbors = []
                if r > 0: neighbors.append((r - 1, c))
                if r < bed_length - 1: neighbors.append((r + 1, c))
                if c > 0: neighbors.append((r, c - 1))
                if c < bed_width - 1: neighbors.append((r, c + 1))
                graph[node] = neighbors

        # Step 2: Get BFS planting order for this bed
        planting_order = bfs_planting(graph, (0, 0))  # Start from top-left corner
        bed = [[None for _ in range(bed_width)] for _ in range(bed_length)]

        # Step 3: Fill the bed using plant icons in BFS order
        icon_index = 0
        for (r, c) in planting_order:
            bed[r][c] = plant_icons[icon_index % len(plant_icons)]
            icon_index += 1

        layout.append(bed)

    return layout


import random

def generate_farm_layout(length, width, plot_size=1):
    plant_icons = [
        "🌱",  "🍆", "🥕", "🥬", "🌽"]

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
    planting_order = bfs_planting(graph, (0, 0))  # start from top-left corner

    # Step 3: Fill layout using planting_order
    layout = [[None for _ in range(cols)] for _ in range(rows)]
    plant_index = 0

    for (r, c) in planting_order:
        layout[r][c] = plant_icons[plant_index % len(plant_icons)]
        plant_index += 1

    return layout

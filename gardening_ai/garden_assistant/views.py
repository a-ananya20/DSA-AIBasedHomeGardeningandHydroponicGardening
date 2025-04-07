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






        
        



from django.shortcuts import render, redirect
from .models import GardenLayout
from .forms import GardenForm

# def optimize_garden_space(request):
#     recommended_plants = []  

#     if request.method == "POST":
#         form = GardenForm(request.POST)
#         if form.is_valid():
#             shape = form.cleaned_data['shape']
#             soil_type = form.cleaned_data['soil_type'].strip().lower()
#             planting_style = form.cleaned_data['planting_style']
#             length = form.cleaned_data.get('length', 1)
#             width = form.cleaned_data.get('width', 1)
#             radius = form.cleaned_data.get('radius', 1)

#             # Calculate area
#             if shape == "rectangle":
#                 area = length * width
#             elif shape == "circle":
#                 area = 3.1416 * (radius ** 2)
#             else:
#                 area = 10  

#             # Get recommended plants
#             recommendations = get_planting_recommendations(area, soil_type, planting_style)
#             recommended_plants = recommendations.get("suggested_plants", [])

#             # Debugging print statements
#             print(f"Shape: {shape}, Soil: {soil_type}, Style: {planting_style}, Area: {area}")
#             print(f"Recommended Plants: {recommended_plants}")

#             # Save form
#             optimized_layout = form.save(commit=False)
#             selected_plants = form.cleaned_data.get("selected_plants", [])
#             print("✅ Selected Plants Before Saving:", selected_plants)
#             if selected_plants:
#                 optimized_layout.selected_plants.set(selected_plants)

#             optimized_layout.save()
            

#             # Store data in session
#             request.session["selected_soil"] = optimized_layout.soil_type
#             request.session["selected_plants"] = [plant.name for plant in selected_plants]

#             return redirect("garden_layout")  # Redirect correctly

#         else:
#             print("Form errors:", form.errors)  # Debugging for errors

#     else:
#         form = GardenForm()

#     return render(request, 'garden_form.html', {'form': form, 'recommended_plants': recommended_plants})


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

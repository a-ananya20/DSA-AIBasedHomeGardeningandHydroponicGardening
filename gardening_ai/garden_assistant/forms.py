from django import forms

class GardenForm(forms.Form):  # Use forms.Form instead of ModelForm
    shape = forms.ChoiceField(choices=[
        ("rectangle", "Rectangle"), 
        ("circle", "Circle"), 
        ("irregular", "Irregular")
    ], required=True)
    
    soil_type = forms.ChoiceField(choices=[
        ("sandy", "Sandy"), 
        ("clay", "Clay"), 
        ("loamy", "Loamy"), 
        ("mixed", "Mixed")
    ], required=True)
    
    planting_style = forms.ChoiceField(choices=[
        ("rows", "Rows"), 
        ("raised_beds", "Raised Beds"), 
        ("containers", "Containers"), 
        ("mixed", "Mixed")
    ], required=True)

    # Custom field for selected plants (users will pick from predefined options)
    selected_plants = forms.MultipleChoiceField(
        choices=[],  # Initially empty, will be set in the view
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),  
        required=False
    )

    length = forms.FloatField(required=False)  # For rectangular shape
    width = forms.FloatField(required=False)
    radius = forms.FloatField(required=False)  # For circular shape

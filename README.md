# 🌿 Sustainable Gardening Assistant

Welcome to the **Sustainable Gardening Assistant** — your personal AI-powered platform for smart, sustainable, and efficient home gardening!  
This project promotes **Home Soil Gardening**, **Hydroponic Gardening**, and a community-powered **Harvest Hub** to grow, learn, and share sustainably.

---

## 🚀 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
  - [🏡 Home Soil Gardening](#-home-soil-gardening)
  - [💧 Hydroponic Gardening](#-hydroponic-gardening)
  - [🌾 Harvest Hub](#-harvest-hub)
  - [🤖 AI Gardening Chatbot](#-ai-gardening-chatbot)
  - [🪴 Plant Disease Detection](#-plant-disease-detection)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [License](#license)

---

## 📖 About the Project

This AI-powered gardening assistant simplifies sustainable gardening by offering intelligent recommendations for both soil-based and hydroponic gardens. It connects growers in a **Harvest Hub**, enabling them to exchange produce and insights. With features like smart watering, seasonal tips, and disease detection, it brings eco-friendly gardening to every home.

---

## ✨ Features

### 🏡 [Home Soil Gardening](#screenshots)
> Get step-by-step guidance for creating a soil garden based on your available space, sunlight, and climate.

### 💧 [Hydroponic Gardening](#screenshots)
> Grow plants using nutrient-rich water systems, ideal for urban or space-limited gardening.

### 🌾 [Harvest Hub](#screenshots)
> Connect with local growers to share/exchange home-grown produce within your neighborhood.

### 🤖 [AI Gardening Chatbot](#screenshots)
> Ask questions, get tips, and solve gardening problems instantly via our smart assistant.

### 🪴 [Plant Disease Detection](#screenshots)
> Upload images and get instant diagnosis and organic solutions for plant diseases.

---

## 🖼️ Screenshots

### 🏠 Home Screen
![Home Screen](screenshots/HOMESCREEN.png)

### 🟢 Dashboard
![Dashboard](screenshots/DASHBOARD.png)

### 🟢 Disease Detection
- Detection Page:  
  ![Disease Detection](screenshots/DISEASEDETECTION.png)
- Prediction Result:  
  ![Disease Prediction Result](screenshots/DISEASEPREDICTIONRESULT.png)

### 🏡 Home Soil Gardening
- Garden Dimension Page:  
  ![Garden Dimension](screenshots/GARDENDIMENSIONPAGE.png)
- Space Selection Page:  
  ![Garden Space Selection](screenshots/GARDENSPACESELECTIONPAGE.png)
- Layout Page:  
  ![Home Garden Layout](screenshots/HOMEGARDENLAYOUT.png)
- Dashboard:  
  ![Home Gardening Dashboard](screenshots/HOMEGARDENINGDASHBOARD.png)

### 💧 Hydroponic Gardening
- Dimensions Page:  
  ![Hydro Dimensions](screenshots/HYDROPONICGARDENDIMENSIONSPAGE.png)
- Chatbot:  
  ![Hydroponic Chatbot](screenshots/HYDROPONICGARDENINGCHATBOT.png)
- Dashboard:  
  ![Hydroponic Dashboard](screenshots/HYDROPONICGARDENINGDASHBOARD.png)
- Layout:  
  ![Hydroponic Layout](screenshots/HYDROPONICGARDENLAYOUT.png)
- Space Selection:  
  ![Hydroponic Space Selection](screenshots/HYDROPONICGARDENSPACESELECTIONPAGE.png)
- Nutrient Details:  
  ![Nutrient Details](screenshots/HYDROPONICNUTRIENTDETAILS.png)
- Plant Nutrient Info:  
  ![Plant Nutrient Info](screenshots/HYDROPONICPLANTNUTRIENTINFO.png)
- Plant Recommendations:  
  ![Plant Recommendations](screenshots/HYDROPONICPLANTRECOMMENDATIONS.png)

### 🌾 Harvest Hub
- Buying Page:  
  ![Harvest Hub Buying](screenshots/HARVESTHUBBUYINGPAGE.png)
- Dashboard:  
  ![Harvest Hub Dashboard](screenshots/HARVESTHUBDASHBOARD.png)
- Selling Page:  
  ![Harvest Hub Selling](screenshots/HARVESTHUBSELLINGPAGE.png)

### 💬 AI Chatbots
- Traditional Gardening Chatbot:  
  ![Traditional Chatbot](screenshots/TRADITIONALGARDENINGCHATBOT.png)

### 🌿 Planting Recommendations
![Plant Recommendations](screenshots/PLANTRECOMMENDATIONS.png)




---

## 🧱 Tech Stack

**Frontend**:  
- HTML  
- CSS  
- JavaScript  
- Bootstrap

**Backend**:  
- Python  
- Django Framework

**Database**:  
- MariaDB

**AI & ML**:  
- Plant disease detection using image classification models




## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
````

---

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

* **On Windows:**

```bash
venv\Scripts\activate
```

* **On macOS/Linux:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Up Database (MariaDB)

Make sure you have MariaDB installed and running. Then:

* Create a database (e.g., `gardeningdb`)
* Update the database connection settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gardeningdb',
        'USER': 'yourusername',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

### 5️⃣  Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```


### 7️⃣  Start the Development Server

```bash
python manage.py runserver
```

Now open your browser and go to:

```
http://127.0.0.1:8000/
```



## 📄 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software as long as the original license is included.  
See the [LICENSE](LICENSE) file for more details.


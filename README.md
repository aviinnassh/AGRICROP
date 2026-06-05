# AGRICROP: Smart Crop & Fertilizer Recommendation System

AGRICROP is a machine learning-powered web application built with Django that assists farmers in making informed agricultural decisions. By analyzing soil and environmental parameters, it provides highly accurate recommendations for which crops to plant and what fertilizers to use.

## 🌟 Features

- **Crop Recommendation:** Recommends the optimal crop to cultivate based on Nitrogen (N), Phosphorous (P), Potassium (K) levels, temperature, humidity, pH value, and rainfall.
- **Fertilizer Suggestion:** Analyzes soil nutrient data and the specific crop you are growing to recommend the most effective fertilizers to maximize yield.
- **Smart Farm Dashboard:** A clean, modern, and interactive dashboard that gives users an overview of farming metrics and insights.
- **User-Friendly Interface:** Built with a responsive and premium design to ensure ease of use across different devices.
- **AI-Driven Accuracy:** Utilizes trained machine learning models to provide reliable and data-backed agricultural predictions.

## 🚀 Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Machine Learning:** Scikit-Learn, Pandas, NumPy
- **Database:** SQLite (Default for Django)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aviinnassh/AGRICROP.git
   cd AGRICROP
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**
   *(Ensure you have a `requirements.txt` file or install necessary libraries manually such as django, scikit-learn, numpy, pandas)*
   ```bash
   pip install -r requirements.txt
   ```

5. **Generate Machine Learning Models:**
   *Because the trained models are too large for GitHub, you must generate them locally:*
   ```bash
   python retrain.py
   python train_fertilizer.py
   ```

6. **Run Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 👨‍💻 Author
- **[aviinnassh](https://github.com/aviinnassh)**

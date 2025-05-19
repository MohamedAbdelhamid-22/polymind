# PolyMind

**PolyMind** is a machine learning-powered web application designed to help businesses forecast sales, predict demand, and implement intelligent dynamic pricing strategies. Built with Django and Streamlit, the project integrates advanced predictive models and dynamic dashboards to deliver actionable retail insights.

## 🚀 Features

- 🔮 **Sales Forecasting** – Predict future sales based on historical trends, calendar events, and business activity  
- 📦 **Demand Prediction** – Estimate demand with features like promotions, seasonality, holidays, and store-specific data  
- 💰 **Dynamic Pricing** – Recommend optimized prices that maximize revenue while respecting demand elasticity  
- 🌐 **Interactive Website** – Django-powered interface for inputting parameters and retrieving predictions  
- 📊 **Streamlit Dashboards** – Visualize trends, forecasts, and pricing recommendations  

## 🛠️ Technologies Used

- **Backend:** Django (Python Web Framework)  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **ML Libraries:** XGBoost, Scikit-learn, Pandas, NumPy  
- **Dashboards:** Streamlit  
- **Model Integration:** `pickle` for model serialization  
- **Database:** MySQL  
- **Visualization:** Matplotlib, Seaborn  

## 📁 Project Structure

```
DEPI_Project/
├── deployment/                  # Django project implementation
│   ├── project/                # Django project files
│   └── manage.py               # Django management script
│
├── notebooks/                  # Jupyter notebooks for development
│   ├── Dynamic_Pricing.ipynb
│   ├── Milestone_1_Data_Collection_Exploration_Preprocessing.ipynb
│   ├── Milestone_2_Advanced_Data_Analysis_Feature_Engineering.ipynb
│   ├── Milestone_3_Machine_Learning_Model_Development.ipynb
│   └── D_Dashboard.py          # Dashboard implementation
│
├── documentation/              # Project documentation
│   ├── DEPI_Project_Presentation.pptx
│   ├── Final_DEPI_Report.docx
│   ├── Milestone_1.docx
│   ├── Milestone_2.docx
│   ├── Milestone_3.docx
│   └── Milestone_4.docx
│
└── README.md                   # Project documentation
```

## ⚙️ Installation & Setup

1. **Prerequisites**
   - MySQL Server installed and running
   - Python 3.8+

2. **Clone the Repository**
   ```bash
   git clone https://github.com/MohamedAbdelhamid-22/DEPI_Project.git
   cd DEPI_Project
   ```

3. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install mysqlclient  # MySQL database adapter for Python
   ```

5. **Database Configuration**
   - Create a MySQL database
   - Update database settings in `deployment/project/settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'your_db_name',
             'USER': 'your_db_user',
             'PASSWORD': 'your_db_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

6. **Run the Application**
   - For Django backend:
     ```bash
     cd deployment
     python manage.py migrate
     python manage.py runserver
     ```

## 👥 Team Members

Connect with us on LinkedIn:
- [Mohamed Abdelhamid](https://www.linkedin.com/in/mohamedwagdymw/)
- [Rawan Asaad](https://www.linkedin.com/in/rawan-asaad/)
- [Akram Gamal](https://www.linkedin.com/in/akram-gamal-mohamed/)
- [Alaa Eid](https://www.linkedin.com/in/alaa-e-abd-elwahhab-ae/)
- [Tarek Adel](https://www.linkedin.com/in/tarek-adell/)
- [Yosef Shabaan](https://www.linkedin.com/in/yosef-shabaan-231546341)


## 🤝 Contributing

We welcome contributions! Please fork the repository and submit pull requests for any improvements or bug fixes.

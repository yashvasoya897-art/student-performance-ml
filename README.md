#  Student Performance Prediction (ML + Django Project)

A Machine Learning based web application that predicts student performance (Marks / Pass-Fail) using academic inputs like study hours, attendance, sleep, and previous marks.

---

## Features

- Login / Register system (User Authentication)
- AI-based Marks Prediction
- Smart Feedback System (Excellent / Good / Improve)
- Performance Graph (Chart.js visualization)
- Prediction History tracking
- User Profile page
- Dark Mode UI
- Responsive Bootstrap design

---

## Machine Learning Model

- Algorithm: Linear Regression / Logistic Regression
- Input Features:
  - Study Hours
  - Attendance %
  - Sleep Hours
  - Previous Marks
- Output:
  - Predicted Marks / Pass-Fail

---

## Tech Stack

- Python (Django)
- HTML, CSS, Bootstrap 5
- Scikit-learn, Pandas, NumPy
- Chart.js
- SQLite3 Database

---

## Project Structure

mlproject/
│
├── predictor/        (Django App)
├── templates/        (HTML Files)
├── static/           (CSS/JS)
├── model.pkl         (Trained ML Model)
├── db.sqlite3        (Database)
├── manage.py

---

## Output Screenshots

(Add screenshots folder in repo)

- Home Page  
- Dashboard  
- Graph Page  

---

##  How to Run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver



# Rural Government Scheme Eligibility Engine

A **Django-based rule engine** that determines eligibility for Indian government schemes using dynamically stored rules in a database.
The system allows users to enter personal details and instantly see which schemes they qualify for, along with explanations of the eligibility rules.

---

## Project Overview

Many citizens are unaware of government schemes they qualify for. This project solves that problem by building a **rule-based eligibility engine** that evaluates scheme conditions dynamically and explains the results.

Users can:

* Enter personal details (income, age, gender, occupation, etc.)
* Automatically evaluate eligibility for multiple schemes
* View rule-by-rule explanations
* Download eligibility reports as PDF
* Explore scheme details and required documents
* View analytics of scheme usage

---

## Key Features

### Dynamic Rule Engine

Eligibility rules are stored in the database and evaluated dynamically instead of hardcoding conditions.

Supported rule operators:

* `eq` → equals
* `lt` → less than
* `gt` → greater than
* `lte` → less than or equal
* `gte` → greater than or equal
* `in` → value inside a list

Example rule:

Income ≤ 200000
Occupation = Farmer

---

### Eligibility Evaluation

Users provide information such as:

* Annual income
* Age
* Gender
* State
* Occupation
* Land ownership
* Disability status

The system evaluates all schemes and returns:

* Eligible schemes
* Not eligible schemes
* Rule evaluation results
* Required documents

---

### Eligibility Explanation

Each scheme shows why a user is eligible or not eligible.

Example:

PM Kisan – Not Eligible

Occupation = Farmer ✔ Passed
Income ≤ 200000 ❌ Failed

---

### Eligibility Summary

After evaluation, the system shows a quick overview:

Eligible Schemes: 4
Not Eligible Schemes: 6
Total Schemes Checked: 10

---

### PDF Eligibility Report

Users can download a **PDF report** containing:

* Scheme name
* Eligibility status
* Scheme description
* Required documents

Generated using **ReportLab**.

---

### Scheme Detail Pages

Each scheme has its own page displaying:

* Description
* Eligibility rules
* Required documents
* Official government link

---

### Analytics Dashboard

A dashboard shows statistics such as:

* Total registered users
* Total eligibility checks
* Scheme popularity
* Eligibility distribution

Charts are generated using **Chart.js**.

---

### Authentication System

Users can:

* Register
* Login
* Logout

Navigation changes based on login status.

---

## Government Schemes Included

Central Government Schemes:

* PM Kisan
* Ayushman Bharat
* PM Awas Yojana
* Beti Bachao Beti Padhao
* Mudra Loan
* Skill India
* PM Fasal Bima Yojana
* PM Ujjwala Yojana
* Atal Pension Yojana
* PM SVANidhi

Maharashtra State Schemes:

* Mahatma Jyotiba Phule Jan Arogya Yojana
* Shetkari Apghat Vima Yojana
* Rajarshi Shahu Maharaj Scholarship
* Pandit Dindayal Upadhyay Gharkul Yojana
* Krushi Pump Yojana

---

## Technology Stack

Backend

* Python
* Django

Frontend

* HTML
* Bootstrap

Visualization

* Chart.js

Database

* SQLite (development)

PDF Generation

* ReportLab

---

## Project Structure

```
rural_scheme_engine/

manage.py

rural_scheme_engine/
    settings.py
    urls.py

schemes/
    models.py
    views.py
    forms.py
    admin.py

    services/
        eligibility_engine.py

    management/
        commands/
            seed_schemes.py

templates/
    base.html
    landing.html
    check.html
    dashboard.html
    analytics.html
    scheme_detail.html
```

---

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/yourusername/rural-scheme-eligibility-engine.git
cd rural-scheme-eligibility-engine
```

### 2. Create virtual environment

```
python -m venv venv
```

Activate it:

Mac/Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Apply migrations

```
python manage.py migrate
```

---

### 5. Seed the database with schemes

```
python manage.py seed_schemes
```

---

### 6. Run the server

```
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Future Improvements

Possible future enhancements:

* Support AND/OR rule groups
* Multilingual support (English / Marathi)
* Scheme recommendation engine
* Admin dashboard for rule management
* Deployment to cloud platforms

---

## Author

**Varadraj Velhal**

MCA Student – PCCOE
Interested in backend development, data systems, and problem-solving.

---

# SmartHire Pro

**SmartHire Pro** is a backend service built with Django & Django REST Framework to power job postings, applications, user authentication, and payments. It offers role‑based users (employers & candidates), JWT auth with email verification & password reset, Stripe payments, and filterable/paginated job listings.

---

## 📦 Tech Stack

- Python 3.10+  
- Django 4.x  
- Django REST Framework  
- django-filter  
- drf_yasg (Swagger UI)  
- PostgreSQL  
- Stripe API  

---

## 🚀 Getting Started

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-org/smarthire-pro.git
   cd smarthire-pro

2. **Create & activate a virtualenv**
    python -m venv venv
    source venv/bin/activate       # Linux/macOS
    venv\Scripts\activate          # Windows

3. **Install dependencies**
    pip install -r requirements.txt

4. **Environment setup**
    A. Create a file named .env in the root directory
    B. Copy the following template into the .env file.
    C. Replace the placeholder values with your own (keep the variable names exactly the same).

    # Database
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

    # Django
    DJANGO_SECRET_KEY=your_django_secret_key

    # Email
    DEFAULT_FROM_EMAIL=SmartHire <your-email@example.com>
    FRONT_END_URL=http://127.0.0.1:8000/api
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_email_app_password

    # Stripe
    STRIPE_SECRET_KEY=your_stripe_secret_key
    STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

    🔐 Keep it Secret
    ⚠️ Do not commit your .env file to version control (e.g., GitHub).
    Make sure .env is listed in your .gitignore.

5. **Run migrations and create superuser**
    commands:
        python manage.py migrate
        python manage.py createsuperuser
6. **Start the server**
    python manage.py runserver

**🔗 API Documentation**
    Swagger UI: http://localhost:8000/swagger/

    ReDoc UI: http://localhost:8000/redoc/

    OpenAPI JSON: http://localhost:8000/swagger.json

    All endpoints are auto-documented via drf_yasg and include request schemas, responses, and query‑param filters.


🎯 Key Endpoints
**Authentication (/api/auth/)**

POST	/api/auth/register/	Register new user (email + password)
POST	/api/auth/token/	Obtain JWT access & refresh tokens
POST	/api/auth/token/refresh/	Refresh JWT access token
GET	/api/auth/verify-email/?token=…	Verify email via token link
POST	/api/auth/resend-verfication-email/	Resend email-verification link
POST	/api/auth/request-password-reset/	Send OTP for password reset
POST	/api/auth/reset-password-with-otp/	Reset password using OTP

**Jobs (/api/jobs/panel/)**

GET	/api/jobs/panel/	List all jobs (filters, search, pagination)
POST	/api/jobs/panel/	Create a new job (employer only)
GET	/api/jobs/panel/{id}/	Retrieve a specific job
PUT	/api/jobs/panel/{id}/	Update a job (owner only)
DELETE	/api/jobs/panel/{id}/	Delete a job (owner only)

Filters: title, employment_type, min_salary, max_salary, plus ?search= and ?ordering=.

**Applications (/api/applications/panel/)**

GET	/api/applications/panel/	List applications (role‑scoped)
POST	/api/applications/panel/	Apply to a job (candidates only)
GET	/api/applications/panel/{id}/	View application details

**Payments (/api/payments/)**

POST	/api/payments/create-payment-intent/	Create Stripe PaymentIntent (returns secret)
POST	/api/payments/confirm-payment/	Confirm & record PaymentIntent status
GET	/api/payments/get-stripe-public-key/	Retrieve Stripe publishable key


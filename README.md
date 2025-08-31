# Django Docker Project

A full-stack web application built with Django, designed for efficient deployment using Docker. This project serves as a robust foundation for building modern web applications with a focus on user profiles, image management via Cloudinary, and background tasks using Celery.

---

### Key Features

* **User Authentication**: Secure user registration, login, and profile management.
* **Profile Management**: Users can create and edit their profiles, including uploading a profile picture.
* **Image Hosting**: Integrates with **Cloudinary** for scalable and reliable image storage and delivery.
* **Asynchronous Tasks**: Utilizes **Celery** and **Redis** for managing background jobs, improving application performance.
* **Containerization**: Ready for deployment with **Docker**, ensuring a consistent environment across development and production.
* **Database**: Supports both **MySQL** (for production) and **SQLite** (for local development).

---

### Technologies Used

* **Backend**: Django 5.2.5, Python 3.11
* **Database**: MySQL, SQLite3
* **Task Queue**: Celery, Redis
* **Cloud Hosting**: Cloudinary
* **Deployment**: Docker, Gunicorn, PythonAnywhere

---

### Local Setup and Installation 💻

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/bizimanasoftware/djangodocker.git](https://github.com/bizimanasoftware/djangodocker.git)
    cd djangodocker
    ```

2.  **Set up the Virtual Environment**
    ```bash
    # Create a new virtual environment
    python -m venv venv
    
    # Activate the virtual environment
    # On macOS/Linux
    source venv/bin/activate
    # On Windows
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the project's root directory. This file should contain your secret keys and Cloudinary credentials.

    ```
    SECRET_KEY=your_secret_key
    DEBUG=True
    
    CLOUDINARY_CLOUD_NAME=your_cloud_name
    CLOUDINARY_API_KEY=your_api_key
    CLOUDINARY_API_SECRET=your_api_secret
    
    # Add other database and environment variables here if needed
    ```

5.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a Superuser**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

    Your application will now be running at `http://127.0.0.1:8000/`.

---

### Deployment on PythonAnywhere

This project is configured to run on PythonAnywhere. Here are the key steps to deploy it.

1.  **Clone the Repository**: Clone your project to your PythonAnywhere account via a Bash console.

2.  **Set Up the Virtual Environment**: Create a virtual environment and install dependencies.
    ```bash
    mkvirtualenv --python=python3.11 my-virtualenv
    pip install -r requirements.txt
    ```

3.  **Configure Web App**: On the **Web** tab, configure your web app settings.
    * **Source code**: `/home/your-username/djangodocker/`
    * **Virtualenv**: `/home/your-username/.virtualenvs/my-virtualenv`
    * **WSGI file**: Set up the `wsgi.py` file to point to your project's settings.

4.  **Static Files**: Configure the static file mapping on the Web tab.
    * **URL**: `/static/`
    * **Directory**: `/home/your-username/djangodocker/staticfiles/`

5.  **Environment Variables**: Add your secret keys and Cloudinary credentials in the "Environment variables" section on the Web tab.

    * *Note:* The Cloudinary integration requires a paid PythonAnywhere account to bypass firewall restrictions on outbound connections.

6.  **Reload**: Click **"Reload"** on the Web tab to apply all changes and launch the application.

---

### How to Use the Admin Portal

To access the Django admin, you must first create a superuser as shown in the local setup steps. Once deployed, you can log in at `https://your-username.pythonanywhere.com/admin/`. Remember to register your models in `your_app/admin.py` to manage them from the portal.
sample: https://bizimanasoftware.pythonanywhere.com/

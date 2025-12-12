# Django Task Automation System

A **real-world task automation system** designed for companies to efficiently manage employee tasks and deadlines. This system is perfect for internal use in organizations and demonstrates modern Django practices including API integration, authentication, CRUD operations, background tasks, and clean database design.

**Live Demo:** https://task-automation-phi.vercel.app


---

## 🔥 Why This Project Is Valuable

Every company needs a reliable **internal task automation system** to track tasks, assign work, and monitor progress. This project highlights:

* RESTful API development
* User authentication & authorization
* CRUD operations
* Background task handling (e.g., email reminders)
* Optimized database design for tasks and assignments

---

## 🔧 Features

* **User Management:** Signup, login, and profile management
* **Task Management:**

  * Create tasks with **title**, **description**, **deadline**, and **priority**
  * Assign tasks to team members
* **Notifications:** Email notifications on task deadlines
* **Dashboard:** View task progress and team performance
* **API Integration:** API endpoints for mobile or third-party apps

---

## 🗂 Database Tables

| Table Name         | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| **User**           | Stores user credentials and profile info                         |
| **Task**           | Stores task details (title, description, deadline, priority)     |
| **TaskAssignment** | Links tasks to assigned team members, tracks status and progress |

---

## ⚙️ Technologies Used

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL / MySQL (configurable)
* **Email Notifications:** Celery + Redis / Django background tasks
* **Frontend (optional):** Django Templates / React / Mobile app integration

---

## 🚀 How to Run the Project

1. **Clone the repository:**

   ```bash
   git clone https://github.com/laiba09Saleem/Task_Automation.git
   cd django-task-automation
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

6. **Access the app:**
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser

---

## 📧 Email Notifications

* Background tasks handle sending email reminders for upcoming task deadlines.
* Configured via **Celery + Redis** or **Django Background Tasks**.

---

## 📝 API Endpoints (Sample)

| Endpoint            | Method | Description                  |
| ------------------- | ------ | ---------------------------- |
| `/api/register/`    | POST   | Register new user            |
| `/api/login/`       | POST   | User login and obtain token  |
| `/api/tasks/`       | GET    | List all tasks               |
| `/api/tasks/`       | POST   | Create new task              |
| `/api/tasks/<id>/`  | PUT    | Update a task                |
| `/api/tasks/<id>/`  | DELETE | Delete a task                |
| `/api/assignments/` | POST   | Assign task to a team member |

---

## 🏢 Perfect For

* Companies looking to manage internal tasks efficiently
* Developers who want to learn **Django, APIs, and background tasks**
* Full-stack projects with backend and mobile app integration

---

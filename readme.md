Proximity-Based Marketing System

A scalable web-based platform that allows businesses to deliver targeted advertisements and promotions to users based on their real-time physical proximity to specific locations (beacons). The system supports real-time communication, campaign management, analytics, and user interactions.

Features

- Beacon Integration – Detects nearby users and triggers relevant ads.
- Campaign Management – Marketers can create and manage geo-targeted campaigns.
- Role-based Access – Admin, Marketer, and Customer roles.
- Real-time Notifications – Customers receive instant alerts when near a beacon.
- Analytics Dashboard – View ad views, clicks, likes, and saves.
- Authentication & Authorization – Secure login and registration system.
- Modern UI – Built with React for a responsive and user-friendly experience.
- RESTful API– Developed using Django REST Framework for frontend-backend communication.

---

Tools Used

| Component        | Technology                      |
|------------------|----------------------------------|
| Backend          | Django, Django REST Framework   |
| Frontend         | React.js                        |
| Realtime Features| Django Channels, WebSockets     |
| Database         | PostgreSQL                      |
| Deployment       | Render, Docker (optional)       |

---

Project Structure

proximitybasedmarketing/
│
├── config/ # Django project config (settings, URLs)
├── core/
│ ├── beacons/ # Beacon management (models, views)
│ ├── campaigns/ # Campaign management
│ ├── advertisements/ # Ads logic and APIs
│ ├── users/ # Authentication, user roles
│ ├── logs/ # Event logging (views, clicks, etc.)
│ ├── notifications/ # WebSocket-based notifications
│ └── dashboards/ # Admin and marketer dashboards
├── frontend/ # React frontend app
├── templates/ # Django templates (optional)
└── manage.py

---
Setup Instructions

Prerequisites

- Python 3.10+
- Node.js (for frontend)
- PostgreSQL
- Redis (for Channels if using real-time)
- Virtualenv (recommended)

Backend Setup

git clone https://github.com/yourusername/proximity_based_marketing.git
cd proximity_based_marketing
python -m venv env
source env/bin/activate
pip install -r local.requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver --settings=config.settings.local

---
API Testing

Use tools like Insomnia or Postman to test the REST APIs. Authentication is token-based (JWT).

Author

Erdey Syoum
Senior Backend Developer
https://www.linkedin.com/in/erdey-syoum-a85313285/ – erdeysyoum@gmail.com – https://github.com/erdey2/

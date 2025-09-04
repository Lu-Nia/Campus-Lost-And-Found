## Campus Digital Lost & Found
A full-stack web application for university students to report and search for lost and found items on campus.

# 🚀 Features
User Authentication: JWT-based login/registration for students

Item Management: Report lost/found items with images and descriptions

Smart Search: Filter items by category, status, location, and keywords

Status Tracking: Items can be marked as Lost → Found → Claimed

Contact System: Built-in contact information for item reporters

Responsive Design: Works perfectly on desktop and mobile devices

Image Upload: Support for uploading item images


# 🛠️ Tech Stack
Frontend
React with custom CSS 

Axios for API calls

React Router for navigation

Context API for state management

# Backend
FastAPI Python framework

MySQL database

SQLAlchemy ORM

JWT authentication

Pydantic for data validation


📦 Installation
Prerequisites
Python 3.9+

Node.js 16+

MySQL 8.0+


Local Development
Clone the repository

bash
git clone https://github.com/Lu-Nia/campus-lost-found.git
cd campus-lost-found
Backend Setup

bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials
Database Setup

sql
CREATE DATABASE LostAndFound;
# The application will automatically create tables on first run
Frontend Setup

bash
cd frontend
npm install
Run the Application

bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 

# Terminal 2 - Frontend
cd frontend
npm start
# 🎯 Usage
For Students
Register/Login using your student number

Browse Items on the main dashboard

Report Found Items using the sidebar form

Update Status of items you've found (Lost → Found → Claimed)

Contact Owners through provided contact information

Item Status Workflow
Lost: Default status when item is reported

Found: Can be marked by other users when item is located

Claimed: Final status when owner retrieves the item

# 📁 Project Structure
text
campus-lost-found/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── models.py        # Database models
│   │   ├── database.py      # Database connection
│   │   ├── auth.py          # Authentication utilities
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── context/        # Auth context
│   │   ├── styles/         # CSS files
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── LICENSE
└── README.md
🔧 API Endpoints
Authentication
POST /auth/register - Register new user

POST /auth/token - Login and get JWT token

GET /auth/me - Get current user info

Items
GET /items - Get all items (with filtering)

POST /items - Create new item

GET /items/{id} - Get specific item

PATCH /items/{id} - Update item status

DELETE /items/{id} - Delete item

GET /items/stats/overview - Get statistics

Users
PATCH /users/password - Update password

(Soon we will offically dockerize the application, we are still in the process currently)

# 🗄️ Database Schema
https://via.placeholder.com/600x300?text=Database+Schema+Diagram

Key Tables:

users - Student accounts and administrators

items - Lost and found items with status tracking

logs - Audit trail for all item modifications

registered_students - Pre-approved student numbers

# 🔐 Security Features
JWT authentication with expiration

Password hashing with bcrypt

SQL injection prevention through ORM

CORS configuration

Input validation on frontend and backend

Audit logging for all operations

# 🚀 Deployment
Environment Variables
Backend .env file:

env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/LostAndFound
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Production Deployment
Set up MySQL database

Configure environment variables

Build and run with Docker:

bash
docker-compose -f docker-compose.prod.yml up --build -d
Set up reverse proxy (Nginx/Apache)

Configure SSL certificates

# 🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

# 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

# 🙏 Acknowledgments
University for the project opportunity. 

Contributors of the project: @Mothibi-Isaac, @Collinjr012, @Walefa

FastAPI and React communities for excellent documentation

All contributors and testers

# 📞 Support
For support, please open an issue on GitHub or contact the development team.

Note: This application is designed for educational purposes and university use. Ensure compliance with your institution's data protection policies before deployment.

A lightweight, modular ticket management web application built using Flask, SQLite, and Blueprints.
The system supports user authentication, role based access control, ticket creation, editing, closing, and deletion.
•	Live deployment: https://vicki888blue.pythonanywhere.com/
•	Source code (GitHub): https://github.com/vicki888blue/myflaskproject

Features
User Authentication
•	Register, login, logout
•	Session based authentication
•	Flash message feedback for errors/success
Role-Based Access Control
Roles defined in auth/roles.py:
•	Admin
•	Agent
•	User
Access controlled via decorators:
•	@login_required
•	@role_required()
Ticket Management
•	List all tickets (logged in users)
•	Create new ticket (Admin + Agent)
•	Edit ticket (Admin + Agent)
•	Close ticket (Admin + Agent)
•	Delete ticket (Admin + Agent)
•	View ticket details
Modular Blueprint Architecture
•	auth/ handles authentication
•	tickets/ handles ticket CRUD (create, read, update,delete
•	Templates stored centrally in /templates
•	SQLite database stored in project root
________________________________________
Project Structure
myflaskproject/
│
├── app.py
├── db.py
├── mydatabase.db
│
├── auth/
│   ├── __init__.py
│   ├── routes.py
│   ├── decorators.py
│   ├── roles.py
│   └── service.py
│
├── tickets/
│   ├── __init__.py
│   ├── routes.py
│   ├── repository.py
│   └── service.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── tickets_list.html
│   ├── tickets_new.html
│   ├── tickets_edit.html
│   └── ticket_detail.html

Running the Application (Locally)
Create a virtual environment
Shell
python -m venv venv
Show more lines
Activate the environment
Windows PowerShell:
Shell
venv\Scripts\Activate.ps1
Show more lines
Install dependencies
Shell
pip install flask SQLAlchemy flask_login flask_wtf wtforms
Show more lines
Run the app
Shell- python app.py
Show more lines
Visit:
http://127.0.0.1:5000/

Unit Testing *
This project includes unittest-based tests in the tests/ directory.
Covered in the test suite:
•	Login page loads
•	Invalid login redirects correctly
•	Successful login redirects to the correct route
•	Ticket list requires login
•	Ticket list loads for logged-in users
•	URL endpoint mapping (tickets.list resolves to /)

Run all tests:
Shell
python -m unittest discover -s tests -p "test_*.py" -v
Show more lines
Example output (your result):
Ran 6 tests in 0.187s
OK

Deployment -PythonAnywhere
The live version is deployed on PythonAnywhere using:
•	WSGI file pointing to the Flask app factory
•	Environment variables for SECRET_KEY and DATABASE_URL
•	Central /templates directory for rendering
•	SQLite DB at /home/username/mydatabase.db
Deployment steps:
1.	Upload project files
2.	Configure WSGI to load create_app()
3.	Install Flask dependencies via Bash console
4.	Reload the web app

Environment Variables
These can be set in PythonAnywhere under Web → Environment Variables:
SECRET_KEY=change-this
DATABASE_URL=sqlite:////home/vicki888blue/mydatabase.db

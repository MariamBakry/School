# School
XonTel Task

This document provides instructions for running the project locally, using the implemented APIs in Postman, and creating a superuser account.

**1.** Setting Up the Development Environment:

**1.1.** Activating the Virtual Environment:
Open a terminal window.
Navigate to the root directory of your project using the cd command.
Create new virtual environment using the following command:
    **python -m venv env_name**
Then activate the virtual environment using the following command: 
    **env_name\Scripts\activate**

**1.2.** Installing Dependencies:
Once the virtual environment is activated, install the required dependencies using pip:
    **pip install django**
    **pip install Django djangorestframework djoser djangorestframework-simplejwt**


**2.** Running the Project:

**2.1.** Migrations and Server:
Run the following commands to apply database migrations and start the development server:
    **python manage.py makemigrations**
    **python manage.py migrate**
    **python manage.py runserver**
This will start the Django development server, typically accessible at http://localhost:8000/ in your web browser. You can then use the provided APIs outlined in the next section.


**3.** Creating a Superuser Account:

Execute the following command in the terminal:
    **python manage.py createsuperuser**
Follow the prompts to enter a username, email address, and password for your superuser account. This account will have full administrative privileges in the Django application.


**4.** Additional Commands:

Activating Users:
To activate one or more existing users, use the following command:
    **python manage.py activate_users username1 username2**
Replace username1, username2, etc. with the actual usernames of the users you want to activate. This command will likely update a flag or field in the database to mark the specified users as active.


**5.** All List views have a pagination with page_size = 3


**6.** Using APIs in Postman

**6.1.** User **Signup** (Student and Teacher):

Path: http://localhost:8000/students/signup/ (for student signup)
    or
Path: http://localhost:8000/teachers/signup/ (for teacher signup)

Method: **POST**

Required Data (in Body):

JSON
    {
        "user": {
            "username": "your_username",
            "email": "your_email@example.com",
            "first_name": "Your First Name",
            "last_name": "Your Last Name",
            "gender": "Female" or "Male" (optional),
            "date_of_birth": "2000-01-01" (optional)
        },
        "password": "your_password",
        "password2": "your_password_confirmation" (must match "password")
    }

**Note:** Don't forget to active the user to be able to use the rest APIs


**6.2.** Accounts URLs:

- **Login**:

Path: http://localhost:8000/login/

Method: **POST**

Required Data (in Body):

JSON
    {
        "username": "your_username",
        "password": "your_password"
    }


- **Logout**:

Path: http://localhost:8000/logout/

Method: **POST**

Authentication: Requires a valid user session (log in before attempting this).


- **User Profile**:

Path: http://localhost:8000/profile/

Method: **GET**

Authentication: Requires a valid user session.


- **Update User Profile**

Path: http://localhost:8000/profile/update/

Method: **PUT**

Authentication: Requires a valid user session. You need to be logged in to update your profile.

Required Data (in Body):

JSON
    {
        "email": "new_email@example.com" (optional),
        "first_name": "Your New First Name" (optional),
        "last_name": "Your New Last Name" (optional),
        "gender": "Female" or "Male" (optional),
        "date_of_birth": "2000-01-01" (optional)
    }

**Note:** You only need to include the fields you want to update in the request body. Other fields will remain unchanged.


**6.3.** Courses:

- Courses List:

Path: http://localhost:8000/courses/

Method: **GET**

Authentication: This endpoint requires authentication with a valid user session (student or teacher).

**Note:** Only admin allowed to create new course, so don't forget to add courses using admin panel and to active them to be able to show them.



**6.4.** Teacher Courses History:

Path: http://localhost:8000/teachers/history/

Method: **GET**

Authentication: This endpoint requires authentication with a valid teacher user's credentials. You'll need to be logged in as a teacher to access this information.

**Note:** Only admin is able to assign teachers to courses ,so don't forget to assign the teacher to courses using admin panel to be able to see his courses history (both active and not active courses of the teacher will be shown).


**6.5.** Enrollments:

- **List Enrolled Courses**:

Path: http://localhost:8000/enrollments/

Method: **GET**

Authentication: Requires a valid student user session.

Response:

The response will contain a list of courses the currently logged-in student is enrolled in.

- **Enroll in a Course**:

Path: http://localhost:8000/enrollments/new-enroll/

Method: **POST**

Authentication: Requires a valid student user session.

Required Data (in Body):

JSON
    {
        "course_name": "The course name you want to enroll in"
    }

**Note:** Be sure that the course start date is in the future to be able to enroll it.

- **Leave a Course**:

Path: http://localhost:8000/enrollments/leave-course/

Method: **POST**

Authentication: Requires a valid student user session.

Required Data (in Body):

JSON
    {
        "course_name": "The course name you want to leave"
    }

**Note:** Be sure that the course start date is in the future to be able to leave it.



**6.6.** The teacher's view of students enrolled in his course:

Path: http://localhost:8000/teachers/<int:course_id>/students/

Method: **GET**

Authentication: This endpoint requires authentication with a valid teacher user's credentials. You'll need to be logged in as a teacher to access this information.

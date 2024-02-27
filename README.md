# School
 XonTel Task

This document provides instructions for running the project locally, using the implemented APIs in Postman, and creating a superuser account.

1. Setting Up the Development Environment:

1.1. Activating the Virtual Environment:

Open a terminal window.
Navigate to the root directory of your project using the cd command.
Activate the virtual environment using the following command:
test\Scripts\activate
Note: Replace test with the actual name of your virtual environment if it's different.

1.2. Installing Dependencies:

Once the virtual environment is activated, install the required dependencies using pip:

pip install Django djangorestframework djoser djangorestframework-simplejwt


2. Running the Project:

2.1. Migrations and Server:

Run the following commands to apply database migrations and start the development server:
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
This will start the Django development server, typically accessible at http://localhost:8000/ in your web browser. You can then use the provided APIs outlined in the next section.


3. Creating a Superuser Account:

Open a terminal window and activate your virtual environment if necessary (refer to step 1.1).
Execute the following command in the terminal:
python manage.py createsuperuser
Follow the prompts to enter a username, email address, and password for your superuser account. This account will have full administrative privileges in the Django application.


4. Additional Commands:

Activating Users:

To activate one or more existing users, use the following command:

python manage.py activate_users username1 username2 ...
Replace username1, username2, etc. with the actual usernames of the users you want to activate. This command will likely update a flag or field in the database to mark the specified users as active.


5. All List views have a pagination with page_size = 3


6. Using APIs in Postman
This section provides instructions for using the implemented APIs in Postman, demonstrating their functionalities and how to interact with them using appropriate data formats.

6.1. Introduction to Postman:

Postman is a popular tool for testing and debugging APIs. If you haven't already, install Postman from https://www.postman.com/ and follow these general steps for each API interaction:

Create a new request or use an existing one in Postman.
Set the HTTP Method (e.g., GET, POST, PUT, DELETE) based on the intended action for the API.
Set the URL for the API endpoint, including the base URL (e.g., http://localhost:8000/) and the specific endpoint path.
(Optional) For POST, PUT, or PATCH requests, provide the required data in the Body section. Use the appropriate format like JSON, form-data, etc., depending on the API's requirements.
(Optional) Set any necessary headers, authentication tokens, or other parameters in the Headers section.
Click Send to execute the request and view the response.

6.2. User Signup (Student and Teacher):

Path: http://localhost:8000/students/signup/ (for student signup) or http://localhost:8000/teachers/signup/ (for teacher signup)

Method: POST

Required Data (in Body):

JSON
{
    "user": {
        "username": "your_username",
        "email": "your_email@example.com",
        "first_name": "Your First Name",
        "last_name": "Your Last Name"
    },
    "password": "your_password",
    "password2": "your_password_confirmation" (must match "password")
}
Use code with caution.
Example Request:

JSON
{
    "user": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "password": "123456",
    "password2": "123456"
}
Use code with caution.

6.3. Teacher Courses History:

Path: http://localhost:8000/teachers/history/

Method: GET

Authentication: This endpoint requires authentication with a valid teacher user's credentials. You'll need to be logged in as a teacher to access this information.

Example Usage:

Log in to Postman using your teacher's credentials (refer to Login API below).
Set the URL and method as specified above.
Send the request.
The response will contain a list of courses taught by the authenticated user.

6.4. Students Enrolled in a Teacher's Course:

Path: http://localhost:8000/courses/<int:course_id>/students/

Method: GET

Authentication: This endpoint requires authentication with a valid teacher user's credentials. You'll need to be logged in as a teacher to access this information.

Path Parameter:

<int:course_id>: Replace this with the actual ID of the course you want to retrieve enrolled students for.
Example Usage:

Log in to Postman using your teacher's credentials (refer to Login API below).
Replace <int:course_id> in the URL with the desired course ID.
Set the URL and method as specified above.
Send the request.
The response will contain a list of students currently enrolled in the specified course.

6.5. Accounts URLs:

- Login:

Path: http://localhost:8000/accounts/login/

Method: POST

Required Data (in Body):

JSON
{
    "username": "your_username",
    "password": "your_password"
}
Use code with caution.
- Logout:

Path: http://localhost:8000/accounts/logout/

Method: GET

Authentication: Requires a valid user session (log in before attempting this).

- User Profile:

Path: http://localhost:8000/accounts/profile/

Method: GET

Authentication: Requires a valid user session.

- Update User Profile
Path: http://localhost:8000/accounts/profile/update/

Method: POST

Authentication: Requires a valid user session. You need to be logged in to update your profile.

Required Data (in Body):

JSON
{
    "username": "new_username" (optional),
    "email": "new_email@example.com" (optional),
    "first_name": "Your New First Name" (optional),
    "last_name": "Your New Last Name" (optional)
}
Use code with caution.
Note: You only need to include the fields you want to update in the request body. Other fields will remain unchanged.

Example Request:

JSON
{
    "email": "updated_johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe Smith"
}
Use code with caution.
Response:

The response will be a JSON object containing the updated user information.

Courses and Enrollments URLs


6.6. Courses:

- List Courses:

Path: http://localhost:8000/courses/

Method: GET

Authentication: This endpoint requires authentication with a valid user session (student or teacher).

6.7. Enrollments:

- List Enrolled Courses:

Path: http://localhost:8000/enrollments/

Method: GET

Authentication: Requires a valid student user session.

Response:

The response will contain a list of courses the currently logged-in student is enrolled in.

- Enroll in a Course:

Path: http://localhost:8000/enrollments/new-enroll/

Method: POST

Authentication: Requires a valid student user session.

Required Data (in Body):

JSON
{
    "course_name": "The course name you want to enroll in"
}
Use code with caution.
Response:

Upon successful enrollment, the response will typically be a success message or an appropriate status code.
In case of errors (e.g., course not found or permission issues), the response will contain an error message or code indicating the problem.
Example Usage:

Log in to Postman using your student credentials (refer to Login API).
Set the URL and method as specified above.
In the Body section, replace "The course name you want to enroll in" with the actual name of the course you want to join.
Send the request.
The response will indicate success or failure and provide any relevant details.

- Leave a Course:

Path: http://localhost:8000/enrollments/leave-course/

Method: POST

Authentication: Requires a valid student user session.

Required Data (in Body):

JSON
{
    "course_name": "The course name you want to leave"
}
Use code with caution.
Response:

Similar to the enrollment endpoint, the response will indicate success or failure based on the outcome of the request. You will receive a success message or error information accordingly.

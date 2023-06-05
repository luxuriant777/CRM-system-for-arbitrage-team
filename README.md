## To perform a POST request to register a user using Postman, you can follow these steps:

1. Open Postman and enter this URL:
   http://localhost:8000/api/register/

2. Select the HTTP method as "POST".

3. Click on the "Body" tab below the URL field.

4. Select the "raw" option and choose "JSON" from the dropdown menu.

5. In the request body, provide the JSON payload containing the username, email, and password. For example:
    ```json
    {
      "username": "example_user",
      "email": "user@example.com",
      "password": "secretpassword"
    }
    ```
6. Click the "Send" button to send the request.
7. Postman will send the POST request to the specified URL with the provided JSON payload. You should receive a 
   response indicating whether the user registration was successful or any errors that occurred. If the registration
   was successful, you will see:
    ```json
    {
        "message": "User registered successfully.",
        "user": {
            "username": "example_user",
            "email": "user@example.com"
        }
    }
    ```
## To perform a POST request to log in as a registered user, you can follow these steps:

1. Open Postman and enter this URL:
   http://localhost:8000/api/login/.

2. Select the HTTP method as "POST".

3. Click on the "Body" tab below the URL field.

4. Select the "raw" option and choose "JSON" from the dropdown menu.

5. In the request body, provide the JSON payload containing the username, email, and password. For example:
    ```json
    {
      "username": "example_user",
      "password": "secretpassword"
    }
    ```
6. Click the "Send" button to send the request.
7. Postman will send the POST request to the specified URL with the provided JSON payload. You should receive a 
   response indicating whether the user login was successful or any errors that occurred. If the login was successful,
   you will see this:
    ```json
    {
        "message": "User logged in successfully.",
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1OTc0MTQ3LCJpYXQiOjE2ODU5NzM4NDcsImp0aSI6ImZkZTE2NWZjZmQyZDRkOTJhY2FjNmQ1NTQyODBlZGQwIiwidXNlcl9pZCI6MiwicGF5bG9hZCI6eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImV4YW1wbGUifX0.F4y3hLbOk3UcJBoSKZIaZvGO2HtXCghgy7vszq4mIuM"
    }
    ```

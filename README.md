## To perform a POST request to register a user, you can follow these steps:

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
## To perform a Get request to list all registered users, you can follow these steps:

1. Open Postman and enter this URL:
   http://localhost:8000/api/users/.

2. Select the HTTP method as "GET".

3. Click on the "Authorisation" tab below the URL field.

4. Select the "Bearer Token" option and enter the token you received when performed the login request. For example:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1OTc0MTQ3LCJpYXQiOjE2ODU5NzM4NDcsImp0aSI6ImZkZTE2NWZjZmQyZDRkOTJhY2FjNmQ1NTQyODBlZGQwIiwidXNlcl9pZCI6MiwicGF5bG9hZCI6eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImV4YW1wbGUifX0.F4y3hLbOk3UcJBoSKZIaZvGO2HtXCghgy7vszq4mIuM
   ```
5. Click the "Send" button to send the request.
6. Postman will send the GET request to the specified URL. You should receive a response with the list of all registered
   users, or message with errors that occurred. If the request was successful, you will see this:
    ```json
   [
       {
           "id": 1,
           "username": "example_user",
           "email": "user@example.com"
       },
       {
           "id": 2,
           "username": "example",
           "email": "user1@example.com"
       },
       {
           "id": 3,
           "username": "example3",
           "email": "user3@example.com"
       },
       {
           "id": 4,
           "username": "example4",
           "email": "user3@example.com"
       }
   ]
    ```

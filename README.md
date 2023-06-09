# Installation
1. Python3 must be installed. If not, please, visit https://www.python.org/ and choose appropriate version for your OS.
2. Clone the repository:
   ```shell
   git clone https://github.com/luxuriant777/CRM-system-for-arbitrage-team
   ```
3. Switch to the `dev` branch:
   ```shell
   git checkout dev
   ```
4. Activate the virtual environment - this is a separate container where all the necessary dependencies will be
installed:
   ```shell
   venv\Scripts\activate (on Windows)
   ```
   ```shell
   source venv/bin/activate (on macOS)
   ```
5. Install all the necessary packages:
   ```shell
   pip install -r requirements.txt
   ```
6. Apply migrations:
   ```shell
   python manage.py migrate
   ```
7. Create a superuser. You will be asked to provide a username, email (optional), and password:
   ```shell
   python manage.py createsuperuser
   ```
   A superuser account can be used to log in to the Django administrative interface and perform administrative tasks. 
8. You can start the development server by running:
   ```shell
   python manage.py runserver
   ```
   Then you will be able to access the administrative interface by visiting http://localhost:8000/admin in your web 
   browser.
# Usage
## 1. Asynchronous processing of `leads` and `orders` creation
   To enable the simultaneous storage of multiple `lead` or `order` creation requests, it is necessary to install
   RabbitMQ and start `celery`. Assuming, that you have [RabbitMQ](https://www.rabbitmq.com/) installed, run the
   following command in the command prompt or bash while in the root folder of the project:
   ```bash
   celery -A crm_arbitrage worker --loglevel=info -P eventlet
   ```
## 2. To register a user (a team member):

1. Open Postman and enter this URL:
   ```bash
   http://127.0.0.1:8000/api/register/
   ```
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
## 3. To login as a registered user:

1. Open Postman and enter this URL:
   ```bash
   http://127.0.0.1:8000/api/login/
   ```
2. Select the HTTP method as "POST".

3. Click on the "Body" tab below the URL field.

4. Select the "raw" option and choose "JSON" from the dropdown menu.

5. In the request body, provide the JSON payload containing the username and password. For example:
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
   The `access_token` should be used to make requests to all endpoints that require authorization.

## 4. To list all registered users:

1. Open Postman and enter this URL:
   ```bash
   http://127.0.0.1:8000/api/users/
   ```
2. Select the HTTP method as "GET".

3. Click on the "Authorization" tab below the URL field.

4. Select the "Bearer Token" option and enter the `access_token` you received when performed the login request. 
   For example:
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
## 5. To create a lead (a basic "visit" to the landing page, with or without making a purchase):
1. Open Postman and enter this URL:
   ```bash
   http://127.0.0.1:8000/api/leads/create/
   ```
2. Select the HTTP method as "POST".

3. Click on the "Body" tab below the URL field.

4. Select the "raw" option and choose "JSON" from the dropdown menu.

5. In the request body, provide the JSON payload containing the ip address, useragent, and referral source. For example:
    ```json
    {
    "ip_address": "192.168.4.1",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "referral_source": "example.com"
    }
    ```
6. Click the "Send" button to send the request.
7. Postman will send the POST request to the specified URL with the provided JSON payload. You should receive a 
   response indicating whether the request was successful or any errors that occurred. If the request was successful,
   you will see this:
    ```json
    {
    "ip_address": "192.168.4.1",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "referral_source": "example.com"
    }
    ```

## 6. To list all available leads:
1. Open Postman and enter this URL:
   ```bash
   http://127.0.0.1:8000/api/leads/list/
   ```
2. Select the HTTP method as "GET".

3. Click on the "Authorization" tab below the URL field.

4. Select the "Bearer Token" option and enter the `access_token` you received when performed the login request. 
   For example:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1OTc0MTQ3LCJpYXQiOjE2ODU5NzM4NDcsImp0aSI6ImZkZTE2NWZjZmQyZDRkOTJhY2FjNmQ1NTQyODBlZGQwIiwidXNlcl9pZCI6MiwicGF5bG9hZCI6eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImV4YW1wbGUifX0.F4y3hLbOk3UcJBoSKZIaZvGO2HtXCghgy7vszq4mIuM
   ```
5. Click the "Send" button to send the request.
6. Postman will send the GET request to the specified URL. You should receive a response with the list of all leads, 
   or message with errors that occurred. If the request was successful, you will see this:
    ```json
   [
    {
        "id": 1,
        "ip_address": "192.168.0.1",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "referral_source": "example.com",
        "created_at": "2023-06-05T16:11:00.675296Z"
    },
    {
        "id": 2,
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "referral_source": "example.com",
        "created_at": "2023-06-05T16:11:13.301890Z"
    },
    {
        "id": 3,
        "ip_address": "192.168.3.1",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "referral_source": "example.com",
        "created_at": "2023-06-05T16:11:17.313468Z"
    }
    ]
    ```

## 7. To create an order (a purchase made by the customer):
1. Open Postman and enter this URL:
   ```bash
   http://127.0.0.1:8000/api/orders/create/
   ```
2. Select the HTTP method as "POST".

3. Click on the "Body" tab below the URL field.

4. Select the "raw" option and choose "JSON" from the dropdown menu.

5. In the request body, provide the JSON payload containing the lead ID, email, phone number, first and last names, and
   delivery address. This simulates a situation where the customer has made a purchase and filled out the order form.
   Here is the example:
    ```json
    {
    "lead_id": 1,
    "email": "example@example.com",
    "phone_number": "1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "delivery_address": "123 Main St, City, Country"
    }
    ```
6. Click the "Send" button to send the request.
7. Postman will send the POST request to the specified URL with the provided JSON payload. You should receive a 
   response indicating whether the request was successful or any errors that occurred. If the request was successful,
   you will see this:
    ```json
    {
    "lead_id": 1,
    "email": "example@example.com",
    "phone_number": "1234567890",
    "first_name": "John",
    "last_name": "Doe",
    "delivery_address": "123 Main St, City, Country",
    "lead": {
        "id": 1,
        "ip_address": "192.168.8.1",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "referral_source": "example.com",
        "created_at": "2023-06-06T03:08:18.381655Z"
        }
    }
    ```

## 8. To list all available orders (with the ability to view associated lead details):
1. Open Postman and enter this URL:
   ```bash
   http://127.0.0.1:8000/api/orders/list/
   ```
2. Select the HTTP method as "GET".

3. Click on the "Authorization" tab below the URL field.

4. Select the "Bearer Token" option and enter the `access_token` you received when performed the login request. 
   For example:
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg1OTc0MTQ3LCJpYXQiOjE2ODU5NzM4NDcsImp0aSI6ImZkZTE2NWZjZmQyZDRkOTJhY2FjNmQ1NTQyODBlZGQwIiwidXNlcl9pZCI6MiwicGF5bG9hZCI6eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImV4YW1wbGUifX0.F4y3hLbOk3UcJBoSKZIaZvGO2HtXCghgy7vszq4mIuM
   ```
5. Click the "Send" button to send the request.
6. Postman will send the GET request to the specified URL. You should receive a response with the list of all orders,
   or message with errors that occurred. If the request was successful, you will see this:
    ```json
   [
    {
        "id": 1,
        "lead_id": 3,
        "email": "example@example.com",
        "phone_number": "1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "delivery_address": "123 Main St, City, Country",
        "created_at": "2023-06-06T02:52:07.115852Z",
        "lead": {
            "id": 3,
            "ip_address": "192.168.8.1",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "referral_source": "example.com",
            "created_at": "2023-06-06T02:51:45.971552Z"
        }
    },
    {
        "id": 2,
        "lead_id": 3,
        "email": "example@example.com",
        "phone_number": "1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "delivery_address": "123 Main St, City, Country",
        "created_at": "2023-06-06T02:52:09.917670Z",
        "lead": {
            "id": 3,
            "ip_address": "192.168.8.1",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "referral_source": "example.com",
            "created_at": "2023-06-06T02:51:45.971552Z"
        }
    },
    {
        "id": 3,
        "lead_id": 3,
        "email": "example@example.com",
        "phone_number": "1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "delivery_address": "123 Main St, City, Country",
        "created_at": "2023-06-06T02:52:11.116232Z",
        "lead": {
            "id": 3,
            "ip_address": "192.168.8.1",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "referral_source": "example.com",
            "created_at": "2023-06-06T02:51:45.971552Z"
        }
     }
    ]
    ```
    Please note that all information related to the details of the corresponding lead will also be included.
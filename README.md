
# Falcon Application
## *User Information Microservice*

## Overview

The **User Information Microservice** is a RESTful API built with the Falcon framework. It allows to create user and retrieve user information. The service uses MongoDB to store user data and also keeps a backup in a JSON file.

## Table of Contents

1. [Installation](#installation)
2. [Environment Variables](#environment-variables)
3. [Running the Application](#running-the-application)
4. [Running Tests](#running-tests)
5. [Usage](#usage)

## Installation

To install the application and its dependencies, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/manikandanbnair/falcon-api.git
   cd falcon-api
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Before running the application, ensure that the following environment variables are set up correctly:

### Step 1: Create a `config.ini` File

Create a config.ini file in the root directory of the project.

### Step 2: Add Environment Variables

Add the following variables to your `config.ini` file:

```plaintext
[database]
MONGO_HOST=your_mongo_host
MONGO_PORT=your_mongo_port
MONGO_DB_NAME=your_database_name
```

- **MONGO_HOST**: The hostname or IP address of your MongoDB server (e.g., `localhost` or `127.0.0.1`).
- **MONGO_PORT**: The port number on which your MongoDB server is running (default is usually `27017`).
- **MONGO_DB_NAME**: The name of the database you want to connect to.

### Step 3: Load the configuration in python

The application will automatically load these variables when it starts, so no additional action is needed.
.
## Running the Application

To run the application using Waitress, use the following command:

```bash
 waitress-serve --listen 0.0.0.0:8080 app:app

```

This will start the server on port 8000. You can access the API at `http://localhost:8000`.

## Running Tests

To run the test cases and generate coverage reports, use the following command:

```bash
coverage run --source=. -m pytest test
```

To view the coverage report, you can use:

```bash
coverage report
```

Or to generate an HTML report:

```bash
coverage html
```

## Usage

### API Endpoints

1. **POST /users**
   - **Description**: Create a new user.
   - **Request Body**: 
     ```json
     {
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30
     }
     ```
   - **Response**: 
     ```json
     {
       "message": "Successfully created"
     }
     ```

2. **GET /users**
   - **Description**: Retrieve all users or a specific user by email.
   - Parameters:
      email (optional): The email address of the user to retrieve. If not provided, all users will be returned.
   - **Response**:
     - If no email is provided:
       ```json
       {
         "Users": ["List of users with their details"]  
       }
       ```
     - If a specific user is requested:
       ```json
         {
              "User": {
                  "name": "name",
                  "age": 12,
                  "email": "name@example.com"
              }
         }
       ```

### Conclusion

The User Information Microservice provides a simple way to manage user data through a RESTful API. 

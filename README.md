# UniLove
## A Dating App for Unity University Students

UniLove is a dating web application tailored specifically for Unity University students, providing a platform for users to connect based on shared interests and hobbies.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Profile creation with interests and hobbies
- User matching based on shared interests
- Secure session management

## Technologies Used

- Flask for backend development
- SQLAlchemy for database interactions
- MySQL as the database
- bcrypt for password hashing
- Docker for containerization (if applicable)

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL server
- Virtual Environment (optional but recommended)

# Quick Start

* This guide will show you how to set up a simple application using Flask and MySQL.

## Installation

* ### 1. Create a Virtual Environment
    * It’s a good practice to create a virtual environment for your project. You can do this with the following command:

            python3 -m venv venv


    * Activate the virtual environment:
        * Windows:
                    venv\Scripts\activate
          
        * macOS/Linux:
                    source venv/bin/activate


* ### 2. Install Required package in requirements.txt
    * After activating your virtual environment, install Flask and the required packages using pip:

            pip install -r requirements.txt


    * You may also want to install other packages, depending on your project’s needs.

* ### 3. Create a Database and Configure MySQL
    * Install MySQL if you haven’t already. Follow the official [MySQL installation guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html).

    * Start the MySQL server and log in:

            mysql -u root -p


    * Create a database for your application:

            CREATE DATABASE your_database_name;
      

    * Create a user and grant privileges (replace your_user and your_password):

            CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
      GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_user'@'localhost';
      FLUSH PRIVILEGES;


* ### 4. Configure Your Flask Application
    * In your Flask application, configure the MySQL connection in your config file or directly in your app:

            from flask import Flask
            from flask_mysqldb import MySQL

            app = Flask(__name__)

      # MySQL Configuration
     
            app.config['MYSQL_HOST'] = 'localhost'
          app.config['MYSQL_USER'] = 'your_user'
          app.config['MYSQL_PASSWORD'] = 'your_password'
          app.config['MYSQL_DB'] = 'your_database_name'

          mysql = MySQL(app)


* ### 5. Run Your Flask Application
    * To start your Flask application, use the following command:

            python3 -m app.v1.app
```bash
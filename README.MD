# Online Shop

This is a simple online shop. The project was developed as an interview project, the specifications are made to closely follow the specifications of the take home project description.


## Project Execution Plan
As a Backend Engineer developing an online shop web application, here's my execution plan detailing what I will do and the rationale behind each step:

### Project Setup
- **Set Up Development Environment**: I'll begin by setting up my development environment. This includes installing Python, Flask, PostgreSQL, and any necessary development tools. I'll use Python and Flask for their simplicity and efficiency in building web applications, and PostgreSQL for its robustness and scalability as a relational database.
- **Initialize Git Repository**: I'll create a Git repository for version control. This will help me manage code changes, track progress, and collaborate efficiently if needed.
- **Create Flask Application Structure**: I'll set up a basic Flask application structure, organizing my project into modular components for easy management and scalability.

### Backend Development
- **Develop RESTful APIs**: I'll build RESTful APIs for handling product listings, user authentication, basket functionalities, and order processing. RESTful architecture ensures a standard, efficient, and scalable way of building web services.
- **Implement CRUD Operations**: For managing products and user data, I'll implement CRUD (Create, Read, Update, Delete) operations. This will form the core functionality of the online shop, allowing users to interact with the product listings and manage their accounts.
- **Session-Based User Authentication**: Implementing a secure, session-based authentication system will ensure that user sessions are managed safely, providing a secure and personalized experience for each user.
- **Database Schema Design**: I'll design a comprehensive database schema in PostgreSQL to store product details, user information, orders, and basket contents. The actual implementation has been done with sqlite to improve portability since, it doesn't require a complex installation to run.

### Frontend Integration
- **Integrate with Jinja Templates**: I'll use Jinja templates for rendering the frontend. Jinja is a powerful templating engine that integrates seamlessly with Flask, allowing for dynamic content rendering in the HTML templates.
- **Apply Tailwind CSS for Styling**: For styling the frontend, I'll utilize Tailwind CSS. Its utility-first approach will enable me to rapidly style the web pages while maintaining design consistency.

### Additional Functionalities and Testing
- **Basket Functionality**: I'll develop the logic for a functional shopping basket, allowing users to add and manage products in their session.
- **Checkout Process and Payment Integration**: Implementing a checkout process, I'll ensure that it is accessible after user login, including options for different payment methods.
- **Product Filtering Feature**: Adding a filtering feature for products based on weight, volume, or size will enhance the user experience, making it easier for users to find what they need.
- **Writing Unit Tests**: Throughout development, I'll write unit tests for the backend logic. This is crucial for ensuring that each part of the application works as intended and maintains high code quality.

### Final Steps
- **Debugging and Refinement**: I'll rigorously test the application to iron out any bugs and refine the user experience.
- **Documentation**: Documenting the code and functionalities will be essential for future reference and potential handovers.

This plan balances efficient development with attention to quality and user experience, ensuring that the final product is both functional and user-friendly.


## Running The App

I have added an online version of the app that can be accessed through [https://onlineshop.bogingo.com](https://onlineshop.bogingo.com).

### Preparation

You can clone the app from github using the command:
```commandline
git clone https://github.com/wegner15/onlineshop
```

After cloning the app, install the required dependencies through the command:

```commandline
pip install -r requirements.txt
```
Note: This command assumes that you have python and pip installed locally
After installing the requirements, create a `.env` file on the root folder and add the environment variables. 
The application will not  run without the environment variables such as database url.

**Sample environment variable**
```
SECRET_KEY='aeOo$XAqGh6nm3Zfk9J5ZqfKI#6Xi^XICAvB@y!'
SQLALCHEMY_DATABASE_URI='sqlite:///database.sqlite'
```

### Running the application

```commandline

flask run --port 8001
```
Now you can navigate to [http://localhost:8001](http://localhost:8001) to access the home page.

## Adding Products

Addition of products should be done by the administrator. However, since the administrator account has not been fully implemented, one can add product through 
the direct link `base_url/add-product`


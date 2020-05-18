# Full Stack Trivia API

This project is a trivia game, which was built as part of the udacity Full Stack Developer Nano Degree course. There was a given frontend and a given database setup but no working API endpoints. Goal of the project was, to get the API running in a way that allows the frontend to work. Another requirement of the project was, that the API could be tested with unittest.

The following documentation describes all the tools which were used for the project and gives a clear documentation of all the APIs. 

The backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

The complete chapter "Getting Started" was already given by udacity.com

### Installing Backend Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server under MAC or Linux, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

To run the server under Windows, execute:
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


### Installing the Frontend Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## API Documentation

### Base URL
http://localhost:3000/

### Authentication
You don't need to authenticate yourself. Just use it.

### Error Handling
If anything goes wrong while you're using the Bookshelf API you will get an Error. Every error includes an HTTP Error Code and a body which contains more information about the issue.

#### HTTP Error Codes
The following HTTP Error Codes are used:


| Error Codes   | Description   |
| ------------- |--------------:|
|400|bad request|
|404|Resource not found|
|422|unprocessable|


#### Messages
Every response contains a `success` and a `message` attribute. The `success` attribute is set to `False` as soon as an error occurs. The `message` attribute contains some more details why the error occured.

#### Example for an error response
Errors are returned as JSON objects in the following format:
``` 
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

### Endpoint Library

#### GET /categories

This endpoint can be used to get all available question-categories

Sample Request:
`curl http://localhost:5000/categories`

Sample Response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions

This endpoint can be used to get all questions paginated. Every page contains 10 books. Additionally the endpoint returns all available categories and the total amount of questions.

Sample Request:
`curl http://localhost:5000/questions?page=2`

Sample Response:
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Fine",
      "category": 5,
      "difficulty": 2,
      "id": 27,
      "question": "How are you?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
#### GET /categories/\<cat_id\>/questions

This endpoint can be used to get all questions from a given category paginated. Every page contains 10 books. Additionally the endpoint returns the current category and the total amount of questions.

Sample Request:
```
curl http://localhost:5000/categories/1/questions
```

Sample Response:
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```


#### POST /questions

##### Create a new question
If you want to create a new book you can use POST /questions. You need to add three parameters to your request body:

* question
  * contains the question as string
* answer
  * contains the answer as string
* difficulty
  * contains a number between 1 (= easy) and 5 (= hard)
* category
  * contains the id of the category

If the creation was successful the endpoints returns a parameter "created" which contains the id of the newly created question.


Sample Request: 
```
curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d "{\"question\":\"What's your name\", \"answer\":\"John\",\"difficulty\":\"2\",\"category\":\"2\"}"
```

Sample Response:
```
{
  "created": 30,
  "success": true
}
```


##### Search for a question
You can use the POST /questions api also for searching for questions. Just add the attribute 'searchTerm' to the body, and pass via that attribute the search string to the endpoint. This endpoint will return the questions which fit to your search paginated to you. Per page you'll receive 10 questions.

Sample Request: 
```
curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d "{\"searchTerm\":\"organ\"}"
```

Sample Response:
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### POST /quizzes
This endpoint needs two parameters which contain the category and a list of previous question. It returns a random questions within the given category, which is not one of the previous questions. 

Sample Request: 
```
curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d "{\"quiz_category\":{\"type\": \"Science\", \"id\": \"1\"},\"previous_questions\":[1,2]}"
```
Sample Response
```
 {
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}
```


#### DELETE /questions/\<int:question_id\>

This API will delete the question with the given question id, passed via the url, if it exists. It returns the id of the deleted question. 

Sample Request:
```
curl http://localhost:5000/questions/3 -X DELETE
```

Sample Response:
```
{
  "deleted": 10,
  "success": true
}
```


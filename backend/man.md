# Overview:
The project consist of two main components: a FastAPI backend and a frontend. The backend, which is built with FastAPI and Docker.
The frontend is a React application that interacts with the backend to display extracted entities from PDF files. The backend provides an API endpoint to extract entities from PDF files using the OpenAI API.

# FastAPI Backend Manual
The backend is a FastAPI application that serves as an API for the frontend. 
It is containerized using Docker for easy deployment and management.
the endpoint /extract_entities/ is used to extract entities from a given pdf using the OpenAI API.
It receives a PDF file, extracts the text from it, and then uses the OpenAI API to extract entities from the text.
It returns the extracted entities in JSON format.

# Frontend Manual
The frontend is a React application that interacts with the FastAPI backend to display extracted entities from PDF files.
it is really simple and it is just a form that allows the user to upload a PDF file and then displays the extracted entities in a table.
# Deploying and Running Your FastAPI App with Docker and Secure API Keys

## 1. clone the repository
To get started, clone the repository containing the FastAPI app and frontend:

```sh
git clone git@github.com:Rhinoj0sa/nd_challenge.git
```

## 2. Build the Docker Image

Open your terminal in  frontend/appfe (where the docker-compose.yml file is located) and run:

```sh
docker build -t my-fastapi-app .
```

---

## 3. Set the OpenAI APIkey in a .env file:
The project uses an OpenAI API key to interact with the OpenAI services. To securely provide this key, you will create a `.env`  with this content:

OPENAI_API_KEY=sk-...your-key...

And save the file in the **frontend/appfe** subdir.

## 4. Run the Docker Container
Run the following command to start your FastAPI app in a Docker container:

```sh
docker compose up --build
```
## 5. Access the API

- Open your browser and go to: [http://localhost:8000/docs](http://localhost:8000/docs)
- Or test with curl:

    ```sh
    curl http://localhost:8000/docs
    ```

---

## 6. Access the frontend
Open your browser and go to: [http://localhost:3000](http://localhost:3000)

## 7. Security Tips

- **Never** hardcode your API key in your code or Dockerfile.
- Add `.env` to your `.gitignore` to avoid committing secrets to version control.

---

**Your FastAPI app is now running in Docker with your API key securely provided!**---


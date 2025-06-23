# Deploying and Running Your FastAPI App with Docker and Secure API Keys

This manual guides you through building, running, and securely providing API keys to your FastAPI app in Docker.

---

## 1. Build the Docker Image

Open your terminal in your project root (where the Dockerfile is located) and run:

```sh
docker build -t my-fastapi-app .
```

---

## 2. Provide Your API Key Securely

**Option A: Pass the API key as an environment variable**

Replace `sk-...your-key...` with your actual API key:

```sh
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=sk-...your-key... \
  --name fastapi-app my-fastapi-app
```

**Option B: Use a .env file**

1. Create a file named .env in your project root with this content:

    ```
    OPENAI_API_KEY=sk-...your-key...
    ```

2. Run the container using the `.env` file:

    ```sh
    docker run -d -p 8000:8000 --env-file .env --name fastapi-app my-fastapi-app
    ```

---

## 3. Access the API

- Open your browser and go to: [http://localhost:8000/docs](http://localhost:8000/docs)
- Or test with curl:

    ```sh
    curl http://localhost:8000/docs
    ```

---

## 4. Stopping and Removing the Container

To stop the running container:

```sh
docker stop fastapi-app
```

To remove the container:

```sh
docker rm fastapi-app
```

---

## 5. Security Tips

- **Never** hardcode your API key in your code or Dockerfile.
- Add `.env` to your `.gitignore` to avoid committing secrets to version control.

---

**Your FastAPI app is now running in Docker with your API key securely provided!**---

## 5. Security Tips

- **Never** hardcode your API key in your code or Dockerfile.
- Add `.env` to your `.gitignore` to avoid committing secrets to version control.

---

**Your FastAPI app is now running in Docker with your API key securely provided!**
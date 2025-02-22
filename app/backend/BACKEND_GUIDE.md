# Backend Environment Setup and Testing

The backend is designed to run independently, allowing for testing without relying on the frontend or the Jetson Orin Nano Super. This setup ensures that the backend can be tested in isolation, without needing the frontend or Jetson device to be active.

Follow the steps below to create and activate the environment. If the environment has already been created, skip to the activation steps.

---

## Step 1: Create the Virtual Environment
```bash
python -m venv venv
```

---

## Step 2: Activate the Virtual Environment

### macOS/Linux
```bash
source venv/bin/activate
```

### Windows (PowerShell)
```powershell
.\venv\Scripts\activate
```

---

## Step 3: Install Dependencies
Ensure all required dependencies are installed within the virtual environment:
```bash
pip install -r requirements.txt
```

---

## Step 4: Run the Backend Server
Before running the backend, ensure your virtual environment is activated.

### Activate the Virtual Environment
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\activate
  ```

### Start the FastAPI Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Explanation:
- `main:app` → Refers to the app instance in `main.py`
- `--host 0.0.0.0` → Makes the backend accessible on your local network
- `--port 8000` → Runs the server on port 8000 (you can change this if needed)
- `--reload` → Enables automatic reloading when code changes (useful during development)

---

## Step 5: Use FastAPI's Automatic Documentation for API Endpoints
FastAPI automatically generates a user-friendly and interactive interface for developers to explore and test API endpoints.

- **Swagger UI**:
```bash
http://localhost:8000/docs
```
- **ReDoc**:
```bash
http://localhost:8000/redoc
```

Ensure to adjust `localhost:8000` if your backend is hosted on a different port.

---

## Step 6: Stop the Server and Deactivate the Environment

### Stop the Uvicorn Server
Press `CTRL + C` in the terminal where Uvicorn is running.

### Deactivate the Virtual Environment
```bash
deactivate
```

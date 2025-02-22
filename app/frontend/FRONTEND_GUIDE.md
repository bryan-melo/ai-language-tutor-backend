# Creating a React Project with Vite

To set up a new React project using Vite, follow these steps:

---

## Step 1: Create the React Project
Run the following command to initialize a new React project:

```bash
npm create vite@latest frontend -- --template react
```

---

## Step 2: Navigate to the Project Directory
After the project is created, change into the frontend directory:

```bash
cd frontend
```

---

## Step 3: Remove Default Dependencies
Before installing dependencies, open the `package.json` file and remove the default dependencies listed under `"dependencies"`, including `react` and `react-dom`.

---

## Step 4: Install the Latest Versions of React
Now, install the most recent versions of React and ReactDOM:

```bash
npm install --save-exact react@rc react-dom@rc
npm install
```

---

## Step 5: Start the Development Server
Once the dependencies are installed, start the development server with:

```bash
npm run dev
```

This will launch your React application, making it accessible via the provided local development URL.

---

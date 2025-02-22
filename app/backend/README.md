# Environment Creation and Activation for the Backend

The backend runs independently to allow the Jetson Orin Nano Super to communicate with it while operating in voice-command mode. Alternatively, this setup enables the app to start the backend when it is loaded, without any dependency on the Jetson Orin Nano Super.

Follow the steps below to create and activate the environment. If the environment has already been created, skip to the activation steps.

## Create Environment
```bash
    python -m venv venv
```

## Activate the Environtment

### Windows
```powershell
    .\venv\Script\activate
```

### Mac/Linux
```bash
    source venv/bin/activate
```

## Deactivate the Environment
```bash
    deactivate
```

## Ensure dependencies are installed within the virtual environment
```bash
    pip install -r requirements.txt
```
# Scribbler

description of app here

## Development Environment

This project uses Visual Studio Code's Dev Containers feature for development. The `.devcontainer` directory includes a `devcontainer.json` configuration file to set up a consistent development environment.

### Using Dev Containers

1. **Install Visual Studio Code**: Ensure you have Visual Studio Code installed.
2. **Install the Remote - Containers Extension**: This allows you to open and develop inside containers.
3. **Open the Project**: Open the `scribbler` folder in Visual Studio Code.
4. **Reopen in Container**: Visual Studio Code will prompt you to reopen the folder in the container. Confirm to start the container setup.

The container is configured to use a Python 3.11 image, install necessary Python packages, and run the Streamlit application.

### Dev Container Configuration

The `.devcontainer/devcontainer.json` file includes:

- A Docker image with Python 3.11.

### Running the Application

Once inside the Dev Container:

1. **Start the Streamlit Application**:
   ```bash
   streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
   ```
   
2. Access the Application: The application will be available at http://localhost:8501.
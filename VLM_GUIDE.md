# VLM (VILA) Integration Guide

This document provides instructions on how to set up, run, and test the VILA Vision-Language Model integration for the Turing Tumble project.

## Features

- **Board Analysis**: Uses the VILA model to analyze an image of the Turing Tumble board.
- **Component Detection**: Identifies the type and position of each component on the board.
- **Dynamic Responses**: Provides real-time analysis instead of static or dummy data.

---

## 🔧 Setup and Installation

### Prerequisites

- **Node.js**: For running the frontend.
- **Python (3.12+ recommended)**: For running the backend.
- **A Python virtual environment**: To manage dependencies.
- **VILA API Credentials**: You need an API key and the correct URL for the VILA service.

### Environment Setup

1.  Navigate to the backend directory:
    ```sh
    cd TTGD/TTG_Backend
    ```

2.  Create a file named `.env` in this directory.

3.  Add your VILA API key and URL to the `.env` file. This file stores your credentials securely.
    ```env
    # Example .env content
    VILA_API_KEY="your_api_key_here"
    VILA_API_URL="your_vila_api_endpoint_url_here"
    ```
    > **Note:** The `VILA_API_URL` could be a local inference server or a cloud-based endpoint from a provider like NVIDIA.

---

## ▶️ Running the Application

### Backend

1.  Navigate to the backend directory:
    ```sh
    cd TTGD/TTG_Backend
    ```
2.  Activate the virtual environment. *Note: Your virtual environment might have a different name.*
    ```sh
    .venv_new\Scripts\activate
    ```
3.  Start the backend server:
    ```sh
    python -m uvicorn api:app --reload
    ```
    The backend server will now be running on `http://localhost:8000`.

### Frontend

1.  In a **new terminal**, navigate to the frontend directory:
    ```sh
    cd TTGD/TTG_Frontend/app
    ```
2.  If you haven't already, install the necessary dependencies:
    ```sh
    npm install
    ```
3.  Start the frontend application:
    ```sh
    npm start
    ```
    The application will now be accessible at `http://localhost:3000`.

---

##  Testing the VLM Integration

To verify that the VILA connection is working correctly, you can run the provided test script.

1.  Make sure the **backend server is running**.

2.  In the terminal where your backend's virtual environment is active, run the following command:
    ```sh
    python test_vila_detection.py
    ```

3.  A successful test will output the message: ` REAL VILA RESPONSE DETECTED!`. If you see a ` DUMMY RESPONSE DETECTED!` message, check your `.env` file and ensure your VILA service is accessible. 
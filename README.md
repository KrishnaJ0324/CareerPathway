# 🚀 Career Pathway

An intelligent web application that analyzes your resume to generate a personalized career roadmap, suggesting relevant jobs and the skills needed to land them. This project leverages AI to provide instant, data-driven career guidance.

## ✨ Live Demo & site

For a guided walkthrough of the features, check out the video demo on YouTube:

[![CareerPathway Project Demo](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/3reStAo9Nq8?feature=shared)

A live version of the application is hosted here. Check it out!

**[➡️ View Live Site](https://guide.everglade.in/)**



## 🌟 Key Features

* **📄 Resume Analysis:** Securely upload your resume in PDF format.
* **🧠 AI-Powered Skill Extraction:** Utilizes AI to intelligently parse your resume and identify your key skills and experiences.
* **🎯 Tailored Job Suggestions:** Recommends specific job titles and roles that are a strong match for your current skill set.
* **🗺️ Personalized Learning Roadmap:** Generates a custom step-by-step career path, suggesting new skills, technologies, and certifications to help you advance.
* **💨 Fast & Responsive:** Built with a modern tech stack for a smooth and intuitive user experience.

## 🛠️ Tech Stack

This project was built using the following technologies:

* **Frontend:** Javascript, HTML5, CSS3 
* **Backend:** Python
* **AI / LLM:** Google Gemini API

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Make sure you have the following installed on your machine:
* Node.js (v18 or higher)
* Python (v3.9 or higher)
* An active Google Gemini API key.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/KrishnaJ0324/CareerPathway.git
    cd careerpathway
    ```

2.  **Setup the Backend (FastAPI):**
    * Navigate to the backend directory:
        ```sh
        cd backend
        ```
    * Create a virtual environment and activate it:
        ```sh
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        ```
    * Install the required Python packages:
        ```sh
        pip install -r requirements.txt
        ```
    * Create a `.env` file in the `backend` directory and add your Gemini API key:
        ```env
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```
    * Run the backend server:
        ```sh
        uvicorn main:app --reload
        ```
    Your backend will be running on `http://127.0.0.1:8000`.

3.  **Setup the Frontend (React):**
    * In a new terminal, navigate to the frontend directory:
        ```sh
        cd frontend
        ```
    * Install the required npm packages:
        ```sh
        npm install
        ```
    * Start the frontend development server:
        ```sh
        npm start
        ```
    Your frontend will be running on `http://localhost:3000`.

## 📝 Usage

1.  Open your browser and navigate to `http://localhost:3000`.
2.  Click the "Upload Resume" button and select your resume file (PDF).
3.  Wait for the AI to process your document.
4.  View your personalized job suggestions and career path roadmap!


## 📧 Contact

Name: Krishna J
email: krishna0324@yahoo.com

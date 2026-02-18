# Resume ATS (Application Tracking System) Scoring Application

This is a web application can generate a consistent resume score for an uploaded PDF resume.

## Features
 - Get consistent resume score for a resume
 - Get an interactive section wise score along with justification and suggestions for improvement
 - Get similarity score between resume and job description along with justification and suggestions

## Application Snap Shots
  <p>Login Page</p>
  <img alt="Login Page" src="https://github.com/user-attachments/assets/dbf88dee-9646-4fe1-94c5-751ba5e387a9" width=50% height=50% />

  <p>Resume and JD Input Page</p>
  <img alt="Resume and JD Input Page" src="https://github.com/user-attachments/assets/be62608a-b21d-40a5-890c-f3cd56ace6f2" width=50% height=50% />

  <p>Resume Score Page</p>
  <img alt="Resume Score Page" src="https://github.com/user-attachments/assets/c1258d75-2010-4710-9d24-52beb3e06912" width=50% height=50% />

  <p>Resume Score with Analysis</p>
  <img alt="Resume Score with Analysis" src="https://github.com/user-attachments/assets/9068bed2-7035-424a-bfa1-dd7d7ad8dcc9" width=50% height=50% />

  <p>Similarity Score with Analysis</p>
  <img alt="Similarity Score with Analysis" src="https://github.com/user-attachments/assets/aed9839b-0c88-448e-be01-759fd3203139" width=50% height=50% />

	
## Technologies used

Frontend - `Streamlit`

Backend - `Python`, `Autogen`, `Python`, `redis`, `MongoDB`, `MySQL`

Deployment - `Docker`, `Kubernetes`, `Github Actions`

## Steps to run locally

### Step 1. Clone the repositories
#### Backend: https://github.com/spandanx/ResumeATS


### Step 2. Install required softwares

`Miniconda`

### Step 3. Prepare backend

#### Create new environment
<p>Open miniconda console. Run the below commands </p>

```
conda create -n env-name python=3.10
conda activate env-name
```

#### Install required packages
```
python -m pip install -r requirements.txt
```

#### Run the python application
```
streamlit run ui.py
```
The (.env) environment file should contain OPENAI_API_KEY and TAVILY_API_KEY

## Architecture
### Functional Diagram
![RESUME_ATS_HLD](https://github.com/user-attachments/assets/8bb2865e-d9a4-4e74-b228-9efe2f6164a8)

### Login Process
![RESUME_ATS_LOGIN_PROCESS](https://github.com/user-attachments/assets/ea922da7-7b11-422a-98b0-952734475eac)



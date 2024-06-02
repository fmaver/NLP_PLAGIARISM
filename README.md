<div align="center" id="top"> 
    <img src="src/plagiarism.png" alt="Plagiarism Detection Project" />

  &#xa0;

  <!-- <a href="https://plagiarismdetectionapp.netlify.app">Demo</a> -->
</div>

<h1 align="center">Plagiarism Detection Project</h1>

<p align="center">
    <img alt="Github top language" src="https://img.shields.io/badge/Language-Python-blue">
</p>

<!-- Status -->

<h4 align="center"> 
	🚧 Plagiarism Detection Project 🚀 Under Construction 🚧<br><br>
  Made by <a href="https://github.com/fmaver" target="_blank">Francisco Maver</a>
</h4> 

<hr>

<p align="center">
  <a href="#overview">Overview</a> &#xa0; | &#xa0; 
  <a href="#features">Features</a> &#xa0; | &#xa0;
  <a href="#installation">Installation</a> &#xa0; | &#xa0;
  <a href="#running-the-application-locally">Running Locally</a> &#xa0; | &#xa0;
  <a href="#usage">Usage</a> &#xa0; | &#xa0;
  <a href="#project-structure">Project Structure</a> &#xa0; | &#xa0;
  <a href="#license">License</a> &#xa0; | &#xa0;
  <a href="#contributing">Contributing</a> &#xa0; | &#xa0;
  <a href="#contact">Contact</a> 
</p>

<br>

## Overview

This project is a plagiarism detection application built using Python 3. It leverages a BERT model for detecting plagiarism and a pre-trained model from sklearn for detecting themes. The application uses Elasticsearch for database management, FastAPI with Uvicorn for the web application, and is containerized using Docker Compose.

## Features

- Detect plagiarism using a BERT model.
- Detect themes in documents using a pre-trained sklearn model.
- Supports text, PPTX, PDF, and DOCX file formats for analysis.
- FastAPI-based RESTful API for file uploads and plagiarism detection.
- Elasticsearch integration for efficient document storage and retrieval.
- Docker Compose setup for easy deployment and management.

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/plagiarism-detection.git
    cd plagiarism-detection
    ```

2. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

## Running the Application Locally

1. Build and start the services using Docker Compose:

    ```bash
    docker-compose up
    ```

   This will start the following services:
   - **Elasticsearch**: The database connection.
   - **Migration**: Converts the zip file containing all documents into text, vectorizes them, and loads them into Elasticsearch.
   - **App (FastAPI)**: Runs the web application and provides the API endpoints.

2. Verify the services are running:

   - Elasticsearch should be available at `http://localhost:9200`.
   - FastAPI app should be available at `http://localhost:8000`.

3. To stop the services, use:

    ```bash
    docker-compose down
    ```

## Usage

### API Endpoint

#### Upload File for Plagiarism Detection

- **URL**: `/upload`
- **Method**: `POST`
- **Allowed file types**: TXT, PPTX, PDF, DOCX

**Example Request**:

```bash
curl -X POST "http://localhost:8000/upload" -F "file=@path_to_your_file"

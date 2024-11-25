<div align="center">
    <h1>Complete MLOps for Network Security</h1>
    <img src="https://github.com/user-attachments/assets/091957d5-d4cd-46d9-8049-1eb1c5c715a2" alt="project-gif" />
</div>

## 📚 Table of Contents
1. [Problem Statement](#-problem-statement)
2. [Goals Achieved](#-goals-achieved)
3. [Project Methodology](#%EF%B8%8F-project-methodology)
   - [Data Ingestion](#data-ingestion)
   - [Data Validation](#data-validation)
   - [Data Transformation](#data-transformation)
   - [Model Building & Testing](#model-building--testing)
   - [Deployment Pipeline](#deployment-pipeline)
4. [Contribution](#-contribution)
5. [Project Outro](#-project-outro)

## 🚩 Problem Statement
The web is filled with malicious traffic which leads to numerous kinds of phishing attempts. This project aims to understand and detect phishing attempts in network traffic using various machine learning algorithms. By leveraging various data processing and modeling strategies, this project provides a robust solution for identifying malicious URLs and enhancing network security.

## 🎯 Goals Achieved
- Developed a comprehensive pipeline for data ingestion, validation, transformation, and model training.
- Implemented a machine learning model capable of predicting phishing attempts with high accuracy.
- Established a deployment pipeline to facilitate easy integration and continuous delivery of the model.

## 🛠️ Project Methodology
### Data Ingestion
The project begins with data ingestion, where data is collected from a MongoDB database. The data is then exported into a structured format for further processing.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/8eaa17e2-1359-4828-a4fd-3d5908dc44aa">

### Data Validation
Once the data is ingested, it undergoes validation to ensure its quality and integrity. This step checks for missing values, schema conformity, and potential dataset drift.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/842306b2-8aff-4a69-9f0e-785316f33956">

### Data Transformation
After validation, the data is transformed to prepare it for modeling. This includes handling missing values, feature scaling, and encoding categorical variables.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/4fe65518-b248-4297-ba97-e94679d1e22c">

### Model Building & Testing
The core of the project involves building and testing various machine learning models. The best-performing model is selected based on evaluation metrics such as accuracy, precision, and recall.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/d5d7bd50-0590-45d8-a864-2fe01c314d5f">

### Deployment Pipeline
Finally, the trained model is deployed using FastAPI, allowing users to make predictions through a web interface. The deployment pipeline ensures that the model can be updated seamlessly as new data becomes available.
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/6369e6e6-65c3-4a1e-965e-f2cc2252db08">

## 🤝 Contribution
I would love contributions from the community! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## 🎉 Project Outro
Thank you for exploring the **Network Security Model Prediction** project! We hope this project serves as a valuable resource for understanding how to implement machine learning solutions for network security. Your feedback and contributions are greatly appreciated. Let's work together to make the internet a safer place! 🌐






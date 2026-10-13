\# Swiggy Customer Analytics



\## Project Overview



Swiggy Customer Analytics is a data analytics project that uses Python, SQL, Machine Learning, and Streamlit to explore customer behavior, segment customers, and recommend customer retention actions.



\## Objectives



\* Clean and prepare customer and order data.

\* Perform Exploratory Data Analysis (EDA).

\* Analyze customer purchasing behavior using RFM analysis.

\* Segment customers using K-Means clustering.

\* Evaluate machine learning and deep learning approaches for churn analysis.

\* Identify customer risk using transparent, rule-based logic.

\* Present insights through an interactive Streamlit application.



\## Tools and Technologies



\* Python

\* Pandas and NumPy

\* Matplotlib and Seaborn

\* Scikit-learn

\* TensorFlow/Keras

\* MySQL

\* Jupyter Notebook

\* Streamlit



\## Project Structure



\* `app/` — Streamlit application

\* `data/` — Data files and processed datasets

\* `models/` — Trained model files (kept locally)

\* `notebooks/` — Data analysis, segmentation, and model evaluation

\* `outputs/tables/` — Analysis results and summaries

\* `sql/` — Database setup and analytical queries

\* `src/` — Python source modules



\## Key Analysis



\* Customer segmentation using RFM analysis and K-Means.

\* Customer risk categorization and retention recommendations.

\* Churn model evaluation, including comparison against chance-level performance.



\## Important Model Limitation



The tested churn models did not demonstrate reliable predictive performance on held-out data. Therefore, churn predictions should not be treated as dependable forecasts. Customer risk categories are heuristic indicators based on customer activity, not validated predictions.



\## Running the Streamlit App



Install the required dependencies, then run:



```bash

streamlit run app/streamlit\_app.py

```



\## Data and Privacy



Raw datasets, large customer-level files, trained models, and temporary files may be excluded from the public repository. The application may require locally available data or model artifacts, depending on its implementation.



\## Project Status



The Streamlit application and analysis notebooks have been developed. This repository documents the Python-based analytics workflow and its current limitations.




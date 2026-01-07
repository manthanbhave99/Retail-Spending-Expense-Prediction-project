# Retail-Spending-Expense-Prediction-project
End-to-end Spend Analytics dashboard using Python, MySQL, Machine Learning, and Streamlit. The project analyzes transaction data, predicts spend using regression models, classifies risk with logistic and decision trees, and segments customers into actionable risk bands.

Spend Analytics & Risk Prediction Dashboard
Project Overview

This project is an end-to-end analytics and machine learning application built using Python, MySQL, Scikit-learn, and Streamlit. It analyzes transaction data to predict spending behavior, classify risk, and segment customers into actionable risk bands through an interactive dashboard.

Key Features

Transaction-level spend analysis

Merchant-wise and trend-based visualizations

Spend prediction using Linear Regression

Risk classification using Logistic Regression and Decision Trees

Customer-level risk segmentation (Low / Medium / High)

Interactive Streamlit dashboard with button-driven predictions

MySQL used as the backend data source

Tech Stack

Programming Language: Python

Database: MySQL

Machine Learning: scikit-learn

Visualization & UI: Streamlit

Data Handling: Pandas

Dataset

The project uses a transactional CSV file containing fields such as:

customer_name

merchant_name

transaction_amount

account_id

city

opening_balance

The data can be loaded directly from CSV or stored and queried from MySQL.

Machine Learning Models

Linear Regression: Predicts estimated transaction amount

Logistic Regression: Classifies high vs normal spend behavior

Decision Tree Regressor: Captures non-linear spend patterns

Decision Tree Classifier: Rule-based risk classification

Risk Segmentation Logic

Customers are aggregated at profile level and classified into:

LOW Risk

MEDIUM Risk

HIGH Risk

Segmentation is based on quantile-based thresholds of total spending, ensuring scalability and explainability.

How to Run the Project
1. Install Dependencies
pip install streamlit pandas scikit-learn mysql-connector-python

2. Ensure Files Are Present

predictions.py

spending expenses.csv

3. Run the Application
streamlit run predictions.py

Business Use Cases

Spend behavior monitoring

Customer risk profiling

Credit and fraud risk pre-screening

Portfolio-level customer segmentation

'''“I built both regression and classification pipelines.
Linear and logistic models provide baseline predictions,
while decision trees capture non-linear relationships and decision rules.
This allows comparison between statistical and rule-based models.”
'''


import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

st.title("Accounts Estimate Dashboard")

# -------------------------
# Load Data
# -------------------------
acc = pd.read_csv("spending expenses.csv")

st.subheader("Transaction Data")
st.dataframe(acc)

# Customer Spending Risk analysis

customer_df = acc.groupby("customer_name").agg(
    total_spend=("transaction_amount", "sum"),
    avg_spend=("transaction_amount", "mean"),
    max_spend=("transaction_amount", "max"),
    
).reset_index()

st.subheader("Customer Profiles")
st.dataframe(customer_df)

# ---- 
# Charts
# -----
st.subheader(" Bar Chart of Amount Spent per Merchant")

merchant_spend = acc.groupby("merchant_name")["transaction_amount"].sum()
st.bar_chart(merchant_spend)

st.subheader("Multiple Line Chart – Merchant Comparison")
multi_line = acc.pivot_table(
    values="transaction_amount",
    index=acc.index,
    columns="merchant_name",
    aggfunc="sum"
)
st.line_chart(multi_line)

st.subheader("Box Plot – Spend Distribution")
st.pyplot(
    acc[["transaction_amount"]].boxplot().figure
)


# Encoding
# -------------------------
le = LabelEncoder()
acc["merchant_encoded"] = le.fit_transform(acc["merchant_name"])

# Linear Regression
# -------------------------
X_lr = acc[["merchant_encoded"]]
y_lr = acc["transaction_amount"]

lin_model = LinearRegression()
lin_model.fit(X_lr, y_lr)

# Logistic Regression
# -------------------------
avg_amount = acc["transaction_amount"].mean()
acc["high_spend"] = (acc["transaction_amount"] >= avg_amount).astype(int)

log_model = LogisticRegression()
log_model.fit(X_lr, acc["high_spend"])


# Decision Tree Models
# -------------------------
dt_reg = DecisionTreeRegressor(max_depth=3, random_state=42)
dt_reg.fit(X_lr, y_lr)

dt_clf = DecisionTreeClassifier(max_depth=3, random_state=42)
dt_clf.fit(X_lr, acc["high_spend"])



# -------------------------
# Prediction Section
# -------------------------
st.subheader("Predictions")

merchant_input = st.selectbox(
    "Select Merchant",
    acc["merchant_name"].unique()
)

merchant_encoded = le.transform([merchant_input])[0]

input_df = pd.DataFrame(
    {"merchant_encoded": [merchant_encoded]}
)

if st.button("Predict"):
    # Linear Regression
    lin_pred = lin_model.predict(input_df)[0]

    # Decision Tree Regression
    dt_pred = dt_reg.predict([[merchant_encoded]])[0]

    # Logistic Regression
    log_class = log_model.predict(input_df)[0]
    log_prob = log_model.predict_proba(input_df)[0][1]

    # Decision Tree Classification
    dt_class = dt_clf.predict(input_df)[0]
    dt_prob = dt_clf.predict_proba(input_df)[0][1]

    st.success(f"Linear Regression Estimate: ₹ {lin_pred:,.2f}")
    st.success(f"Decision Tree Estimate: ₹ {dt_pred:,.2f}")

    st.info(
        f"Logistic Regression → "
        f"{'HIGH SPEND' if log_class else 'NORMAL SPEND'} "
        f"(Probability: {log_prob:.2%})"
    )

    st.info(
        f"Decision Tree → "
        f"{'HIGH SPEND' if dt_class else 'NORMAL SPEND'} "
        f"(Probability: {dt_prob:.2%})"
    )


# ----- Customer Risk Analysis -------




# Risk Prediction

low_threshold = customer_df["total_spend"].quantile(0.33)
high_threshold = customer_df["total_spend"].quantile(0.66)

def assign_risk_band(total_spend):
    if total_spend <= low_threshold:
        return "LOW"
    elif total_spend <= high_threshold:
        return "MEDIUM"
    else:
        return "HIGH"

customer_df["risk_band"] = customer_df["total_spend"].apply(assign_risk_band)

# Risk Band Distribution
# -------------------------
st.subheader("Risk Band Distribution")
st.bar_chart(customer_df["risk_band"].value_counts())


st.subheader("Predict Customer Risk")

customer_input = st.selectbox(
    "Select Customer",
    customer_df["customer_name"].unique()
)



# Risk Check Button

if st.button("Check Risk"):
    selected_customer = customer_df[
        customer_df["customer_name"] == customer_input
    ].iloc[0]

    st.write(f"Customer Name: **{customer_input}**")
    st.write(f"Total Spend: ₹ {selected_customer['total_spend']:,.2f}")
    st.write(f"Average Spend: ₹ {selected_customer['avg_spend']:,.2f}")
    st.write(f"Maximum Transaction: ₹ {selected_customer['max_spend']:,.2f}")


    st.write(f"### Risk Band: **{selected_customer['risk_band']}**")

    # Business Interpretation
    if selected_customer["risk_band"] == "HIGH":
        st.error(
            "High-risk customer detected. "
            "Immediate monitoring is recommended."
        )
    elif selected_customer["risk_band"] == "MEDIUM":
        st.warning(
            "Medium-risk customer. "
            "Regular monitoring advised."
        )
    else:
        st.success(
            "Low-risk customer. "
            "Spending behavior is normal."
        )
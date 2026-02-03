# Gemini AI Chatbot (Analytics Assistant)
from dotenv import load_dotenv
import google.generativeai as genai
import os
import re

# --- Load API key ---
load_dotenv()
api_key = os.getenv("api")
genai.configure(api_key=api_key)
print("API Key loaded:", bool(api_key))



# Initialize model
model = genai.GenerativeModel(
    "models/gemini-2.5-flash",
    system_instruction=(
        "You are a data analytics assistant. "
        "You explain in 3-4 lines about said customer  "
    )
)

selected_customer_name = st.selectbox(
    "Select Customer for AI Analysis",
    customer_df["customer_name"].unique()
)
selected_customer_row = customer_df[
    customer_df["customer_name"] == selected_customer_name
].iloc[0]

total_spend = float(selected_customer_row["total_spend"])
avg_spend = float(selected_customer_row["avg_spend"])
max_spend = float(selected_customer_row["max_spend"])
risk_band = (selected_customer_row["risk_band"])


st.subheader("AI Risk Explanation")

# Input
user_question = st.text_input(
    "Ask a question about Expense Pediction or Customer Risk"
)

# 🔑 Create a placeholder (clears previous output)
ai_output_container = st.empty()

if st.button("Ask AI"):
    if user_question.strip():
        # 🔍 Detect customer names in input
        # -----------------------------
        mentioned_customers = re.findall(r"Customer_\d+", user_question)

        if mentioned_customers and selected_customer_name not in mentioned_customers:
            st.warning(
                f"You selected **{selected_customer_name}**, "
                f"but asked about **{mentioned_customers[0]}**. "
                "Answer is shown for the selected customer."
            )


        prompt = f"""
        You must answer ONLY for the selected customer below.
        Ignore any customer names mentioned in the user question.

        Selected Customer Profile:
         {selected_customer_name}
        Total Spend: ₹{total_spend:,.2f}
        Average Spend: ₹{avg_spend:,.2f}
        Maximum Transaction: ₹{max_spend:,.2f}
        Risk Band: ₹{risk_band}

        Summarize in 2-3 lines using only this data. Must contain
         {selected_customer_name} and give some relevant suggestion if  in short.

        Question:
        {user_question}
        """

        response = model.generate_content(prompt)

        # ✅ This replaces previous output instead of appending
        ai_output_container.markdown("### AI Output")
        ai_output_container.write(response.text)

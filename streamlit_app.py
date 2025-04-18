import streamlit as st
import openai
import os

st.set_page_config(page_title="Case Prep Agent", page_icon="🧠", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #FFD700;'>🧠 Case Interview Prep Agent</h1>",
    unsafe_allow_html=True,
)

st.sidebar.markdown("## 🎛️ Customize Your Session")
tier = st.sidebar.selectbox("Your Case Prep Level:", ["Beginner", "Intermediate", "Interview-Ready"])
hint_mode = st.sidebar.toggle("Hint Mode", value=True)
feature = st.sidebar.selectbox("AI Feature:", [
    "Case Decomposition Assistant",
    "Live Rubric Feedback",
    "Synthesis Coach",
    "Case Buddy Mode"
])

st.sidebar.markdown("---")
api_key = st.sidebar.text_input("🔑 Enter your OpenAI API Key:", type="password")
submit = st.sidebar.button("Run Agent")

user_input = st.text_area("📝 Enter your case prompt, response, or summary depending on the selected tool:", height=200)

def build_prompt(tier, hint, feature, user_input):
    hint_line = " Provide guidance to the user." if hint else " Do not give hints unless asked."
    if feature == "Case Decomposition Assistant":
        return f"You are a case interview coach. Break this case into components: framework, key issues, data needed, and hypotheses. Case: {user_input}.{hint_line}"
    elif feature == "Live Rubric Feedback":
        return f"You are a case interview evaluator. Score this response (1–10) on: structure, math, insight, and synthesis. Then provide concise feedback. Response: {user_input}.{hint_line}"
    elif feature == "Synthesis Coach":
        return f"You are a synthesis coach. Evaluate the user's case conclusion for clarity, logic, and impact. Offer suggestions to improve. Conclusion: {user_input}.{hint_line}"
    elif feature == "Case Buddy Mode":
        return f"You are acting as a case partner. Respond to the user's last answer with a realistic follow-up question or challenge. Input: {user_input}.{hint_line}"
    else:
        return "Invalid feature."

if submit and api_key and user_input:
    with st.spinner("Thinking like a consultant..."):
        try:
            client = openai.OpenAI(api_key=api_key)
            prompt = build_prompt(tier, hint_mode, feature, user_input)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful case interview coach for MBA students."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            st.markdown("### 🤖 Agent Response:")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
elif submit and not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os


def generate_recovery_advice(risk_score, risk_level, shap_features):

    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",   # fast + good
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY"),
        )

        feature_summary = "\n".join(
            [f"- {f['feature']} ({f['direction']})"
             for f in shap_features]
        )

        prompt = ChatPromptTemplate.from_template("""
You are a sports injury prevention assistant.

Risk score: {risk_score}
Risk level: {risk_level}

Key contributing factors:
{feature_summary}

Provide:
1. Short explanation.
2. 3 actionable recovery steps.
Keep concise.
""")

        chain = prompt | llm

        response = chain.invoke({
            "risk_score": risk_score,
            "risk_level": risk_level,
            "feature_summary": feature_summary
        })

        return response.content

    except Exception as e:
        return f"Groq AI unavailable: {str(e)}"
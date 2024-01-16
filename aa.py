# Define a dictionary to store the AI capabilities in Power BI and their descriptions
power_bi_ai_capabilities = {
    "AI-powered Data Analysis": "Power BI offers AI-powered data analysis capabilities, including natural language querying and automated insights. Users can ask questions in plain language, and Power BI generates visualizations and insights based on the data.",
    "AI-powered Visualization": "Power BI leverages AI to create more impactful visualizations by suggesting appropriate charts and visual elements based on the data and analysis context.",
    "Custom Machine Learning Models": "Power BI supports the integration of custom machine learning models, enabling users to create and utilize their own AI models for advanced data analysis and predictions."
}

# Print the AI capabilities in Power BI and their descriptions
print("Power BI AI Capabilities:")
for capability, description in power_bi_ai_capabilities.items():
    print(f"{capability}: {description}")

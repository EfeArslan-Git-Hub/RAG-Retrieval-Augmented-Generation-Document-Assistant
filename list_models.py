import google.generativeai as genai
import getpass

print("--- Google Gemini Model Lister ---")
print("This script helps identify which models are available for your API Key.")
api_key = input("Please paste your Google API Key (input will be visible): ")

if not api_key:
    print("Error: API Key is empty.")
else:
    try:
        genai.configure(api_key=api_key)
        print("\nFetching available models...")
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("\nNo models found! Your API Key might be invalid or has no access.")
        else:
            print("\nSuccess! Please copy one of the model names above (e.g., 'models/gemini-1.5-flash') and let the assistant know.")
            
    except Exception as e:
        print(f"\nError connecting to Google API: {str(e)}")

import google.generativeai as genai
import re
import os

print("--- Auto-Configure Gemini Model ---")
api_key = input("Please paste your Google API Key (input will be visible): ")

if not api_key:
    print("Error: API Key is empty.")
    exit()

try:
    print("\nConnecting to Google API...")
    genai.configure(api_key=api_key)
    
    valid_model = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Prefer gemini-1.5-flash if available, otherwise take the first one
            if 'gemini-1.5-flash' in m.name:
                valid_model = m.name
                break
            if not valid_model:
                valid_model = m.name # Take the first one as fallback
    
    if not valid_model:
        print("\nERROR: No suitable models found for this API Key.")
    else:
        print(f"\nFound valid model: {valid_model}")
        
        # Update src/chatbot.py
        file_path = os.path.join("src", "chatbot.py")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Regex to replace model="..."
        new_content = re.sub(r'model="[^"]+"', f'model="{valid_model}"', content)
        
        if content != new_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Successfully updated src/chatbot.py to use {valid_model}")
        else:
            print("File already uses this model.")

except Exception as e:
    print(f"\nError: {str(e)}")

print("\nPress Enter to exit...")
input()

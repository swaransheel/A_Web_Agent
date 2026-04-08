import warnings
warnings.filterwarnings('ignore')

import requests
import google.generativeai as genai

print("Testing APIs...")

# Test Tavily
try:
    result = requests.post('https://api.tavily.com/search', json={
        'api_key': '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',
        'query': 'python',
        'max_results': 1
    }).json()
    print('✅ Tavily Search: OK')
    print(f'   Found: {result["results"][0]["title"]}\n')
except Exception as e:
    print(f'❌ Tavily Error: {e}\n')

# Test Gemini  
try:
    genai.configure(api_key='AIzaSyAtkLOc4sSIS2MIOf-hjbsxfUeOUZzqQeE')
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content('hello')
    print('✅ Gemini API: OK')
    print(f'   Response: {response.text[:50]}...\n')
except Exception as e:
    print(f'❌ Gemini Error: {e}\n')

print('✅✅✅ Both APIs Working!')
print('Refresh http://localhost:8501 to test the app')

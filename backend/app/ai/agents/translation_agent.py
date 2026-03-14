import os

SUPPORTED_LANGUAGES = {
    'tamil': 'Tamil',
    'hindi': 'Hindi',
    'malayalam': 'Malayalam',
    'english': 'English',
}

def _get_model():
    import google.generativeai as genai
    api_key = os.getenv('GEMINI_API_KEY', '')
    if not api_key:
        raise ValueError('GEMINI_API_KEY not set in .env')
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def translate(text: str, target_language: str) -> str:
    if target_language == 'english' or target_language not in SUPPORTED_LANGUAGES:
        return text
    lang_name = SUPPORTED_LANGUAGES[target_language]
    try:
        model = _get_model()
        prompt = f'Translate this Indian legal explanation into {lang_name}. Keep legal terms like FIR, IPC, Section as-is. Simple language only.\n\n{text}\n\n{lang_name} translation:'
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f'[Translation Error] {e}'

def translate_query_to_english(query: str, source_language: str) -> str:
    if source_language == 'english':
        return query
    lang_name = SUPPORTED_LANGUAGES.get(source_language, 'Tamil')
    try:
        model = _get_model()
        prompt = f'Translate this {lang_name} legal question to English. Return only the English translation.\n\n{query}'
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f'[Translation] Query translation failed: {e}')
        return query

def run(query: str, answer: str, target_language: str) -> dict:
    translated = translate(answer, target_language)
    return {
        'original_answer': answer,
        'translated_answer': translated,
        'language': target_language,
        'language_name': SUPPORTED_LANGUAGES.get(target_language, 'Unknown'),
    }

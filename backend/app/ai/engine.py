import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils.language_detector import detect_language
from agents import legal_agent, fraud_agent, lawyer_agent, translation_agent

def run_query(query: str, language: str = 'auto', channel: str = 'chat') -> dict:
    if language == 'auto':
        language = detect_language(query)
    if language != 'english':
        english_query = translation_agent.translate_query_to_english(query, language)
    else:
        english_query = query
    fraud_result = fraud_agent.run(english_query)
    is_fraud = fraud_result['is_fraud_case']
    if is_fraud and fraud_result.get('answer'):
        answer = fraud_result['answer']
        model_used = fraud_result.get('model_used', 'unknown')
        sources = fraud_result.get('sources', [])
    else:
        legal_result = legal_agent.run(english_query)
        answer = legal_result['answer']
        model_used = legal_result['model_used']
        sources = legal_result['sources']
    lawyer_advice = lawyer_agent.run(english_query)
    translated = None
    if language != 'english':
        translated = translation_agent.run(query, answer, language)
        display_answer = translated['translated_answer']
    else:
        display_answer = answer
    sms_answer = None
    if channel == 'sms':
        sms_answer = display_answer[:320]
    return {
        'query_language': language,
        'english_query': english_query,
        'answer': answer,
        'translated_answer': display_answer,
        'sms_answer': sms_answer,
        'model_used': model_used,
        'sources': sources,
        'lawyer_advice': lawyer_advice,
        'is_fraud': is_fraud,
        'channel': channel,
        'translation': translated,
    }

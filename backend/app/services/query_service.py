import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ai.engine import run_query

def ask_legal_question(question: str, language: str = 'auto', channel: str = 'chat') -> dict:
    try:
        result = run_query(question, language=language, channel=channel)
        return result
    except Exception as e:
        print(f'[QueryService Error] {e}')
        return {
            'query_language': language,
            'english_query': question,
            'answer': f'Sorry, I could not process your request. Error: {str(e)}',
            'translated_answer': f'Sorry, I could not process your request. Error: {str(e)}',
            'sms_answer': None,
            'model_used': 'error',
            'sources': [],
            'lawyer_advice': {'specialization': 'General Practice Lawyer', 'suggestion': 'Please consult a lawyer.', 'legal_aid': {'helpline': '15100'}},
            'is_fraud': False,
            'channel': channel,
            'translation': None,
        }

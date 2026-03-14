ISSUE_TO_SPECIALIZATION = {
    'divorce': 'Family Lawyer',
    'marriage': 'Family Lawyer',
    'property': 'Property / Civil Lawyer',
    'land': 'Property / Civil Lawyer',
    'cybercrime': 'Cyber Law Specialist',
    'hacked': 'Cyber Law Specialist',
    'fraud': 'Criminal / Cyber Lawyer',
    'cheque': 'Commercial / Banking Lawyer',
    'contract': 'Commercial Lawyer',
    'accident': 'Motor Accident Claims Lawyer',
    'vehicle': 'Motor Accident Claims Lawyer',
    'consumer': 'Consumer Forum Advocate',
    'complaint': 'Consumer Forum Advocate',
    'fir': 'Criminal Defense Lawyer',
    'arrest': 'Criminal Defense Lawyer',
    'bail': 'Criminal Defense Lawyer',
    'labour': 'Labour / Employment Lawyer',
    'salary': 'Labour / Employment Lawyer',
}

LEGAL_AID = {
    'national': 'National Legal Services Authority (NALSA) — nalsa.gov.in',
    'tamilnadu': 'Tamil Nadu State Legal Services Authority — tnlsa.nic.in',
    'helpline': 'Legal Aid Helpline: 15100 (toll-free)',
}

def classify_issue(query: str) -> str:
    q = query.lower()
    for keyword, specialization in ISSUE_TO_SPECIALIZATION.items():
        if keyword in q:
            return specialization
    return 'General Practice Lawyer'

def run(query: str) -> dict:
    specialization = classify_issue(query)
    return {
        'specialization': specialization,
        'legal_aid': LEGAL_AID,
        'suggestion': f'For your issue, consult a {specialization}. Free legal aid: call 15100',
    }

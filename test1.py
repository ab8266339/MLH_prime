import json
import os
from pprint import pprint

from watson_developer_cloud import ToneAnalyzerV3



def invokeToneConversation(payload, maintainToneHistoryInContext=True):
    # load the .env file containing your environment variables for the required
    # services (conversation and tone)

    # replace with your own tone analyzer credentials
    tone_analyzer = ToneAnalyzerV3(
        username=os.environ.get('TONE_ANALYZER_USERNAME') or '0480936e-64df-4a8f-a420-0c59d557555c',
        password=os.environ.get('TONE_ANALYZER_PASSWORD') or 'SvzV7J6HjZDE',
        version='2016-04-01')

    # replace with your own workspace_id
    workspace_id = os.environ.get('WORKSPACE_ID') or 'YOUR WORKSPACE ID'

    tone = tone_analyzer.tone(text=payload)
    tone_dict = tone['document_tone']['tone_categories'][0]['tones']
    joy = tone_dict[3]['score']
    pprint (tone)
    pprint(tone_dict)
    pprint(joy)
    return tone


test_text = 'love your mother'
invokeToneConversation(test_text)
# synchronous call to conversation with tone included in the context
# pprint(invokeToneConversation(payload, maintainToneHistoryInContext))
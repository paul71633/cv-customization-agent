import os
from typing import Dict, Any

class Config:
    # LLM Settings
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
    USE_LOCAL_MODELS = os.getenv('USE_LOCAL_MODELS', 'false').lower() == 'true'
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '512'))
    DEFAULT_TONE = os.getenv('DEFAULT_TONE', 'professional')
    
    # Model configurations
    DEFAULT_MODELS = {
        'text_generation': 'microsoft/DialoGPT-medium',
        'summarization': 'facebook/bart-large-cnn',
        'text2text': 'google/flan-t5-base',
        'grammar': 'grammarly/coedit-large'
    }
    
    # File settings
    SUPPORTED_FORMATS = ['pdf', 'docx', 'doc']
    MAX_FILE_SIZE_MB = 10
import os
from typing import Dict, Any

class Config:
    # LLM Settings
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')
    USE_LOCAL_MODELS = os.getenv('USE_LOCAL_MODELS', 'false').lower() == 'true'
    
    # Model configurations
    DEFAULT_MODELS = {
        'text_generation': 'microsoft/DialoGPT-medium',
        'summarization': 'facebook/bart-large-cnn',
        'text2text': 'google/flan-t5-base',
        'grammar': 'grammarly/coedit-large'
    }
    
    # Rewriting settings
    DEFAULT_TONE = 'professional'
    MAX_TOKENS = 512
    TEMPERATURE = 0.7
    
    # File settings
    SUPPORTED_FORMATS = ['pdf', 'docx', 'doc']
    MAX_FILE_SIZE_MB = 10
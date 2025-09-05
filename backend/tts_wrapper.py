"""
TTS Wrapper - Handles optional TTS dependencies gracefully
"""
import logging

# Try to import TTS, but handle gracefully if not available
try:
    from TTS.api import TTS as CoquiTTS
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
    from TTS.config.shared_configs import BaseDatasetConfig
    TTS_AVAILABLE = True
    logging.info("TTS modules loaded successfully")
except ImportError as e:
    logging.warning(f"TTS modules not available: {e}")
    TTS_AVAILABLE = False
    
    # Create dummy classes for when TTS is not available
    class CoquiTTS:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("TTS not available in this deployment")
    
    class XttsConfig:
        pass
    
    class XttsAudioConfig:
        pass
    
    class XttsArgs:
        pass
    
    class BaseDatasetConfig:
        pass

def get_tts_instance(*args, **kwargs):
    """Get TTS instance if available, otherwise raise informative error"""
    if not TTS_AVAILABLE:
        raise RuntimeError("TTS functionality not available in this deployment. Please install TTS package.")
    return CoquiTTS(*args, **kwargs)
"""
User Preferences Service for Mainza Consciousness
Manages user preference settings and provides default configurations
"""

import logging
from typing import Dict, Any, Optional
from backend.models.user_preferences import UserPreferences, UserPreferencesUpdate, ResponseVerbosity

logger = logging.getLogger(__name__)

class UserPreferencesService:
    """Service for managing user preferences"""
    
    def __init__(self):
        self._default_preferences = UserPreferences.get_default()
        self._user_preferences_cache: Dict[str, UserPreferences] = {}
    
    def get_user_preferences(self, user_id: str) -> UserPreferences:
        """Get user preferences, creating default if not exists"""
        try:
            if user_id in self._user_preferences_cache:
                return self._user_preferences_cache[user_id]
            
            # For now, return default preferences
            # In the future, this could load from database
            preferences = self._default_preferences
            self._user_preferences_cache[user_id] = preferences
            
            logger.debug(f"Retrieved preferences for user {user_id}")
            return preferences
            
        except Exception as e:
            logger.error(f"Error getting preferences for user {user_id}: {e}")
            return self._default_preferences
    
    def update_user_preferences(self, user_id: str, updates: UserPreferencesUpdate) -> UserPreferences:
        """Update user preferences"""
        try:
            current_preferences = self.get_user_preferences(user_id)
            
            # Apply updates
            update_data = updates.dict(exclude_unset=True)
            updated_data = current_preferences.dict()
            updated_data.update(update_data)
            
            # Create new preferences object
            new_preferences = UserPreferences(**updated_data)
            self._user_preferences_cache[user_id] = new_preferences
            
            logger.info(f"Updated preferences for user {user_id}: {update_data}")
            return new_preferences
            
        except Exception as e:
            logger.error(f"Error updating preferences for user {user_id}: {e}")
            return self.get_user_preferences(user_id)
    
    def get_response_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get response-specific preferences for formatting"""
        try:
            preferences = self.get_user_preferences(user_id)
            return {
                'verbosity': preferences.verbosity.value,
                'max_length': preferences.max_response_length,
                'show_tools_used': preferences.show_tools_used,
                'format_tables': preferences.format_tables,
                'show_context_info': preferences.show_context_info,
                'progressive_disclosure': preferences.progressive_disclosure
            }
        except Exception as e:
            logger.error(f"Error getting response preferences for user {user_id}: {e}")
            return {
                'verbosity': 'detailed',
                'max_length': 500,
                'show_tools_used': True,
                'format_tables': True,
                'show_context_info': True,
                'progressive_disclosure': True
            }
    
    def get_ui_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get UI-specific preferences"""
        try:
            preferences = self.get_user_preferences(user_id)
            return {
                'dark_mode': preferences.dark_mode,
                'compact_mode': preferences.compact_mode,
                'auto_suggestions': preferences.auto_suggestions
            }
        except Exception as e:
            logger.error(f"Error getting UI preferences for user {user_id}: {e}")
            return {
                'dark_mode': True,
                'compact_mode': False,
                'auto_suggestions': True
            }
    
    def get_agent_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get agent-specific preferences"""
        try:
            preferences = self.get_user_preferences(user_id)
            return {
                'preferred_agent': preferences.preferred_agent,
                'consciousness_awareness': preferences.consciousness_awareness,
                'emotional_responses': preferences.emotional_responses
            }
        except Exception as e:
            logger.error(f"Error getting agent preferences for user {user_id}: {e}")
            return {
                'preferred_agent': None,
                'consciousness_awareness': True,
                'emotional_responses': True
            }
    
    def reset_to_defaults(self, user_id: str) -> UserPreferences:
        """Reset user preferences to defaults"""
        try:
            default_preferences = UserPreferences.get_default()
            self._user_preferences_cache[user_id] = default_preferences
            
            logger.info(f"Reset preferences to defaults for user {user_id}")
            return default_preferences
            
        except Exception as e:
            logger.error(f"Error resetting preferences for user {user_id}: {e}")
            return self._default_preferences
    
    def get_preference_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user preferences"""
        try:
            preferences = self.get_user_preferences(user_id)
            return {
                'user_id': user_id,
                'verbosity': preferences.verbosity.value,
                'max_response_length': preferences.max_response_length,
                'preferred_agent': preferences.preferred_agent,
                'consciousness_awareness': preferences.consciousness_awareness,
                'emotional_responses': preferences.emotional_responses,
                'dark_mode': preferences.dark_mode,
                'compact_mode': preferences.compact_mode
            }
        except Exception as e:
            logger.error(f"Error getting preference summary for user {user_id}: {e}")
            return {
                'user_id': user_id,
                'error': str(e)
            }

# Global instance
user_preferences_service = UserPreferencesService()

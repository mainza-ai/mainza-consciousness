import os
import time
import jwt  # PyJWT
import logging
import asyncio
import json
from typing import Optional, Dict, Any

# Import LiveKit API for server-side operations
from livekit import api
from livekit.protocol import room as proto_room
from google.protobuf import json_format

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")

# LiveKit VideoGrant payload structure
class VideoGrant:
    def __init__(self, room=None, room_join=True, can_publish=True, can_publish_data=True, can_subscribe=True):
        self.room = room
        self.room_join = room_join
        self.can_publish = can_publish
        self.can_publish_data = can_publish_data
        self.can_subscribe = can_subscribe
    def as_dict(self):
        d = {"roomJoin": self.room_join, "canPublish": self.can_publish, "canPublishData": self.can_publish_data, "canSubscribe": self.can_subscribe}
        if self.room:
            d["room"] = self.room
        return d

def generate_access_token(room: str, identity: str) -> str:
    """Generate JWT access token for LiveKit room"""
    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        raise ValueError("LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set")
    
    # Create access token using the LiveKit API
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity(identity).with_name(identity)
    token.with_grants(api.VideoGrants(
        room_join=True,
        room=room,
        can_publish=True,
        can_subscribe=True,
        can_publish_data=True
    ))
    
    return token.to_jwt()

async def get_or_create_rtmp_ingress(room: str, user: str) -> Dict[str, Any]:
    """
    Get or create an RTMP ingress for the specified room and user.
    Uses the LiveKit API client for proper ingress management.
    """
    try:
        if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET or not LIVEKIT_URL:
            raise ValueError("LIVEKIT_API_KEY, LIVEKIT_API_SECRET, and LIVEKIT_URL must be set")
        
        # Create LiveKit API client
        livekit_api = api.LiveKitAPI(
            url=LIVEKIT_URL,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET
        )
        
        try:
            # Import the protocol messages for ingress requests
            from livekit.protocol import ingress as proto_ingress
            from livekit.protocol import models
            
            # Try to list existing ingresses first
            list_request = proto_ingress.ListIngressRequest()
            ingresses_response = await livekit_api.ingress.list_ingress(list_request)
            
            # Look for existing ingress for this room
            existing_ingress = None
            for ingress in ingresses_response.items:
                if (ingress.room_name == room and 
                    ingress.input_type == proto_ingress.IngressInput.RTMP_INPUT and
                    ingress.state.status in [proto_ingress.IngressState.ENDPOINT_PUBLISHING, proto_ingress.IngressState.ENDPOINT_BUFFERING, proto_ingress.IngressState.ENDPOINT_COMPLETE]):
                    existing_ingress = ingress
                    break
            
            if existing_ingress:
                logging.info(f"Found existing RTMP ingress: {existing_ingress.stream_key}")
                return {
                    "rtmp_url": existing_ingress.url,
                    "stream_key": existing_ingress.stream_key,
                    "ingress_id": existing_ingress.ingress_id
                }
            
            # Create new RTMP ingress
            create_request = proto_ingress.CreateIngressRequest()
            create_request.input_type = proto_ingress.IngressInput.RTMP_INPUT
            create_request.room_name = room
            create_request.participant_name = f"tts-{user}"
            create_request.participant_identity = f"tts-{user}"
            
            # Set audio configuration
            create_request.audio.source = models.TrackSource.MICROPHONE
            create_request.audio.preset = proto_ingress.IngressAudioEncodingPreset.OPUS_STEREO_96KBPS
            
            response = await livekit_api.ingress.create_ingress(create_request)
            
            logging.info(f"Created new RTMP ingress: {response.stream_key}")
            
            return {
                "rtmp_url": response.url,
                "stream_key": response.stream_key,
                "ingress_id": response.ingress_id
            }
            
        finally:
            await livekit_api.aclose()
            
    except Exception as e:
        logging.error(f"Error in get_or_create_rtmp_ingress: {str(e)}")
        raise 

async def send_data_message_to_room(room_name: str, payload: Dict[str, Any]):
    """
    Sends a data message to all participants in a given room.
    """
    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET or not LIVEKIT_URL:
        logging.error("LiveKit server environment variables not set. Cannot send data message.")
        return

    livekit_api = None
    try:
        livekit_api = api.LiveKitAPI(
            url=LIVEKIT_URL,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET
        )
        
        # The Python SDK uses Protobuf for requests. We create a SendDataRequest.
        request = proto_room.SendDataRequest()
        request.room = room_name
        # The payload must be bytes. We'll encode our JSON string to UTF-8.
        request.data = json.dumps(payload).encode('utf-8')
        # RELIABLE means delivery is guaranteed and ordered.
        # Use the correct DataPacket kind for current LiveKit version
        try:
            request.kind = proto_room.DataPacket.RELIABLE
        except AttributeError:
            # Fallback for different LiveKit versions
            try:
                request.kind = 1  # RELIABLE = 1 in most versions
            except:
                logging.warning("Could not set DataPacket kind, using default")
        
        # Send the data request
        await livekit_api.room.send_data(request)
        logging.info(f"Successfully sent data message to room '{room_name}'")

    except Exception as e:
        error_msg = str(e)
        
        # Handle specific LiveKit errors more gracefully
        if "TwirpError" in error_msg and "unavailable" in error_msg:
            logging.warning(f"LiveKit service unavailable for room '{room_name}'. This is normal if LiveKit is not running or not needed for current functionality.")
        elif "no response from servers" in error_msg:
            logging.warning(f"LiveKit servers not responding for room '{room_name}'. Check if Docker services are running: docker compose ps")
        else:
            logging.error(f"Failed to send data message to room '{room_name}': {e}")
        
        # Don't raise the exception - LiveKit failures shouldn't break the main application
        return False
    finally:
        if livekit_api:
            await livekit_api.aclose()
    
    return True 
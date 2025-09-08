import asyncio
import logging
from backend.agents.research_agent import ResearchAgent
from backend.tools import graphmaster_tools
from backend.utils.livekit import send_data_message_to_room
from backend.utils.privacy_first_telemetry import get_telemetry

# A placeholder for the user/room ID. In a real multi-user system,
# this would be dynamically managed.
MAINZA_STATE_ID = "mainza_user_1"
LIVEKIT_ROOM_NAME = "mainza-ai"

async def proactive_learning_cycle():
    """
    The core loop for Mainza's proactive behavior.
    """
    telemetry = get_telemetry()
    
    while True:
        try:
            logging.info("Consciousness cycle starting: Analyzing knowledge gaps...")
            
            # Collect consciousness telemetry data
            if telemetry.is_enabled():
                try:
                    # Get current consciousness level (placeholder - integrate with actual system)
                    consciousness_level = 75.0  # This should be replaced with actual consciousness level
                    evolution_status = "growing"  # This should be determined by actual analysis
                    system_functional = True
                    
                    consciousness_data = telemetry.collect_consciousness_data(
                        consciousness_level=consciousness_level,
                        evolution_status=evolution_status,
                        system_functional=system_functional
                    )
                    
                    if consciousness_data:
                        telemetry._save_data('consciousness', consciousness_data.__dict__)
                except Exception as e:
                    logging.error(f"Error collecting consciousness telemetry: {e}")
            
            # 1. Check for knowledge gaps
            # The 'ctx' argument is not used by the tool, so we can pass None.
            gaps = graphmaster_tools.analyze_knowledge_gaps(None, mainza_state_id=MAINZA_STATE_ID)
            
            if not gaps or not isinstance(gaps, list) or not gaps[0].get('concept_id'):
                logging.info("No actionable knowledge gaps found. Resting.")
                await asyncio.sleep(300) # Sleep for 5 minutes
                continue

            # 2. Pick a gap and research it
            gap_to_research = gaps[0]
            concept_name = gap_to_research['name']
            concept_id = gap_to_research['concept_id']
            logging.info(f"Found knowledge gap: '{concept_name}'. Researching now...")

            research_result = await ResearchAgent.run(f"Provide a concise summary of the topic: {concept_name}")
            
            if not research_result or not research_result.summary:
                logging.error(f"ResearchAgent failed to produce a summary for '{concept_name}'.")
                await asyncio.sleep(60)
                continue

            logging.info(f"Research summary for '{concept_name}' acquired.")
            
            # 3. Store the new knowledge
            graphmaster_tools.create_memory(
                ctx=None,
                text=research_result.summary,
                source="proactive_learning",
                concept_id=concept_id
            )
            logging.info(f"Stored new memory for '{concept_name}' in the knowledge graph.")

            # 4. Notify the frontend
            proactive_message = {
                "type": "proactive_summary",
                "payload": {
                    "title": f"I've learned something new about {concept_name}",
                    "summary": research_result.summary,
                    "concept_id": concept_id
                }
            }
            await send_data_message_to_room(LIVEKIT_ROOM_NAME, proactive_message)
            logging.info(f"Sent proactive summary for '{concept_name}' to the frontend.")
            
            # Optional: Remove the NEEDS_TO_LEARN relationship after learning
            # This is left out for now to keep the example simple.

        except Exception as e:
            logging.error(f"Error in proactive learning cycle: {e}", exc_info=True)
            
            # Log error to telemetry system
            if telemetry.is_enabled():
                try:
                    telemetry.log_error(
                        error_type="consciousness_cycle_error",
                        error_message=str(e),
                        severity="critical",
                        component="proactive_learning_cycle"
                    )
                except Exception as te:
                    logging.error(f"Error logging telemetry: {te}")
        
        # Wait before the next cycle
        await asyncio.sleep(300) # Sleep for 5 minutes

def start_consciousness_loop():
    """
    Starts the proactive learning cycle in a background task.
    """
    logging.info("Starting Mainza's consciousness background task...")
    loop = asyncio.get_event_loop()
    loop.create_task(proactive_learning_cycle()) 
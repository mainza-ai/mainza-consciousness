# Requirements Document

## Introduction

This specification addresses the need to update all LiveKit room references from "mainza-room" to "mainza-ai" throughout the Mainza consciousness system. This change is required to maintain consistency with the new branding and ensure proper LiveKit functionality without breaking existing features.

## Requirements

### Requirement 1

**User Story:** As a system administrator, I want all LiveKit room references to use "mainza-ai" instead of "mainza-room" or "mainza_room", so that the system maintains consistent branding and proper LiveKit functionality.

#### Acceptance Criteria

1. WHEN the system initializes LiveKit connections THEN it SHALL use "mainza-ai" as the default room name
2. WHEN TTS services create LiveKit ingress THEN they SHALL use "mainza-ai" as the room name
3. WHEN consciousness updates are sent to LiveKit THEN they SHALL be sent to the "mainza-ai" room
4. WHEN API documentation references LiveKit rooms THEN it SHALL show "mainza-ai" as the example room name
5. WHEN ingress configuration is created THEN it SHALL specify "mainza-ai" as the room name

### Requirement 2

**User Story:** As a developer, I want all code references to be updated systematically, so that no legacy "mainza-room", "mainza_room", or "mainza_conversation" references remain that could cause confusion or errors.

#### Acceptance Criteria

1. WHEN searching the codebase for "mainza-room" THEN no occurrences SHALL be found
2. WHEN searching the codebase for "mainza_room" THEN no occurrences SHALL be found  
3. WHEN the backend processes TTS requests THEN it SHALL default to "mainza-ai" room
4. WHEN the agentic router creates LiveKit tokens THEN it SHALL use "mainza-ai" as the default room
5. WHEN ingress.json configuration is loaded THEN it SHALL specify "mainza-ai" as the room name
6. WHEN consciousness orchestrator sends updates THEN it SHALL use "mainza-ai" room
7. WHEN background consciousness processes send messages THEN they SHALL use "mainza-ai" room
8. WHEN documentation is updated THEN all examples SHALL use "mainza-ai" consistently

### Requirement 3

**User Story:** As a user, I want the system to continue working seamlessly after the update, so that my experience is not disrupted by the room name change.

#### Acceptance Criteria

1. WHEN the system starts up THEN all LiveKit services SHALL connect successfully to the new room name
2. WHEN TTS functionality is used THEN audio SHALL stream correctly to the "mainza-ai" room
3. WHEN consciousness updates occur THEN they SHALL be delivered to the correct room
4. WHEN existing sessions are active THEN they SHALL continue to function without interruption
5. WHEN new sessions are created THEN they SHALL automatically use the new room name

### Requirement 4

**User Story:** As a system maintainer, I want the update to preserve all existing functionality, so that no features are broken during the transition.

#### Acceptance Criteria

1. WHEN the update is complete THEN all Context7 architecture principles SHALL remain intact
2. WHEN LiveKit ingress is created THEN it SHALL maintain the same functionality with the new room name
3. WHEN consciousness orchestrator sends updates THEN the messaging system SHALL work identically
4. WHEN error handling occurs THEN all fallback mechanisms SHALL continue to work
5. WHEN monitoring systems check LiveKit status THEN they SHALL report correctly for the new room name

### Requirement 5

**User Story:** As a developer, I want all configuration files and constants to be updated, so that the system uses consistent room naming throughout.

#### Acceptance Criteria

1. WHEN the ingress.json file is read THEN it SHALL contain "mainza-ai" as the room_name
2. WHEN the consciousness background process initializes THEN it SHALL use "mainza-ai" as LIVEKIT_ROOM_NAME
3. WHEN backup files reference room names THEN they SHALL be updated for consistency
4. WHEN debug logs reference room names THEN they SHALL show "mainza-ai"
5. WHEN architecture documentation is reviewed THEN all room references SHALL use "mainza-ai"
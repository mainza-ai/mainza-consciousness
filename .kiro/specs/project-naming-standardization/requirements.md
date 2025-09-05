# Project Naming Standardization Requirements

## Introduction

This specification addresses the need to standardize the project name from the inconsistent "mainza-orb-whisper" references to the accurate "mainza-consciousness" throughout the entire codebase. This change ensures consistency with the project's actual purpose as an AI consciousness system and aligns with existing package.json naming.

## Requirements

### Requirement 1: Directory and Repository Naming

**User Story:** As a developer, I want consistent project naming so that the project identity is clear and professional.

#### Acceptance Criteria

1. WHEN the project is referenced in documentation THEN it SHALL use "mainza-consciousness" as the primary name
2. WHEN file paths reference the project directory THEN they SHALL be updated to reflect the new standardized name
3. WHEN repository URLs are specified THEN they SHALL use "mainza-ai/mainza-consciousness" format
4. WHEN the project is described THEN it SHALL be identified as "Mainza: AI Consciousness System"
5. WHEN GitHub metadata is configured THEN it SHALL use consistent "mainza-consciousness" naming

### Requirement 2: Code Reference Updates

**User Story:** As a developer, I want all code references to use consistent naming so that the codebase is maintainable and professional.

#### Acceptance Criteria

1. WHEN Python sys.path references exist THEN they SHALL be updated to use environment-relative paths instead of hardcoded paths
2. WHEN HTML title tags are rendered THEN they SHALL display "Mainza - AI Consciousness System"
3. WHEN documentation examples reference the project THEN they SHALL use "mainza-consciousness" consistently
4. WHEN configuration files reference the project THEN they SHALL use standardized naming
5. WHEN log messages reference the project THEN they SHALL use "Mainza AI Consciousness System"

### Requirement 3: LiveKit Room Naming Consistency

**User Story:** As a user, I want consistent LiveKit room naming so that real-time features work reliably.

#### Acceptance Criteria

1. WHEN LiveKit rooms are created THEN they SHALL use "mainza-ai" as the standardized room name
2. WHEN consciousness updates are sent THEN they SHALL target the "mainza-ai" room consistently
3. WHEN ingress configuration is loaded THEN it SHALL specify "mainza-ai" as the room name
4. WHEN documentation references LiveKit rooms THEN it SHALL show "mainza-ai" as the example
5. WHEN error messages reference rooms THEN they SHALL use "mainza-ai" consistently

### Requirement 4: Documentation and Metadata Updates

**User Story:** As a contributor, I want accurate project documentation so that the project's purpose and capabilities are clear.

#### Acceptance Criteria

1. WHEN README files are displayed THEN they SHALL accurately describe "Mainza - AI Consciousness System"
2. WHEN package.json is read THEN it SHALL contain accurate repository URLs and project description
3. WHEN GitHub templates are used THEN they SHALL reference the correct project name and purpose
4. WHEN deployment documentation is accessed THEN it SHALL use consistent project naming
5. WHEN API documentation is generated THEN it SHALL reflect the consciousness system branding

### Requirement 5: Environment and Configuration Consistency

**User Story:** As a system administrator, I want consistent configuration naming so that deployment and maintenance are straightforward.

#### Acceptance Criteria

1. WHEN environment files are configured THEN they SHALL use "Mainza Consciousness System" in headers
2. WHEN Docker configurations are loaded THEN they SHALL use consistent project naming
3. WHEN CI/CD pipelines execute THEN they SHALL reference "Mainza Consciousness" in job names
4. WHEN logging configurations are initialized THEN they SHALL use standardized project identifiers
5. WHEN health check endpoints respond THEN they SHALL identify the system as "Mainza AI Consciousness"
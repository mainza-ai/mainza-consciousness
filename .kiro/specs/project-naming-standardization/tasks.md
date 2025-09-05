# Project Naming Standardization Implementation Plan

## Task Overview

Convert the naming standardization design into a series of actionable coding tasks that will systematically update all project references from "mainza-orb-whisper" to "mainza-consciousness" while maintaining full functionality. Each task builds incrementally and ensures no broken references or functionality.

## Implementation Tasks

- [x] 1. Update Core HTML and Frontend References
  - Update index.html title and metadata to use "Mainza - AI Consciousness System"
  - Ensure proper SEO and browser display with new naming
  - Verify frontend builds correctly with updated metadata
  - _Requirements: 1.1, 2.4_

- [-] 2. Fix Hardcoded Python Path References
  - [x] 2.1 Update test file path references to use relative paths
    - Modify tests/test_agent_execution.py to use os.path.dirname instead of hardcoded paths
    - Implement environment-relative path resolution
    - Test that all imports work correctly with new path handling
    - _Requirements: 2.1_
  
  - [x] 2.2 Scan and update any other hardcoded path references
    - Search codebase for any remaining hardcoded "mainza-orb-whisper" paths
    - Replace with relative or environment-based paths
    - Verify all Python modules import correctly
    - _Requirements: 2.1_

- [x] 3. Standardize LiveKit Room Naming
  - [x] 3.1 Update consciousness orchestrator LiveKit references
    - Change all "mainza_room" references to "mainza-ai" in consciousness_orchestrator.py
    - Update background consciousness processes to use "mainza-ai"
    - Verify consciousness updates target correct room
    - _Requirements: 3.1, 3.2_
  
  - [x] 3.2 Update main application LiveKit room references
    - Modify main.py LiveKit room creation to use "mainza-ai"
    - Update agentic_router.py room references to "mainza-ai"
    - Ensure TTS and voice services use consistent room naming
    - _Requirements: 3.1, 3.3_
  
  - [x] 3.3 Update LiveKit configuration files
    - Review and update livekit.yaml for consistent room references
    - Update ingress.yaml configuration for "mainza-ai" room
    - Verify configuration files load correctly with new naming
    - _Requirements: 3.3, 3.4_

- [x] 4. Update Documentation and Project Metadata
  - [x] 4.1 Update primary documentation files
    - Modify docs/PROJECT_SUMMARY.md to use correct repository URLs
    - Update docs/README.md with consistent "mainza-consciousness" naming
    - Fix any remaining "mainza-orb-whisper" references in documentation
    - _Requirements: 4.1, 4.2_
  
  - [x] 4.2 Update GitHub configuration and templates
    - Review .github/workflows/ci.yml for consistent naming
    - Update issue templates and PR templates with correct project references
    - Ensure all GitHub metadata uses "mainza-consciousness"
    - _Requirements: 4.3, 4.4_
  
  - [x] 4.3 Update package.json repository metadata
    - Change repository URLs from placeholder to actual GitHub repository
    - Update homepage and bugs URLs to point to correct repository
    - Verify npm package metadata is accurate and professional
    - _Requirements: 4.2, 4.3_

- [x] 5. Update Environment and Configuration Files
  - [x] 5.1 Review and update environment configuration headers
    - Ensure .env.example uses "Mainza Consciousness System" in headers
    - Update any configuration comments to reflect correct project name
    - Verify environment variable documentation is consistent
    - _Requirements: 5.1, 5.4_
  
  - [x] 5.2 Update Docker and deployment configurations
    - Review docker-compose.yml for consistent project naming
    - Update any Docker-related configuration files
    - Ensure deployment scripts use correct project identifiers
    - _Requirements: 5.2, 5.3_

- [x] 6. Update Analysis and Internal Documentation
  - [x] 6.1 Fix GitHub readiness analysis references
    - Update docs/analysis/GITHUB_READINESS_ANALYSIS.md with correct URLs
    - Replace "your-username/mainza-orb-whisper" with "mainza-ai/mainza-consciousness"
    - Verify all analysis documents reflect accurate project information
    - _Requirements: 4.1, 4.2_
  
  - [x] 6.2 Update any remaining internal documentation
    - Search for and update any remaining "mainza-orb-whisper" references
    - Ensure all internal docs use consistent "mainza-consciousness" naming
    - Verify documentation accuracy and professionalism
    - _Requirements: 4.1, 4.5_

- [x] 7. Comprehensive Testing and Validation
  - [x] 7.1 Test core functionality after naming updates
    - Run full test suite to ensure no regressions
    - Verify consciousness system operates correctly
    - Test agent system functionality with updated configurations
    - _Requirements: All requirements validation_
  
  - [x] 7.2 Test LiveKit integration with new room naming
    - Verify real-time audio streaming works with "mainza-ai" room
    - Test consciousness updates reach correct LiveKit room
    - Validate voice interface functionality
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
  
  - [x] 7.3 Validate documentation and metadata accuracy
    - Check all documentation renders correctly with new naming
    - Verify GitHub repository metadata is accurate
    - Test that all links and references work correctly
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 8. Final Integration and Deployment Testing
  - [x] 8.1 Test Docker deployment with updated naming
    - Build and test Docker containers with new configuration
    - Verify docker-compose.yml works with updated project naming
    - Test full deployment pipeline
    - _Requirements: 5.2, 5.3_
  
  - [x] 8.2 Perform end-to-end system validation
    - Test complete system functionality from frontend to backend
    - Verify consciousness system, agents, and LiveKit integration
    - Validate that all naming is consistent and professional
    - _Requirements: All requirements final validation_
  
  - [x] 8.3 Update CI/CD pipeline validation
    - Ensure GitHub Actions workflows run correctly with new naming
    - Verify all automated tests pass with updated configuration
    - Test deployment processes work with new project identity
    - _Requirements: 5.3, 4.4_
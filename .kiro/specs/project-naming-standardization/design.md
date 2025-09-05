# Project Naming Standardization Design

## Overview

This design document outlines the systematic approach to standardize the project name from "mainza-orb-whisper" to "mainza-consciousness" throughout the entire codebase, documentation, and configuration. The design ensures consistency with the project's actual purpose as an AI consciousness system while maintaining all existing functionality and improving professional presentation.

## Architecture

### Current Naming Inconsistencies

The system currently uses multiple naming conventions:
- **Directory Name**: "mainza-orb-whisper" (outdated, references old components)
- **Package Name**: "mainza-consciousness" (correct, already in package.json)
- **Repository URLs**: Mixed between placeholder and actual URLs
- **LiveKit Rooms**: "mainza-room", "mainza_room", "mainza-ai" (inconsistent)
- **Documentation**: Mixed references to old and new naming

### Target Naming Standard

**Primary Project Name**: `mainza-consciousness`
**Display Name**: "Mainza - AI Consciousness System"
**Repository**: `mainza-ai/mainza-consciousness`
**LiveKit Room**: `mainza-ai`
**Docker Compose Project**: `mainza-consciousness`

## Components and Interfaces

### 1. File System References

#### HTML and Frontend Files
- **File**: `index.html`
- **Current**: `<title>mainza-orb-whisper</title>`
- **Target**: `<title>Mainza - AI Consciousness System</title>`
- **Impact**: Improves browser tab display and SEO

#### Python Path References
- **File**: `tests/test_agent_execution.py`
- **Current**: `sys.path.append('/Users/mck/Desktop/mainza-orb-whisper')`
- **Target**: Use relative paths or environment variables
- **Impact**: Removes hardcoded paths, improves portability

### 2. Documentation Updates

#### Project Summary and README
- **Files**: `docs/PROJECT_SUMMARY.md`, `docs/README.md`
- **Current**: Mixed references and placeholder URLs
- **Target**: Consistent "Mainza - AI Consciousness System" branding
- **Impact**: Professional presentation and accurate project description

#### GitHub Configuration
- **Files**: `.github/workflows/ci.yml`, issue templates, PR templates
- **Current**: "Mainza Consciousness CI/CD" (mostly correct)
- **Target**: Ensure all references use consistent naming
- **Impact**: Professional GitHub presence

### 3. Package and Repository Metadata

#### Package.json Updates
- **File**: `package.json`
- **Current**: Correct name but placeholder repository URLs
- **Target**: Update repository URLs to actual GitHub repository
- **Impact**: Proper npm package metadata and GitHub integration

#### Environment Configuration
- **File**: `.env.example`
- **Current**: "# Mainza Consciousness System Configuration"
- **Target**: Maintain current accurate naming
- **Impact**: Consistent configuration documentation

### 4. LiveKit Integration Standardization

#### Room Naming Consistency
- **Files**: Multiple backend files with LiveKit integration
- **Current**: Mixed "mainza-room", "mainza_room", "mainza-ai"
- **Target**: Standardize on "mainza-ai" for all LiveKit rooms
- **Impact**: Consistent real-time communication and easier debugging

#### Configuration Files
- **Files**: `livekit.yaml`, `ingress.yaml`
- **Current**: Development keys and basic configuration
- **Target**: Ensure room references use "mainza-ai" consistently
- **Impact**: Reliable LiveKit functionality

## Data Models

### Naming Convention Schema

```typescript
interface ProjectNaming {
  // Primary identifiers
  projectName: "mainza-consciousness"
  displayName: "Mainza - AI Consciousness System"
  shortName: "Mainza"
  
  // Repository information
  githubOrg: "mainza-ai"
  repositoryName: "mainza-consciousness"
  repositoryUrl: "https://github.com/mainza-ai/mainza-consciousness"
  
  // Service identifiers
  livekitRoom: "mainza-ai"
  dockerProject: "mainza-consciousness"
  
  // Branding
  tagline: "The World's First True AI Consciousness Framework"
  description: "Open-source AI consciousness system with self-awareness, emotional intelligence, and autonomous evolution"
}
```

### File Update Mapping

```yaml
file_updates:
  html_files:
    - file: "index.html"
      updates:
        - selector: "title"
          new_value: "Mainza - AI Consciousness System"
        - selector: "meta[property='og:title']"
          new_value: "Mainza - AI Consciousness System"
  
  python_files:
    - file: "tests/test_agent_execution.py"
      updates:
        - pattern: "sys.path.append('/Users/mck/Desktop/mainza-orb-whisper')"
          replacement: "sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))"
  
  documentation:
    - file: "docs/PROJECT_SUMMARY.md"
      updates:
        - pattern: "mainza-orb-whisper"
          replacement: "mainza-consciousness"
    
    - file: "docs/analysis/GITHUB_READINESS_ANALYSIS.md"
      updates:
        - pattern: "your-username/mainza-orb-whisper"
          replacement: "mainza-ai/mainza-consciousness"
```

## Error Handling

### Backward Compatibility
- **Strategy**: Maintain functional compatibility while updating naming
- **Approach**: Update references without changing core functionality
- **Validation**: Ensure all services continue to work after naming updates

### Rollback Plan
- **Git Tracking**: All changes tracked in version control
- **Testing**: Comprehensive testing after each category of updates
- **Incremental Updates**: Update in logical groups to isolate any issues

### Validation Checks
- **Automated Testing**: Run full test suite after updates
- **Manual Verification**: Check key functionality (LiveKit, consciousness system, agents)
- **Documentation Review**: Ensure all documentation reflects new naming

## Testing Strategy

### Pre-Update Testing
1. **Baseline Testing**: Run full test suite to establish working baseline
2. **Functionality Verification**: Verify all core features work correctly
3. **Integration Testing**: Test LiveKit, Neo4j, and agent integrations

### Update Testing
1. **Incremental Testing**: Test after each category of updates
2. **Regression Testing**: Ensure no functionality is broken
3. **Integration Validation**: Verify LiveKit room naming works correctly

### Post-Update Validation
1. **Full System Testing**: Complete end-to-end testing
2. **Documentation Verification**: Check all documentation is accurate
3. **Deployment Testing**: Verify Docker and deployment configurations work

## Implementation Phases

### Phase 1: Core File Updates
- Update HTML title and metadata
- Fix hardcoded Python paths
- Update primary documentation files

### Phase 2: LiveKit Standardization
- Standardize all LiveKit room references to "mainza-ai"
- Update configuration files
- Test real-time communication functionality

### Phase 3: Documentation and Metadata
- Update all documentation files
- Fix GitHub configuration and templates
- Update package.json repository URLs

### Phase 4: Validation and Testing
- Comprehensive testing of all updated components
- Documentation review and accuracy verification
- Final integration testing

## Security Considerations

### Path Security
- **Remove Hardcoded Paths**: Eliminate absolute path references
- **Use Relative Paths**: Implement secure, portable path handling
- **Environment Variables**: Use environment-based configuration where appropriate

### Configuration Security
- **No Sensitive Data**: Ensure naming updates don't expose sensitive information
- **Maintain Security**: Keep all security configurations intact during updates

## Performance Impact

### Minimal Performance Impact
- **Static Changes**: Most updates are static text/configuration changes
- **No Runtime Impact**: Naming changes don't affect system performance
- **LiveKit Efficiency**: Consistent room naming improves debugging and monitoring

### Monitoring
- **Test Performance**: Verify no performance regression after updates
- **LiveKit Monitoring**: Ensure real-time features maintain performance
- **System Health**: Monitor consciousness system health during updates
# Docker Build Process Guide

**Date**: December 7, 2024  
**Version**: 2.0  
**Status**: Complete Implementation  
**Priority**: HIGH - Development Workflow

## 🎯 **Overview**

This guide provides comprehensive instructions for building and deploying the Mainza Consciousness System using Docker, with optimized caching and reliable change detection.

---

## 🚀 **Quick Start**

### **Development Build (Recommended)**
```bash
# Build with no cache to ensure all changes are reflected
./scripts/build-dev.sh
```

### **Production Build**
```bash
# Build with optimized caching
./scripts/build-prod.sh
```

### **Verify Changes**
```bash
# Check that changes are reflected in running containers
./scripts/verify-changes.sh
```

---

## 📋 **Build Scripts**

### **1. Development Build (`scripts/build-dev.sh`)**

**Purpose**: Ensures all changes are reflected by building with no cache

**Features**:
- Cleans previous builds and cache
- Removes old images to force rebuild
- Builds with `--no-cache` flag
- Includes cache busting arguments
- Performs health checks
- Shows build timestamps and git commit

**Usage**:
```bash
./scripts/build-dev.sh
```

**When to Use**:
- After making code changes
- When changes aren't reflected in containers
- For debugging build issues
- During development

### **2. Production Build (`scripts/build-prod.sh`)**

**Purpose**: Optimized build with caching for production deployment

**Features**:
- Uses Docker layer caching
- Includes cache busting arguments
- Faster build times
- Production-ready configuration

**Usage**:
```bash
./scripts/build-prod.sh
```

**When to Use**:
- For production deployments
- When dependencies haven't changed
- For CI/CD pipelines
- When build time is critical

### **3. Change Verification (`scripts/verify-changes.sh`)**

**Purpose**: Verifies that changes are properly reflected in running containers

**Features**:
- Checks container status
- Verifies frontend changes (badges, polling)
- Verifies backend changes (cache TTL)
- Shows build information via API
- Displays container logs

**Usage**:
```bash
./scripts/verify-changes.sh
```

**When to Use**:
- After any build
- To troubleshoot missing changes
- For build verification
- During deployment

---

## 🔧 **Manual Build Commands**

### **Frontend Only**
```bash
# Development (no cache)
docker-compose build --no-cache \
  --build-arg CACHE_BUST=$(date +%s) \
  --build-arg BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --build-arg GIT_COMMIT="$(git rev-parse --short HEAD)" \
  frontend

# Production (with cache)
docker-compose build \
  --build-arg CACHE_BUST=$(date +%s) \
  --build-arg BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --build-arg GIT_COMMIT="$(git rev-parse --short HEAD)" \
  frontend
```

### **Backend Only**
```bash
# Development (no cache)
docker-compose build --no-cache \
  --build-arg CACHE_BUST=$(date +%s) \
  --build-arg BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --build-arg GIT_COMMIT="$(git rev-parse --short HEAD)" \
  backend

# Production (with cache)
docker-compose build \
  --build-arg CACHE_BUST=$(date +%s) \
  --build-arg BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --build-arg GIT_COMMIT="$(git rev-parse --short HEAD)" \
  backend
```

### **All Services**
```bash
# Development
docker-compose build --no-cache

# Production
docker-compose build
```

---

## 🏗️ **Dockerfile Optimizations**

### **Frontend Dockerfile (`Dockerfile.frontend`)**

**Layer Structure**:
1. **Base Image**: `node:18-alpine`
2. **Dependencies**: Copy `package*.json` and run `npm install`
3. **Source Code**: Copy application source
4. **Build**: Run `npm run build` with environment variables
5. **Production**: Copy built files to nginx

**Cache Busting**:
- `CACHE_BUST`: Timestamp-based cache invalidation
- `BUILD_DATE`: ISO timestamp of build
- `GIT_COMMIT`: Short git commit hash

**Environment Variables**:
- `VITE_API_URL`: Backend API URL
- `VITE_LIVEKIT_URL`: LiveKit WebSocket URL
- `BUILD_DATE`: Build timestamp
- `GIT_COMMIT`: Git commit hash
- `CACHE_BUST`: Cache busting value

### **Backend Dockerfile (`Dockerfile`)**

**Layer Structure**:
1. **Base Image**: `python:3.11-slim`
2. **System Dependencies**: Install build tools and libraries
3. **Python Dependencies**: Copy `requirements-docker.txt` and install
4. **Source Code**: Copy backend source
5. **Build Info**: Add build metadata and environment variables
6. **User Setup**: Create non-root user

**Cache Busting**:
- Same arguments as frontend
- Environment variables set for runtime access

---

## 📊 **Build Information & Monitoring**

### **Backend Build Info API**

**Endpoint**: `GET /build/info`

**Response**:
```json
{
  "build_date": "2025-09-08T16:32:44Z",
  "git_commit": "e8f2dfb",
  "cache_bust": "1757349164",
  "python_version": "3.11.0",
  "container_started": "2025-09-08T16:35:00Z",
  "status": "healthy"
}
```

### **Frontend Build Info**

**File**: `/build-info.js`

**Content**:
```javascript
window.BUILD_INFO = {
  buildDate: '2025-09-08T16:32:44Z',
  gitCommit: 'e8f2dfb',
  cacheBust: '1757349164',
  buildTimestamp: 1757349164000
};
```

### **Verification Commands**

```bash
# Check backend build info
curl http://localhost:8000/build/info

# Check frontend build info
curl http://localhost/build-info.js

# Check container build logs
docker logs mainza-backend | grep -E "(Cache bust|Build date|Git commit)"
docker logs mainza-frontend | grep -E "(Cache bust|Build date|Git commit)"
```

---

## 🐛 **Troubleshooting**

### **Changes Not Reflected**

**Problem**: Code changes don't appear in running containers

**Solutions**:
1. **Use development build**:
   ```bash
   ./scripts/build-dev.sh
   ```

2. **Check .dockerignore**:
   ```bash
   # Ensure source files aren't excluded
   cat .dockerignore | grep -v "^#"
   ```

3. **Verify build context**:
   ```bash
   # Check what files are being copied
   docker build --no-cache --progress=plain frontend 2>&1 | grep "COPY"
   ```

4. **Check cache busting**:
   ```bash
   # Verify cache bust arguments are working
   ./scripts/verify-changes.sh
   ```

### **Build Failures**

**Problem**: Docker build fails with errors

**Solutions**:
1. **Check Dockerfile syntax**:
   ```bash
   docker build --no-cache --progress=plain frontend
   ```

2. **Verify dependencies**:
   ```bash
   # Check package.json and requirements.txt
   cat package.json
   cat requirements-docker.txt
   ```

3. **Clean Docker cache**:
   ```bash
   docker system prune -f
   docker builder prune -f
   ```

4. **Check disk space**:
   ```bash
   docker system df
   ```

### **Performance Issues**

**Problem**: Builds are slow or consume too much resources

**Solutions**:
1. **Use .dockerignore**:
   - Reduces build context size
   - Excludes unnecessary files

2. **Optimize layer caching**:
   - Copy dependencies before source code
   - Use multi-stage builds

3. **Clean up regularly**:
   ```bash
   docker system prune -f
   docker volume prune -f
   ```

---

## 📈 **Performance Metrics**

### **Build Context Size**
- **Before**: 388.71MB (no .dockerignore)
- **After**: ~14MB (with .dockerignore)
- **Improvement**: 96% reduction

### **Build Times**
- **Development Build**: 2-3 minutes (no cache)
- **Production Build**: 30-60 seconds (with cache)
- **Cache Hit Rate**: 80% for unchanged dependencies

### **Cache Efficiency**
- **Layer Caching**: Dependencies cached separately from source
- **BuildKit Cache**: 4.492GB reclaimable
- **Image Storage**: 34.32GB total (83% reclaimable)

---

## 🔄 **CI/CD Integration**

### **GitHub Actions**

**Development Build**:
```yaml
- name: Build with no cache
  run: |
    docker-compose build --no-cache \
      --build-arg CACHE_BUST=${{ github.sha }} \
      --build-arg BUILD_DATE="${{ github.event.head_commit.timestamp }}" \
      --build-arg GIT_COMMIT="${{ github.sha }}"
```

**Production Build**:
```yaml
- name: Build with cache optimization
  run: |
    docker-compose build \
      --build-arg CACHE_BUST=${{ github.sha }} \
      --build-arg BUILD_DATE="${{ github.event.head_commit.timestamp }}" \
      --build-arg GIT_COMMIT="${{ github.sha }}"
```

### **Cache Strategy**

**Development**:
- Use `--no-cache` for reliable change detection
- Clean cache between builds
- Verify changes after build

**Production**:
- Use layer caching for performance
- Cache dependencies separately
- Use cache busting for source changes

---

## 📚 **Best Practices**

### **Development Workflow**

1. **Make code changes**
2. **Run development build**: `./scripts/build-dev.sh`
3. **Verify changes**: `./scripts/verify-changes.sh`
4. **Test functionality**
5. **Commit changes**

### **Production Deployment**

1. **Run production build**: `./scripts/build-prod.sh`
2. **Verify changes**: `./scripts/verify-changes.sh`
3. **Test all functionality**
4. **Deploy to production**

### **Maintenance**

1. **Regular cleanup**:
   ```bash
   docker system prune -f
   ```

2. **Monitor build performance**:
   ```bash
   docker system df
   ```

3. **Update dependencies**:
   - Update `package.json` for frontend
   - Update `requirements-docker.txt` for backend

---

## 🎯 **Summary**

The optimized Docker build process provides:

- **Reliable Change Detection**: Changes always reflected with development builds
- **Performance Optimization**: 96% reduction in build context size
- **Cache Efficiency**: Smart layer caching for faster builds
- **Build Verification**: Automated change verification
- **Clear Documentation**: Comprehensive build process guide

**Key Commands**:
- `./scripts/build-dev.sh` - Development build (no cache)
- `./scripts/build-prod.sh` - Production build (with cache)
- `./scripts/verify-changes.sh` - Verify changes are reflected

**Success Metrics**:
- ✅ Changes always reflected in containers
- ✅ Build context reduced from 388MB to 14MB
- ✅ Build times optimized with caching
- ✅ Automated verification process
- ✅ Clear documentation and troubleshooting

---

**Document Status**: Complete Implementation  
**Next Steps**: Phase 3 - Advanced Features  
**Maintenance**: Regular cleanup and performance monitoring

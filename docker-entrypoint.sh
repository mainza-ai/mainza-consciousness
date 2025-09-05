#!/bin/sh
# Mainza Frontend Docker Entrypoint Script

set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting Mainza Frontend..."

# Environment variable substitution in built files (if needed)
if [ -n "$VITE_API_URL" ]; then
    log "Configuring API URL: $VITE_API_URL"
    # Replace placeholder in built files if needed
    find /usr/share/nginx/html -name "*.js" -exec sed -i "s|__VITE_API_URL__|$VITE_API_URL|g" {} \;
fi

if [ -n "$VITE_LIVEKIT_URL" ]; then
    log "Configuring LiveKit URL: $VITE_LIVEKIT_URL"
    # Replace placeholder in built files if needed
    find /usr/share/nginx/html -name "*.js" -exec sed -i "s|__VITE_LIVEKIT_URL__|$VITE_LIVEKIT_URL|g" {} \;
fi

# Validate nginx configuration
log "Validating nginx configuration..."
nginx -t

log "Mainza Frontend ready to serve consciousness interface!"

# Execute the main command
exec "$@"
# Multi-stage build for environment variable support
FROM nginx:alpine

# Install envsubst for environment variable substitution
RUN apk add --no-cache gettext

# Copy static files
COPY frontend-simple/ /usr/share/nginx/html/

# Copy custom nginx config  
COPY frontend-simple/nginx.conf /etc/nginx/nginx.conf

# Create startup script that substitutes environment variables
RUN cat > /docker-entrypoint.d/30-substitute-env.sh << 'EOF'
#!/bin/sh
set -e

# Set default API_BASE_URL if not provided
export API_BASE_URL="${API_BASE_URL:-https://instagram-api.teabag.online/api/v1}"

# Substitute environment variables in app.js
envsubst '${API_BASE_URL}' < /usr/share/nginx/html/app.js.template > /usr/share/nginx/html/app.js

echo "Environment variables substituted. API_BASE_URL: $API_BASE_URL"
EOF

# Make the script executable
RUN chmod +x /docker-entrypoint.d/30-substitute-env.sh

# Rename app.js to app.js.template for substitution
RUN mv /usr/share/nginx/html/app.js /usr/share/nginx/html/app.js.template

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
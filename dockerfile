# OWASP Juice Shop Docker Image
# Using official Juice Shop image for security pipeline validation
# Repository: https://github.com/juice-shop/juice-shop

FROM bkimminich/juice-shop:latest

# Expose Juice Shop port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production \
    LOG_LEVEL=error \
    PORT=3000

# Use node user (non-root) - already configured in base image
USER node

# Working directory
WORKDIR /juice-shop

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})" || exit 1

# Start Juice Shop
CMD ["npm", "start"]

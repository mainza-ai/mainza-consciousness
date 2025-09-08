// Frontend Build Information
// This file contains build metadata that gets embedded in the frontend

const buildInfo = {
  buildDate: process.env.BUILD_DATE || new Date().toISOString(),
  gitCommit: process.env.GIT_COMMIT || 'unknown',
  cacheBust: process.env.CACHE_BUST || Date.now().toString(),
  buildTimestamp: Date.now(),
  version: '2.1.0'
};

// Make it available globally
if (typeof window !== 'undefined') {
  window.BUILD_INFO = buildInfo;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = buildInfo;
}

console.log('Build Info:', buildInfo);

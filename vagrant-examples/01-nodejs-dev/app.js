const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

// 미들웨어
app.use(express.json());

// 라우트
app.get('/', (req, res) => {
  res.json({
    message: 'Hello from Vagrant Node.js!',
    environment: process.env.NODE_ENV || 'development',
    nodeVersion: process.version,
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime()
  });
});

// 서버 시작
app.listen(port, '0.0.0.0', () => {
  console.log(`========================================`);
  console.log(`Server running on port ${port}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`Node version: ${process.version}`);
  console.log(`========================================`);
  console.log(`Access: http://localhost:${port}`);
  console.log(`Health: http://localhost:${port}/health`);
  console.log(`========================================`);
});

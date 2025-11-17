#!/bin/bash

# Node.js 설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# 서비스 디렉토리 생성
mkdir -p /opt/user-service
cd /opt/user-service

# package.json 생성
cat > package.json << 'EOF'
{
  "name": "user-service",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.0"
  }
}
EOF

# 서비스 코드 생성
cat > index.js << 'EOF'
const express = require('express');
const app = express();
app.use(express.json());

const users = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
];

app.get('/', (req, res) => {
  res.json({ service: 'user-service', users });
});

app.get('/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  res.json(user || { error: 'User not found' });
});

app.listen(3000, '0.0.0.0', () => {
  console.log('User service running on port 3000');
});
EOF

# 의존성 설치
npm install

# systemd 서비스 생성
cat > /etc/systemd/system/user-service.service << 'EOF'
[Unit]
Description=User Microservice
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/user-service
ExecStart=/usr/bin/node index.js
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start user-service
systemctl enable user-service

echo "User service started on port 3000"

#!/bin/bash

# Node.js 설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# 서비스 디렉토리 생성
mkdir -p /opt/order-service
cd /opt/order-service

# package.json 생성
cat > package.json << 'EOF'
{
  "name": "order-service",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "express": "^4.18.2"
  }
}
EOF

# 서비스 코드 생성
cat > index.js << 'EOF'
const express = require('express');
const app = express();
app.use(express.json());

const orders = [
  { id: 1, userId: 1, productId: 1, quantity: 1, status: 'completed' },
  { id: 2, userId: 2, productId: 2, quantity: 2, status: 'pending' }
];

app.get('/', (req, res) => {
  res.json({ service: 'order-service', orders });
});

app.get('/:id', (req, res) => {
  const order = orders.find(o => o.id === parseInt(req.params.id));
  res.json(order || { error: 'Order not found' });
});

app.post('/', (req, res) => {
  const newOrder = {
    id: orders.length + 1,
    ...req.body,
    status: 'pending'
  };
  orders.push(newOrder);
  res.status(201).json(newOrder);
});

app.listen(3000, '0.0.0.0', () => {
  console.log('Order service running on port 3000');
});
EOF

# 의존성 설치
npm install

# systemd 서비스 생성
cat > /etc/systemd/system/order-service.service << 'EOF'
[Unit]
Description=Order Microservice
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/order-service
ExecStart=/usr/bin/node index.js
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start order-service
systemctl enable order-service

echo "Order service started on port 3000"

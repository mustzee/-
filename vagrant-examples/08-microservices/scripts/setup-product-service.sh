#!/bin/bash

# Node.js 설치
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# 서비스 디렉토리 생성
mkdir -p /opt/product-service
cd /opt/product-service

# package.json 생성
cat > package.json << 'EOF'
{
  "name": "product-service",
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

const products = [
  { id: 1, name: 'Laptop', price: 999.99, stock: 10 },
  { id: 2, name: 'Mouse', price: 29.99, stock: 50 },
  { id: 3, name: 'Keyboard', price: 79.99, stock: 30 }
];

app.get('/', (req, res) => {
  res.json({ service: 'product-service', products });
});

app.get('/:id', (req, res) => {
  const product = products.find(p => p.id === parseInt(req.params.id));
  res.json(product || { error: 'Product not found' });
});

app.listen(3000, '0.0.0.0', () => {
  console.log('Product service running on port 3000');
});
EOF

# 의존성 설치
npm install

# systemd 서비스 생성
cat > /etc/systemd/system/product-service.service << 'EOF'
[Unit]
Description=Product Microservice
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/product-service
ExecStart=/usr/bin/node index.js
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start product-service
systemctl enable product-service

echo "Product service started on port 3000"

#!/bin/bash

apt-get update
apt-get install -y nginx

cat > /etc/nginx/nginx.conf << 'EOF'
user www-data;
worker_processes auto;

events {
    worker_connections 768;
}

http {
    upstream user_service {
        server 192.168.60.21:3000;
    }

    upstream product_service {
        server 192.168.60.22:3000;
    }

    upstream order_service {
        server 192.168.60.23:3000;
    }

    server {
        listen 80;

        location /api/users {
            proxy_pass http://user_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/products {
            proxy_pass http://product_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/orders {
            proxy_pass http://order_service/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location / {
            return 200 '{"message": "API Gateway", "services": ["/api/users", "/api/products", "/api/orders"]}\n';
            add_header Content-Type application/json;
        }
    }
}
EOF

systemctl restart nginx
echo "API Gateway configured on port 80"

# 마이크로서비스 아키텍처

실제 마이크로서비스 아키텍처를 시뮬레이션하는 멀티 VM 환경입니다.

## 아키텍처 다이어그램

```
                        ┌────────────────┐
                        │  API Gateway   │
                        │ (192.168.60.10)│
                        │     Nginx      │
                        └────────┬───────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
          ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
          │User Service │ │Product Svc  │ │Order Service│
          │(192.168.60.21)│(192.168.60.22)│(192.168.60.23)│
          │  Node.js    │ │  Node.js    │ │  Node.js    │
          └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
                 │               │               │
                 └───────────────┼───────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
          ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
          │  Database   │ │    Cache    │ │    Queue    │
          │(192.168.60.30)│(192.168.60.40)│(192.168.60.50)│
          │ PostgreSQL  │ │    Redis    │ │  RabbitMQ   │
          └─────────────┘ └─────────────┘ └─────────────┘
```

## 서비스 구성

| 서비스 | 역할 | IP 주소 | 포트 | 기술 스택 |
|--------|------|---------|------|-----------|
| API Gateway | 라우팅, 인증 | 192.168.60.10 | 80 | Nginx |
| User Service | 사용자 관리 | 192.168.60.21 | 3000 | Node.js |
| Product Service | 상품 관리 | 192.168.60.22 | 3000 | Node.js |
| Order Service | 주문 관리 | 192.168.60.23 | 3000 | Node.js |
| Database | 데이터 저장 | 192.168.60.30 | 5432 | PostgreSQL |
| Cache | 캐싱 | 192.168.60.40 | 6379 | Redis |
| Message Queue | 비동기 메시징 | 192.168.60.50 | 5672 | RabbitMQ |

## 사용 방법

### 1. 전체 인프라 시작

```bash
# 모든 서비스 시작
vagrant up

# 또는 순차적으로
vagrant up database cache queue
vagrant up user-service product-service order-service
vagrant up gateway
```

### 2. API 테스트

#### Gateway 접속
```bash
# 서비스 목록
curl http://localhost:8080/

# 응답:
# {"message": "API Gateway", "services": ["/api/users", "/api/products", "/api/orders"]}
```

#### User Service
```bash
# 모든 사용자 조회
curl http://localhost:8080/api/users

# 특정 사용자 조회
curl http://localhost:8080/api/users/1
```

#### Product Service
```bash
# 모든 상품 조회
curl http://localhost:8080/api/products

# 특정 상품 조회
curl http://localhost:8080/api/products/1
```

#### Order Service
```bash
# 모든 주문 조회
curl http://localhost:8080/api/orders

# 특정 주문 조회
curl http://localhost:8080/api/orders/1

# 새 주문 생성
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "productId": 2, "quantity": 3}'
```

## 서비스 접속

### SSH 접속
```bash
# API Gateway
vagrant ssh gateway

# 각 마이크로서비스
vagrant ssh user-service
vagrant ssh product-service
vagrant ssh order-service

# 인프라
vagrant ssh database
vagrant ssh cache
vagrant ssh queue
```

### 서비스 로그 확인

```bash
# User Service 로그
vagrant ssh user-service
sudo journalctl -u user-service -f

# Product Service 로그
vagrant ssh product-service
sudo journalctl -u product-service -f

# Order Service 로그
vagrant ssh order-service
sudo journalctl -u order-service -f
```

## 데이터베이스 접속

### PostgreSQL
```bash
vagrant ssh database

# 각 서비스별 데이터베이스
psql -U microuser -d userdb
psql -U microuser -d productdb
psql -U microuser -d orderdb
# 비밀번호: micro123
```

## Redis 사용

```bash
vagrant ssh cache

# Redis CLI
redis-cli

# 테스트 명령어
127.0.0.1:6379> SET user:1 "John Doe"
127.0.0.1:6379> GET user:1
127.0.0.1:6379> KEYS *
```

## RabbitMQ 관리

### 웹 관리 콘솔
```bash
# URL: http://192.168.60.50:15672
# Username: admin
# Password: admin123
```

### CLI 사용
```bash
vagrant ssh queue

# 큐 목록
rabbitmqctl list_queues

# Exchange 목록
rabbitmqctl list_exchanges

# 연결 확인
rabbitmqctl list_connections
```

## 서비스 확장

### 새 마이크로서비스 추가

1. Vagrantfile에 새 서비스 정의 추가
2. 서비스 셋업 스크립트 생성
3. API Gateway 라우팅 설정 업데이트

예시: Payment Service 추가

```ruby
config.vm.define "payment-service" do |svc|
  svc.vm.hostname = "payment-service"
  svc.vm.network "private_network", ip: "192.168.60.24"
  svc.vm.provision "shell", path: "scripts/setup-payment-service.sh"
end
```

Gateway 설정 업데이트:
```nginx
upstream payment_service {
    server 192.168.60.24:3000;
}

location /api/payments {
    proxy_pass http://payment_service/;
}
```

## 서비스 간 통신 패턴

### 1. 동기 통신 (HTTP)

User Service에서 Product Service 호출:

```javascript
const http = require('http');

function getProduct(productId) {
  return new Promise((resolve, reject) => {
    http.get(`http://192.168.60.22:3000/${productId}`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}
```

### 2. 비동기 통신 (Message Queue)

```javascript
const amqp = require('amqplib');

// Producer (주문 생성 시)
async function publishOrder(order) {
  const connection = await amqp.connect('amqp://192.168.60.50');
  const channel = await connection.createChannel();
  await channel.assertQueue('orders');
  channel.sendToQueue('orders', Buffer.from(JSON.stringify(order)));
  await channel.close();
  await connection.close();
}

// Consumer (주문 처리)
async function consumeOrders() {
  const connection = await amqp.connect('amqp://192.168.60.50');
  const channel = await connection.createChannel();
  await channel.assertQueue('orders');
  channel.consume('orders', (msg) => {
    const order = JSON.parse(msg.content.toString());
    console.log('Processing order:', order);
    channel.ack(msg);
  });
}
```

### 3. 캐싱 (Redis)

```javascript
const redis = require('redis');
const client = redis.createClient({
  host: '192.168.60.40',
  port: 6379
});

// 캐시 읽기
async function getFromCache(key) {
  return new Promise((resolve, reject) => {
    client.get(key, (err, data) => {
      if (err) reject(err);
      resolve(data ? JSON.parse(data) : null);
    });
  });
}

// 캐시 쓰기
async function setCache(key, value, ttl = 3600) {
  client.setex(key, ttl, JSON.stringify(value));
}
```

## 모니터링 및 헬스 체크

### 서비스 헬스 체크

각 서비스에 `/health` 엔드포인트 추가:

```javascript
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'user-service',
    timestamp: new Date().toISOString()
  });
});
```

### 모니터링 스크립트

```bash
#!/bin/bash
# check-services.sh

services=(
  "user-service:192.168.60.21:3000"
  "product-service:192.168.60.22:3000"
  "order-service:192.168.60.23:3000"
)

for service in "${services[@]}"; do
  IFS=':' read -r name ip port <<< "$service"
  if curl -sf "http://$ip:$port/health" > /dev/null; then
    echo "✓ $name is healthy"
  else
    echo "✗ $name is down"
  fi
done
```

## 로드 테스트

### Apache Bench 사용

```bash
# 설치
sudo apt-get install apache2-utils

# 로드 테스트 (1000 요청, 동시 10개)
ab -n 1000 -c 10 http://localhost:8080/api/users
ab -n 1000 -c 10 http://localhost:8080/api/products
ab -n 1000 -c 10 http://localhost:8080/api/orders
```

## 장애 시나리오 테스트

### 서비스 다운

```bash
# Product Service 중지
vagrant halt product-service

# API 테스트 - 타임아웃 또는 에러 발생
curl http://localhost:8080/api/products

# 서비스 재시작
vagrant up product-service
```

### 데이터베이스 장애

```bash
# 데이터베이스 중지
vagrant halt database

# 서비스 동작 확인 (캐시 사용)
curl http://localhost:8080/api/users
```

## 배포 전략

### Blue-Green Deployment

1. 새 버전의 서비스를 별도 VM에 배포
2. Gateway 라우팅을 새 버전으로 전환
3. 이전 버전 종료

### Canary Deployment

Gateway에서 일부 트래픽만 새 버전으로:

```nginx
upstream user_service {
    server 192.168.60.21:3000 weight=9;  # 기존
    server 192.168.60.25:3000 weight=1;  # 신규 (10%)
}
```

## 보안 강화

### API Gateway에 인증 추가

```nginx
# JWT 검증, Rate Limiting 등
# Nginx Plus 또는 별도 인증 서비스 필요
```

### 서비스 간 통신 암호화

- TLS/SSL 인증서 사용
- VPN 또는 Service Mesh (Istio, Linkerd) 도입

## 로깅 및 추적

### 중앙화된 로깅

각 서비스에서 로그를 ELK Stack으로 전송:

```javascript
const winston = require('winston');
const ElasticsearchTransport = require('winston-elasticsearch');

const logger = winston.createLogger({
  transports: [
    new ElasticsearchTransport({
      level: 'info',
      clientOpts: { node: 'http://elasticsearch:9200' }
    })
  ]
});
```

### 분산 추적

Jaeger, Zipkin 등을 사용한 요청 추적

## 트러블슈팅

### 서비스가 시작되지 않는 경우

```bash
# 서비스 상태 확인
vagrant ssh user-service
sudo systemctl status user-service

# 로그 확인
sudo journalctl -u user-service -n 50
```

### Gateway 라우팅 문제

```bash
vagrant ssh gateway

# Nginx 설정 테스트
sudo nginx -t

# 에러 로그
sudo tail -f /var/log/nginx/error.log
```

### 네트워크 연결 문제

```bash
# Ping 테스트
vagrant ssh user-service
ping 192.168.60.30  # Database

# 포트 확인
telnet 192.168.60.30 5432
```

## VM 관리

```bash
# 모든 서비스 상태
vagrant status

# 특정 서비스 재시작
vagrant reload user-service

# 모든 서비스 중지
vagrant halt

# 모든 서비스 삭제
vagrant destroy -f
```

## 확장 아이디어

1. **Service Discovery**: Consul, Eureka
2. **Configuration Management**: Spring Cloud Config
3. **Circuit Breaker**: Hystrix, Resilience4j
4. **API Documentation**: Swagger/OpenAPI
5. **Monitoring**: Prometheus + Grafana
6. **Log Aggregation**: ELK Stack
7. **Distributed Tracing**: Jaeger, Zipkin
8. **Service Mesh**: Istio, Linkerd

## 학습 목표

이 예제를 통해 다음을 학습할 수 있습니다:

- 마이크로서비스 아키텍처 패턴
- 서비스 간 통신 (동기/비동기)
- API Gateway 패턴
- 데이터 분리 및 관리
- 캐싱 전략
- 메시지 큐를 통한 비동기 처리
- 서비스 확장 및 배포 전략
- 장애 처리 및 복원력

## 팁

- 각 서비스는 독립적으로 배포 가능합니다
- 데이터베이스를 서비스별로 분리하여 독립성 확보
- Redis로 자주 조회되는 데이터 캐싱
- RabbitMQ로 비동기 작업 처리
- API Gateway로 모든 요청을 중앙 관리

# 멀티 머신 환경

여러 VM으로 구성된 실제 운영 환경과 유사한 인프라 구성 예제입니다.

## 아키텍처

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    │  (192.168.50.100)│
                    │   nginx         │
                    └────────┬────────┘
                             │
               ┌─────────────┴─────────────┐
               │                           │
        ┌──────▼──────┐             ┌──────▼──────┐
        │  Web Server 1│             │  Web Server 2│
        │(192.168.50.101)│             │(192.168.50.102)│
        │   nginx      │             │   nginx      │
        └──────────────┘             └──────────────┘
               │                           │
               └─────────────┬─────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
         ┌──────▼──────┐           ┌──────▼──────┐
         │  Database   │           │    Cache    │
         │(192.168.50.110)│         │(192.168.50.120)│
         │   MySQL     │           │    Redis    │
         └─────────────┘           └─────────────┘
```

## VM 구성

| 이름 | 역할 | IP 주소 | 포트 | 메모리 |
|------|------|---------|------|--------|
| lb | 로드 밸런서 | 192.168.50.100 | 8080→80 | 512MB |
| web1 | 웹 서버 1 | 192.168.50.101 | 8081→80 | 1GB |
| web2 | 웹 서버 2 | 192.168.50.102 | 8082→80 | 1GB |
| db | 데이터베이스 | 192.168.50.110 | 3306→3306 | 1GB |
| cache | 캐시 | 192.168.50.120 | 6379→6379 | 512MB |

## 사용 방법

### 1. 전체 인프라 시작

```bash
# 모든 VM 시작
vagrant up

# 또는 개별 시작
vagrant up lb
vagrant up web1
vagrant up web2
vagrant up db
vagrant up cache
```

### 2. 로드 밸런서 테스트

브라우저에서 http://localhost:8080 접속

여러 번 새로고침하면 web1과 web2가 번갈아 응답합니다.

### 3. 개별 웹 서버 접속

- **Web1**: http://localhost:8081
- **Web2**: http://localhost:8082

### 4. VM SSH 접속

```bash
# 로드 밸런서
vagrant ssh lb

# 웹 서버 1
vagrant ssh web1

# 데이터베이스
vagrant ssh db

# 캐시
vagrant ssh cache
```

## 서비스 테스트

### 로드 밸런싱 테스트

```bash
# 여러 번 요청하여 라운드 로빈 확인
for i in {1..10}; do
  curl http://localhost:8080 | grep "<h1>"
done
```

### MySQL 연결 테스트

```bash
# 호스트에서
mysql -h localhost -P 3306 -u root -p
# 비밀번호: root

# VM 내부에서 (web1 예시)
vagrant ssh web1
mysql -h 192.168.50.110 -u root -p
```

### Redis 연결 테스트

```bash
# redis-cli 설치 (호스트)
sudo apt-get install redis-tools  # Linux
brew install redis  # macOS

# 연결
redis-cli -h localhost -p 6379

# 테스트 명령어
127.0.0.1:6379> SET test "Hello from Redis"
127.0.0.1:6379> GET test
127.0.0.1:6379> PING
```

## VM 간 통신 테스트

### Web 서버에서 DB 접속

```bash
vagrant ssh web1

# MySQL 클라이언트 설치
sudo apt-get update
sudo apt-get install -y mysql-client

# DB 접속
mysql -h 192.168.50.110 -u root -p
# 비밀번호: root
```

### Web 서버에서 Redis 접속

```bash
vagrant ssh web1

# Redis 클라이언트 설치
sudo apt-get install -y redis-tools

# Redis 접속
redis-cli -h 192.168.50.120

# 테스트
SET mykey "Hello"
GET mykey
```

## 로드 밸런서 설정

현재 라운드 로빈 방식으로 설정되어 있습니다.

### 다른 로드 밸런싱 알고리즘

lb VM에 SSH 접속 후 `/etc/nginx/nginx.conf` 수정:

```nginx
# IP 해시 (같은 클라이언트는 같은 서버로)
upstream backend {
    ip_hash;
    server 192.168.50.101:80;
    server 192.168.50.102:80;
}

# 최소 연결
upstream backend {
    least_conn;
    server 192.168.50.101:80;
    server 192.168.50.102:80;
}

# 가중치 부여
upstream backend {
    server 192.168.50.101:80 weight=3;
    server 192.168.50.102:80 weight=1;
}
```

변경 후:
```bash
sudo systemctl reload nginx
```

## 헬스 체크

### 웹 서버 상태 확인

```bash
# web1 상태
curl http://192.168.50.101

# web2 상태
curl http://192.168.50.102
```

### 서비스 모니터링

각 VM에서:

```bash
# CPU/메모리 사용량
top

# 네트워크 연결
sudo netstat -tulpn

# 디스크 사용량
df -h
```

## 스케일링 시나리오

### 웹 서버 추가

Vagrantfile에 web3 추가:

```ruby
config.vm.define "web3" do |web|
  web.vm.hostname = "web3"
  web.vm.network "private_network", ip: "192.168.50.103"
  # ... 설정 추가
end
```

로드 밸런서 설정 업데이트:

```nginx
upstream backend {
    server 192.168.50.101:80;
    server 192.168.50.102:80;
    server 192.168.50.103:80;
}
```

### 특정 서버 제외

```bash
# web1 중지
vagrant halt web1

# 로드 밸런서가 자동으로 web2로만 트래픽 전송
```

## 실전 시나리오

### 1. 장애 시뮬레이션

```bash
# web1 중지
vagrant halt web1

# 로드 밸런서 여전히 작동 (web2로 트래픽 전송)
curl http://localhost:8080
```

### 2. 롤링 업데이트

```bash
# web1 업데이트
vagrant ssh web1
# 업데이트 작업...
exit

# web1 재시작
vagrant reload web1

# web2 업데이트
vagrant ssh web2
# 업데이트 작업...
exit

# web2 재시작
vagrant reload web2
```

### 3. 데이터베이스 백업

```bash
vagrant ssh db

# 백업 생성
mysqldump -u root -p --all-databases > /vagrant/backup.sql

# 백업은 호스트의 프로젝트 디렉토리에 저장됨
```

## 모니터링

### Nginx 상태 페이지 활성화

lb VM의 nginx 설정에 추가:

```nginx
server {
    listen 8080;
    location /status {
        stub_status on;
        access_log off;
    }
}
```

접속:
```bash
curl http://192.168.50.100:8080/status
```

### MySQL 모니터링

```sql
-- 연결 확인
SHOW PROCESSLIST;

-- 상태 확인
SHOW STATUS;

-- 변수 확인
SHOW VARIABLES LIKE 'max_connections';
```

## VM 관리

```bash
# 모든 VM 상태 확인
vagrant status

# 특정 VM 재시작
vagrant reload web1

# 모든 VM 중지
vagrant halt

# 특정 VM 삭제
vagrant destroy web1

# 모든 VM 삭제
vagrant destroy -f
```

## 네트워크 테스트

```bash
# ping 테스트 (web1에서)
vagrant ssh web1
ping 192.168.50.110  # DB
ping 192.168.50.120  # Cache

# 포트 확인
telnet 192.168.50.110 3306  # MySQL
telnet 192.168.50.120 6379  # Redis
```

## 트러블슈팅

### VM이 시작되지 않는 경우

```bash
# VirtualBox 확인
vboxmanage list vms
vboxmanage list runningvms

# 로그 확인
vagrant up <vm-name> --debug
```

### 네트워크 연결 문제

```bash
# IP 확인
vagrant ssh <vm-name>
ip addr show

# 라우팅 테이블
ip route
```

### 로드 밸런서가 작동하지 않는 경우

```bash
vagrant ssh lb

# Nginx 설정 테스트
sudo nginx -t

# Nginx 로그 확인
sudo tail -f /var/log/nginx/error.log

# Upstream 서버 확인
curl http://192.168.50.101
curl http://192.168.50.102
```

## 확장 아이디어

1. **모니터링 서버 추가**: Prometheus + Grafana
2. **로그 집계**: ELK Stack (Elasticsearch, Logstash, Kibana)
3. **메시지 큐 추가**: RabbitMQ, Kafka
4. **컨테이너 오케스트레이션**: Docker Swarm, Kubernetes
5. **CI/CD 파이프라인**: Jenkins, GitLab CI

## 팁

- 프로덕션 환경을 미러링하여 테스트 가능
- 네트워크 문제, 장애 복구 시나리오 연습
- 마이크로서비스 아키텍처 학습
- 로드 밸런싱 전략 실험

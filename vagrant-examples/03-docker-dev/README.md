# Docker 개발 환경

Docker와 Docker Compose를 사용한 컨테이너 기반 개발 환경입니다.

## 포함된 내용

- Ubuntu 20.04 LTS
- Docker Engine
- Docker Compose
- 샘플 멀티 컨테이너 애플리케이션
  - Nginx (웹 서버)
  - Node.js (애플리케이션)
  - PostgreSQL (데이터베이스)
  - Redis (캐시)
  - Adminer (데이터베이스 관리 UI)

## 사용 방법

### 1. VM 시작

```bash
vagrant up
```

VM이 시작되면 자동으로 Docker Compose 서비스들이 실행됩니다.

### 2. SSH 접속

```bash
vagrant ssh
```

### 3. Docker 명령어 사용

```bash
# 실행 중인 컨테이너 확인
docker ps

# 모든 컨테이너 확인
docker ps -a

# 컨테이너 로그 확인
docker logs vagrant-nginx
docker logs vagrant-app -f  # 실시간 로그

# 컨테이너 내부 접속
docker exec -it vagrant-app sh
```

### 4. Docker Compose 명령어

```bash
cd /vagrant

# 서비스 시작
docker-compose up -d

# 서비스 중지
docker-compose down

# 서비스 재시작
docker-compose restart

# 로그 확인
docker-compose logs -f

# 특정 서비스만 재시작
docker-compose restart app

# 서비스 상태 확인
docker-compose ps
```

## 접속 정보

### 웹 서비스
- **Nginx**: http://localhost:8080
- **Node.js App**: http://localhost:3000
- **Adminer (DB 관리)**: http://localhost:8081

### 데이터베이스 (Adminer 로그인 정보)
- **System**: PostgreSQL
- **Server**: db
- **Username**: postgres
- **Password**: postgres
- **Database**: myapp

### Redis
- **Host**: localhost
- **Port**: 6379

## 디렉토리 구조

```
03-docker-dev/
├── Vagrantfile
├── docker-compose.yml
├── README.md
├── html/              # Nginx 정적 파일
│   └── index.html
├── app/               # Node.js 애플리케이션
│   ├── package.json
│   └── server.js
└── nginx.conf         # Nginx 설정
```

## 샘플 애플리케이션 실행

필요한 디렉토리와 파일들이 자동으로 생성됩니다:

```bash
# HTML 파일 생성
mkdir -p html
echo '<h1>Hello from Docker!</h1>' > html/index.html

# Node.js 앱 생성
mkdir -p app
cd app
cat > package.json << 'EOF'
{
  "name": "docker-app",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
EOF

cat > server.js << 'EOF'
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Docker Node.js!' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
EOF

# 서비스 재시작
cd /vagrant
docker-compose restart app
```

## 유용한 Docker 명령어

### 이미지 관리
```bash
# 이미지 목록
docker images

# 이미지 다운로드
docker pull nginx:latest

# 이미지 삭제
docker rmi nginx:latest

# 사용하지 않는 이미지 정리
docker image prune
```

### 컨테이너 관리
```bash
# 컨테이너 중지
docker stop vagrant-nginx

# 컨테이너 시작
docker start vagrant-nginx

# 컨테이너 재시작
docker restart vagrant-nginx

# 컨테이너 삭제
docker rm vagrant-nginx

# 모든 중지된 컨테이너 삭제
docker container prune
```

### 볼륨 관리
```bash
# 볼륨 목록
docker volume ls

# 볼륨 상세 정보
docker volume inspect 03-docker-dev_postgres-data

# 사용하지 않는 볼륨 삭제
docker volume prune
```

### 네트워크 관리
```bash
# 네트워크 목록
docker network ls

# 네트워크 상세 정보
docker network inspect 03-docker-dev_app-network
```

### 시스템 정리
```bash
# 모든 사용하지 않는 리소스 정리
docker system prune

# 볼륨까지 포함해서 정리
docker system prune -a --volumes
```

## 데이터 백업

### PostgreSQL 백업
```bash
# 백업 생성
docker exec vagrant-postgres pg_dump -U postgres myapp > backup.sql

# 복원
cat backup.sql | docker exec -i vagrant-postgres psql -U postgres myapp
```

### Redis 백업
```bash
# 백업 생성
docker exec vagrant-redis redis-cli SAVE
docker cp vagrant-redis:/data/dump.rdb ./redis-backup.rdb

# 복원
docker cp ./redis-backup.rdb vagrant-redis:/data/dump.rdb
docker restart vagrant-redis
```

## 트러블슈팅

### 포트 충돌
```bash
# 포트 사용 중인 프로세스 확인
sudo lsof -i :80
sudo lsof -i :5432

# docker-compose.yml에서 포트 변경
```

### 컨테이너가 계속 재시작되는 경우
```bash
# 로그 확인
docker logs vagrant-app

# 컨테이너 내부 확인
docker exec -it vagrant-app sh
```

### 디스크 공간 부족
```bash
# 디스크 사용량 확인
docker system df

# 정리
docker system prune -a
```

## VM 관리

```bash
# VM 중지
vagrant halt

# VM 재시작
vagrant reload

# VM 삭제 (데이터 볼륨도 삭제됨)
vagrant destroy
```

## 팁

- Docker 컨테이너는 VM 재시작 시 자동으로 시작됩니다
- 데이터는 Docker 볼륨에 저장되어 컨테이너 재시작 시에도 유지됩니다
- `docker-compose.yml`을 수정한 후 `docker-compose up -d`로 적용
- Adminer를 통해 웹 브라우저에서 데이터베이스를 관리할 수 있습니다

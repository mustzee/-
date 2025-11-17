# Vagrant 실습 예제 모음

Vagrant 완전정복 가이드의 실습 예제 모음입니다. 각 예제는 독립적으로 실행 가능하며, 실제 개발 환경에서 바로 사용할 수 있습니다.

## 📚 예제 목록

### 1. [Node.js 개발 환경](./01-nodejs-dev/)
**난이도**: ⭐ 초급
**소요 시간**: 5분
**기술 스택**: Node.js 18, npm, yarn, pm2, nodemon

Node.js 애플리케이션 개발을 위한 완전한 환경입니다.

```bash
cd 01-nodejs-dev
vagrant up
```

**주요 기능**:
- Node.js 18.x 설치
- 글로벌 패키지 (pm2, nodemon)
- Express 샘플 애플리케이션
- 자동 의존성 설치

**접속**: http://localhost:3000

---

### 2. [Django 개발 환경](./02-django-dev/)
**난이도**: ⭐⭐ 초중급
**소요 시간**: 7분
**기술 스택**: Python 3.8, Django 4, PostgreSQL, DRF

Django 웹 프레임워크와 PostgreSQL을 사용한 개발 환경입니다.

```bash
cd 02-django-dev
vagrant up
```

**주요 기능**:
- Django 4.x + Python 가상 환경
- PostgreSQL 12 자동 설정
- Django REST Framework
- 자동 DB 생성 및 설정

**접속**: http://localhost:8000

---

### 3. [Docker 개발 환경](./03-docker-dev/)
**난이도**: ⭐⭐ 초중급
**소요 시간**: 10분
**기술 스택**: Docker, Docker Compose, Nginx, PostgreSQL, Redis

Docker와 Docker Compose를 사용한 컨테이너 기반 개발 환경입니다.

```bash
cd 03-docker-dev
vagrant up
```

**포함된 서비스**:
- Nginx (리버스 프록시)
- Node.js 애플리케이션
- PostgreSQL
- Redis
- Adminer (DB 관리)

**접속**:
- 웹: http://localhost:8080
- Adminer: http://localhost:8081

---

### 4. [Kubernetes (k3s) 클러스터](./04-kubernetes-k3s/)
**난이도**: ⭐⭐⭐ 중급
**소요 시간**: 15분
**기술 스택**: k3s, kubectl, Kubernetes

경량 Kubernetes 배포판 k3s를 사용한 3노드 클러스터입니다.

```bash
cd 04-kubernetes-k3s
vagrant up
```

**클러스터 구성**:
- 마스터 노드 × 1 (2GB RAM)
- 워커 노드 × 2 (1GB RAM)
- kubectl 자동 설정
- 샘플 deployment 포함

**접속**:
```bash
vagrant ssh k8s-master-1
kubectl get nodes
```

---

### 5. [WordPress (Ansible 프로비저닝)](./05-wordpress-ansible/)
**난이도**: ⭐⭐⭐ 중급
**소요 시간**: 10분
**기술 스택**: WordPress, Ansible, Apache, MySQL, PHP

Ansible로 자동 프로비저닝되는 WordPress 환경입니다.

```bash
cd 05-wordpress-ansible
vagrant up
```

**주요 기능**:
- Ansible 자동 프로비저닝
- LAMP 스택 완전 자동 설치
- WordPress 자동 다운로드 및 설정
- phpMyAdmin 포함

**접속**: http://localhost:8080

---

### 6. [LAMP 스택](./06-lamp-stack/)
**난이도**: ⭐⭐ 초중급
**소요 시간**: 8분
**기술 스택**: Linux, Apache, MySQL, PHP, Composer

전통적인 LAMP 스택 웹 개발 환경입니다.

```bash
cd 06-lamp-stack
vagrant up
```

**포함된 내용**:
- Apache 2.4 + PHP 7.4
- MySQL 8.0
- phpMyAdmin
- Composer

**접속**:
- PHP Info: http://localhost:8080
- phpMyAdmin: http://localhost:8080/phpmyadmin

---

### 7. [멀티 머신 환경](./07-multi-machine/)
**난이도**: ⭐⭐⭐ 중급
**소요 시간**: 12분
**기술 스택**: Nginx, MySQL, Redis

실제 운영 환경과 유사한 멀티 티어 아키텍처입니다.

```bash
cd 07-multi-machine
vagrant up
```

**인프라 구성**:
- 로드 밸런서 × 1
- 웹 서버 × 2
- 데이터베이스 × 1 (MySQL)
- 캐시 서버 × 1 (Redis)

**접속**: http://localhost:8080 (로드 밸런싱)

---

### 8. [마이크로서비스 아키텍처](./08-microservices/)
**난이도**: ⭐⭐⭐⭐ 고급
**소요 시간**: 20분
**기술 스택**: Node.js, PostgreSQL, Redis, RabbitMQ, Nginx

실제 마이크로서비스 아키텍처를 시뮬레이션하는 환경입니다.

```bash
cd 08-microservices
vagrant up
```

**서비스 구성**:
- API Gateway (Nginx)
- User Service (Node.js)
- Product Service (Node.js)
- Order Service (Node.js)
- PostgreSQL (3개 DB)
- Redis (캐시)
- RabbitMQ (메시지 큐)

**접속**: http://localhost:8080

---

## 🚀 빠른 시작

### 사전 요구사항

1. **Vagrant 설치** (2.2.0 이상)
   ```bash
   # macOS
   brew install vagrant

   # Windows (Chocolatey)
   choco install vagrant

   # Linux
   wget https://releases.hashicorp.com/vagrant/2.4.0/vagrant_2.4.0_linux_amd64.zip
   ```

2. **VirtualBox 설치** (6.0 이상)
   - https://www.virtualbox.org/wiki/Downloads

3. **최소 시스템 요구사항**
   - RAM: 8GB (권장 16GB)
   - 디스크 공간: 20GB
   - CPU: 2코어 이상

### 예제 실행 방법

```bash
# 1. 원하는 예제 디렉토리로 이동
cd 01-nodejs-dev

# 2. VM 시작
vagrant up

# 3. SSH 접속 (필요한 경우)
vagrant ssh

# 4. 사용이 끝나면 VM 중지
vagrant halt

# 5. VM 완전 삭제
vagrant destroy
```

## 📖 학습 경로

### 초보자 추천 순서
1. **01-nodejs-dev** - Vagrant 기본 익히기
2. **06-lamp-stack** - 웹 개발 환경 구축
3. **02-django-dev** - 프로비저닝 이해하기
4. **07-multi-machine** - 멀티 VM 관리

### 중급자 추천 순서
1. **03-docker-dev** - 컨테이너 환경
2. **05-wordpress-ansible** - 인프라 자동화
3. **04-kubernetes-k3s** - 컨테이너 오케스트레이션
4. **08-microservices** - 마이크로서비스 아키텍처

## 💡 유용한 명령어

### VM 관리
```bash
vagrant up              # VM 시작/생성
vagrant halt            # VM 중지
vagrant reload          # VM 재시작
vagrant destroy         # VM 삭제
vagrant ssh             # SSH 접속
vagrant status          # 상태 확인
vagrant global-status   # 모든 VM 상태
```

### 프로비저닝
```bash
vagrant provision                    # 프로비저닝 실행
vagrant reload --provision           # 재시작 + 프로비저닝
vagrant up --no-provision            # 프로비저닝 없이 시작
```

### 스냅샷
```bash
vagrant snapshot save <name>         # 스냅샷 생성
vagrant snapshot list                # 스냅샷 목록
vagrant snapshot restore <name>      # 스냅샷 복원
```

## 🎯 예제별 추천 사용 사례

| 예제 | 추천 사용 사례 |
|------|---------------|
| Node.js | JavaScript 백엔드, Express API 개발 |
| Django | Python 웹 애플리케이션, REST API |
| Docker | 마이크로서비스, 컨테이너 학습 |
| Kubernetes | 클러스터 관리, 컨테이너 오케스트레이션 |
| WordPress | CMS 개발, 플러그인/테마 개발 |
| LAMP | PHP 웹 애플리케이션, Laravel/Symfony |
| Multi-Machine | 분산 시스템, 로드 밸런싱 학습 |
| Microservices | 마이크로서비스 패턴, 서비스 메시 |

## 🔧 트러블슈팅

### 일반적인 문제

#### 1. VirtualBox Guest Additions 버전 불일치
```bash
vagrant plugin install vagrant-vbguest
vagrant reload
```

#### 2. 포트 충돌
```bash
# 사용 중인 포트 확인 (Linux/macOS)
sudo lsof -i :8080

# Windows
netstat -ano | findstr :8080
```

#### 3. 메모리 부족
Vagrantfile에서 메모리 설정 조정:
```ruby
vb.memory = "1024"  # 2048 → 1024로 감소
```

#### 4. 네트워크 문제 (NFS)
```bash
# macOS/Linux에서 NFS 재시작
sudo nfsd restart

# 또는 NFS 비활성화 (Vagrantfile)
config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
```

### 디버깅

```bash
# 상세 로그 출력
VAGRANT_LOG=debug vagrant up

# 프로비저닝 문제 확인
vagrant provision --debug
```

## 📊 예제별 리소스 요구사항

| 예제 | VM 수 | 총 메모리 | 총 CPU | 디스크 |
|------|-------|-----------|--------|--------|
| Node.js | 1 | 2GB | 2 | ~3GB |
| Django | 1 | 2GB | 2 | ~3GB |
| Docker | 1 | 4GB | 2 | ~5GB |
| Kubernetes | 3 | 4GB | 4 | ~8GB |
| WordPress | 1 | 2GB | 2 | ~3GB |
| LAMP | 1 | 2GB | 2 | ~3GB |
| Multi-Machine | 5 | 4GB | 5 | ~10GB |
| Microservices | 7 | 4.5GB | 7 | ~12GB |

## 🛠️ 커스터마이징

각 예제의 `Vagrantfile`을 수정하여 커스터마이징 가능합니다:

```ruby
# 메모리 변경
vb.memory = "4096"

# CPU 코어 변경
vb.cpus = 4

# 네트워크 IP 변경
config.vm.network "private_network", ip: "192.168.50.100"

# 포트 포워딩 추가
config.vm.network "forwarded_port", guest: 3000, host: 3000
```

## 📝 추가 학습 자료

### 공식 문서
- [Vagrant 공식 문서](https://developer.hashicorp.com/vagrant/docs)
- [VirtualBox 문서](https://www.virtualbox.org/wiki/Documentation)

### 관련 가이드
- [VAGRANT_COMPLETE_GUIDE.md](../VAGRANT_COMPLETE_GUIDE.md) - Vagrant 완전정복 가이드

### 커뮤니티
- [Vagrant GitHub](https://github.com/hashicorp/vagrant)
- [Stack Overflow - Vagrant](https://stackoverflow.com/questions/tagged/vagrant)

## 🤝 기여하기

이 예제들을 개선하고 싶으신가요?

1. 이슈 제기: 버그 리포트, 기능 제안
2. Pull Request: 코드 개선, 새로운 예제 추가
3. 문서 개선: README 오타 수정, 설명 보완

## 📜 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

## ⚠️ 주의사항

1. **프로덕션 사용 금지**: 이 예제들은 학습 및 개발 목적입니다
2. **보안 설정**: 기본 비밀번호가 포함되어 있으므로 프로덕션에서는 반드시 변경
3. **리소스 관리**: 사용하지 않는 VM은 `vagrant halt` 또는 `vagrant destroy`로 정리
4. **네트워크**: 일부 예제는 인터넷 연결이 필요합니다 (패키지 다운로드)

## 🆘 도움말

문제가 발생했나요?

1. 각 예제의 `README.md` 파일 확인
2. `VAGRANT_COMPLETE_GUIDE.md`의 트러블슈팅 섹션 참조
3. GitHub Issues에 질문 등록

---

**Happy Vagrant Learning! 🚀**

각 예제를 통해 Vagrant의 강력함을 경험하고, 실제 프로젝트에 적용해보세요!

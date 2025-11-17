# Node.js 개발 환경

Node.js 개발을 위한 Vagrant 환경입니다.

## 포함된 내용

- Ubuntu 20.04 LTS
- Node.js 18.x
- npm, yarn
- pm2, nodemon (글로벌)
- Git, Build tools

## 사용 방법

### 1. VM 시작

```bash
vagrant up
```

### 2. SSH 접속

```bash
vagrant ssh
```

### 3. 프로젝트 디렉토리로 이동

```bash
cd /vagrant
```

### 4. Node.js 애플리케이션 실행

```bash
# 직접 실행
node app.js

# nodemon으로 실행 (자동 재시작)
nodemon app.js

# pm2로 실행 (프로세스 관리)
pm2 start app.js
pm2 list
pm2 logs
pm2 stop app.js
```

## 샘플 애플리케이션

간단한 Express 서버를 만들어보세요:

```bash
# Express 설치
npm init -y
npm install express

# app.js 생성
cat > app.js << 'EOF'
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Vagrant Node.js!');
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server running at http://0.0.0.0:${port}`);
});
EOF

# 실행
node app.js
```

브라우저에서 http://localhost:3000 접속

## 포트 포워딩

- 3000 → 3000 (Node.js 기본 포트)
- 8080 → 8080 (추가 포트)

## VM 관리

```bash
# VM 중지
vagrant halt

# VM 재시작
vagrant reload

# VM 삭제
vagrant destroy
```

## 팁

- 호스트의 파일 변경이 자동으로 게스트에 반영됩니다
- nodemon을 사용하면 파일 변경 시 자동으로 서버가 재시작됩니다
- pm2를 사용하면 프로세스를 백그라운드에서 관리할 수 있습니다

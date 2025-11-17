# SSH (Secure Shell)

## 목차
- [SSH 기본](#ssh-기본)
- [SSH 키 관리](#ssh-키-관리)
- [SSH 설정](#ssh-설정)
- [SSH 터널링](#ssh-터널링)
- [고급 기능](#고급-기능)
- [보안 강화](#보안-강화)
- [실전 예제](#실전-예제)

---

## SSH 기본

### 기본 연결

```bash
# 기본 연결
$ ssh user@hostname
$ ssh user@192.168.1.100

# 사용자명 생략 (현재 사용자)
$ ssh hostname

# 포트 지정
$ ssh -p 2222 user@hostname

# IPv4 강제
$ ssh -4 user@hostname

# IPv6 강제
$ ssh -6 user@hostname

# 상세 출력
$ ssh -v user@hostname    # Verbose
$ ssh -vv user@hostname   # More verbose
$ ssh -vvv user@hostname  # Debug

# 명령 실행 후 종료
$ ssh user@hostname 'ls -la'
$ ssh user@hostname 'uname -a'
$ ssh user@hostname 'df -h'

# 명령 결과를 로컬에 저장
$ ssh user@hostname 'cat /var/log/syslog' > local_file.log

# 원격에서 스크립트 실행
$ ssh user@hostname 'bash -s' < local_script.sh
$ cat script.sh | ssh user@hostname 'bash -s'

# Pseudo-terminal 할당
$ ssh -t user@hostname 'sudo command'
$ ssh -t user@hostname 'top'

# X11 포워딩
$ ssh -X user@hostname
$ ssh -Y user@hostname  # Trusted X11

# 압축 사용
$ ssh -C user@hostname

# Keep-alive
$ ssh -o ServerAliveInterval=60 user@hostname
```

### SSH 클라이언트 옵션

```bash
# 설정 파일 지정
$ ssh -F /path/to/config user@hostname

# 식별 파일 (키)
$ ssh -i ~/.ssh/id_rsa user@hostname
$ ssh -i /path/to/private_key user@hostname

# 엄격한 호스트 키 확인 비활성화 (주의!)
$ ssh -o StrictHostKeyChecking=no user@hostname
$ ssh -o UserKnownHostsFile=/dev/null user@hostname

# 비밀번호 인증 비활성화
$ ssh -o PasswordAuthentication=no user@hostname

# 타임아웃 설정
$ ssh -o ConnectTimeout=10 user@hostname

# 로그인 쉘 없이
$ ssh -N user@hostname  # 터널링에 유용

# 백그라운드 실행
$ ssh -f user@hostname command

# 여러 연결 재사용 (ControlMaster)
$ ssh -o ControlMaster=auto -o ControlPath=/tmp/ssh-%r@%h:%p user@hostname
```

---

## SSH 키 관리

### SSH 키 생성

```bash
# RSA 키 생성 (기본)
$ ssh-keygen
$ ssh-keygen -t rsa -b 4096

# 파일명 지정
$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/my_key

# 코멘트 추가
$ ssh-keygen -t rsa -b 4096 -C "user@email.com"

# 비밀번호 없이 (자동화용, 주의!)
$ ssh-keygen -t rsa -b 4096 -N ""

# Ed25519 (권장, 더 안전하고 빠름)
$ ssh-keygen -t ed25519
$ ssh-keygen -t ed25519 -C "user@email.com"

# ECDSA
$ ssh-keygen -t ecdsa -b 521

# DSA (권장하지 않음, 구버전 호환용만)
$ ssh-keygen -t dsa

# 키 생성 결과
# - ~/.ssh/id_rsa (또는 id_ed25519): 개인 키 (비밀!)
# - ~/.ssh/id_rsa.pub (또는 id_ed25519.pub): 공개 키

# 생성된 키 확인
$ ls -la ~/.ssh/
-rw------- 1 user user  464 Nov 17 10:00 id_ed25519
-rw-r--r-- 1 user user   98 Nov 17 10:00 id_ed25519.pub
```

### 공개 키 배포

```bash
# ssh-copy-id 사용 (권장)
$ ssh-copy-id user@hostname
$ ssh-copy-id -i ~/.ssh/id_rsa.pub user@hostname
$ ssh-copy-id -p 2222 user@hostname

# 수동으로 복사
$ cat ~/.ssh/id_rsa.pub | ssh user@hostname 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'

# 또는
$ scp ~/.ssh/id_rsa.pub user@hostname:~/
$ ssh user@hostname
$ mkdir -p ~/.ssh
$ cat ~/id_rsa.pub >> ~/.ssh/authorized_keys
$ rm ~/id_rsa.pub
$ chmod 700 ~/.ssh
$ chmod 600 ~/.ssh/authorized_keys

# 여러 호스트에 배포
$ for host in host1 host2 host3; do
    ssh-copy-id user@$host
done
```

### 키 관리

```bash
# 키 지문 확인
$ ssh-keygen -lf ~/.ssh/id_rsa.pub
$ ssh-keygen -lf ~/.ssh/id_ed25519.pub

# 지문을 ASCII art로
$ ssh-keygen -lvf ~/.ssh/id_rsa.pub

# 키 비밀번호 변경
$ ssh-keygen -p -f ~/.ssh/id_rsa

# 기존 키에 비밀번호 추가
$ ssh-keygen -p -f ~/.ssh/id_rsa

# 공개 키 재생성 (개인 키로부터)
$ ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub

# 키 검증
$ ssh-keygen -y -f ~/.ssh/id_rsa  # 공개 키 출력되면 OK

# 호스트 키 확인
$ ssh-keygen -F hostname
$ ssh-keygen -H -F hostname  # 해시된 형태로

# 호스트 키 삭제 (IP 변경 시)
$ ssh-keygen -R hostname
$ ssh-keygen -R 192.168.1.100

# known_hosts 해싱
$ ssh-keygen -H
```

### SSH Agent

```bash
# Agent 시작
$ eval $(ssh-agent)
$ ssh-agent bash

# 키 추가
$ ssh-add ~/.ssh/id_rsa
$ ssh-add ~/.ssh/id_ed25519

# 모든 기본 키 추가
$ ssh-add

# 추가된 키 목록
$ ssh-add -l
$ ssh-add -L  # 공개 키 전체 출력

# 키 삭제
$ ssh-add -d ~/.ssh/id_rsa

# 모든 키 삭제
$ ssh-add -D

# Agent 종료
$ ssh-agent -k

# 타임아웃 설정 (1시간)
$ ssh-add -t 3600 ~/.ssh/id_rsa

# 확인 요청
$ ssh-add -c ~/.ssh/id_rsa

# Keychain 사용 (영구 agent)
$ sudo apt install keychain
$ eval $(keychain --eval ~/.ssh/id_rsa)

# ~/.bashrc에 추가
eval $(keychain --eval --quiet id_rsa id_ed25519)
```

---

## SSH 설정

### SSH 클라이언트 설정

```bash
# ~/.ssh/config
$ vi ~/.ssh/config

# 기본 설정
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222

# 사용
$ ssh myserver  # ssh admin@192.168.1.100 -p 2222와 동일

# 키 파일 지정
Host myserver
    HostName 192.168.1.100
    User admin
    IdentityFile ~/.ssh/myserver_key

# 프록시 점프
Host internal-server
    HostName 10.0.0.50
    User admin
    ProxyJump bastion-host

# 또는
Host internal-server
    HostName 10.0.0.50
    User admin
    ProxyCommand ssh -W %h:%p bastion-host

# 여러 호스트 패턴
Host web-*
    User webadmin
    IdentityFile ~/.ssh/web_key

Host db-*
    User dbadmin
    IdentityFile ~/.ssh/db_key

# 와일드카드
Host *.example.com
    User commonuser
    Port 22

# 모든 호스트에 대한 기본값
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
    ControlMaster auto
    ControlPath /tmp/ssh-%r@%h:%p
    ControlPersist 10m

# 고급 설정 예제
Host production
    HostName prod.example.com
    User deploy
    IdentityFile ~/.ssh/prod_key
    Port 2222
    ForwardAgent yes
    LocalForward 8080 localhost:80
    RemoteForward 9000 localhost:3000
    ServerAliveInterval 60
    StrictHostKeyChecking yes
    UserKnownHostsFile ~/.ssh/known_hosts

# SSH 다중 연결 (ControlMaster)
Host *
    ControlMaster auto
    ControlPath ~/.ssh/control-%r@%h:%p
    ControlPersist 10m

# 파일 권한 설정
$ chmod 600 ~/.ssh/config
```

### SSH 서버 설정

```bash
# 서버 설정 파일
$ sudo vi /etc/ssh/sshd_config

# 주요 설정:

# 포트 변경
Port 2222

# 루트 로그인 금지
PermitRootLogin no

# 또는 키 인증만 허용
PermitRootLogin prohibit-password

# 비밀번호 인증 비활성화
PasswordAuthentication no

# 빈 비밀번호 금지
PermitEmptyPasswords no

# 공개 키 인증 활성화
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# X11 포워딩
X11Forwarding yes

# 특정 사용자만 허용
AllowUsers user1 user2 admin

# 특정 그룹만 허용
AllowGroups sshusers admins

# 특정 사용자 거부
DenyUsers baduser

# 로그인 시도 제한
MaxAuthTries 3
MaxSessions 10

# 타임아웃
ClientAliveInterval 300
ClientAliveCountMax 2
LoginGraceTime 60

# TCP KeepAlive
TCPKeepAlive yes

# DNS 확인 비활성화 (빠른 로그인)
UseDNS no

# SFTP 서브시스템
Subsystem sftp /usr/lib/openssh/sftp-server

# Chroot (SFTP만)
Match Group sftpusers
    ChrootDirectory /home/%u
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no

# 설정 테스트
$ sudo sshd -t

# 설정 적용
$ sudo systemctl reload sshd
$ sudo systemctl restart sshd

# 설정 확인
$ sudo sshd -T
```

---

## SSH 터널링

### 로컬 포트 포워딩

```bash
# 로컬 포트를 원격으로
$ ssh -L local_port:remote_host:remote_port user@ssh_server

# 예: 로컬 8080 → 원격의 localhost:80
$ ssh -L 8080:localhost:80 user@webserver
# 이제 http://localhost:8080으로 웹서버 접근

# 예: 로컬 3306 → DB 서버 3306 (SSH 서버를 통해)
$ ssh -L 3306:dbserver.internal:3306 user@bastion
# mysql -h localhost -P 3306으로 DB 접근

# 모든 인터페이스에서 접근 허용
$ ssh -L 0.0.0.0:8080:localhost:80 user@webserver

# 여러 포트 포워딩
$ ssh -L 8080:localhost:80 -L 3306:localhost:3306 user@server

# 백그라운드 실행
$ ssh -f -N -L 8080:localhost:80 user@server
```

### 원격 포트 포워딩

```bash
# 원격 포트를 로컬로
$ ssh -R remote_port:local_host:local_port user@ssh_server

# 예: 원격 8080 → 로컬 localhost:80
$ ssh -R 8080:localhost:80 user@remote
# 원격에서 localhost:8080으로 로컬 웹서버 접근

# 예: 역방향 셸 (방화벽 우회)
$ ssh -R 2222:localhost:22 user@public_server
# public_server에서: ssh -p 2222 localhost로 접속

# 모든 인터페이스에서 접근 허용 (서버 설정 필요)
$ ssh -R 0.0.0.0:8080:localhost:80 user@server
# 서버의 /etc/ssh/sshd_config에 GatewayPorts yes 필요

# 여러 포트
$ ssh -R 8080:localhost:80 -R 3000:localhost:3000 user@server

# 백그라운드
$ ssh -f -N -R 8080:localhost:80 user@server
```

### 동적 포트 포워딩 (SOCKS 프록시)

```bash
# SOCKS 프록시 생성
$ ssh -D 1080 user@server

# 백그라운드로
$ ssh -f -N -D 1080 user@server

# 사용: 브라우저 SOCKS 설정에 localhost:1080 입력

# curl로 SOCKS 프록시 사용
$ curl --socks5 localhost:1080 http://example.com

# Git에서 사용
$ git config --global http.proxy 'socks5://127.0.0.1:1080'

# 모든 트래픽을 SSH 터널로 (VPN처럼)
$ ssh -D 1080 user@server
# + 시스템 전역 프록시 설정
```

### ProxyJump (점프 호스트)

```bash
# 기본 사용
$ ssh -J jumphost targethost
$ ssh -J user1@jumphost user2@targethost

# 여러 점프 호스트
$ ssh -J jump1,jump2,jump3 targethost

# 포트 지정
$ ssh -J user@jumphost:2222 targethost

# ~/.ssh/config에 설정
Host targethost
    HostName 10.0.0.50
    User admin
    ProxyJump jumphost

Host jumphost
    HostName bastion.example.com
    User bastion_user
    Port 2222
```

---

## 고급 기능

### SCP (Secure Copy)

```bash
# 로컬 → 원격
$ scp file.txt user@host:/path/to/destination/
$ scp file.txt user@host:~/

# 원격 → 로컬
$ scp user@host:/path/to/file.txt ./
$ scp user@host:~/file.txt /local/path/

# 디렉토리 복사 (재귀)
$ scp -r directory/ user@host:/path/

# 여러 파일
$ scp file1.txt file2.txt user@host:/path/

# 포트 지정
$ scp -P 2222 file.txt user@host:/path/

# 대역폭 제한 (KB/s)
$ scp -l 1024 file.txt user@host:/path/

# 압축
$ scp -C file.txt user@host:/path/

# 원격 → 원격 (로컬을 통해)
$ scp user1@host1:/path/file.txt user2@host2:/path/

# 속도 향상 (암호화 줄임)
$ scp -c aes128-ctr file.txt user@host:/path/

# 진행 상황 숨기기
$ scp -q file.txt user@host:/path/

# 보존 (타임스탬프, 권한)
$ scp -p file.txt user@host:/path/
```

### SFTP (SSH File Transfer Protocol)

```bash
# SFTP 연결
$ sftp user@hostname
sftp> ls
sftp> cd /path
sftp> pwd
sftp> lpwd  # 로컬 pwd

# 파일 다운로드
sftp> get remote_file
sftp> get remote_file local_file

# 여러 파일
sftp> mget *.txt

# 디렉토리 다운로드
sftp> get -r remote_directory

# 파일 업로드
sftp> put local_file
sftp> put local_file remote_file

# 여러 파일
sftp> mput *.txt

# 디렉토리 업로드
sftp> put -r local_directory

# 기타 명령
sftp> mkdir newdir
sftp> rmdir olddir
sftp> rm file.txt
sftp> rename old.txt new.txt
sftp> chmod 644 file.txt
sftp> chown 1000 file.txt

# 로컬 명령 (l prefix)
sftp> lcd /local/path
sftp> lls
sftp> lmkdir newdir

# 배치 모드
$ sftp -b commands.txt user@host

# commands.txt:
cd /remote/path
get file.txt
put local.txt
bye

# 한 줄 명령
$ echo "get /remote/file.txt" | sftp user@host
```

### rsync over SSH

```bash
# 기본 사용
$ rsync -avz source/ user@host:/destination/

# 옵션:
# -a: 아카이브 모드 (권한, 타임스탬프 보존)
# -v: Verbose
# -z: 압축
# -h: 사람이 읽기 쉬운 형식
# -P: 진행상황 + 부분 전송 보존

# 포트 지정
$ rsync -avz -e "ssh -p 2222" source/ user@host:/destination/

# SSH 키 지정
$ rsync -avz -e "ssh -i /path/to/key" source/ user@host:/destination/

# 삭제 동기화 (주의!)
$ rsync -avz --delete source/ user@host:/destination/

# Dry run (실제 수행하지 않고 확인)
$ rsync -avzn source/ user@host:/destination/
$ rsync -avz --dry-run source/ user@host:/destination/

# 특정 파일 제외
$ rsync -avz --exclude="*.log" source/ user@host:/destination/
$ rsync -avz --exclude-from=exclude.txt source/ user@host:/destination/

# 진행상황 표시
$ rsync -avzP source/ user@host:/destination/
$ rsync -avz --progress source/ user@host:/destination/

# 대역폭 제한
$ rsync -avz --bwlimit=1000 source/ user@host:/destination/

# 원격 → 로컬
$ rsync -avz user@host:/source/ /local/destination/

# 백업 (타임스탬프)
$ rsync -avz --backup --suffix=.$(date +%Y%m%d) source/ user@host:/destination/

# 증분 백업
$ rsync -avz --link-dest=/previous/backup source/ /new/backup/

# 통계
$ rsync -avz --stats source/ user@host:/destination/
```

---

## 보안 강화

### SSH Fail2ban

```bash
# 설치
$ sudo apt install fail2ban

# 설정
$ sudo vi /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600

# 서비스 시작
$ sudo systemctl enable fail2ban
$ sudo systemctl start fail2ban

# 상태 확인
$ sudo fail2ban-client status
$ sudo fail2ban-client status sshd

# 수동 차단/해제
$ sudo fail2ban-client set sshd banip 192.168.1.100
$ sudo fail2ban-client set sshd unbanip 192.168.1.100
```

### 2FA (Two-Factor Authentication)

```bash
# Google Authenticator 설치
$ sudo apt install libpam-google-authenticator

# 사용자별 설정
$ google-authenticator
# QR 코드 스캔하여 앱에 등록

# SSH에 PAM 설정
$ sudo vi /etc/pam.d/sshd
# 맨 위에 추가:
auth required pam_google_authenticator.so

# SSHD 설정
$ sudo vi /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# 재시작
$ sudo systemctl restart sshd
```

---

## 실전 예제

### 예제 1: SSH 배스천 호스트 구성

```bash
# ~/.ssh/config
Host bastion
    HostName bastion.example.com
    User bastion_user
    Port 2222
    IdentityFile ~/.ssh/bastion_key

Host internal-*
    User admin
    ProxyJump bastion
    IdentityFile ~/.ssh/internal_key

Host internal-web
    HostName 10.0.1.10

Host internal-db
    HostName 10.0.1.20

# 사용:
$ ssh internal-web
$ ssh internal-db
```

### 예제 2: SSH 터널 관리 스크립트

```bash
#!/bin/bash
# ssh_tunnel.sh

case "$1" in
    start)
        ssh -f -N -L 3306:db.internal:3306 bastion
        ssh -f -N -L 8080:web.internal:80 bastion
        echo "Tunnels started"
        ;;
    stop)
        pkill -f "ssh -f -N -L 3306"
        pkill -f "ssh -f -N -L 8080"
        echo "Tunnels stopped"
        ;;
    status)
        ps aux | grep "ssh -f -N -L" | grep -v grep
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        ;;
esac
```

---

## 문제 해결

### Permission denied (publickey)

```bash
# 권한 확인
$ chmod 700 ~/.ssh
$ chmod 600 ~/.ssh/authorized_keys
$ chmod 600 ~/.ssh/id_rsa

# 서버에서 authorized_keys 확인
$ cat ~/.ssh/authorized_keys

# SELinux 컨텍스트 (RHEL/CentOS)
$ restorecon -Rv ~/.ssh
```

### Host key verification failed

```bash
# known_hosts에서 제거
$ ssh-keygen -R hostname

# 다시 연결
$ ssh user@hostname
```

---

## 요약

SSH 핵심:

1. **키 인증**: 비밀번호보다 안전
2. **설정 파일**: ~/.ssh/config로 편리하게
3. **터널링**: 보안 통신 경로 생성
4. **보안**: Fail2ban, 2FA, 키 관리

---

[다음: 파일 전송 →](file-transfer.md)

[← 네트워크 진단으로 돌아가기](diagnostics.md)

[← 목차로 돌아가기](../README.md)

# 로깅 시스템

## 목차
- [소개](#소개)
- [syslog](#syslog)
- [rsyslog](#rsyslog)
- [journald](#journald)
- [로그 파일](#로그-파일)
- [로그 회전](#로그-회전)
- [로그 분석](#로그-분석)
- [중앙 집중식 로깅](#중앙-집중식-로깅)
- [로그 보안](#로그-보안)
- [실전 예제](#실전-예제)

---

## 소개

Linux 시스템에서 로깅은 시스템 모니터링, 디버깅, 보안 감사의 핵심입니다.

### 로깅 시스템 종류

```bash
# 전통적 syslog
# - syslogd (전통적)
# - rsyslog (현대적, 기능 풍부)
# - syslog-ng (고급 필터링)

# systemd 환경
# - journald (바이너리 로그)
# - rsyslog와 journald 병행 사용 가능

# 현재 로깅 시스템 확인
$ ps aux | grep -E 'syslog|journal'
root      1234  rsyslogd
root      1235  systemd-journald

$ systemctl status rsyslog
$ systemctl status systemd-journald
```

---

## syslog

### syslog 기본 개념

```bash
# Syslog 메시지 구조
# Facility.Priority: Message
# 예: kern.warning: High temperature detected

# Facility (어디서)
kern        # 커널 메시지
user        # 사용자 프로세스
mail        # 메일 시스템
daemon      # 시스템 데몬
auth        # 인증/보안
syslog      # syslog 자체
lpr         # 프린터
news        # 뉴스
uucp        # UUCP
cron        # cron/at
authpriv    # 인증 (private)
ftp         # FTP
local0-7    # 로컬 사용

# Priority (심각도)
emerg       # 0: 긴급 (시스템 불가능)
alert       # 1: 경보 (즉시 조치 필요)
crit        # 2: 치명적
err         # 3: 오류
warning     # 4: 경고
notice      # 5: 주의
info        # 6: 정보
debug       # 7: 디버그
```

### logger 명령

```bash
# logger - syslog에 메시지 전송

# 기본 사용
$ logger "Test message"
$ logger "System backup completed"

# priority 지정
$ logger -p user.info "Info message"
$ logger -p user.warning "Warning message"
$ logger -p user.err "Error message"

# tag 지정
$ logger -t myapp "Application started"
$ logger -t backup "Backup completed"

# facility 지정
$ logger -p local0.info "Local message"

# 파일에서 읽기
$ logger -f /tmp/messages.txt

# 스크립트에서 사용
#!/bin/bash
logger -t backup -p user.info "Starting backup"
if backup_command; then
    logger -t backup -p user.info "Backup successful"
else
    logger -t backup -p user.err "Backup failed"
fi

# syslog 서버로 전송
$ logger -n 192.168.1.100 -P 514 "Remote log message"
```

---

## rsyslog

### rsyslog 설정

```bash
# rsyslog 설정 파일
$ cat /etc/rsyslog.conf

# 모듈 로드
module(load="imuxsock")   # 로컬 소켓
module(load="imklog")     # 커널 로그
module(load="imudp")      # UDP syslog 수신
module(load="imtcp")      # TCP syslog 수신

# UDP 수신 (514 포트)
input(type="imudp" port="514")

# TCP 수신
input(type="imtcp" port="514")

# 규칙 (Facility.Priority Action)
# *.* 모든 메시지
# mail.* 모든 메일 메시지
# kern.warning 커널 경고 이상

# 예제 규칙
kern.*                          /var/log/kern.log
*.info;mail.none;authpriv.none  /var/log/messages
authpriv.*                      /var/log/secure
mail.*                          /var/log/maillog
cron.*                          /var/log/cron
*.emerg                         :omusrmsg:*
```

### rsyslog 규칙 문법

```bash
# 전통적 문법
facility.priority    action

# 예제
*.info              /var/log/messages
mail.*              /var/log/mail.log
kern.warning        /var/log/kern.log

# 여러 facility
mail,news.info      /var/log/mail-news.log

# Priority 선택
*.=warning          /var/log/warning.log  # warning만
*.!error            /var/log/non-error.log  # error 제외
*.>=warning         /var/log/important.log  # warning 이상

# 여러 대상
*.emerg             :omusrmsg:*  # 모든 사용자에게
*.alert             root,admin   # 특정 사용자에게
*.crit              |/dev/xconsole  # 파이프

# 원격 서버
*.* @@remote-server:514  # TCP
*.* @remote-server:514   # UDP

# 프로그램 필터
:programname, isequal, "sshd"    /var/log/ssh.log

# RainerScript (고급)
if $programname == 'myapp' then {
    action(type="omfile" file="/var/log/myapp.log")
    stop
}

if $msg contains 'error' then {
    action(type="omfile" file="/var/log/errors.log")
}
```

### rsyslog 템플릿

```bash
# /etc/rsyslog.conf 또는 /etc/rsyslog.d/*.conf

# 커스텀 템플릿
template(name="CustomFormat" type="string"
    string="%timestamp% %hostname% %syslogtag% %msg%\n"
)

# 날짜별 파일
template(name="DailyLog" type="string"
    string="/var/log/app-%$YEAR%-%$MONTH%-%$DAY%.log"
)

# 사용
*.* ?CustomFormat
*.* ?DailyLog

# JSON 형식
template(name="JsonFormat" type="list") {
    constant(value="{")
    constant(value="\"timestamp\":\"")
    property(name="timereported" dateFormat="rfc3339")
    constant(value="\",\"host\":\"")
    property(name="hostname")
    constant(value="\",\"severity\":\"")
    property(name="syslogseverity-text")
    constant(value="\",\"message\":\"")
    property(name="msg" format="json")
    constant(value="\"}\n")
}

*.* ?JsonFormat;RSYSLOG_FileFormat
```

### 필터링 예제

```bash
# /etc/rsyslog.d/myapp.conf

# 특정 애플리케이션
:programname, isequal, "myapp"      /var/log/myapp.log
& stop  # 이후 규칙 중지

# SSH 로그인
:programname, isequal, "sshd"       /var/log/ssh-auth.log

# 특정 메시지 포함
:msg, contains, "Failed password"   /var/log/failed-login.log

# 정규식
:msg, regex, "error|warning"        /var/log/important.log

# IP 주소
:msg, contains, "192.168.1.100"     /var/log/client-100.log

# facility와 프로그램 조합
if $syslogfacility-text == 'local0' and $programname == 'myapp' then {
    action(type="omfile" file="/var/log/myapp-local0.log")
    stop
}

# 설정 적용
$ sudo systemctl restart rsyslog

# 테스트
$ logger -t myapp "Test message"
$ tail /var/log/myapp.log
```

---

## journald

### journalctl 기본

```bash
# 전체 로그
$ journalctl

# 최근 로그
$ journalctl -n 50
$ journalctl -n 100 --no-pager

# 실시간 (tail -f)
$ journalctl -f
$ journalctl -f -n 20

# 부팅별
$ journalctl --list-boots
$ journalctl -b          # 현재 부팅
$ journalctl -b -1       # 이전 부팅
$ journalctl -b 0        # 현재 부팅

# 커널 메시지
$ journalctl -k
$ journalctl --dmesg
$ journalctl -b -k       # 현재 부팅의 커널 메시지
```

### 시간 범위 필터

```bash
# 특정 시간부터
$ journalctl --since "2024-11-17 00:00:00"
$ journalctl --since "1 hour ago"
$ journalctl --since "yesterday"
$ journalctl --since "2 days ago"
$ journalctl --since "10 minutes ago"
$ journalctl --since "2024-11-17" --until "2024-11-18"

# 상대 시간
$ journalctl --since "09:00" --until "17:00"
$ journalctl --since "today"

# 조합
$ journalctl --since "2024-11-01" --until "2024-11-17 23:59:59"
```

### 필터링

```bash
# Unit/서비스별
$ journalctl -u nginx
$ journalctl -u nginx.service
$ journalctl -u ssh
$ journalctl -u nginx -u postgresql

# Priority별
$ journalctl -p err            # 에러 이상
$ journalctl -p warning        # 경고 이상
$ journalctl -p 0..3           # emerg, alert, crit, err
# 0=emerg, 1=alert, 2=crit, 3=err, 4=warning, 5=notice, 6=info, 7=debug

# 프로세스 ID
$ journalctl _PID=1234

# 실행 파일
$ journalctl _EXE=/usr/bin/nginx
$ journalctl _COMM=nginx

# 사용자
$ journalctl _UID=1000

# 조합
$ journalctl -u nginx --since "1 hour ago" -p err
$ journalctl _UID=1000 --since today

# 메시지 패턴 (grep)
$ journalctl -u nginx | grep "error"
$ journalctl --since "1 hour ago" | grep -i "failed"
```

### 출력 형식

```bash
# 기본 (short)
$ journalctl

# 자세히
$ journalctl -o verbose
$ journalctl -o verbose-json

# JSON
$ journalctl -o json
$ journalctl -o json-pretty

# 메시지만
$ journalctl -o cat

# ISO 타임스탬프
$ journalctl -o short-iso
$ journalctl -o short-precise

# syslog 형식
$ journalctl -o syslog

# export (바이너리)
$ journalctl -o export > journal.export
$ journalctl --file=journal.export
```

### journald 설정

```bash
# /etc/systemd/journald.conf
$ sudo vi /etc/systemd/journald.conf

[Journal]
# 저장 위치
Storage=persistent        # /var/log/journal
#Storage=volatile         # /run/log/journal (메모리)
#Storage=auto             # /var 있으면 persistent

# 크기 제한
SystemMaxUse=500M        # 최대 디스크 사용
SystemKeepFree=1G        # 남겨둘 여유 공간
SystemMaxFileSize=100M   # 파일당 최대 크기

# 런타임 (메모리)
RuntimeMaxUse=200M
RuntimeKeepFree=512M
RuntimeMaxFileSize=50M

# 보존 기간
MaxRetentionSec=1month
MaxFileSec=1week

# 전송
ForwardToSyslog=yes      # rsyslog로 전송
ForwardToKMsg=no
ForwardToConsole=no
ForwardToWall=yes

# 압축
Compress=yes

# 동기화
SyncIntervalSec=5m

# 설정 적용
$ sudo systemctl restart systemd-journald
```

### journald 관리

```bash
# 디스크 사용량
$ journalctl --disk-usage
Archived and active journals take up 512.0M in the file system.

# 오래된 로그 정리
$ sudo journalctl --vacuum-time=7d    # 7일 이전 삭제
$ sudo journalctl --vacuum-size=100M  # 100MB로 제한
$ sudo journalctl --vacuum-files=5    # 5개 파일만

# 로그 검증
$ sudo journalctl --verify

# 로그 회전
$ sudo systemctl kill --kill-who=main --signal=SIGUSR2 systemd-journald

# 영구 저장 활성화
$ sudo mkdir -p /var/log/journal
$ sudo systemd-tmpfiles --create --prefix /var/log/journal
$ sudo systemctl restart systemd-journald

# 확인
$ ls -la /var/log/journal/
```

---

## 로그 파일

### 주요 로그 파일

```bash
# 시스템 로그
/var/log/syslog          # 일반 시스템 로그 (Debian/Ubuntu)
/var/log/messages        # 일반 시스템 로그 (Red Hat/Fedora)
/var/log/kern.log        # 커널 로그
/var/log/dmesg           # 부팅 메시지

# 인증
/var/log/auth.log        # 인증 로그 (Debian/Ubuntu)
/var/log/secure          # 인증 로그 (Red Hat/Fedora)

# 서비스
/var/log/apache2/        # Apache 웹 서버
/var/log/nginx/          # Nginx 웹 서버
/var/log/mysql/          # MySQL
/var/log/postgresql/     # PostgreSQL

# 애플리케이션
/var/log/apt/            # APT 패키지 관리
/var/log/dpkg.log        # dpkg
/var/log/yum.log         # YUM
/var/log/cron            # Cron 작업

# 기타
/var/log/boot.log        # 부팅 로그
/var/log/faillog         # 실패한 로그인
/var/log/lastlog         # 마지막 로그인
/var/log/wtmp            # 로그인 기록 (바이너리)
/var/log/btmp            # 실패한 로그인 (바이너리)
```

### 로그 파일 조회

```bash
# 실시간 모니터링
$ tail -f /var/log/syslog
$ tail -f /var/log/auth.log
$ tail -f /var/log/nginx/access.log

# 최근 로그
$ tail -n 100 /var/log/syslog
$ tail -n 50 /var/log/auth.log

# 검색
$ grep "error" /var/log/syslog
$ grep -i "failed" /var/log/auth.log
$ grep "192.168.1.100" /var/log/nginx/access.log

# 여러 파일 검색
$ grep -r "error" /var/log/nginx/
$ grep -h "error" /var/log/nginx/*.log

# 날짜 범위 (로그에 날짜 포함 시)
$ grep "Nov 17" /var/log/syslog
$ awk '/Nov 17 09:/,/Nov 17 10:/' /var/log/syslog

# 통계
$ grep "error" /var/log/syslog | wc -l
$ grep "GET" /var/log/nginx/access.log | wc -l
```

### 바이너리 로그

```bash
# wtmp - 로그인 기록
$ last
$ last -n 10
$ last -s today
$ last user
$ last reboot

# btmp - 실패한 로그인
$ sudo lastb
$ sudo lastb | head -20

# lastlog - 마지막 로그인
$ lastlog
$ lastlog -u user

# utmp - 현재 로그인
$ who
$ w

# faillog - 로그인 실패 횟수
$ faillog
$ sudo faillog -u user
$ sudo faillog -r -u user  # 리셋
```

---

## 로그 회전

### logrotate 설정

```bash
# logrotate 설정 파일
/etc/logrotate.conf       # 전역 설정
/etc/logrotate.d/         # 서비스별 설정

# /etc/logrotate.conf
$ cat /etc/logrotate.conf
# 주별 회전
weekly

# 4주치 보관
rotate 4

# 새 로그 파일 생성
create

# 날짜로 이름 지정
dateext

# 압축
compress

# 서비스별 설정 포함
include /etc/logrotate.d

# /var/log/wtmp, /var/log/btmp 등 특수 설정
/var/log/wtmp {
    monthly
    create 0664 root utmp
    minsize 1M
    rotate 1
}
```

### logrotate 규칙

```bash
# /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily                 # 매일 회전
    rotate 14             # 14일치 보관
    compress              # 압축
    delaycompress         # 최신 파일은 압축 안 함
    notifempty            # 빈 파일은 회전 안 함
    create 0640 nginx adm # 새 파일 생성
    sharedscripts         # 스크립트 한 번만 실행
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}

# 회전 빈도
hourly      # 시간별
daily       # 일별
weekly      # 주별
monthly     # 월별

# 크기 기반
size 100M   # 100MB 이상 시
minsize 1M  # 최소 크기

# 보관 기간
rotate 7    # 7개 보관
maxage 30   # 30일 후 삭제

# 압축
compress
nocompress
compresscmd gzip
compressext .gz
delaycompress

# 파일 생성
create 0644 user group
nocreate

# 누락 허용
missingok
nomissingok

# 빈 파일
notifempty
ifempty

# 스크립트
prerotate
    # 회전 전 실행
endscript

postrotate
    # 회전 후 실행
    systemctl reload nginx
endscript

# 여러 파일
/var/log/myapp/*.log /var/log/myapp/debug.log {
    daily
    rotate 7
}
```

### logrotate 실행

```bash
# 수동 실행
$ sudo logrotate /etc/logrotate.conf

# 강제 실행 (테스트)
$ sudo logrotate -f /etc/logrotate.conf

# 디버그 모드 (실제 실행 안 함)
$ sudo logrotate -d /etc/logrotate.conf
$ sudo logrotate -d /etc/logrotate.d/nginx

# verbose
$ sudo logrotate -v /etc/logrotate.conf

# 상태 파일
$ cat /var/lib/logrotate/status
logrotate state -- version 2
"/var/log/nginx/access.log" 2024-11-17-3:0:0
"/var/log/nginx/error.log" 2024-11-17-3:0:0

# cron 작업 (자동 실행)
$ cat /etc/cron.daily/logrotate
#!/bin/sh
/usr/sbin/logrotate /etc/logrotate.conf
```

### logrotate 예제

```bash
# 애플리케이션 로그
$ sudo vi /etc/logrotate.d/myapp
/opt/myapp/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 myapp myapp
    sharedscripts
    postrotate
        systemctl reload myapp > /dev/null 2>&1 || true
    endscript
}

# 크기 기반 회전
/var/log/bigapp/*.log {
    size 100M
    rotate 10
    compress
    missingok
    notifempty
}

# 날짜 형식 회전
/var/log/dated/*.log {
    daily
    rotate 365
    compress
    dateext
    dateformat -%Y%m%d
    extension .log
    # 결과: app-20241117.log.gz
}
```

---

## 로그 분석

### 기본 분석 도구

```bash
# grep - 패턴 검색
$ grep "error" /var/log/syslog
$ grep -i "failed" /var/log/auth.log  # 대소문자 무시
$ grep -v "normal" /var/log/app.log   # 제외
$ grep -E "error|warning" /var/log/syslog  # 정규식

# awk - 필드 처리
$ awk '/error/ {print $0}' /var/log/syslog
$ awk '{print $1, $5}' /var/log/nginx/access.log
$ awk '$9 == 404' /var/log/nginx/access.log  # 404 에러

# sed - 스트림 편집
$ sed -n '/error/p' /var/log/syslog
$ sed -n '/2024-11-17 09:/,/2024-11-17 10:/p' /var/log/syslog

# cut - 필드 추출
$ cut -d' ' -f1-3 /var/log/syslog
$ cut -d':' -f1 /etc/passwd

# sort, uniq - 정렬 및 중복 제거
$ awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c
$ awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c  # HTTP 상태 코드
```

### 통계 및 집계

```bash
# IP별 접속 수 (Nginx)
$ awk '{print $1}' /var/log/nginx/access.log | \
    sort | uniq -c | sort -rn | head -20

# HTTP 상태 코드별 집계
$ awk '{print $9}' /var/log/nginx/access.log | \
    sort | uniq -c | sort -rn

# 시간대별 요청 수
$ awk '{print $4}' /var/log/nginx/access.log | \
    cut -d: -f2 | sort | uniq -c

# 가장 많이 요청된 URL
$ awk '{print $7}' /var/log/nginx/access.log | \
    sort | uniq -c | sort -rn | head -20

# 실패한 로그인 시도 (auth.log)
$ grep "Failed password" /var/log/auth.log | \
    awk '{print $(NF-3)}' | sort | uniq -c | sort -rn

# 사용자별 sudo 사용
$ grep "sudo" /var/log/auth.log | \
    grep "COMMAND" | awk '{print $6}' | \
    cut -d= -f2 | sort | uniq -c
```

### 로그 분석 스크립트

```bash
# Nginx 접속 분석
#!/bin/bash
LOG="/var/log/nginx/access.log"

echo "=== Nginx Access Log Analysis ==="
echo "Date: $(date)"
echo

echo "Top 10 IP addresses:"
awk '{print $1}' "$LOG" | sort | uniq -c | sort -rn | head -10
echo

echo "HTTP Status Code Distribution:"
awk '{print $9}' "$LOG" | sort | uniq -c | sort
echo

echo "Top 10 Requested URLs:"
awk '{print $7}' "$LOG" | sort | uniq -c | sort -rn | head -10
echo

echo "Requests by Hour:"
awk '{print $4}' "$LOG" | cut -d: -f2 | sort | uniq -c
echo

echo "User Agents (Top 5):"
awk -F'"' '{print $6}' "$LOG" | sort | uniq -c | sort -rn | head -5
```

### 실시간 모니터링

```bash
# 실패한 SSH 로그인 모니터링
$ tail -f /var/log/auth.log | grep "Failed password"

# 에러만 표시
$ tail -f /var/log/syslog | grep --line-buffered -i error

# 여러 로그 동시 모니터링
$ tail -f /var/log/syslog /var/log/auth.log

# multitail (설치 필요)
$ sudo apt install multitail
$ multitail /var/log/syslog /var/log/auth.log
$ multitail -s 2 /var/log/nginx/access.log /var/log/nginx/error.log
```

---

## 중앙 집중식 로깅

### rsyslog 서버 설정

```bash
# 서버 측 (/etc/rsyslog.conf)
$ sudo vi /etc/rsyslog.conf

# UDP 수신 활성화
module(load="imudp")
input(type="imudp" port="514")

# TCP 수신 활성화 (권장)
module(load="imtcp")
input(type="imtcp" port="514")

# 원격 로그 저장
$template RemoteLog,"/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log"
*.* ?RemoteLog
& stop

# 방화벽 허용
$ sudo ufw allow 514/tcp
$ sudo ufw allow 514/udp

# 재시작
$ sudo systemctl restart rsyslog

# 클라이언트 측 (/etc/rsyslog.conf)
$ sudo vi /etc/rsyslog.conf

# 모든 로그를 서버로 전송
*.* @@log-server:514  # TCP
*.* @log-server:514   # UDP

# 특정 로그만
*.err @@log-server:514
mail.* @@log-server:514

# 재시작
$ sudo systemctl restart rsyslog
```

### 고급 중앙 로깅

```bash
# TLS 암호화 전송
# 서버
$ sudo vi /etc/rsyslog.conf
module(load="imtcp"
    StreamDriver.Name="gtls"
    StreamDriver.Mode="1"
    StreamDriver.Authmode="anon"
)

input(type="imtcp" port="6514")

# 클라이언트
*.* @@(o)log-server:6514

# Elasticsearch 전송 (Elastic Stack)
module(load="omelasticsearch")
template(name="es-template" type="list") {
    ...
}
action(type="omelasticsearch"
    server="localhost"
    serverport="9200"
    template="es-template")
```

---

## 로그 보안

### 로그 파일 권한

```bash
# 일반적인 권한
$ ls -l /var/log/
-rw-r----- 1 syslog adm  /var/log/syslog
-rw-r----- 1 syslog adm  /var/log/auth.log
-rw-r--r-- 1 root   root /var/log/dmesg

# 민감한 로그는 제한적 권한
$ sudo chmod 640 /var/log/auth.log
$ sudo chown root:adm /var/log/auth.log

# 로그 그룹에 사용자 추가
$ sudo usermod -aG adm user
```

### 로그 무결성

```bash
# AIDE (Advanced Intrusion Detection Environment)
$ sudo apt install aide
$ sudo aideinit
$ sudo aide --check

# 로그 서명
$ sudo vi /etc/logrotate.d/signed
/var/log/important.log {
    daily
    postrotate
        md5sum /var/log/important.log > /var/log/important.log.md5
        gpg --sign /var/log/important.log.md5
    endscript
}

# 원격 백업
rsync -avz /var/log/ backup-server:/backup/logs/
```

### 로그 분리

```bash
# 사용자별 로그 분리
# /etc/rsyslog.d/user-logs.conf
template(name="UserLog" type="string"
    string="/var/log/users/%programname%-%$YEAR%%$MONTH%%$DAY%.log"
)

if $syslogfacility-text == 'local0' then {
    action(type="omfile" dynaFile="UserLog")
    stop
}

# 애플리케이션별 로그 격리
:programname, isequal, "webapp" /var/log/webapp/app.log
& stop
```

---

## 실전 예제

### 종합 로그 모니터링 스크립트

```bash
#!/bin/bash
# log-monitor.sh

LOG="/var/log/syslog"
AUTH="/var/log/auth.log"
ALERT_EMAIL="admin@example.com"

# 에러 체크
ERRORS=$(grep -c "error" "$LOG")
if [ $ERRORS -gt 100 ]; then
    echo "High error rate: $ERRORS errors" | \
        mail -s "Alert: High Error Rate" "$ALERT_EMAIL"
fi

# 실패한 로그인 체크
FAILED=$(grep -c "Failed password" "$AUTH")
if [ $FAILED -gt 10 ]; then
    echo "Suspicious login attempts: $FAILED" | \
        mail -s "Security Alert" "$ALERT_EMAIL"
fi

# 디스크 사용량 체크
DISK=$(df /var/log | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK -gt 80 ]; then
    echo "/var/log disk usage: $DISK%" | \
        mail -s "Disk Space Alert" "$ALERT_EMAIL"
fi
```

---

## 요약

로깅 핵심 도구:

1. **rsyslog**: 전통적 시스템 로깅
2. **journald**: systemd 바이너리 로깅
3. **logrotate**: 로그 회전 및 압축
4. **logger**: 수동 로그 생성

주요 로그 위치:
- /var/log/syslog (시스템)
- /var/log/auth.log (인증)
- /var/log/kern.log (커널)

명령어:
```bash
journalctl -u service -f         # 실시간 로그
tail -f /var/log/syslog           # 전통적 방식
grep "error" /var/log/syslog      # 검색
logrotate -f /etc/logrotate.conf  # 강제 회전
```

---

[← cron으로 돌아가기](cron.md)

[← 목차로 돌아가기](../README.md)

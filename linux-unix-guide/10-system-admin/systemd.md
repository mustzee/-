# systemd

## 목차
- [소개](#소개)
- [서비스 관리](#서비스-관리)
- [Unit 파일](#unit-파일)
- [타겟 (Targets)](#타겟-targets)
- [타이머 (Timers)](#타이머-timers)
- [journald 로깅](#journald-로깅)
- [시스템 부팅](#시스템-부팅)
- [리소스 제어](#리소스-제어)
- [네트워크 관리](#네트워크-관리)
- [문제 해결](#문제-해결)
- [실전 예제](#실전-예제)

---

## 소개

systemd는 현대 Linux 배포판의 init 시스템이자 시스템 및 서비스 관리자입니다.

### systemd 개요

```bash
# systemd 버전 확인
$ systemd --version
systemd 255 (255.2-1)
+PAM +AUDIT +SELINUX +APPARMOR +IMA +SMACK ...

# PID 1 확인
$ ps -p 1
  PID TTY          TIME CMD
    1 ?        00:00:02 systemd

# systemd 구조
$ pstree -p 1
systemd(1)─┬─accounts-daemon(584)
           ├─cron(571)
           ├─dbus-daemon(573)
           ├─networkd(387)
           ├─sshd(628)
           └─systemd-journal(203)

# systemd 디렉토리
/etc/systemd/          # 사용자 설정
/lib/systemd/          # 패키지 기본 설정
/run/systemd/          # 런타임 설정
/usr/lib/systemd/      # 시스템 기본 설정
```

### Unit 타입

```bash
# systemd unit 타입들
.service    # 서비스 (데몬)
.socket     # 소켓 기반 활성화
.device     # 하드웨어 장치
.mount      # 마운트 포인트
.automount  # 자동 마운트
.swap       # 스왑 공간
.target     # Unit 그룹
.path       # 경로 기반 활성화
.timer      # 타이머 (cron 대체)
.slice      # 리소스 그룹
.scope      # 외부 프로세스 그룹

# 모든 unit 확인
$ systemctl list-units
$ systemctl list-units --all
$ systemctl list-units --type=service
$ systemctl list-units --type=timer
$ systemctl list-units --state=running
```

---

## 서비스 관리

### 기본 서비스 명령

```bash
# 서비스 상태 확인
$ systemctl status nginx
● nginx.service - A high performance web server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled)
     Active: active (running) since Mon 2024-11-17 09:00:00 KST
       Docs: man:nginx(8)
   Main PID: 1234 (nginx)
      Tasks: 5 (limit: 4915)
     Memory: 8.5M
        CPU: 125ms
     CGroup: /system.slice/nginx.service
             ├─1234 nginx: master process
             └─1235 nginx: worker process

# 서비스 시작
$ sudo systemctl start nginx

# 서비스 중지
$ sudo systemctl stop nginx

# 서비스 재시작
$ sudo systemctl restart nginx

# 설정 다시 로드 (중단 없이)
$ sudo systemctl reload nginx

# 재시작 또는 재로드 (가능하면 reload)
$ sudo systemctl reload-or-restart nginx

# 서비스 활성화 (부팅 시 자동 시작)
$ sudo systemctl enable nginx
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service

# 서비스 비활성화
$ sudo systemctl disable nginx
Removed /etc/systemd/system/multi-user.target.wants/nginx.service

# 활성화 및 시작 (한 번에)
$ sudo systemctl enable --now nginx

# 비활성화 및 중지
$ sudo systemctl disable --now nginx
```

### 서비스 조회

```bash
# 모든 서비스
$ systemctl list-units --type=service
$ systemctl list-units --type=service --all

# 실행 중인 서비스
$ systemctl list-units --type=service --state=running

# 실패한 서비스
$ systemctl list-units --type=service --state=failed
$ systemctl --failed

# 활성화된 서비스 (부팅 시 시작)
$ systemctl list-unit-files --type=service --state=enabled

# 특정 서비스 검색
$ systemctl list-units --type=service | grep nginx
$ systemctl list-unit-files | grep ssh

# 서비스 의존성 확인
$ systemctl list-dependencies nginx
$ systemctl list-dependencies nginx --all
$ systemctl list-dependencies nginx --reverse

# 서비스 파일 위치
$ systemctl show nginx -p FragmentPath
FragmentPath=/lib/systemd/system/nginx.service

# 서비스 상태 간단히
$ systemctl is-active nginx
active

$ systemctl is-enabled nginx
enabled

$ systemctl is-failed nginx
inactive
```

### 서비스 마스킹

```bash
# 서비스 마스킹 (완전히 차단)
$ sudo systemctl mask nginx
Created symlink /etc/systemd/system/nginx.service → /dev/null

# 마스킹된 서비스는 시작 불가
$ sudo systemctl start nginx
Failed to start nginx.service: Unit nginx.service is masked.

# 언마스킹
$ sudo systemctl unmask nginx
Removed /etc/systemd/system/nginx.service

# 마스크 상태 확인
$ systemctl is-enabled nginx
masked
```

### 서비스 프로퍼티

```bash
# 모든 프로퍼티 보기
$ systemctl show nginx

# 특정 프로퍼티
$ systemctl show nginx -p MainPID
MainPID=1234

$ systemctl show nginx -p ActiveState
ActiveState=active

$ systemctl show nginx -p CPUUsageNSec
CPUUsageNSec=125000000

# 여러 프로퍼티
$ systemctl show nginx -p MainPID -p MemoryCurrent -p CPUUsageNSec

# 프로퍼티 설정 (런타임)
$ sudo systemctl set-property nginx CPUQuota=50%
```

---

## Unit 파일

### Service Unit 파일 구조

```bash
# 예제: /etc/systemd/system/myapp.service
[Unit]
Description=My Application
Documentation=https://example.com/docs
After=network.target
Requires=network.target
Wants=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStartPre=/opt/myapp/scripts/pre-start.sh
ExecStart=/opt/myapp/bin/myapp --config /etc/myapp/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/opt/myapp/scripts/stop.sh
Restart=on-failure
RestartSec=10s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp
Environment="ENV=production"
EnvironmentFile=/etc/myapp/environment

[Install]
WantedBy=multi-user.target
```

### Service Type

```bash
# Type=simple (기본값)
# ExecStart가 메인 프로세스
[Service]
Type=simple
ExecStart=/usr/bin/myapp

# Type=forking
# 프로세스가 fork하고 부모는 종료
[Service]
Type=forking
PIDFile=/var/run/myapp.pid
ExecStart=/usr/bin/myapp --daemon

# Type=oneshot
# 일회성 작업, 완료될 때까지 대기
[Service]
Type=oneshot
ExecStart=/usr/bin/setup-script.sh
RemainAfterExit=yes

# Type=notify
# 프로세스가 systemd에 준비 완료 알림
[Service]
Type=notify
ExecStart=/usr/bin/myapp
NotifyAccess=main

# Type=idle
# 다른 작업이 끝날 때까지 대기
[Service]
Type=idle
ExecStart=/usr/bin/myapp
```

### Unit 파일 생성 및 수정

```bash
# 새 서비스 생성
$ sudo vi /etc/systemd/system/myapp.service

# 최소 예제
[Unit]
Description=My Application

[Service]
ExecStart=/usr/local/bin/myapp

[Install]
WantedBy=multi-user.target

# daemon-reload (설정 다시 로드)
$ sudo systemctl daemon-reload

# 서비스 활성화 및 시작
$ sudo systemctl enable --now myapp

# 서비스 편집 (안전)
$ sudo systemctl edit nginx
# 편집기에서 override 설정 입력
[Service]
CPUQuota=50%
MemoryLimit=1G

# 저장 위치: /etc/systemd/system/nginx.service.d/override.conf

# 전체 파일 편집
$ sudo systemctl edit --full myapp

# override 파일 삭제
$ sudo rm /etc/systemd/system/nginx.service.d/override.conf
$ sudo systemctl daemon-reload

# 서비스 파일 검증
$ systemd-analyze verify myapp.service
```

### 환경 변수

```bash
# Unit 파일에 직접
[Service]
Environment="VAR1=value1"
Environment="VAR2=value2"

# 환경 파일 사용
[Service]
EnvironmentFile=/etc/myapp/environment

# /etc/myapp/environment 내용
VAR1=value1
VAR2=value2
DATABASE_URL=postgres://localhost/mydb

# 여러 파일
[Service]
EnvironmentFile=/etc/default/myapp
EnvironmentFile=/etc/myapp/environment

# 런타임에 환경 변수 확인
$ sudo systemctl show myapp -p Environment
```

### 의존성 관리

```bash
# After/Before - 순서 지정
[Unit]
After=network.target
After=postgresql.service
Before=nginx.service

# Requires - 강한 의존성 (필수)
[Unit]
Requires=postgresql.service
# postgresql이 실패하면 이 서비스도 중지

# Wants - 약한 의존성 (권장)
[Unit]
Wants=redis.service
# redis 실패해도 이 서비스 계속 실행

# Conflicts - 충돌
[Unit]
Conflicts=another-service.service
# 둘 중 하나만 실행 가능

# BindsTo - 바인딩
[Unit]
BindsTo=postgresql.service
# postgresql이 중지되면 자동으로 중지

# PartOf - 일부
[Unit]
PartOf=multi-app.target
# 타겟이 중지/재시작되면 함께 중지/재시작
```

---

## 타겟 (Targets)

### 타겟 개요

```bash
# 타겟 = runlevel (SysV init의 런레벨과 유사)

# 주요 타겟
poweroff.target      # 시스템 종료 (runlevel 0)
rescue.target        # 복구 모드 (runlevel 1)
multi-user.target    # 다중 사용자, CLI (runlevel 3)
graphical.target     # GUI (runlevel 5)
reboot.target        # 재부팅 (runlevel 6)

# 현재 타겟 확인
$ systemctl get-default
graphical.target

# 기본 타겟 변경
$ sudo systemctl set-default multi-user.target
$ sudo systemctl set-default graphical.target

# 모든 타겟
$ systemctl list-units --type=target
$ systemctl list-units --type=target --all

# 활성 타겟
$ systemctl list-units --type=target --state=active
```

### 타겟 전환

```bash
# 특정 타겟으로 전환
$ sudo systemctl isolate multi-user.target
$ sudo systemctl isolate graphical.target
$ sudo systemctl isolate rescue.target

# 복구 모드
$ sudo systemctl rescue

# 긴급 모드
$ sudo systemctl emergency

# 시스템 종료
$ sudo systemctl poweroff
$ sudo systemctl halt

# 재부팅
$ sudo systemctl reboot

# 절전
$ sudo systemctl suspend
$ sudo systemctl hibernate
$ sudo systemctl hybrid-sleep
```

### 사용자 정의 타겟

```bash
# 커스텀 타겟 생성
$ sudo vi /etc/systemd/system/myapp.target
[Unit]
Description=My Application Stack
Requires=multi-user.target
After=multi-user.target
Wants=postgresql.service
Wants=redis.service
Wants=nginx.service
Wants=myapp.service

[Install]
WantedBy=multi-user.target

# 활성화
$ sudo systemctl daemon-reload
$ sudo systemctl enable myapp.target

# 타겟 시작
$ sudo systemctl start myapp.target

# 타겟에 서비스 추가
$ sudo systemctl add-wants myapp.target another-service.service
```

---

## 타이머 (Timers)

### 타이머 기본

```bash
# 타이머 목록
$ systemctl list-timers
NEXT                         LEFT          LAST  PASSED UNIT
Mon 2024-11-17 03:00:00 KST  8h left       -     -      backup.timer
Mon 2024-11-17 06:00:00 KST  11h left      -     -      cleanup.timer

# 모든 타이머 (비활성 포함)
$ systemctl list-timers --all

# 타이머 상태
$ systemctl status backup.timer
```

### 타이머 생성

```bash
# 1. 서비스 파일 생성
$ sudo vi /etc/systemd/system/backup.service
[Unit]
Description=Backup Task

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=backup
StandardOutput=journal

# 2. 타이머 파일 생성
$ sudo vi /etc/systemd/system/backup.timer
[Unit]
Description=Backup Timer
Requires=backup.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 03:00:00
Persistent=true
RandomizedDelaySec=30m

[Install]
WantedBy=timers.target

# 3. 활성화 및 시작
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now backup.timer

# 타이머 확인
$ systemctl list-timers backup.timer
$ systemctl status backup.timer
```

### OnCalendar 문법

```bash
# 시간 지정 예제
[Timer]
# 매일 03:00
OnCalendar=*-*-* 03:00:00
OnCalendar=03:00

# 매주 월요일 09:00
OnCalendar=Mon *-*-* 09:00:00
OnCalendar=Mon 09:00

# 매월 1일 00:00
OnCalendar=*-*-01 00:00:00

# 매 15분마다
OnCalendar=*:0/15

# 평일 09:00-17:00, 매시간
OnCalendar=Mon..Fri *-*-* 09..17:00:00

# 여러 시간 지정
OnCalendar=06:00
OnCalendar=12:00
OnCalendar=18:00

# 문법 확인
$ systemd-analyze calendar "Mon *-*-* 09:00:00"
  Original form: Mon *-*-* 09:00:00
Normalized form: Mon *-*-* 09:00:00
    Next elapse: Mon 2024-11-18 09:00:00 KST
```

### 다양한 타이머 유형

```bash
# OnBootSec - 부팅 후 시간
[Timer]
OnBootSec=15min

# OnStartupSec - systemd 시작 후
[Timer]
OnStartupSec=5min

# OnActiveSec - 타이머 활성화 후
[Timer]
OnActiveSec=1h

# OnUnitActiveSec - 서비스 마지막 실행 후
[Timer]
OnUnitActiveSec=1d

# OnUnitInactiveSec - 서비스 마지막 비활성화 후
[Timer]
OnUnitInactiveSec=30min

# 복합 예제
[Timer]
OnBootSec=10min
OnUnitActiveSec=1d
Persistent=true
# 부팅 10분 후 실행, 이후 매일
```

### 타이머 고급 설정

```bash
# 영구성 (부팅 중 놓친 실행)
[Timer]
OnCalendar=daily
Persistent=true
# 시스템이 꺼져있어 놓친 작업을 즉시 실행

# 무작위 지연
[Timer]
OnCalendar=hourly
RandomizedDelaySec=10m
# 0-10분 사이 무작위 지연

# 정확도
[Timer]
OnCalendar=*:0/5
AccuracySec=1s
# 1초 정확도 (기본값은 1분)

# 타이머만 활성화
[Timer]
OnCalendar=daily
Unit=backup.service
# 다른 이름의 서비스 지정
```

---

## journald 로깅

### 로그 조회

```bash
# 전체 로그
$ journalctl

# 최근 로그
$ journalctl -n 50  # 최근 50줄
$ journalctl -n 100 --no-pager

# 실시간 로그 (tail -f)
$ journalctl -f
$ journalctl -f -n 20

# 특정 서비스
$ journalctl -u nginx
$ journalctl -u nginx -u postgresql

# 시간 범위
$ journalctl --since "2024-11-17 00:00:00"
$ journalctl --since "1 hour ago"
$ journalctl --since "yesterday"
$ journalctl --since "2 days ago"
$ journalctl --until "2024-11-17 23:59:59"
$ journalctl --since "09:00" --until "17:00"

# 부팅별 로그
$ journalctl --list-boots
$ journalctl -b     # 현재 부팅
$ journalctl -b -1  # 이전 부팅
$ journalctl -b 0   # 현재 부팅

# 우선순위별
$ journalctl -p err  # 에러 이상
$ journalctl -p warning  # 경고 이상
# emerg, alert, crit, err, warning, notice, info, debug

# 조합
$ journalctl -u nginx --since "1 hour ago" -p err
```

### 로그 필터링

```bash
# 프로세스 ID
$ journalctl _PID=1234

# 사용자
$ journalctl _UID=1000

# 실행 파일
$ journalctl _EXE=/usr/bin/nginx

# 커널 메시지
$ journalctl -k
$ journalctl --dmesg

# grep과 함께
$ journalctl -u nginx | grep "error"
$ journalctl --since "1 hour ago" | grep -i "failed"

# JSON 출력
$ journalctl -u nginx -o json
$ journalctl -u nginx -o json-pretty

# 출력 형식
$ journalctl -o verbose  # 자세히
$ journalctl -o cat      # 메시지만
$ journalctl -o short-iso  # ISO 타임스탬프
```

### 로그 관리

```bash
# 디스크 사용량
$ journalctl --disk-usage
Archived and active journals take up 512.0M in the file system.

# 로그 크기 제한 확인
$ cat /etc/systemd/journald.conf
[Journal]
SystemMaxUse=500M
SystemKeepFree=1G
SystemMaxFileSize=100M
RuntimeMaxUse=200M

# 설정 적용
$ sudo systemctl restart systemd-journald

# 오래된 로그 삭제
$ sudo journalctl --vacuum-time=7d  # 7일 이전 삭제
$ sudo journalctl --vacuum-size=100M  # 100MB로 제한
$ sudo journalctl --vacuum-files=5  # 5개 파일만 유지

# 로그 검증
$ sudo journalctl --verify

# 로그 회전
$ sudo systemctl kill --kill-who=main --signal=SIGUSR2 systemd-journald.service
```

### 로그 영구 저장

```bash
# 기본적으로 /run/log/journal (재부팅 시 삭제)
# 영구 저장 활성화

# 저장 디렉토리 생성
$ sudo mkdir -p /var/log/journal
$ sudo systemd-tmpfiles --create --prefix /var/log/journal

# journald.conf 설정
$ sudo vi /etc/systemd/journald.conf
[Journal]
Storage=persistent

# 재시작
$ sudo systemctl restart systemd-journald

# 확인
$ ls /var/log/journal/
```

---

## 시스템 부팅

### 부팅 분석

```bash
# 부팅 시간 분석
$ systemd-analyze
Startup finished in 3.245s (kernel) + 8.123s (userspace) = 11.368s
graphical.target reached after 8.056s in userspace

# 각 서비스별 시간
$ systemd-analyze blame
5.234s mysql.service
3.891s nginx.service
2.456s NetworkManager.service
...

# 타임라인 생성 (SVG)
$ systemd-analyze plot > boot.svg
$ firefox boot.svg

# 크리티컬 체인 (가장 긴 경로)
$ systemd-analyze critical-chain
graphical.target @8.056s
└─multi-user.target @8.055s
  └─mysql.service @2.821s +5.234s
    └─network.target @2.820s
      └─NetworkManager.service @367ms +2.456s
```

### 부팅 타겟 설정

```bash
# GRUB에서 부팅 타겟 지정
# GRUB 메뉴에서 'e' 누르고
linux ... systemd.unit=rescue.target

# 또는
linux ... systemd.unit=multi-user.target

# 영구 변경
$ sudo systemctl set-default multi-user.target
$ sudo systemctl set-default graphical.target

# 확인
$ systemctl get-default
```

### 부팅 문제 해결

```bash
# 복구 모드로 부팅
# GRUB에서
systemd.unit=rescue.target

# 긴급 모드
systemd.unit=emergency.target

# 루트 쉘
init=/bin/bash

# 부팅 로그 확인
$ journalctl -xb
$ journalctl -b -p err

# 실패한 서비스
$ systemctl --failed

# 서비스 의존성 문제
$ systemctl list-dependencies --all graphical.target
```

---

## 리소스 제어

### CPU 제한

```bash
# Unit 파일에서
[Service]
CPUQuota=50%  # CPU의 50%로 제한
CPUWeight=100  # 상대적 가중치 (1-10000)

# 런타임에 설정
$ sudo systemctl set-property nginx.service CPUQuota=50%

# 확인
$ systemctl show nginx -p CPUQuota
CPUQuota=50%

# cgroup 확인
$ cat /sys/fs/cgroup/system.slice/nginx.service/cpu.max
50000 100000
```

### 메모리 제한

```bash
# Unit 파일에서
[Service]
MemoryLimit=1G
MemoryMax=1G
MemoryHigh=800M  # soft limit
MemoryLow=100M   # 보호 수준

# 런타임 설정
$ sudo systemctl set-property nginx.service MemoryLimit=1G
$ sudo systemctl set-property nginx.service MemoryMax=1G

# 확인
$ systemctl show nginx -p MemoryLimit -p MemoryMax

# OOM 정책
[Service]
OOMPolicy=stop  # kill, continue, stop
OOMScoreAdjust=-1000  # OOM killer 우선순위
```

### I/O 제한

```bash
# Unit 파일에서
[Service]
IOWeight=100  # I/O 가중치 (10-1000)
IOReadBandwidthMax=/dev/sda 10M
IOWriteBandwidthMax=/dev/sda 5M
IOReadIOPSMax=/dev/sda 1000
IOWriteIOPSMax=/dev/sda 500

# 런타임 설정
$ sudo systemctl set-property nginx.service \
    IOWriteBandwidthMax="/dev/sda 5M"
```

### 태스크 제한

```bash
# 프로세스/스레드 수 제한
[Service]
TasksMax=100

# 런타임 설정
$ sudo systemctl set-property nginx.service TasksMax=100

# 무제한
$ sudo systemctl set-property nginx.service TasksMax=infinity
```

### Slice 사용

```bash
# Slice로 리소스 그룹 관리
$ sudo vi /etc/systemd/system/myapps.slice
[Unit]
Description=My Applications Slice
Before=slices.target

[Slice]
CPUQuota=200%
MemoryLimit=4G

# 서비스를 slice에 추가
[Service]
Slice=myapps.slice

# slice 시작
$ sudo systemctl start myapps.slice

# slice 내 서비스 확인
$ systemd-cgls myapps.slice
```

---

## 네트워크 관리

### systemd-networkd

```bash
# systemd-networkd 활성화
$ sudo systemctl enable --now systemd-networkd

# 네트워크 설정 파일 생성
$ sudo vi /etc/systemd/network/20-wired.network
[Match]
Name=eth0

[Network]
DHCP=yes

# 정적 IP
$ sudo vi /etc/systemd/network/20-wired.network
[Match]
Name=eth0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=8.8.8.8
DNS=8.8.4.4

# 재시작
$ sudo systemctl restart systemd-networkd

# 상태 확인
$ networkctl
$ networkctl status eth0
$ networkctl list
```

### systemd-resolved

```bash
# systemd-resolved 활성화
$ sudo systemctl enable --now systemd-resolved

# DNS 설정 연결
$ sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

# DNS 상태
$ resolvectl status
$ resolvectl query example.com

# DNS 캐시 초기화
$ sudo resolvectl flush-caches

# DNS 통계
$ resolvectl statistics
```

---

## 문제 해결

### 서비스 디버깅

```bash
# 자세한 상태
$ systemctl status nginx -l --no-pager

# 로그 확인
$ journalctl -u nginx -n 100 --no-pager
$ journalctl -u nginx -f

# 설정 검증
$ systemd-analyze verify nginx.service

# 의존성 문제
$ systemctl list-dependencies nginx --all
$ systemctl list-dependencies nginx --reverse

# cgroup 확인
$ systemd-cgls
$ systemd-cgtop
```

### 일반적인 문제

```bash
# 1. 서비스 시작 실패
$ systemctl status failed-service
$ journalctl -u failed-service -n 50

# 2. 의존성 순환
$ systemd-analyze verify problematic.service
# 의존성 조정 필요

# 3. 타임아웃
[Service]
TimeoutStartSec=90s
TimeoutStopSec=30s

# 4. 권한 문제
[Service]
User=myapp
Group=myapp
# 파일 권한 확인

# 5. 환경 변수
$ systemctl show myapp -p Environment
# EnvironmentFile 확인
```

---

## 실전 예제

### 웹 애플리케이션 서비스

```bash
# /etc/systemd/system/webapp.service
[Unit]
Description=Web Application
Documentation=https://example.com/docs
After=network.target postgresql.service redis.service
Wants=postgresql.service redis.service

[Service]
Type=notify
User=webapp
Group=webapp
WorkingDirectory=/opt/webapp

# 환경 설정
Environment="PORT=8000"
EnvironmentFile=/etc/webapp/env

# 시작 전 체크
ExecStartPre=/opt/webapp/scripts/pre-start.sh

# 메인 프로세스
ExecStart=/opt/webapp/venv/bin/gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 60 \
    app:application

# 재로드
ExecReload=/bin/kill -HUP $MAINPID

# 종료
ExecStopPost=/opt/webapp/scripts/cleanup.sh

# 재시작 정책
Restart=always
RestartSec=10s

# 리소스 제한
CPUQuota=200%
MemoryMax=2G
TasksMax=1000

# 보안
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/webapp/data

# 로깅
StandardOutput=journal
StandardError=journal
SyslogIdentifier=webapp

[Install]
WantedBy=multi-user.target
```

### 백업 타이머

```bash
# /etc/systemd/system/backup.service
[Unit]
Description=System Backup
After=network.target

[Service]
Type=oneshot
User=backup
Group=backup

ExecStartPre=/usr/local/bin/backup-pre-check.sh
ExecStart=/usr/local/bin/backup.sh
ExecStartPost=/usr/local/bin/backup-cleanup.sh

StandardOutput=journal
StandardError=journal
SyslogIdentifier=backup

# 타임아웃 60분
TimeoutStartSec=3600s

# /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer
Requires=backup.service

[Timer]
# 매일 새벽 2시
OnCalendar=*-*-* 02:00:00

# 부팅 시 놓친 실행
Persistent=true

# 무작위 지연 (부하 분산)
RandomizedDelaySec=30m

# 정확도
AccuracySec=1m

[Install]
WantedBy=timers.target

# 활성화
$ sudo systemctl daemon-reload
$ sudo systemctl enable --now backup.timer
$ systemctl list-timers backup.timer
```

### 모니터링 서비스

```bash
# /etc/systemd/system/monitor.service
[Unit]
Description=System Monitor
After=network.target

[Service]
Type=simple
User=monitor
Group=monitor

ExecStart=/usr/local/bin/monitor.py

Restart=always
RestartSec=30s

# 감시견 (watchdog)
WatchdogSec=60s

# 리소스 제한
CPUQuota=25%
MemoryMax=500M

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

# 감시견 사용 예제 (Python)
# import systemd.daemon
# while True:
#     do_work()
#     systemd.daemon.notify('WATCHDOG=1')
```

---

## 요약

systemd 핵심 명령어:

1. **서비스**: `systemctl start/stop/restart/reload`
2. **상태**: `systemctl status`, `systemctl is-active`
3. **부팅**: `systemctl enable/disable`
4. **로그**: `journalctl -u service`, `journalctl -f`
5. **분석**: `systemd-analyze`, `systemd-analyze blame`
6. **타이머**: `systemctl list-timers`

Unit 파일 주요 섹션:
- **[Unit]**: 설명, 의존성
- **[Service]**: 실행 명령, 타입, 리소스
- **[Install]**: 설치 타겟
- **[Timer]**: 타이머 설정

---

[다음: cron →](cron.md)

[← 사용자 관리로 돌아가기](user-management.md)

[← 목차로 돌아가기](../README.md)

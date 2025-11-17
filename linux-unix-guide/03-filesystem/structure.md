# 파일시스템 구조

## 목차
- [FHS 개요](#fhs-개요)
- [루트 디렉토리 구조](#루트-디렉토리-구조)
- [주요 디렉토리 상세](#주요-디렉토리-상세)
- [경로와 탐색](#경로와-탐색)
- [디렉토리 계층 예제](#디렉토리-계층-예제)

---

## FHS 개요

FHS (Filesystem Hierarchy Standard)는 리눅스 및 유닉스 시스템의 디렉토리 구조와 내용을 정의하는 표준입니다.

### FHS의 목적

```
1. 일관성: 모든 리눅스 배포판에서 유사한 구조
2. 예측 가능성: 파일 위치를 쉽게 추측 가능
3. 호환성: 소프트웨어가 다양한 시스템에서 작동
4. 관리 용이성: 시스템 관리자가 쉽게 탐색
```

### 디렉토리 분류

```
정적 vs 동적
├─ 정적: 시스템 운영 중 변경되지 않음 (/bin, /lib)
└─ 동적: 자주 변경됨 (/var, /tmp)

공유 가능 vs 공유 불가
├─ 공유 가능: 여러 시스템에서 NFS로 공유 (/usr, /opt)
└─ 공유 불가: 호스트별로 고유 (/etc, /boot)
```

---

## 루트 디렉토리 구조

### 전체 디렉토리 트리

```bash
$ ls -l /
total 96
drwxr-xr-x   2 root root  4096 /bin      → /usr/bin (심볼릭 링크)
drwxr-xr-x   4 root root  4096 /boot     부트로더 파일, 커널
drwxr-xr-x  20 root root  4240 /dev      디바이스 파일
drwxr-xr-x 135 root root 12288 /etc      시스템 설정 파일
drwxr-xr-x   3 root root  4096 /home     사용자 홈 디렉토리
drwxr-xr-x  14 root root  4096 /lib      → /usr/lib (심볼릭 링크)
drwxr-xr-x   2 root root  4096 /lib64    → /usr/lib64 (심볼릭 링크)
drwx------   2 root root 16384 /lost+found  복구된 파일
drwxr-xr-x   3 root root  4096 /media    이동식 미디어 마운트
drwxr-xr-x   2 root root  4096 /mnt      임시 마운트 포인트
drwxr-xr-x   3 root root  4096 /opt      추가 소프트웨어
dr-xr-xr-x 258 root root     0 /proc     프로세스 정보 (가상)
drwx------   5 root root  4096 /root     root 사용자 홈
drwxr-xr-x  28 root root   880 /run      런타임 데이터
drwxr-xr-x   2 root root  4096 /sbin     → /usr/sbin (심볼릭 링크)
drwxr-xr-x   2 root root  4096 /srv      서비스 데이터
dr-xr-xr-x  13 root root     0 /sys      시스템 정보 (가상)
drwxrwxrwt  15 root root  4096 /tmp      임시 파일
drwxr-xr-x  14 root root  4096 /usr      사용자 프로그램
drwxr-xr-x  13 root root  4096 /var      가변 데이터
```

### 간단한 시각화

```
/
├── bin → usr/bin          실행 파일
├── boot                   부팅 관련
├── dev                    디바이스
├── etc                    설정 파일
├── home                   사용자 홈
│   ├── user1
│   └── user2
├── lib → usr/lib          라이브러리
├── media                  마운트 포인트
├── mnt                    마운트 포인트
├── opt                    추가 소프트웨어
├── proc                   프로세스 정보
├── root                   root 홈
├── run                    런타임 데이터
├── sbin → usr/sbin        시스템 실행 파일
├── srv                    서비스 데이터
├── sys                    시스템 정보
├── tmp                    임시 파일
├── usr                    사용자 프로그램
│   ├── bin
│   ├── lib
│   ├── local
│   └── share
└── var                    가변 데이터
    ├── log
    ├── cache
    └── tmp
```

---

## 주요 디렉토리 상세

### /bin - 기본 명령어

```bash
# 모든 사용자가 사용할 수 있는 필수 명령어
$ ls /bin | head -20
bash        # Bourne Again Shell
cat         # 파일 내용 출력
chmod       # 권한 변경
chown       # 소유자 변경
cp          # 파일 복사
date        # 날짜/시간
dd          # 데이터 변환/복사
df          # 디스크 사용량
dmesg       # 커널 메시지
echo        # 텍스트 출력
false       # 항상 실패 반환
grep        # 패턴 검색
kill        # 프로세스 종료
ln          # 링크 생성
ls          # 디렉토리 목록
mkdir       # 디렉토리 생성
mount       # 파일시스템 마운트
mv          # 파일 이동
ps          # 프로세스 목록
pwd         # 현재 디렉토리

# 현대 시스템에서는 /bin → /usr/bin 심볼릭 링크
$ ls -ld /bin
lrwxrwxrwx 1 root root 7 /bin -> usr/bin
```

### /boot - 부팅 파일

```bash
$ ls -lh /boot
total 95M
-rw-r--r-- 1 root root 8.5M config-5.15.0-78-generic       # 커널 설정
-rw-r--r-- 1 root root 257K config-5.15.0-76-generic
drwxr-xr-x 5 root root 4.0K efi                           # EFI 부트로더
drwxr-xr-x 5 root root 4.0K grub                          # GRUB 설정
-rw-r--r-- 1 root root  85M initrd.img-5.15.0-78-generic  # 초기 RAM 디스크
-rw-r--r-- 1 root root  84M initrd.img-5.15.0-76-generic
-rw-r--r-- 1 root root 182K memtest86+.bin                # 메모리 테스트
-rw-r--r-- 1 root root 184K memtest86+.elf
-rw-r--r-- 1 root root 184K memtest86+_multiboot.bin
-rw-r--r-- 1 root root 5.9M System.map-5.15.0-78-generic  # 커널 심볼 맵
-rw------- 1 root root  12M vmlinuz-5.15.0-78-generic     # 압축된 커널
-rw------- 1 root root  11M vmlinuz-5.15.0-76-generic

# GRUB 설정
$ ls /boot/grub/
fonts  grub.cfg  grubenv  locale  unicode.pf2  x86_64-efi
```

### /dev - 디바이스 파일

```bash
# 블록 디바이스 (저장 장치)
$ ls -l /dev/sd* /dev/nvme*
brw-rw---- 1 root disk 8, 0  /dev/sda       # 전체 디스크
brw-rw---- 1 root disk 8, 1  /dev/sda1      # 첫 번째 파티션
brw-rw---- 1 root disk 8, 2  /dev/sda2
brw-rw---- 1 root disk 259, 0 /dev/nvme0n1  # NVMe SSD

# 문자 디바이스
$ ls -l /dev/tty* | head -5
crw--w---- 1 root tty  4, 0  /dev/tty0      # 가상 콘솔
crw--w---- 1 root tty  4, 1  /dev/tty1
crw-rw-rw- 1 root tty  5, 0  /dev/tty       # 현재 터미널

# 특수 디바이스
$ ls -l /dev/{null,zero,random,urandom}
crw-rw-rw- 1 root root 1, 3  /dev/null      # 모든 데이터 버림
crw-rw-rw- 1 root root 1, 5  /dev/zero      # 0 바이트 생성
crw-rw-rw- 1 root root 1, 8  /dev/random    # 랜덤 데이터
crw-rw-rw- 1 root root 1, 9  /dev/urandom   # 랜덤 데이터 (빠름)

# 디바이스 사용 예제
$ dd if=/dev/zero of=/tmp/testfile bs=1M count=10
10+0 records in
10+0 records out
10485760 bytes (10 MB) copied

$ echo "Hello" > /dev/null  # 출력 버림

$ head -c 16 /dev/urandom | base64  # 랜덤 문자열 생성
Kg8vN2xQc9F3mZkR
```

### /etc - 설정 파일

```bash
# 주요 설정 파일들
$ ls -l /etc/*.conf
-rw-r--r-- 1 root root   2969 /etc/adduser.conf
-rw-r--r-- 1 root root   1371 /etc/ca-certificates.conf
-rw-r--r-- 1 root root   5090 /etc/deluser.conf
-rw-r--r-- 1 root root    497 /etc/nsswitch.conf
-rw-r--r-- 1 root root    552 /etc/pam.conf
-rw-r--r-- 1 root root    767 /etc/resolv.conf

# 중요 시스템 파일
/etc/passwd              # 사용자 계정 정보
/etc/shadow              # 암호화된 비밀번호
/etc/group               # 그룹 정보
/etc/fstab               # 파일시스템 마운트 정보
/etc/hostname            # 호스트 이름
/etc/hosts               # 정적 호스트 이름 매핑
/etc/network/interfaces  # 네트워크 설정
/etc/ssh/sshd_config     # SSH 서버 설정

# 예제: 사용자 정보 확인
$ cat /etc/passwd | head -3
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin

# 네트워크 설정
$ cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       hostname
192.168.1.100   server.local server

# DNS 설정
$ cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
search local.domain
```

### /home - 사용자 홈 디렉토리

```bash
# 각 사용자의 개인 공간
$ ls -la /home/
drwxr-xr-x  3 root  root   4096 /home/
drwxr-xr-x 25 alice alice  4096 /home/alice/
drwxr-xr-x 18 bob   bob    4096 /home/bob/
drwxr-xr-x 32 carol carol  4096 /home/carol/

# 사용자 홈 디렉토리 구조
$ ls -la ~/
drwxr-xr-x 25 user user 4096 .                    # 홈 디렉토리
drwxr-xr-x  3 root root 4096 ..                   # 부모 (/home)
-rw-------  1 user user 7234 .bash_history        # bash 히스토리
-rw-r--r--  1 user user  220 .bash_logout
-rw-r--r--  1 user user 3526 .bashrc              # bash 설정
-rw-r--r--  1 user user  807 .profile
drwx------  2 user user 4096 .ssh                 # SSH 키
drwxr-xr-x  3 user user 4096 Documents
drwxr-xr-x  2 user user 4096 Downloads
drwxr-xr-x  2 user user 4096 Pictures

# 숨김 파일 (dot files) - 설정 파일들
$ ls -a ~ | grep "^\."
.bash_history
.bashrc
.cache
.config
.gitconfig
.local
.profile
.ssh
.vimrc
```

### /proc - 프로세스 정보 (가상 파일시스템)

```bash
# 프로세스별 디렉토리
$ ls /proc/ | grep "^[0-9]" | head -5
1        # PID 1 (init/systemd)
2        # PID 2
10
100
1000

# 프로세스 정보 확인
$ ls /proc/1/
attr     cmdline  environ  limits    mounts      root      statm
auxv     comm     exe      map_files net         sched     status
cgroup   cwd      fd       maps      ns          schedstat syscall
clear_refs       fdinfo   io       mem       numa_maps   sessionid task

$ cat /proc/1/cmdline
/sbin/init

$ cat /proc/1/status | head -10
Name:   systemd
State:  S (sleeping)
Tgid:   1
Pid:    1
PPid:   0

# 시스템 정보
$ cat /proc/cpuinfo | head -20    # CPU 정보
$ cat /proc/meminfo | head -10    # 메모리 정보
$ cat /proc/version               # 커널 버전
Linux version 5.15.0-78-generic (buildd@lcy02-amd64-026)

$ cat /proc/uptime
12345.67 98765.43  # 시스템 가동 시간 (초)

$ cat /proc/loadavg
0.45 0.32 0.28 2/567 12345  # 1분, 5분, 15분 평균 부하
```

### /sys - 시스템 정보 (가상 파일시스템)

```bash
# 하드웨어 정보
$ ls /sys/
block  bus  class  dev  devices  firmware  fs  kernel  module  power

# 블록 디바이스 정보
$ cat /sys/block/sda/size
976773168  # 섹터 수

$ cat /sys/block/sda/queue/scheduler
[mq-deadline] none

# 네트워크 인터페이스
$ cat /sys/class/net/eth0/address
52:54:00:12:34:56

$ cat /sys/class/net/eth0/operstate
up

$ cat /sys/class/net/eth0/speed
1000  # Mbps

# CPU 주파수
$ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
2600000  # kHz

# 전원 관리
$ cat /sys/class/power_supply/BAT0/capacity
85  # 배터리 %
```

### /tmp - 임시 파일

```bash
# 모든 사용자가 쓸 수 있는 임시 공간
$ ls -ld /tmp
drwxrwxrwt 15 root root 4096 /tmp
# t = sticky bit: 파일 소유자만 삭제 가능

# 임시 파일 생성
$ mktemp
/tmp/tmp.Xb3k9f2L4p

$ mktemp -d  # 임시 디렉토리
/tmp/tmp.vK8m2p1N9q

# 임시 파일은 재부팅 시 삭제됨
# systemd-tmpfiles가 관리

# tmpfs로 마운트 (RAM 디스크)
$ df -h /tmp
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           1.6G  123M  1.5G   8% /tmp
```

### /usr - 사용자 프로그램

```bash
# /usr 구조
$ ls -l /usr/
drwxr-xr-x  2 root root  /usr/bin        # 실행 파일
drwxr-xr-x  2 root root  /usr/sbin       # 시스템 관리 명령
drwxr-xr-x 44 root root  /usr/lib        # 라이브러리
drwxr-xr-x 10 root root  /usr/local      # 로컬 설치 프로그램
drwxr-xr-x  3 root root  /usr/share      # 아키텍처 독립 파일
drwxr-xr-x  2 root root  /usr/include    # C 헤더 파일
drwxr-xr-x  4 root root  /usr/src        # 소스 코드

# /usr/bin - 대부분의 명령어
$ ls /usr/bin | wc -l
2345  # 수천 개의 프로그램

# /usr/local - 시스템 관리자가 설치한 프로그램
$ ls /usr/local/
bin  etc  games  include  lib  man  sbin  share  src

# /usr/share - 데이터 파일
$ ls /usr/share/
applications  doc  fonts  icons  locale  man  pixmaps  themes

# 매뉴얼 페이지
$ ls /usr/share/man/
man1  man2  man3  man4  man5  man6  man7  man8

# 예제: 매뉴얼 보기
$ man ls  # /usr/share/man/man1/ls.1.gz 읽음
```

### /var - 가변 데이터

```bash
# /var 구조
$ ls -l /var/
drwxr-xr-x  2 root root  /var/backups   # 백업
drwxr-xr-x 14 root root  /var/cache     # 캐시
drwxr-xr-x 39 root root  /var/lib       # 상태 정보
drwxrwxr-x 10 root syslog /var/log      # 로그 파일
drwxr-xr-x  2 root root  /var/opt       # /opt 데이터
drwxr-xr-x  5 root root  /var/spool     # 큐 (메일, 프린터)
drwxrwxrwt  2 root root  /var/tmp       # 임시 파일 (재부팅 후에도 유지)

# 로그 파일
$ ls -lh /var/log/ | head -10
-rw-r--r--  1 root   root   234K auth.log       # 인증 로그
-rw-r-----  1 syslog adm    456K syslog         # 시스템 로그
-rw-r--r--  1 root   root   123K kern.log       # 커널 로그
-rw-rw-r--  1 root   utmp    12K btmp           # 실패한 로그인
-rw-rw-r--  1 root   utmp   345K wtmp           # 로그인 기록
drwxr-xr-x  2 root   root   4.0K apt            # APT 로그
drwxr-xr-x  3 root   root   4.0K nginx          # Nginx 로그

# 로그 확인
$ tail -f /var/log/syslog  # 실시간 로그 보기

# 패키지 캐시
$ du -sh /var/cache/apt/
567M    /var/cache/apt/

# 데이터베이스 파일
$ ls /var/lib/
apt  dpkg  mysql  postgresql  systemd
```

### /root - root 사용자 홈

```bash
# root 사용자의 홈 디렉토리
$ sudo ls -la /root/
drwx------  5 root root 4096 .
drwxr-xr-x 24 root root 4096 ..
-rw-------  1 root root  123 .bash_history
-rw-r--r--  1 root root 3106 .bashrc
-rw-r--r--  1 root root  161 .profile
drwx------  2 root root 4096 .ssh

# /home이 아닌 /에 위치하는 이유:
# - /home이 마운트 실패해도 root 로그인 가능
# - 응급 복구 상황에서 접근 용이
```

### /opt - 추가 소프트웨어

```bash
# 서드파티 소프트웨어 설치 위치
$ ls -l /opt/
drwxr-xr-x  3 root root 4096 google
drwxr-xr-x  5 root root 4096 teamviewer
drwxr-xr-x  4 root root 4096 zoom

# 각 소프트웨어는 자체 포함 디렉토리 구조
$ ls /opt/google/chrome/
chrome  chrome-sandbox  chrome_crashpad_handler  libEGL.so  libGLESv2.so
```

### /srv - 서비스 데이터

```bash
# 웹 서버, FTP 서버 등의 데이터
$ ls -l /srv/
drwxr-xr-x 2 root root 4096 ftp
drwxr-xr-x 3 root root 4096 www

# 웹 사이트 파일
$ ls /srv/www/
html  mysite.com  blog.example.org
```

---

## 경로와 탐색

### 절대 경로 vs 상대 경로

```bash
# 절대 경로 (/ 로 시작)
$ cd /usr/local/bin
$ pwd
/usr/local/bin

$ cat /etc/passwd  # 항상 같은 파일

# 상대 경로 (현재 위치 기준)
$ cd /home/user
$ cd Documents     # /home/user/Documents
$ pwd
/home/user/Documents

$ cd ../Downloads  # /home/user/Downloads
$ pwd
/home/user/Downloads

$ cat ./file.txt           # 현재 디렉토리의 file.txt
$ cat ../../etc/passwd     # 상대 경로로 /etc/passwd
```

### 특수 디렉토리 기호

```bash
# . (현재 디렉토리)
$ pwd
/home/user

$ ls .
Documents  Downloads  Pictures

$ ./script.sh  # 현재 디렉토리의 스크립트 실행

# .. (부모 디렉토리)
$ cd ..
$ pwd
/home

$ cd ../../etc
$ pwd
/etc

# ~ (홈 디렉토리)
$ cd ~
$ pwd
/home/user

$ cd ~alice  # alice의 홈
$ pwd
/home/alice

# - (이전 디렉토리)
$ cd /var/log
$ cd /etc
$ cd -  # /var/log로 돌아감
/var/log

$ cd -  # /etc로 다시 돌아감
/etc
```

### 경로 탐색 명령어

```bash
# pwd - 현재 디렉토리
$ pwd
/home/user/Documents/projects

$ pwd -P  # 심볼릭 링크 해석
/home/user/real/path

# basename - 파일/디렉토리 이름만
$ basename /usr/local/bin/script.sh
script.sh

$ basename /usr/local/bin
bin

# dirname - 디렉토리 부분만
$ dirname /usr/local/bin/script.sh
/usr/local/bin

$ dirname /usr/local/bin
/usr/local

# readlink - 심볼릭 링크 타겟
$ readlink /bin
usr/bin

$ readlink -f /bin/ls  # 절대 경로로 해석
/usr/bin/ls
```

---

## 디렉토리 계층 예제

### 예제 1: 웹 서버 구조

```bash
/var/www/mysite/
├── public_html/           # 웹 루트
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── logo.png
├── logs/                  # 로그 파일
│   ├── access.log
│   └── error.log
└── config/                # 설정 파일
    └── site.conf
```

### 예제 2: 프로젝트 구조

```bash
/home/user/projects/myapp/
├── src/                   # 소스 코드
│   ├── main.py
│   ├── utils.py
│   └── tests/
│       └── test_main.py
├── docs/                  # 문서
│   └── README.md
├── config/                # 설정
│   ├── dev.yml
│   └── prod.yml
├── data/                  # 데이터
│   └── sample.csv
├── venv/                  # 가상 환경
└── requirements.txt       # 의존성
```

### 예제 3: 시스템 관리 구조

```bash
# 로그 분석 경로
/var/log/
├── nginx/
│   ├── access.log
│   └── error.log
├── mysql/
│   └── error.log
└── syslog

# 백업 경로
/var/backups/
├── mysql/
│   └── dump_2024-11-17.sql.gz
├── etc/
│   └── etc_2024-11-17.tar.gz
└── home/
    └── user_2024-11-17.tar.gz

# 스크립트 경로
/usr/local/bin/
├── backup.sh
├── deploy.sh
└── monitor.sh

/etc/cron.d/
└── backup_job  # 크론 작업 정의
```

---

## 실전 팁

### 디렉토리 찾기

```bash
# 특정 디렉토리 찾기
$ find / -type d -name "nginx" 2>/dev/null
/etc/nginx
/var/log/nginx
/usr/share/nginx

# 대용량 디렉토리 찾기
$ du -h --max-depth=1 / 2>/dev/null | sort -hr | head -10
8.5G    /usr
3.2G    /var
1.5G    /home
500M    /opt

# 디스크 사용량 확인
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       465G  123G  320G  28% /
/dev/sda1       511M  5.3M  506M   2% /boot/efi
```

### 빠른 탐색

```bash
# pushd/popd - 디렉토리 스택
$ pushd /var/log
/var/log ~

$ pushd /etc
/etc /var/log ~

$ dirs -v
 0  /etc
 1  /var/log
 2  ~

$ popd
/var/log ~

# autojump (설치 필요)
$ j log  # /var/log로 이동
$ j doc  # ~/Documents로 이동
```

---

## 요약

리눅스 파일시스템은 FHS 표준을 따르며, 각 디렉토리는 명확한 목적을 가집니다:

- **/bin, /usr/bin**: 실행 파일
- **/etc**: 설정 파일
- **/home**: 사용자 데이터
- **/var**: 가변 데이터 (로그, 캐시)
- **/tmp**: 임시 파일
- **/proc, /sys**: 가상 파일시스템

이 구조를 이해하면 시스템 탐색과 관리가 훨씬 쉬워집니다.

---

[다음: 파일시스템 타입 →](types.md)

[← 시스템 계층으로 돌아가기](../02-system-architecture/system-layers.md)

[← 목차로 돌아가기](../README.md)

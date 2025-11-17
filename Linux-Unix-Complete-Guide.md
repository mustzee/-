# 리눅스/유닉스 완벽 가이드 (Linux/Unix Complete Guide)

## 목차 (Table of Contents)

1. [소개 및 역사](#1-소개-및-역사)
2. [시스템 아키텍처](#2-시스템-아키텍처)
3. [파일 시스템 구조](#3-파일-시스템-구조)
4. [필수 명령어](#4-필수-명령어)
5. [파일 작업 및 권한](#5-파일-작업-및-권한)
6. [프로세스 관리](#6-프로세스-관리)
7. [셸과 스크립팅](#7-셸과-스크립팅)
8. [네트워킹](#8-네트워킹)
9. [패키지 관리](#9-패키지-관리)
10. [시스템 관리](#10-시스템-관리)
11. [보안](#11-보안)
12. [고급 주제](#12-고급-주제)
13. [문제 해결](#13-문제-해결)

---

## 1. 소개 및 역사

### 1.1 유닉스(Unix)의 탄생
- **1969년**: AT&T 벨 연구소의 Ken Thompson과 Dennis Ritchie가 개발
- **1973년**: C 언어로 재작성되어 이식성 확보
- **철학**: "Do one thing and do it well" - 작은 도구들의 조합

### 1.2 유닉스 계열
- **BSD (Berkeley Software Distribution)**: FreeBSD, OpenBSD, NetBSD
- **System V**: Solaris, AIX, HP-UX
- **macOS**: Darwin 커널 기반 (BSD 계열)

### 1.3 리눅스(Linux)의 등장
- **1991년**: Linus Torvalds가 개발 시작
- **특징**:
  - 오픈소스 운영체제
  - GNU 프로젝트와 결합 (GNU/Linux)
  - 다양한 배포판 존재

### 1.4 주요 리눅스 배포판
- **Debian 계열**: Ubuntu, Linux Mint, Pop!_OS
- **Red Hat 계열**: RHEL, Fedora, CentOS, Rocky Linux
- **Arch 계열**: Arch Linux, Manjaro
- **SUSE 계열**: openSUSE, SLES
- **독립형**: Gentoo, Slackware

---

## 2. 시스템 아키텍처

### 2.1 커널 (Kernel)
```
사용자 공간 (User Space)
    ↓
시스템 콜 인터페이스 (System Call Interface)
    ↓
커널 공간 (Kernel Space)
    ├── 프로세스 관리
    ├── 메모리 관리
    ├── 파일 시스템
    ├── 네트워크 스택
    └── 디바이스 드라이버
    ↓
하드웨어 (Hardware)
```

### 2.2 시스템 계층 구조
1. **하드웨어**: CPU, 메모리, 디스크, 네트워크 카드
2. **커널**: 하드웨어 리소스 관리
3. **셸**: 사용자와 커널 간 인터페이스
4. **애플리케이션**: 사용자 프로그램

### 2.3 부팅 프로세스
```
BIOS/UEFI
    ↓
부트로더 (GRUB/LILO)
    ↓
커널 로드
    ↓
initramfs/initrd
    ↓
init/systemd (PID 1)
    ↓
런레벨/타겟 실행
    ↓
로그인 프롬프트
```

---

## 3. 파일 시스템 구조

### 3.1 FHS (Filesystem Hierarchy Standard)

```
/                   루트 디렉토리
├── bin/           필수 사용자 명령어 바이너리
├── boot/          부트로더 파일, 커널
├── dev/           디바이스 파일
├── etc/           시스템 설정 파일
├── home/          사용자 홈 디렉토리
├── lib/           공유 라이브러리
├── media/         이동식 미디어 마운트 포인트
├── mnt/           임시 마운트 포인트
├── opt/           선택적 애플리케이션 소프트웨어
├── proc/          프로세스 및 커널 정보 (가상 파일시스템)
├── root/          root 사용자 홈 디렉토리
├── run/           런타임 데이터
├── sbin/          시스템 관리 바이너리
├── srv/           서비스 데이터
├── sys/           시스템 및 커널 정보 (가상 파일시스템)
├── tmp/           임시 파일
├── usr/           사용자 유틸리티 및 애플리케이션
│   ├── bin/       사용자 명령어
│   ├── lib/       라이브러리
│   ├── local/     로컬 소프트웨어
│   └── share/     아키텍처 독립적 데이터
└── var/           가변 데이터
    ├── log/       로그 파일
    ├── mail/      메일 박스
    └── spool/     스풀 디렉토리
```

### 3.2 파일 시스템 타입
- **ext4**: 리눅스 기본 파일시스템
- **XFS**: 고성능 저널링 파일시스템
- **Btrfs**: Copy-on-Write 파일시스템
- **ZFS**: 고급 기능의 파일시스템
- **NFS**: 네트워크 파일시스템
- **tmpfs**: 메모리 기반 파일시스템

### 3.3 inode와 파일 구조
- **inode**: 파일 메타데이터 저장 (권한, 소유자, 타임스탬프, 데이터 블록 위치)
- **Hard Link**: 동일 inode를 가리키는 여러 파일명
- **Symbolic Link**: 다른 파일 경로를 가리키는 포인터

---

## 4. 필수 명령어

### 4.1 파일 및 디렉토리 탐색
```bash
# 현재 디렉토리 표시
pwd

# 디렉토리 이동
cd /path/to/directory
cd ~              # 홈 디렉토리로
cd -              # 이전 디렉토리로
cd ..             # 상위 디렉토리로

# 파일 목록
ls                # 기본 목록
ls -l             # 상세 정보
ls -la            # 숨김 파일 포함
ls -lh            # 사람이 읽기 쉬운 크기
ls -ltr           # 시간순 정렬 (역순)

# 트리 구조 출력
tree
tree -L 2         # 깊이 2까지만
```

### 4.2 파일 작업
```bash
# 파일 생성
touch file.txt
touch file{1..5}.txt  # file1.txt ~ file5.txt 생성

# 파일 복사
cp source.txt dest.txt
cp -r dir1/ dir2/     # 디렉토리 재귀 복사
cp -p file1 file2     # 속성 보존

# 파일 이동/이름 변경
mv old.txt new.txt
mv file.txt /path/to/destination/

# 파일 삭제
rm file.txt
rm -r directory/      # 디렉토리 재귀 삭제
rm -rf directory/     # 강제 삭제 (주의!)
rm -i file.txt        # 확인 후 삭제

# 디렉토리 생성
mkdir directory
mkdir -p path/to/nested/dir  # 중첩 디렉토리 생성

# 디렉토리 삭제
rmdir empty_directory
```

### 4.3 파일 내용 보기
```bash
# 전체 내용 출력
cat file.txt
cat file1.txt file2.txt  # 여러 파일 연결

# 페이지 단위 보기
less file.txt
more file.txt

# 처음/끝 부분만 보기
head file.txt          # 처음 10줄
head -n 20 file.txt    # 처음 20줄
tail file.txt          # 마지막 10줄
tail -n 20 file.txt    # 마지막 20줄
tail -f /var/log/syslog  # 실시간 로그 모니터링

# 파일 내용 검색
grep "pattern" file.txt
grep -r "pattern" directory/  # 재귀 검색
grep -i "pattern" file.txt    # 대소문자 무시
grep -n "pattern" file.txt    # 줄 번호 표시
grep -v "pattern" file.txt    # 패턴 제외
```

### 4.4 텍스트 처리
```bash
# 정렬
sort file.txt
sort -r file.txt       # 역순 정렬
sort -n file.txt       # 숫자 정렬
sort -u file.txt       # 중복 제거 후 정렬

# 중복 제거
uniq file.txt
uniq -c file.txt       # 중복 개수 표시

# 단어/줄/문자 개수
wc file.txt
wc -l file.txt         # 줄 수
wc -w file.txt         # 단어 수
wc -c file.txt         # 바이트 수

# 텍스트 치환
sed 's/old/new/' file.txt
sed 's/old/new/g' file.txt      # 모든 매칭 치환
sed -i 's/old/new/g' file.txt   # 파일 직접 수정

# 패턴 처리
awk '{print $1}' file.txt       # 첫 번째 필드 출력
awk -F: '{print $1}' /etc/passwd  # 구분자 지정

# 컬럼 추출
cut -d: -f1 /etc/passwd         # : 구분자로 첫 필드
cut -c1-10 file.txt             # 1-10번째 문자
```

### 4.5 파일 찾기
```bash
# 파일 검색
find /path -name "*.txt"
find . -type f -name "*.log"
find . -type d -name "config"
find . -mtime -7              # 7일 이내 수정
find . -size +100M            # 100MB 이상
find . -perm 644              # 특정 권한

# 파일 찾아서 실행
find . -name "*.tmp" -delete
find . -name "*.txt" -exec chmod 644 {} \;

# 빠른 파일 검색 (데이터베이스 기반)
locate filename
updatedb                      # 데이터베이스 업데이트

# 명령어 위치 찾기
which python
whereis ls
type cd
```

### 4.6 압축 및 아카이브
```bash
# tar 아카이브
tar -cvf archive.tar files/    # 생성
tar -xvf archive.tar           # 추출
tar -tvf archive.tar           # 내용 보기
tar -czvf archive.tar.gz files/  # gzip 압축
tar -xzvf archive.tar.gz       # gzip 압축 해제
tar -cjvf archive.tar.bz2 files/ # bzip2 압축
tar -xjvf archive.tar.bz2      # bzip2 압축 해제

# gzip/gunzip
gzip file.txt              # file.txt.gz 생성
gunzip file.txt.gz         # 압축 해제

# zip/unzip
zip archive.zip files/
unzip archive.zip
unzip -l archive.zip       # 내용 보기
```

### 4.7 시스템 정보
```bash
# 시스템 정보
uname -a                   # 모든 시스템 정보
uname -r                   # 커널 버전
hostname                   # 호스트명
uptime                     # 가동 시간

# CPU 정보
lscpu
cat /proc/cpuinfo

# 메모리 정보
free -h
cat /proc/meminfo

# 디스크 정보
df -h                      # 디스크 사용량
du -sh directory/          # 디렉토리 크기
du -h --max-depth=1        # 서브디렉토리 크기

# 하드웨어 정보
lshw                       # 전체 하드웨어
lspci                      # PCI 장치
lsusb                      # USB 장치
lsblk                      # 블록 장치

# 시스템 로그
dmesg                      # 커널 메시지
journalctl                 # systemd 로그
```

---

## 5. 파일 작업 및 권한

### 5.1 파일 권한 이해

```
-rwxr-xr-x  1 user group 4096 Jan 01 12:00 file.txt
│││││││││
││││││││└─ 기타(Others) 실행 권한
│││││││└── 기타 쓰기 권한
││││││└─── 기타 읽기 권한
│││││└──── 그룹(Group) 실행 권한
││││└───── 그룹 쓰기 권한
│││└────── 그룹 읽기 권한
││└─────── 소유자(Owner) 실행 권한
│└──────── 소유자 쓰기 권한
└───────── 소유자 읽기 권한
```

**파일 타입**:
- `-`: 일반 파일
- `d`: 디렉토리
- `l`: 심볼릭 링크
- `c`: 문자 디바이스
- `b`: 블록 디바이스
- `s`: 소켓
- `p`: 파이프

### 5.2 권한 변경
```bash
# chmod: 권한 변경
chmod 755 file.txt         # rwxr-xr-x
chmod 644 file.txt         # rw-r--r--
chmod u+x file.txt         # 소유자에게 실행 권한 추가
chmod g-w file.txt         # 그룹 쓰기 권한 제거
chmod o=r file.txt         # 기타 사용자 읽기만
chmod a+x file.txt         # 모두에게 실행 권한 추가
chmod -R 755 directory/    # 재귀적 권한 변경

# 숫자 권한
# r(read) = 4, w(write) = 2, x(execute) = 1
# 755 = rwxr-xr-x (4+2+1, 4+0+1, 4+0+1)
# 644 = rw-r--r-- (4+2+0, 4+0+0, 4+0+0)
# 600 = rw------- (4+2+0, 0+0+0, 0+0+0)
```

### 5.3 소유권 변경
```bash
# chown: 소유자 변경
chown user file.txt
chown user:group file.txt
chown -R user:group directory/

# chgrp: 그룹 변경
chgrp group file.txt
chgrp -R group directory/
```

### 5.4 특수 권한
```bash
# SUID (Set User ID): 실행 시 소유자 권한으로 실행
chmod u+s file
chmod 4755 file

# SGID (Set Group ID): 실행 시 그룹 권한으로 실행
chmod g+s file
chmod 2755 file

# Sticky Bit: 디렉토리에서 소유자만 파일 삭제 가능
chmod +t directory
chmod 1755 directory

# umask: 기본 권한 마스크
umask              # 현재 umask 확인
umask 022          # 파일 644, 디렉토리 755
umask 077          # 파일 600, 디렉토리 700
```

### 5.5 ACL (Access Control Lists)
```bash
# ACL 설정
setfacl -m u:username:rwx file.txt
setfacl -m g:groupname:rx file.txt
setfacl -m d:u:username:rwx directory/  # 기본 ACL

# ACL 보기
getfacl file.txt

# ACL 제거
setfacl -x u:username file.txt
setfacl -b file.txt  # 모든 ACL 제거
```

---

## 6. 프로세스 관리

### 6.1 프로세스 보기
```bash
# ps: 프로세스 상태
ps                     # 현재 셸의 프로세스
ps aux                 # 모든 프로세스 상세 정보
ps -ef                 # 모든 프로세스 (다른 형식)
ps -u username         # 특정 사용자 프로세스
ps -C processname      # 특정 프로세스명

# top: 실시간 프로세스 모니터링
top
htop                   # 향상된 top (설치 필요)

# pgrep/pkill: 프로세스 검색/종료
pgrep firefox
pgrep -u username
pkill firefox
```

### 6.2 프로세스 제어
```bash
# 프로세스 시작
command &              # 백그라운드 실행
nohup command &        # 로그아웃 후에도 실행

# 작업 제어
jobs                   # 백그라운드 작업 목록
fg %1                  # 작업 1을 포그라운드로
bg %1                  # 작업 1을 백그라운드로
Ctrl+Z                 # 현재 작업 일시정지
Ctrl+C                 # 현재 작업 종료

# 프로세스 종료
kill PID               # SIGTERM (정상 종료)
kill -9 PID            # SIGKILL (강제 종료)
kill -15 PID           # SIGTERM (명시적)
killall processname    # 이름으로 모든 프로세스 종료
```

### 6.3 프로세스 우선순위
```bash
# nice: 우선순위 설정하여 실행 (-20 ~ 19, 낮을수록 높은 우선순위)
nice -n 10 command
nice -10 command

# renice: 실행 중 프로세스 우선순위 변경
renice 10 -p PID
renice 10 -u username

# ionice: I/O 우선순위
ionice -c 3 -p PID     # idle class
```

### 6.4 시스템 리소스 모니터링
```bash
# vmstat: 가상 메모리 통계
vmstat 1               # 1초마다 업데이트

# iostat: I/O 통계
iostat 1

# mpstat: CPU 통계
mpstat -P ALL 1

# sar: 시스템 활동 리포트
sar -u 1 10            # CPU 사용률, 1초마다 10번
sar -r 1 10            # 메모리 사용률
sar -n DEV 1 10        # 네트워크 통계
```

---

## 7. 셸과 스크립팅

### 7.1 주요 셸 종류
- **sh**: Bourne Shell (원조)
- **bash**: Bourne Again Shell (가장 일반적)
- **zsh**: Z Shell (현대적 기능)
- **fish**: Friendly Interactive Shell
- **ksh**: Korn Shell
- **csh/tcsh**: C Shell

### 7.2 셸 환경 변수
```bash
# 환경 변수 보기
env                    # 모든 환경 변수
echo $PATH
echo $HOME
echo $USER
echo $SHELL

# 환경 변수 설정
export VAR="value"
export PATH="$PATH:/new/path"

# 영구적 설정
~/.bashrc              # bash 설정 파일
~/.bash_profile        # 로그인 시 실행
~/.profile             # 범용 프로필
/etc/profile           # 시스템 전체 프로필
/etc/bash.bashrc       # 시스템 전체 bashrc

# 설정 다시 로드
source ~/.bashrc
. ~/.bashrc
```

### 7.3 Bash 스크립팅 기초
```bash
#!/bin/bash
# 스크립트 시작 (shebang)

# 변수
name="World"
echo "Hello, $name"
echo "Hello, ${name}"

# 명령 치환
current_date=$(date)
current_date=`date`

# 산술 연산
result=$((5 + 3))
result=$((5 * 3))
let result=5+3

# 배열
arr=("a" "b" "c")
echo ${arr[0]}
echo ${arr[@]}         # 모든 요소
echo ${#arr[@]}        # 배열 길이

# 조건문
if [ "$name" = "World" ]; then
    echo "Hello, World"
elif [ "$name" = "Linux" ]; then
    echo "Hello, Linux"
else
    echo "Hello, Unknown"
fi

# 파일 테스트
if [ -f "file.txt" ]; then
    echo "파일이 존재합니다"
fi

if [ -d "directory" ]; then
    echo "디렉토리가 존재합니다"
fi

# 반복문
for i in {1..5}; do
    echo "Number: $i"
done

for file in *.txt; do
    echo "File: $file"
done

while [ $count -lt 10 ]; do
    echo $count
    ((count++))
done

# 함수
function greet() {
    echo "Hello, $1"
}
greet "User"

# 인자 처리
echo "스크립트명: $0"
echo "첫 번째 인자: $1"
echo "모든 인자: $@"
echo "인자 개수: $#"

# 종료 상태
command
if [ $? -eq 0 ]; then
    echo "성공"
else
    echo "실패"
fi
```

### 7.4 고급 스크립팅
```bash
# 에러 처리
set -e                 # 에러 발생 시 중단
set -u                 # 미정의 변수 사용 시 에러
set -x                 # 디버그 모드
set -euo pipefail      # 안전한 스크립트

# trap: 시그널 처리
trap "echo 'Interrupted'; exit" INT TERM

# case 문
case $var in
    start)
        echo "Starting..."
        ;;
    stop)
        echo "Stopping..."
        ;;
    *)
        echo "Unknown option"
        ;;
esac

# Here Document
cat << EOF
Multiple lines
of text
EOF

# 파일 디스크립터
exec 3< input.txt      # 읽기용 FD 3
exec 4> output.txt     # 쓰기용 FD 4
```

### 7.5 유용한 셸 기능
```bash
# 히스토리
history
!n                     # n번째 명령 실행
!!                     # 이전 명령 반복
!string                # string으로 시작하는 최근 명령

# 명령 치환
cd $(dirname $(which python))

# 프로세스 치환
diff <(ls dir1) <(ls dir2)

# 파이프와 리다이렉션
command > file         # 출력 리다이렉션
command >> file        # 추가
command 2> file        # 에러 리다이렉션
command &> file        # 출력과 에러 모두
command 2>&1           # 에러를 출력으로
command | tee file     # 출력과 파일 동시 저장

# xargs
find . -name "*.txt" | xargs grep "pattern"
cat files.txt | xargs -I {} cp {} /dest/
```

---

## 8. 네트워킹

### 8.1 네트워크 설정 확인
```bash
# IP 주소 확인
ip addr show
ip a
ifconfig               # 레거시

# 라우팅 테이블
ip route show
route -n               # 레거시

# 네트워크 인터페이스
ip link show
ip link set eth0 up
ip link set eth0 down

# DNS 설정
cat /etc/resolv.conf
systemd-resolve --status  # systemd-resolved 사용 시
```

### 8.2 네트워크 연결 테스트
```bash
# ping: 연결 테스트
ping google.com
ping -c 4 8.8.8.8      # 4번만 ping

# traceroute: 경로 추적
traceroute google.com
tracepath google.com

# 호스트명 해석
host google.com
nslookup google.com
dig google.com
dig @8.8.8.8 google.com  # 특정 DNS 서버 사용
```

### 8.3 포트 및 연결 확인
```bash
# netstat: 네트워크 통계 (레거시)
netstat -tuln          # 리스닝 포트
netstat -an            # 모든 연결
netstat -r             # 라우팅 테이블

# ss: 소켓 통계 (현대적)
ss -tuln               # 리스닝 TCP/UDP
ss -tan                # 모든 TCP 연결
ss -s                  # 통계 요약

# lsof: 열린 파일 (네트워크 포트 포함)
lsof -i                # 모든 인터넷 연결
lsof -i :80            # 포트 80
lsof -i TCP            # TCP 연결만

# nmap: 포트 스캔
nmap localhost
nmap -p 1-1000 192.168.1.1
```

### 8.4 파일 전송
```bash
# scp: 보안 복사
scp file.txt user@host:/path/
scp user@host:/path/file.txt .
scp -r directory/ user@host:/path/

# rsync: 동기화
rsync -avz source/ dest/
rsync -avz source/ user@host:/dest/
rsync -avz --delete source/ dest/  # 삭제된 파일도 반영
rsync -avz --progress source/ dest/

# wget: 다운로드
wget http://example.com/file.zip
wget -c http://example.com/file.zip  # 이어받기
wget -r http://example.com/          # 재귀 다운로드

# curl: URL 전송 도구
curl http://example.com
curl -O http://example.com/file.zip  # 파일명 유지
curl -o filename http://example.com/file.zip
curl -I http://example.com           # 헤더만
curl -X POST -d "data=value" http://example.com/api
```

### 8.5 SSH
```bash
# SSH 연결
ssh user@host
ssh -p 2222 user@host  # 포트 지정
ssh -i key.pem user@host  # 키 파일 사용

# SSH 키 생성
ssh-keygen -t rsa -b 4096
ssh-keygen -t ed25519

# SSH 키 복사
ssh-copy-id user@host

# SSH 설정 (~/.ssh/config)
Host myserver
    HostName example.com
    User myuser
    Port 2222
    IdentityFile ~/.ssh/mykey

# SSH 터널링
ssh -L 8080:localhost:80 user@host  # 로컬 포트 포워딩
ssh -R 8080:localhost:80 user@host  # 원격 포트 포워딩
ssh -D 1080 user@host               # SOCKS 프록시

# SSH 에이전트
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa
```

### 8.6 방화벽
```bash
# iptables (레거시)
iptables -L            # 규칙 보기
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -j DROP

# firewalld (RHEL/CentOS)
firewall-cmd --state
firewall-cmd --list-all
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --reload

# ufw (Ubuntu)
ufw status
ufw enable
ufw allow 22/tcp
ufw allow ssh
ufw deny 23/tcp
ufw delete allow 80/tcp
```

---

## 9. 패키지 관리

### 9.1 Debian/Ubuntu (APT)
```bash
# 패키지 업데이트
sudo apt update                # 패키지 목록 업데이트
sudo apt upgrade               # 패키지 업그레이드
sudo apt full-upgrade          # 의존성 포함 전체 업그레이드
sudo apt dist-upgrade          # 배포판 업그레이드

# 패키지 설치/제거
sudo apt install package
sudo apt install package1 package2
sudo apt remove package        # 패키지만 제거
sudo apt purge package         # 설정 파일까지 제거
sudo apt autoremove            # 불필요한 패키지 제거

# 패키지 검색/정보
apt search keyword
apt show package
apt list --installed
apt list --upgradable

# 로컬 .deb 파일 설치
sudo dpkg -i package.deb
sudo apt install -f            # 의존성 해결
```

### 9.2 Red Hat/CentOS (YUM/DNF)
```bash
# DNF (Fedora, RHEL 8+)
sudo dnf check-update
sudo dnf update
sudo dnf install package
sudo dnf remove package
sudo dnf search keyword
sudo dnf info package
sudo dnf list installed

# YUM (RHEL 7, CentOS 7)
sudo yum check-update
sudo yum update
sudo yum install package
sudo yum remove package
sudo yum search keyword
sudo yum info package

# RPM (저수준 패키지 관리)
rpm -ivh package.rpm           # 설치
rpm -Uvh package.rpm           # 업그레이드
rpm -e package                 # 제거
rpm -qa                        # 설치된 패키지
rpm -qi package                # 패키지 정보
rpm -ql package                # 패키지 파일 목록
```

### 9.3 Arch Linux (Pacman)
```bash
# 패키지 관리
sudo pacman -Syu               # 시스템 업데이트
sudo pacman -S package         # 패키지 설치
sudo pacman -R package         # 패키지 제거
sudo pacman -Rs package        # 의존성 포함 제거
sudo pacman -Ss keyword        # 패키지 검색
sudo pacman -Si package        # 패키지 정보
sudo pacman -Q                 # 설치된 패키지
sudo pacman -Sc                # 캐시 정리
```

### 9.4 기타 패키지 관리자
```bash
# Snap (Ubuntu)
sudo snap install package
sudo snap remove package
snap list
snap find keyword

# Flatpak
flatpak install package
flatpak uninstall package
flatpak list
flatpak search keyword

# AppImage
chmod +x app.AppImage
./app.AppImage
```

---

## 10. 시스템 관리

### 10.1 사용자 및 그룹 관리
```bash
# 사용자 생성
sudo useradd username
sudo useradd -m username       # 홈 디렉토리 생성
sudo useradd -m -s /bin/bash username
sudo adduser username          # 대화형 (Debian/Ubuntu)

# 사용자 수정
sudo usermod -aG group username  # 그룹 추가
sudo usermod -s /bin/zsh username  # 셸 변경
sudo usermod -L username       # 계정 잠금
sudo usermod -U username       # 계정 잠금 해제

# 사용자 삭제
sudo userdel username
sudo userdel -r username       # 홈 디렉토리까지 삭제

# 비밀번호 변경
passwd
sudo passwd username
passwd -l username             # 비밀번호 잠금
passwd -u username             # 비밀번호 잠금 해제

# 그룹 관리
sudo groupadd groupname
sudo groupdel groupname
sudo gpasswd -a user group     # 사용자를 그룹에 추가
sudo gpasswd -d user group     # 사용자를 그룹에서 제거

# 사용자/그룹 정보
id username
groups username
whoami
who
w
last                           # 로그인 이력
```

### 10.2 systemd 서비스 관리
```bash
# 서비스 상태
systemctl status service
systemctl is-active service
systemctl is-enabled service

# 서비스 제어
sudo systemctl start service
sudo systemctl stop service
sudo systemctl restart service
sudo systemctl reload service

# 부팅 시 자동 시작
sudo systemctl enable service
sudo systemctl disable service
sudo systemctl enable --now service  # 활성화 후 바로 시작

# 서비스 목록
systemctl list-units --type=service
systemctl list-units --type=service --all
systemctl list-unit-files

# 로그 확인
journalctl -u service
journalctl -u service -f       # 실시간 로그
journalctl -u service --since today
journalctl -b                  # 현재 부팅 로그
journalctl -b -1               # 이전 부팅 로그
journalctl --disk-usage
```

### 10.3 시스템 부팅 및 런레벨
```bash
# systemd 타겟
systemctl get-default          # 기본 타겟
sudo systemctl set-default multi-user.target
sudo systemctl set-default graphical.target

# 시스템 제어
sudo systemctl reboot
sudo systemctl poweroff
sudo systemctl suspend
sudo systemctl hibernate

# 부팅 분석
systemd-analyze
systemd-analyze blame          # 부팅 시간 분석
systemd-analyze critical-chain
```

### 10.4 크론(Cron) 작업 스케줄링
```bash
# crontab 편집
crontab -e                     # 현재 사용자
sudo crontab -e -u username    # 특정 사용자

# crontab 형식
# 분 시 일 월 요일 명령
# * * * * * command
# 0 2 * * * /path/to/backup.sh  # 매일 02:00

# crontab 예제
*/5 * * * * command            # 5분마다
0 * * * * command              # 매 시각
0 0 * * * command              # 매일 자정
0 0 * * 0 command              # 매주 일요일 자정
0 0 1 * * command              # 매월 1일 자정

# crontab 보기/삭제
crontab -l
crontab -r

# 시스템 cron
/etc/crontab
/etc/cron.d/
/etc/cron.daily/
/etc/cron.weekly/
/etc/cron.monthly/
```

### 10.5 로그 관리
```bash
# 주요 로그 파일
/var/log/syslog                # 시스템 로그 (Debian/Ubuntu)
/var/log/messages              # 시스템 로그 (RHEL/CentOS)
/var/log/auth.log              # 인증 로그
/var/log/kern.log              # 커널 로그
/var/log/apache2/              # Apache 로그
/var/log/nginx/                # Nginx 로그

# journalctl (systemd)
journalctl -n 50               # 최근 50줄
journalctl -p err              # 에러만
journalctl --since "1 hour ago"
journalctl --until "2023-01-01"
journalctl -k                  # 커널 메시지

# logrotate (로그 로테이션)
/etc/logrotate.conf
/etc/logrotate.d/
sudo logrotate -f /etc/logrotate.conf
```

---

## 11. 보안

### 11.1 기본 보안 원칙
1. **최소 권한 원칙**: 필요한 최소한의 권한만 부여
2. **정기적 업데이트**: 시스템 및 패키지 업데이트
3. **강력한 비밀번호**: 복잡하고 긴 비밀번호 사용
4. **불필요한 서비스 비활성화**: 공격 표면 최소화
5. **로그 모니터링**: 이상 활동 감지

### 11.2 SSH 보안
```bash
# /etc/ssh/sshd_config
PermitRootLogin no             # root 로그인 금지
PasswordAuthentication no      # 비밀번호 인증 비활성화 (키 인증만)
Port 2222                      # 기본 포트 변경
AllowUsers user1 user2         # 특정 사용자만 허용
MaxAuthTries 3                 # 인증 시도 제한

# 설정 적용
sudo systemctl restart sshd
```

### 11.3 방화벽 설정
```bash
# UFW 기본 설정
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 특정 IP만 허용
sudo ufw allow from 192.168.1.100 to any port 22
```

### 11.4 파일 무결성 검사
```bash
# md5sum
md5sum file.txt
md5sum -c checksums.md5

# sha256sum
sha256sum file.txt
sha256sum -c checksums.sha256

# 파일 무결성 모니터링 (AIDE)
sudo aide --init
sudo aide --check
```

### 11.5 SELinux / AppArmor
```bash
# SELinux (RHEL/CentOS)
getenforce                     # 상태 확인
sudo setenforce 0              # Permissive 모드
sudo setenforce 1              # Enforcing 모드
sestatus                       # 상세 상태

# AppArmor (Ubuntu)
sudo aa-status                 # 상태 확인
sudo aa-enforce /path/to/profile
sudo aa-complain /path/to/profile
sudo aa-disable /path/to/profile
```

### 11.6 보안 도구
```bash
# fail2ban: 침입 방지
sudo systemctl status fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd

# rkhunter: 루트킷 검사
sudo rkhunter --check

# chkrootkit: 루트킷 검사
sudo chkrootkit

# lynis: 보안 감사
sudo lynis audit system

# ClamAV: 안티바이러스
sudo freshclam                 # 바이러스 DB 업데이트
clamscan -r /home              # 스캔
```

---

## 12. 고급 주제

### 12.1 LVM (Logical Volume Management)
```bash
# 물리 볼륨 생성
sudo pvcreate /dev/sdb

# 볼륨 그룹 생성
sudo vgcreate vg_data /dev/sdb

# 논리 볼륨 생성
sudo lvcreate -L 10G -n lv_data vg_data

# 파일시스템 생성 및 마운트
sudo mkfs.ext4 /dev/vg_data/lv_data
sudo mkdir /mnt/data
sudo mount /dev/vg_data/lv_data /mnt/data

# 볼륨 확장
sudo lvextend -L +5G /dev/vg_data/lv_data
sudo resize2fs /dev/vg_data/lv_data

# 정보 확인
pvdisplay
vgdisplay
lvdisplay
```

### 12.2 RAID
```bash
# mdadm으로 RAID 구성
# RAID 1 (미러링)
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc

# RAID 5
sudo mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd

# RAID 상태 확인
cat /proc/mdstat
sudo mdadm --detail /dev/md0

# RAID 설정 저장
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
```

### 12.3 컨테이너 (Docker 기초)
```bash
# Docker 기본 명령
docker pull image:tag
docker run -d -p 80:80 nginx
docker ps                      # 실행 중인 컨테이너
docker ps -a                   # 모든 컨테이너
docker images                  # 이미지 목록

# 컨테이너 관리
docker start container_id
docker stop container_id
docker restart container_id
docker rm container_id
docker rmi image_id

# 로그 및 실행
docker logs container_id
docker exec -it container_id /bin/bash

# Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs
```

### 12.4 systemd 타이머
```bash
# /etc/systemd/system/backup.service
[Unit]
Description=Backup Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh

# /etc/systemd/system/backup.timer
[Unit]
Description=Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

# 타이머 활성화
sudo systemctl enable backup.timer
sudo systemctl start backup.timer
systemctl list-timers
```

### 12.5 네트워크 본딩 (Bonding)
```bash
# /etc/network/interfaces (Debian/Ubuntu)
auto bond0
iface bond0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    bond-mode 802.3ad
    bond-slaves eth0 eth1
    bond-miimon 100

# 본딩 모드
# mode=0 (balance-rr): 라운드 로빈
# mode=1 (active-backup): 액티브-백업
# mode=2 (balance-xor): XOR
# mode=4 (802.3ad): LACP
# mode=6 (balance-alb): 적응형 로드 밸런싱
```

### 12.6 커널 매개변수 조정
```bash
# sysctl로 커널 매개변수 확인/변경
sysctl -a                      # 모든 매개변수
sysctl net.ipv4.ip_forward     # 특정 매개변수
sudo sysctl -w net.ipv4.ip_forward=1  # 임시 변경

# 영구적 변경 (/etc/sysctl.conf)
net.ipv4.ip_forward = 1
vm.swappiness = 10
net.core.somaxconn = 1024

# 적용
sudo sysctl -p
```

---

## 13. 문제 해결

### 13.1 시스템이 부팅되지 않을 때
```bash
# 복구 모드로 부팅
# GRUB 메뉴에서 'Advanced options' → 'recovery mode'

# 단일 사용자 모드
# GRUB에서 'e' 키 → linux 라인 끝에 'single' 또는 '1' 추가

# Live USB로 부팅하여 복구
sudo mount /dev/sda1 /mnt
sudo chroot /mnt
# 필요한 작업 수행
exit
sudo umount /mnt
```

### 13.2 디스크 공간 부족
```bash
# 디스크 사용량 확인
df -h
du -sh /*
du -h --max-depth=1 /var

# 큰 파일 찾기
find / -type f -size +100M -exec ls -lh {} \;
find / -type f -size +1G -exec ls -lh {} \;

# 로그 파일 정리
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=500M
sudo find /var/log -type f -name "*.log" -mtime +30 -delete

# 패키지 캐시 정리
sudo apt clean                 # Debian/Ubuntu
sudo dnf clean all             # Fedora/RHEL
```

### 13.3 성능 문제
```bash
# CPU 사용률 높은 프로세스
top
htop
ps aux --sort=-%cpu | head

# 메모리 사용률 높은 프로세스
ps aux --sort=-%mem | head

# I/O 대기 확인
iostat -x 1
iotop

# 네트워크 대역폭
iftop
nethogs
vnstat
```

### 13.4 네트워크 문제
```bash
# 연결 확인
ping -c 4 8.8.8.8              # IP 연결
ping -c 4 google.com           # DNS 해석 및 연결

# DNS 문제
nslookup google.com
dig google.com
cat /etc/resolv.conf

# 라우팅 문제
ip route show
traceroute google.com

# 방화벽 확인
sudo iptables -L -n
sudo ufw status
```

### 13.5 권한 문제
```bash
# 파일 소유권 및 권한 확인
ls -l file
namei -l /path/to/file

# 권한 수정
sudo chown user:group file
sudo chmod 644 file

# 실행 권한 문제
chmod +x script.sh
```

### 13.6 서비스 시작 실패
```bash
# 상세 상태 확인
systemctl status service.service

# 로그 확인
journalctl -xe
journalctl -u service.service -n 50

# 설정 파일 검증
sudo nginx -t                  # Nginx
sudo apache2ctl configtest     # Apache

# 의존성 확인
systemctl list-dependencies service.service
```

### 13.7 커널 패닉 / 시스템 크래시
```bash
# 크래시 덤프 확인
ls /var/crash/

# 커널 로그
dmesg | less
journalctl -k

# 메모리 테스트
# 부팅 시 GRUB에서 'memtest86+' 선택
```

### 13.8 유용한 진단 명령
```bash
# 시스템 정보
uname -a
lsb_release -a                 # 배포판 정보
hostnamectl

# 하드웨어 정보
lshw -short
lscpu
lsmem
lsblk
lspci
lsusb

# 네트워크 진단
mtr google.com                 # traceroute + ping
tcpdump -i eth0                # 패킷 캡처
netstat -statistics

# 프로세스 트레이싱
strace -p PID
ltrace command
```

---

## 부록 A: 자주 사용하는 단축키

### Bash 단축키
```
Ctrl+A          줄 시작으로
Ctrl+E          줄 끝으로
Ctrl+U          커서 앞 전체 삭제
Ctrl+K          커서 뒤 전체 삭제
Ctrl+W          단어 삭제
Ctrl+L          화면 지우기
Ctrl+R          명령 히스토리 검색
Ctrl+C          현재 명령 중단
Ctrl+D          로그아웃 / EOF
Ctrl+Z          프로세스 일시정지
!!              이전 명령 반복
!$              이전 명령의 마지막 인자
```

### Vi/Vim 기본 명령
```
i               입력 모드
Esc             명령 모드
:w              저장
:q              종료
:wq or :x       저장 후 종료
:q!             저장 없이 강제 종료
dd              줄 삭제
yy              줄 복사
p               붙여넣기
u               실행 취소
/pattern        검색
n               다음 검색 결과
:%s/old/new/g   전체 치환
```

---

## 부록 B: 정규 표현식

### 기본 메타 문자
```
.               임의의 한 문자
*               0회 이상 반복
+               1회 이상 반복
?               0회 또는 1회
^               줄 시작
$               줄 끝
[abc]           a, b, c 중 하나
[^abc]          a, b, c 제외
[a-z]           a부터 z까지
\d              숫자 [0-9]
\w              단어 문자 [a-zA-Z0-9_]
\s              공백 문자
|               OR
()              그룹화
{n}             정확히 n번
{n,}            n번 이상
{n,m}           n번 이상 m번 이하
```

### 예제
```bash
grep '^[0-9]' file.txt         # 숫자로 시작하는 줄
grep '[a-z]*$' file.txt         # 소문자로 끝나는 줄
grep '\b[A-Z]{3}\b' file.txt   # 정확히 3개의 대문자
```

---

## 부록 C: 원라이너 모음

```bash
# 가장 큰 파일 10개 찾기
du -ah / | sort -rh | head -n 10

# 중복 줄 제거
sort file.txt | uniq

# 특정 포트 사용 프로세스 찾기
lsof -i :8080

# 디렉토리 트리를 파일로 저장
tree -a > tree.txt

# 파일에서 IP 주소 추출
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' file.txt

# 시스템 부팅 시간
uptime -s

# 가장 많이 사용된 명령어
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10

# 디렉토리별 파일 개수
find . -type f | sed 's|/[^/]*$|/|' | sort | uniq -c

# CPU 코어 수
nproc

# 전체 메모리
free -h | awk '/^Mem:/ {print $2}'

# 특정 확장자 파일 일괄 변경
for file in *.txt; do mv "$file" "${file%.txt}.md"; done

# 빠른 HTTP 서버 시작
python3 -m http.server 8000

# 랜덤 비밀번호 생성
openssl rand -base64 32

# 파일의 특정 줄만 출력
sed -n '10,20p' file.txt

# 파일 끝에 내용 추가
echo "text" | tee -a file.txt

# 현재 디렉토리 크기
du -sh .

# 모든 숨김 파일 표시
ls -ld .*

# 특정 날짜 이후 수정된 파일
find . -type f -newermt "2024-01-01"

# JSON 예쁘게 출력
cat file.json | python3 -m json.tool

# 시스템 부하 평균
cat /proc/loadavg

# 가장 많은 메모리 사용 프로세스
ps aux | sort -nk 4 | tail -5
```

---

## 부록 D: 유용한 환경 변수

```bash
$HOME           홈 디렉토리
$USER           현재 사용자
$PATH           실행 파일 검색 경로
$SHELL          현재 셸
$PWD            현재 작업 디렉토리
$OLDPWD         이전 작업 디렉토리
$EDITOR         기본 텍스트 에디터
$LANG           로케일 설정
$PS1            프롬프트 설정
$HISTSIZE       히스토리 크기
$HOSTNAME       호스트명
$RANDOM         랜덤 숫자
$$              현재 셸 PID
$?              마지막 명령 종료 상태
```

---

## 부록 E: 참고 자료

### 공식 문서
- [Linux Documentation Project](https://tldp.org/)
- [Arch Wiki](https://wiki.archlinux.org/) - 배포판 무관 우수한 문서
- [Ubuntu Documentation](https://help.ubuntu.com/)
- [RHEL Documentation](https://access.redhat.com/documentation/)

### 온라인 리소스
- `man command` - 명령어 매뉴얼
- `info command` - GNU Info 문서
- `command --help` - 간단한 도움말
- [ExplainShell](https://explainshell.com/) - 명령어 설명
- [Command Line Challenge](https://cmdchallenge.com/) - 실습

### 책 추천
- "The Linux Command Line" - William Shotts
- "UNIX and Linux System Administration Handbook" - Evi Nemeth
- "How Linux Works" - Brian Ward

---

## 마치며

이 가이드는 리눅스/유닉스 시스템의 기본부터 고급 주제까지 포괄적으로 다룹니다. 각 섹션은 독립적으로 읽을 수 있으며, 필요에 따라 참고할 수 있습니다.

**학습 팁**:
1. 실습 환경을 구축하고 직접 명령어를 실행해보세요
2. 가상 머신이나 컨테이너를 사용하면 안전하게 실험할 수 있습니다
3. `man` 페이지를 자주 참고하세요
4. 스크립트를 작성하여 반복 작업을 자동화하세요
5. 커뮤니티에 참여하여 질문하고 답변하세요

**안전 수칙**:
- `rm -rf`는 항상 신중하게 사용
- 프로덕션 시스템에서는 변경 전 백업
- 권한 상승(`sudo`)은 필요할 때만
- 알 수 없는 명령어는 실행 전 확인

리눅스/유닉스를 즐겁게 배우시기 바랍니다! 🐧

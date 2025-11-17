# 프로세스 보기

## 목차
- [프로세스 기본 개념](#프로세스-기본-개념)
- [ps 명령어](#ps-명령어)
- [top 명령어](#top-명령어)
- [htop 명령어](#htop-명령어)
- [/proc 파일시스템](#proc-파일시스템)
- [기타 유틸리티](#기타-유틸리티)
- [실전 예제](#실전-예제)

---

## 프로세스 기본 개념

### 프로세스란?

프로세스는 실행 중인 프로그램의 인스턴스입니다.

```bash
# 프로세스 속성:
# - PID: 프로세스 ID (고유 번호)
# - PPID: 부모 프로세스 ID
# - UID/GID: 사용자/그룹 ID
# - 상태: Running, Sleeping, Stopped, Zombie
# - 우선순위: Nice 값, 스케줄링 우선순위
# - 메모리: 가상/물리 메모리 사용량
# - CPU: CPU 사용률
```

### 프로세스 상태

```bash
# 프로세스 상태 코드:
# R - Running (실행 중)
# S - Sleeping (대기 중)
# D - Uninterruptible sleep (입출력 대기)
# T - Stopped (정지됨)
# Z - Zombie (종료되었으나 부모가 회수하지 않음)
# < - 높은 우선순위
# N - 낮은 우선순위
# L - 메모리 잠금
# s - 세션 리더
# + - 포그라운드 프로세스 그룹
```

---

## ps 명령어

### 기본 사용법

```bash
# 현재 터미널의 프로세스
$ ps
  PID TTY          TIME CMD
 1234 pts/0    00:00:00 bash
 5678 pts/0    00:00:00 ps

# 모든 프로세스 (BSD 스타일)
$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 168344 11844 ?        Ss   Nov16   0:03 /sbin/init
user      1234  0.0  0.2  21584  5124 pts/0    Ss   10:23   0:00 -bash
user      5678  0.0  0.1  38348  3428 pts/0    R+   10:45   0:00 ps aux

# 모든 프로세스 (System V 스타일)
$ ps -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 Nov16 ?        00:00:03 /sbin/init
user      1234     1  0 10:23 pts/0    00:00:00 -bash
user      5678  1234  0 10:45 pts/0    00:00:00 ps -ef

# 전체 정보 (풀 포맷)
$ ps -ef --forest
$ ps auxf

# 사용자별
$ ps -u username
$ ps -U username

# 프로세스 ID로
$ ps -p 1234
$ ps -p 1234,5678,9012

# 커맨드 이름으로
$ ps -C nginx
$ ps -C apache2

# 트리 형태
$ ps -ejH
$ ps axjf
```

### ps 출력 커스터마이징

```bash
# 특정 컬럼만 표시
$ ps -eo pid,ppid,cmd,%mem,%cpu
  PID  PPID CMD                         %MEM %CPU
    1     0 /sbin/init                   0.1  0.0
 1234     1 -bash                        0.2  0.0

# 더 많은 컬럼
$ ps -eo user,pid,ppid,cmd,etime,nice,pri
USER       PID  PPID CMD                      ELAPSED  NI PRI
root         1     0 /sbin/init                  5-12:34  0  19
user      1234     1 -bash                          2:15  0  19

# 정렬
$ ps aux --sort=-%mem        # 메모리 사용량 내림차순
$ ps aux --sort=-%cpu        # CPU 사용량 내림차순
$ ps aux --sort=-rss         # RSS(실제 메모리) 내림차순
$ ps aux --sort=pid          # PID 오름차순

# 복합 정렬
$ ps aux --sort=-%cpu,-%mem

# 상위 10개
$ ps aux --sort=-%mem | head -11

# 특정 사용자의 프로세스
$ ps -u www-data -o pid,cmd

# 스레드 포함
$ ps -eLf
$ ps -T

# 보안 정보 포함
$ ps -eo pid,user,args,selinux

# 커널 스레드 제외
$ ps aux --ppid 2 -p 2 --deselect
```

### 프로세스 검색

```bash
# 이름으로 검색
$ ps aux | grep nginx
user      1234  0.0  0.5  12345  5432 ?        Ss   10:00   0:00 nginx: master
user      1235  0.0  0.3  12345  3456 ?        S    10:00   0:00 nginx: worker

# grep 자신 제외
$ ps aux | grep [n]ginx
$ ps aux | grep nginx | grep -v grep

# pgrep 사용 (더 편리)
$ pgrep nginx
1234
1235

# 프로세스 이름도 함께
$ pgrep -l nginx
1234 nginx
1235 nginx

# 전체 커맨드라인
$ pgrep -a nginx
1234 nginx: master process /usr/sbin/nginx
1235 nginx: worker process

# 특정 사용자의 프로세스
$ pgrep -u www-data
$ pgrep -u www-data nginx

# 부모 프로세스 ID로
$ pgrep -P 1

# 최신 프로세스
$ pgrep -n chrome
$ pgrep -o chrome  # 가장 오래된

# 개수 세기
$ pgrep -c nginx
2
```

### 프로세스 정보 상세 보기

```bash
# 환경변수 포함
$ ps eww -p 1234

# 전체 커맨드라인
$ ps -p 1234 -o cmd --no-headers
/usr/bin/python3 /usr/local/bin/myapp.py --config /etc/myapp.conf

# 프로세스 계층 구조
$ ps -ejH
$ pstree
systemd─┬─NetworkManager───2*[{NetworkManager}]
        ├─accounts-daemon───2*[{accounts-daemon}]
        ├─apache2───5*[apache2]
        ├─cron
        ├─dbus-daemon
        └─systemd-logind

# 특정 프로세스 트리
$ pstree -p 1234
$ pstree -s 1234  # 상위 부모까지

# ASCII 아트로
$ pstree -a

# 사용자별 트리
$ pstree username
```

---

## top 명령어

### 기본 사용

```bash
# top 실행
$ top

# 출력 예시:
top - 10:45:23 up 5 days,  3:21,  2 users,  load average: 0.15, 0.10, 0.08
Tasks: 245 total,   1 running, 244 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.3 us,  0.7 sy,  0.0 ni, 96.8 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :  15867.2 total,   8234.5 free,   3456.7 used,   4176.0 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.  11234.5 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 user      20   0 2345678 123456  45678 S   5.3   0.8   1:23.45 chrome
 5678 user      20   0 1234567  98765  32109 S   2.0   0.6   0:45.12 firefox
    1 root      20   0  168344  11844   8234 S   0.0   0.1   0:03.45 systemd

# 해석:
# load average: 1분, 5분, 15분 평균 부하
# Tasks: 프로세스 개수 및 상태
# Cpu(s): us(사용자), sy(시스템), ni(nice), id(유휴), wa(IO 대기)
# Mem: 메모리 사용량
# Swap: 스왑 사용량
```

### top 인터랙티브 명령

```bash
# top 실행 중 사용 가능한 키:

# h 또는 ? : 도움말
# q : 종료
# k : 프로세스 종료 (PID 입력 필요)
# r : nice 값 변경
# u : 특정 사용자 필터
# M : 메모리 사용량 정렬
# P : CPU 사용량 정렬
# T : 실행 시간 정렬
# N : PID 정렬
# < : 정렬 필드 이전
# > : 정렬 필드 다음
# c : 커맨드라인 전체 표시 토글
# V : 포레스트 모드 (트리 보기)
# f : 필드 선택
# 1 : CPU 코어별 표시
# t : CPU 그래프 토글
# m : 메모리 그래프 토글
# W : 설정 저장 (~/.toprc)
# z : 컬러 토글
# x : 정렬 필드 하이라이트
# y : Running 프로세스 하이라이트
# Space : 즉시 새로고침
# d : 업데이트 간격 변경 (기본 3초)
```

### top 옵션

```bash
# 배치 모드 (스크립트용)
$ top -b -n 1
$ top -b -n 1 > top_output.txt

# 특정 프로세스만
$ top -p 1234
$ top -p 1234,5678,9012

# 특정 사용자
$ top -u username

# 업데이트 간격 지정 (초)
$ top -d 1

# CPU 코어별 표시로 시작
$ top -1

# 메모리 순 정렬로 시작
$ top -o %MEM
$ top -o RES

# CPU 순 정렬
$ top -o %CPU

# 특정 횟수만 업데이트 후 종료
$ top -n 5

# 보안 모드 (kill, renice 비활성화)
$ top -s

# 아이들 프로세스 숨기기
$ top -i
```

### top 실전 활용

```bash
# 메모리 상위 10개 프로세스
$ top -b -n 1 -o %MEM | head -17

# CPU 상위 프로세스 모니터링
$ top -b -d 5 -n 12 > cpu_monitor.txt  # 1분간 (5초x12)

# 특정 프로세스 모니터링
$ watch -n 1 "ps aux | grep nginx | grep -v grep"

# 프로세스 리소스 사용 기록
$ while true; do
    echo "$(date)" >> process_log.txt
    top -b -n 1 -p 1234 >> process_log.txt
    sleep 60
done
```

---

## htop 명령어

### htop 설치 및 기본 사용

```bash
# 설치
$ sudo apt install htop        # Ubuntu/Debian
$ sudo dnf install htop        # Fedora/RHEL
$ sudo pacman -S htop          # Arch

# 실행
$ htop

# htop 장점:
# - 컬러풀한 인터페이스
# - 마우스 지원
# - 수평/수직 스크롤
# - 프로세스 트리 보기
# - 여러 프로세스 선택 가능
# - 통합 검색
# - 더 직관적인 사용법
```

### htop 키 바인딩

```bash
# 네비게이션:
# ↑↓ : 프로세스 선택
# PgUp/PgDn : 페이지 이동
# Home/End : 시작/끝
# Space : 프로세스 태그 (다중 선택)

# 정렬:
# F6 또는 > : 정렬 기준 선택
# P : CPU% 정렬
# M : MEM% 정렬
# T : TIME+ 정렬
# N : PID 정렬

# 액션:
# F9 또는 k : 프로세스 종료 (시그널 선택)
# F7 : nice 값 증가 (우선순위 낮춤)
# F8 : nice 값 감소 (우선순위 높임)
# F4 또는 \ : 필터
# F3 또는 / : 검색
# F5 또는 t : 트리 보기 토글
# u : 사용자 필터
# c : 커맨드라인 전체 표시
# H : 사용자 스레드 숨기기/보이기
# K : 커널 스레드 숨기기/보이기
# F2 : 설정
# F10 또는 q : 종료

# 보기:
# F1 또는 h : 도움말
# F2 또는 S : 설정
# l : 프로세스 파일 열기 (lsof)
# s : strace 실행
```

### htop 설정

```bash
# F2로 설정 메뉴 진입

# 설정 옵션:
# - Meters: CPU, 메모리, 스왑 등의 미터 커스터마이징
# - Display options: 업데이트 간격, 트리 보기 등
# - Colors: 색상 스킴 선택
# - Columns: 표시할 컬럼 선택

# 명령행 옵션
$ htop -d 10          # 업데이트 간격 (1초 = 10)
$ htop -u username    # 특정 사용자
$ htop -p 1234,5678   # 특정 PID
$ htop -s MEM%        # 메모리 순 정렬
$ htop -t             # 트리 모드로 시작
```

---

## /proc 파일시스템

### /proc 개요

```bash
# /proc는 가상 파일시스템
# 커널과 프로세스 정보를 파일 형태로 제공

$ ls /proc/
1/     1234/  cmdline    filesystems  meminfo     swaps
2/     cpuinfo  devices  interrupts   modules     sys/
self/  diskstats  fb     ioports      net/        uptime
...
```

### /proc/[PID]/ 디렉토리

```bash
# 프로세스별 디렉토리
$ ls /proc/1234/
cmdline  cwd@  environ  exe@  fd/  maps  stat  status  ...

# 커맨드라인
$ cat /proc/1234/cmdline
/usr/bin/python3/usr/local/bin/app.py

# 읽기 쉽게
$ tr '\0' ' ' < /proc/1234/cmdline
/usr/bin/python3 /usr/local/bin/app.py

# 또는
$ cat /proc/1234/cmdline | xargs -0 echo

# 현재 작업 디렉토리
$ ls -l /proc/1234/cwd
lrwxrwxrwx 1 user user 0 Nov 17 10:00 /proc/1234/cwd -> /home/user/project

# 실행 파일
$ ls -l /proc/1234/exe
lrwxrwxrwx 1 user user 0 Nov 17 10:00 /proc/1234/exe -> /usr/bin/python3

# 환경 변수
$ cat /proc/1234/environ
PATH=/usr/binHOME=/home/userUSER=user

# 읽기 쉽게
$ tr '\0' '\n' < /proc/1234/environ
PATH=/usr/bin:/usr/local/bin
HOME=/home/user
USER=user

# 열린 파일 디스크립터
$ ls -l /proc/1234/fd/
lrwx------ 1 user user 64 Nov 17 10:00 0 -> /dev/pts/0
lrwx------ 1 user user 64 Nov 17 10:00 1 -> /dev/pts/0
lrwx------ 1 user user 64 Nov 17 10:00 2 -> /dev/pts/0
lr-x------ 1 user user 64 Nov 17 10:00 3 -> /var/log/app.log

# 메모리 맵
$ cat /proc/1234/maps
00400000-00452000 r-xp 00000000 08:01 123456  /usr/bin/myapp
00651000-00652000 r--p 00051000 08:01 123456  /usr/bin/myapp
...

# 프로세스 상태
$ cat /proc/1234/status
Name:   myapp
State:  S (sleeping)
Tgid:   1234
Pid:    1234
PPid:   1
Uid:    1000    1000    1000    1000
Gid:    1000    1000    1000    1000
VmSize:  123456 kB
VmRSS:   45678 kB
Threads:    4
...

# 간단한 통계
$ cat /proc/1234/stat
1234 (myapp) S 1 1234 1234 34816 1234 4194304 ...

# 스레드 목록
$ ls /proc/1234/task/
1234/  1235/  1236/  1237/

# 메모리 사용량
$ cat /proc/1234/statm
30864 11419 2876 82 0 7751 0

# IO 통계
$ cat /proc/1234/io
rchar: 123456789
wchar: 987654321
syscr: 12345
syscw: 6789
read_bytes: 10485760
write_bytes: 5242880
```

### 시스템 전역 정보

```bash
# CPU 정보
$ cat /proc/cpuinfo
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 142
model name      : Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz
...

# 메모리 정보
$ cat /proc/meminfo
MemTotal:       16248832 kB
MemFree:         8432156 kB
MemAvailable:   11502348 kB
Buffers:          423164 kB
Cached:          3876420 kB
SwapCached:            0 kB
SwapTotal:       2097148 kB
SwapFree:        2097148 kB
...

# 가동 시간
$ cat /proc/uptime
453621.45 1721458.90
# 첫 번째: 가동 시간 (초)
# 두 번째: 유휴 시간 (초, CPU별 합계)

# 평균 부하
$ cat /proc/loadavg
0.15 0.10 0.08 1/245 5678
# 1분, 5분, 15분 평균 / 실행중/전체 / 마지막 PID

# 파일시스템 정보
$ cat /proc/filesystems
nodev   sysfs
nodev   rootfs
nodev   proc
        ext4
        ext3
...

# 마운트 정보
$ cat /proc/mounts
sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
/dev/sda1 / ext4 rw,relatime,errors=remount-ro 0 0
...

# 네트워크 통계
$ cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
  eth0: 1234567890  987654    0    0    0     0          0         0 9876543210  876543    0    0    0     0       0          0
    lo: 123456      1234    0    0    0     0          0         0   123456    1234    0    0    0     0       0          0

# 커널 버전
$ cat /proc/version
Linux version 5.15.0-78-generic (buildd@ubuntu) (gcc version 11.3.0)

# 커널 커맨드라인
$ cat /proc/cmdline
BOOT_IMAGE=/boot/vmlinuz-5.15.0-78-generic root=UUID=... ro quiet splash
```

### /proc 실전 활용

```bash
# 프로세스가 사용하는 실제 메모리
$ awk '/^Rss:/{ sum += $2 } END { print sum " KB" }' /proc/1234/smaps

# 프로세스의 TCP 연결
$ sudo cat /proc/1234/net/tcp

# 프로세스가 열고 있는 파일 수
$ ls /proc/1234/fd | wc -l

# 좀비 프로세스 찾기
$ ps aux | awk '$8 ~ /Z/ { print }'

# 또는
$ for pid in /proc/[0-9]*; do
    if grep -q "State:.*Z (zombie)" $pid/status 2>/dev/null; then
        cat $pid/status | grep -E "Name|PPid|State"
    fi
done

# 가장 많은 메모리 사용하는 프로세스
$ for pid in /proc/[0-9]*; do
    awk '/^VmRSS:/ { print $2 " " FILENAME }' $pid/status 2>/dev/null
done | sort -rn | head -10

# CPU별 사용량
$ grep 'cpu ' /proc/stat
cpu  123456 789 234567 8901234 12345 0 6789 0 0 0

# 시스템 인터럽트
$ cat /proc/interrupts

# 모듈 정보
$ cat /proc/modules
```

---

## 기타 유틸리티

### pidof - PID 찾기

```bash
# 프로세스 이름으로 PID 찾기
$ pidof nginx
1234 1235 1236

# 첫 번째 PID만
$ pidof -s nginx
1234

# PID만 (에러 메시지 없음)
$ pidof -x script.sh
```

### pgrep - 프로세스 검색

```bash
# 이미 위에서 다뤘지만 추가 예제

# 여러 패턴
$ pgrep -f "python.*myapp"

# 정확한 매칭
$ pgrep -x bash

# 최근 생성된 프로세스
$ pgrep -n chrome

# 가장 오래된 프로세스
$ pgrep -o chrome

# 프로세스 개수
$ pgrep -c nginx

# 구분자 지정
$ pgrep -d, nginx
1234,1235,1236
```

### lsof - 열린 파일 보기

```bash
# 특정 프로세스가 연 파일
$ lsof -p 1234

# 특정 파일을 연 프로세스
$ lsof /var/log/syslog

# 특정 디렉토리
$ lsof +D /var/log/

# 특정 포트
$ lsof -i :80
$ lsof -i :8080

# TCP 연결
$ lsof -i tcp

# UDP 연결
$ lsof -i udp

# 특정 사용자
$ lsof -u username

# 사용자 제외
$ lsof -u ^username

# 네트워크 연결
$ lsof -i
$ lsof -i -n  # 호스트명 해석 안 함

# 삭제된 파일을 여전히 열고 있는 프로세스
$ lsof | grep deleted
$ lsof +L1

# 특정 파일시스템
$ lsof /dev/sda1
```

### fuser - 파일 사용 프로세스

```bash
# 파일 사용 중인 프로세스
$ fuser /var/log/syslog
/var/log/syslog:      1234

# 자세한 정보
$ fuser -v /var/log/syslog

# PID와 사용자
$ fuser -u /var/log/syslog

# 포트 사용
$ fuser 80/tcp
$ fuser 8080/tcp

# 마운트 포인트 사용
$ fuser -m /mnt/data

# 프로세스 종료
$ fuser -k /mnt/data
```

---

## 실전 예제

### 예제 1: 메모리 누수 찾기

```bash
# 메모리 사용량 모니터링
$ while true; do
    date >> mem_monitor.txt
    ps aux --sort=-%mem | head -20 >> mem_monitor.txt
    echo "---" >> mem_monitor.txt
    sleep 300  # 5분마다
done

# 특정 프로세스 메모리 추적
$ watch -n 5 "ps -p 1234 -o pid,vsz,rss,cmd"

# /proc로 상세 모니터링
$ while true; do
    echo "$(date) $(awk '/VmRSS/ {print $2}' /proc/1234/status) KB" >> mem_log.txt
    sleep 60
done
```

### 예제 2: CPU 사용률 높은 프로세스 찾기

```bash
# CPU 상위 10개
$ ps aux --sort=-%cpu | head -11

# 실시간 모니터링
$ top -o %CPU

# htop으로
$ htop -s PERCENT_CPU

# 스크립트로 로깅
$ top -b -n 1 -o %CPU | head -15 > cpu_usage.txt

# CPU 100% 사용 프로세스 찾기
$ ps aux | awk '$3 > 80.0 { print }'

# 평균 CPU 사용률 계산 (1분간)
$ for i in {1..12}; do
    top -b -n 1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
    sleep 5
done | awk '{ sum += $1; n++ } END { print sum/n "%" }'
```

### 예제 3: 좀비 프로세스 처리

```bash
# 좀비 프로세스 찾기
$ ps aux | grep 'Z'
$ ps aux | awk '$8 == "Z" { print }'

# 부모 프로세스 찾기
$ ps -o ppid= -p <zombie_pid>

# 부모 프로세스에 SIGCHLD 보내기
$ kill -s SIGCHLD <parent_pid>

# 부모 프로세스 재시작이 필요한 경우
$ sudo systemctl restart <service>

# 자동으로 좀비와 부모 찾기
$ ps aux | awk '$8 == "Z" { print $2 }' | while read zpid; do
    ppid=$(ps -o ppid= -p $zpid)
    echo "Zombie: $zpid, Parent: $ppid"
    echo "Parent command: $(ps -p $ppid -o cmd=)"
done
```

### 예제 4: 특정 애플리케이션 모니터링

```bash
# Nginx 프로세스 모니터링
$ watch -n 2 "ps aux | grep nginx | grep -v grep"

# Apache 워커 수 확인
$ ps aux | grep apache2 | grep -v grep | wc -l

# MySQL 연결 수
$ ps aux | grep mysql | wc -l

# 특정 사용자의 모든 프로세스
$ ps -u www-data -o pid,cmd

# 프로세스 트리로 보기
$ pstree -p www-data
```

### 예제 5: 프로세스 리소스 제한 확인

```bash
# 프로세스 제한 확인
$ cat /proc/1234/limits
Limit                     Soft Limit           Hard Limit           Units
Max cpu time              unlimited            unlimited            seconds
Max file size             unlimited            unlimited            bytes
Max data size             unlimited            unlimited            bytes
Max stack size            8388608              unlimited            bytes
Max core file size        0                    unlimited            bytes
Max open files            1024                 1048576              files
...

# 현재 열린 파일 수
$ ls /proc/1234/fd | wc -l

# 파일 디스크립터 제한과 사용량 비교
$ echo "Limit: $(ulimit -n)"
$ echo "Used: $(ls /proc/$$/fd | wc -l)"
```

---

## 문제 해결

### 프로세스가 안 보일 때

```bash
# 권한 문제 - sudo 사용
$ sudo ps aux

# 커널 스레드 포함
$ ps aux
$ ps -eaf

# 모든 세션
$ ps -e
$ ps -A
```

### 프로세스 정보가 부정확할 때

```bash
# 캐시 클리어 후 다시 확인
$ sync
$ sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'

# /proc가 마운트되어 있는지 확인
$ mount | grep proc
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
```

### 프로세스 찾기 어려울 때

```bash
# 여러 방법 조합
$ ps aux | grep myapp
$ pgrep -a myapp
$ pidof myapp
$ lsof -c myapp
$ pstree -p | grep myapp

# systemd 서비스인 경우
$ systemctl status myapp
$ systemctl show myapp
```

---

## 성능 고려사항

```bash
# ps는 /proc를 읽으므로 많은 프로세스가 있으면 느림
# 필요한 정보만 가져오기
$ ps -eo pid,cmd --no-headers

# top/htop은 지속적으로 시스템 정보를 읽으므로
# 업데이트 간격을 늘려 부하 감소
$ top -d 5  # 5초마다
$ htop -d 50  # 5초마다

# 스크립트에서는 배치 모드 사용
$ top -b -n 1

# 큰 시스템에서는 특정 프로세스만 모니터링
$ ps -p 1234,5678 -o pid,cmd,%cpu,%mem
```

---

## 요약

프로세스 보기 도구:

1. **ps** - 프로세스 스냅샷
   - `ps aux` - 모든 프로세스
   - `ps -ef` - 전체 포맷
   - `ps --sort=-%mem` - 정렬

2. **top** - 실시간 모니터링
   - 인터랙티브한 프로세스 뷰어
   - CPU, 메모리 사용량 실시간 확인

3. **htop** - 개선된 top
   - 더 나은 UI
   - 마우스 지원
   - 트리 뷰

4. **/proc** - 프로세스 파일시스템
   - `/proc/[PID]/` - 프로세스별 정보
   - 직접 커널 정보 접근

5. **기타 도구**
   - pgrep, pidof - PID 찾기
   - lsof - 열린 파일
   - pstree - 프로세스 트리

---

[다음: 프로세스 제어 →](process-control.md)

[← 특수 권한으로 돌아가기](../05-permissions/special.md)

[← 목차로 돌아가기](../README.md)

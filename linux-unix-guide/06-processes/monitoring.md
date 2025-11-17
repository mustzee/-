# 시스템 모니터링

## 목차
- [성능 모니터링 개요](#성능-모니터링-개요)
- [vmstat - 가상 메모리 통계](#vmstat---가상-메모리-통계)
- [iostat - IO 통계](#iostat---io-통계)
- [mpstat - CPU 통계](#mpstat---cpu-통계)
- [sar - 시스템 활동 보고](#sar---시스템-활동-보고)
- [기타 모니터링 도구](#기타-모니터링-도구)
- [실전 예제](#실전-예제)

---

## 성능 모니터링 개요

### 모니터링해야 할 주요 리소스

```bash
# 4가지 주요 리소스:
# 1. CPU - 프로세서 사용률
# 2. Memory - 메모리 사용량
# 3. Disk I/O - 디스크 입출력
# 4. Network - 네트워크 트래픽

# 성능 지표:
# - Throughput (처리량)
# - Latency (지연시간)
# - Utilization (사용률)
# - Saturation (포화도)
# - Errors (오류율)
```

### sysstat 패키지 설치

```bash
# Ubuntu/Debian
$ sudo apt update
$ sudo apt install sysstat

# RHEL/Fedora
$ sudo dnf install sysstat

# Arch
$ sudo pacman -S sysstat

# 활성화 (Ubuntu/Debian)
$ sudo vi /etc/default/sysstat
# ENABLED="true"

# 서비스 시작
$ sudo systemctl enable sysstat
$ sudo systemctl start sysstat

# 데이터 수집 설정
$ sudo vi /etc/cron.d/sysstat
# */10 * * * * root /usr/lib/sysstat/sa1 1 1

# 설치 확인
$ sar
$ iostat
$ mpstat
```

---

## vmstat - 가상 메모리 통계

### 기본 사용법

```bash
# 한 번 실행
$ vmstat
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 8234156 423164 3876420    0    0    12    45  123  456  2  1 97  0  0

# 컬럼 설명:
# procs:
#   r: 실행 대기 중인 프로세스 수
#   b: I/O 대기 중인 프로세스 수 (uninterruptible sleep)
#
# memory: (KB)
#   swpd: 스왑 사용량
#   free: 사용 가능한 메모리
#   buff: 버퍼 캐시
#   cache: 페이지 캐시
#
# swap: (KB/s)
#   si: 스왑 인 (디스크→메모리)
#   so: 스왑 아웃 (메모리→디스크)
#
# io: (blocks/s)
#   bi: 블록 디바이스로부터 받은 블록
#   bo: 블록 디바이스로 보낸 블록
#
# system:
#   in: 초당 인터럽트 수
#   cs: 초당 컨텍스트 스위치 수
#
# cpu: (%)
#   us: 사용자 시간
#   sy: 시스템 시간
#   id: 유휴 시간
#   wa: I/O 대기 시간
#   st: stolen time (가상화)
```

### vmstat 활용

```bash
# 2초마다 업데이트
$ vmstat 2

# 10번만 출력
$ vmstat 2 10

# 5초마다, 12번 (1분간)
$ vmstat 5 12

# MB 단위
$ vmstat -S M 2

# 활성/비활성 메모리 표시
$ vmstat -a 2

# 디스크 통계
$ vmstat -d
disk- ------------reads------------ ------------writes----------- -----IO------
       total merged sectors      ms  total merged sectors      ms    cur    sec
sda   123456   1234 1234567   12345 234567   2345 2345678   23456      0    123
sdb    12345    123  123456    1234  23456    234  234567    2345      0     12

# 슬랩 정보 (커널 메모리 캐시)
$ vmstat -m
Cache                       Num  Total   Size  Pages
ext4_inode_cache         123456 234567    1024     4
dentry                   234567 345678     192    21

# 파티션별 통계
$ vmstat -p /dev/sda1
sda1          reads   read sectors  writes    requested writes
               12345     123456     23456      234567

# 타임스탬프 포함
$ vmstat -t 2
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu----- -----timestamp-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st                 KST
 1  0      0 8234156 423164 3876420    0    0    12    45  123  456  2  1 97  0  0 2024-11-17 10:45:23
```

### vmstat 분석

```bash
# 메모리 부족 징후:
# - si, so가 계속 0이 아님 (스와핑 발생)
# - free가 매우 낮음
# - buff+cache가 줄어듦

# CPU 병목:
# - r (실행 대기)이 CPU 코어 수보다 많음
# - us+sy가 높음 (>80%)
# - id가 낮음 (<20%)

# I/O 병목:
# - b (I/O 대기)가 높음
# - wa (I/O wait)가 높음 (>20%)
# - bi, bo가 높음

# 스크립트로 모니터링
#!/bin/bash
vmstat 5 | while read line; do
    echo "$(date): $line"
    wa=$(echo $line | awk '{print $16}')
    if [ -n "$wa" ] && [ "$wa" -gt 20 ] 2>/dev/null; then
        echo "WARNING: High I/O wait: ${wa}%"
    fi
done
```

---

## iostat - IO 통계

### 기본 사용법

```bash
# 기본 출력
$ iostat
Linux 5.15.0-78-generic (hostname)      11/17/2024      _x86_64_        (4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.34    0.00    0.87    0.12    0.00   96.67

Device             tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd
sda               5.67       123.45       234.56         0.00   12345678   23456789          0
sdb               1.23        12.34        23.45         0.00    1234567    2345678          0

# 컬럼 설명:
# tps: 초당 전송 수 (Transfers per second)
# kB_read/s: 초당 읽은 KB
# kB_wrtn/s: 초당 쓴 KB
# kB_read: 총 읽은 KB
# kB_wrtn: 총 쓴 KB
```

### iostat 옵션

```bash
# 2초마다 업데이트
$ iostat 2

# 확장 통계
$ iostat -x 2
Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              5.67    3.45    123.45    234.56     0.12     0.23   2.07   6.25    2.34    5.67   0.02    21.78    67.95   1.23   1.12

# 확장 컬럼 설명:
# r/s, w/s: 초당 읽기/쓰기 요청
# rkB/s, wkB/s: 초당 읽기/쓰기 KB
# rrqm/s, wrqm/s: 초당 병합된 읽기/쓰기 요청
# %rrqm, %wrqm: 병합 비율
# r_await, w_await: 읽기/쓰기 평균 대기 시간 (ms)
# aqu-sz: 평균 큐 크기
# rareq-sz, wareq-sz: 평균 요청 크기 (KB)
# svctm: 서비스 시간 (ms)
# %util: 디바이스 사용률

# CPU 통계만
$ iostat -c 2

# 디스크 통계만
$ iostat -d 2

# MB 단위
$ iostat -m 2

# 특정 디바이스
$ iostat -x sda 2

# 여러 디바이스
$ iostat -x sda sdb 2

# NFS 통계
$ iostat -n 2

# 파티션별 통계
$ iostat -p sda 2

# 타임스탬프
$ iostat -t 2

# JSON 출력
$ iostat -o JSON 2

# 사람이 읽기 쉬운 형식
$ iostat -h 2
```

### iostat 분석

```bash
# I/O 병목 징후:
# - %util이 높음 (>80%)
# - await가 높음 (>10ms SSD, >20ms HDD)
# - aqu-sz가 높음 (큐가 쌓임)

# 순차 읽기/쓰기:
# - rareq-sz, wareq-sz가 큼
# - 높은 처리량

# 랜덤 읽기/쓰기:
# - 요청 크기가 작음
# - 높은 IOPS, 낮은 처리량

# 모니터링 스크립트
#!/bin/bash
iostat -x 5 | while read line; do
    if echo "$line" | grep -q '^sda'; then
        util=$(echo $line | awk '{print $NF}' | cut -d. -f1)
        if [ "$util" -gt 80 ] 2>/dev/null; then
            echo "$(date): WARNING: High disk utilization on sda: ${util}%"
        fi
    fi
done
```

---

## mpstat - CPU 통계

### 기본 사용법

```bash
# 전체 CPU 평균
$ mpstat
Linux 5.15.0-78-generic (hostname)      11/17/2024      _x86_64_        (4 CPU)

10:45:23 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:45:23 AM  all    2.34    0.00    0.87    0.12    0.00    0.05    0.00    0.00    0.00   96.62

# 컬럼 설명:
# %usr: 사용자 레벨 (애플리케이션)
# %nice: nice 우선순위 프로세스
# %sys: 시스템 레벨 (커널)
# %iowait: I/O 대기
# %irq: 하드웨어 인터럽트
# %soft: 소프트웨어 인터럽트
# %steal: 가상화 환경에서 stolen time
# %guest: 게스트 OS 실행
# %idle: 유휴
```

### mpstat 옵션

```bash
# 모든 CPU 코어 개별 표시
$ mpstat -P ALL 2
10:45:23 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
10:45:23 AM  all    2.34    0.00    0.87    0.12    0.00    0.05    0.00    0.00    0.00   96.62
10:45:23 AM    0    3.45    0.00    1.23    0.23    0.00    0.08    0.00    0.00    0.00   95.01
10:45:23 AM    1    1.89    0.00    0.67    0.08    0.00    0.04    0.00    0.00    0.00   97.32
10:45:23 AM    2    2.12    0.00    0.78    0.10    0.00    0.05    0.00    0.00    0.00   96.95
10:45:23 AM    3    1.98    0.00    0.81    0.06    0.00    0.03    0.00    0.00    0.00   97.12

# 특정 CPU만
$ mpstat -P 0 2
$ mpstat -P 0,2,4 2

# 2초마다, 10번
$ mpstat 2 10

# 인터럽트 통계
$ mpstat -I ALL 2
$ mpstat -I SUM 2
$ mpstat -I CPU 2
$ mpstat -I SCPU 2

# JSON 출력
$ mpstat -o JSON 2

# 타임스탬프
$ mpstat -T 2
```

### mpstat 분석

```bash
# CPU 병목:
# - %usr + %sys가 높음 (>80%)
# - %idle이 낮음 (<20%)
# - 특정 코어만 100% (단일 스레드 병목)

# I/O 대기:
# - %iowait가 높음 (>20%)
# - 스토리지 성능 문제

# 컨텍스트 스위칭:
# - %sys가 높음
# - 너무 많은 프로세스/스레드

# CPU 불균형 탐지
#!/bin/bash
mpstat -P ALL 2 1 | grep -v "^$\|Linux\|Average\|CPU" | while read line; do
    cpu=$(echo $line | awk '{print $2}')
    idle=$(echo $line | awk '{print $NF}')
    if [ "$cpu" != "all" ]; then
        usage=$(echo "100 - $idle" | bc)
        if (( $(echo "$usage > 80" | bc -l) )); then
            echo "CPU $cpu is heavily loaded: ${usage}%"
        fi
    fi
done
```

---

## sar - 시스템 활동 보고

### sar 개요

```bash
# sar (System Activity Reporter):
# - 가장 포괄적인 성능 모니터링 도구
# - 데이터 수집 및 보고
# - /var/log/sysstat/에 저장
# - sa1 (수집), sa2 (보고)

# 오늘의 모든 통계
$ sar

# 시간 범위 지정
$ sar -s 10:00:00 -e 12:00:00

# 특정 날짜
$ sar -f /var/log/sysstat/sa16  # 16일 데이터
```

### CPU 모니터링

```bash
# CPU 사용률 (기본)
$ sar -u 2 5
Linux 5.15.0-78-generic (hostname)      11/17/2024      _x86_64_        (4 CPU)

10:45:23 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle
10:45:25 AM     all      2.34      0.00      0.87      0.12      0.00     96.67
10:45:27 AM     all      3.45      0.00      1.23      0.23      0.00     95.09
...

# 모든 CPU 코어
$ sar -P ALL 2 5

# 특정 CPU
$ sar -P 0,2 2 5
```

### 메모리 모니터링

```bash
# 메모리 사용률
$ sar -r 2 5
10:45:23 AM kbmemfree   kbavail kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit
10:45:25 AM   8234156  11502348   3456789     21.80    423164   3876420   5432167     33.30

# 스왑 사용률
$ sar -S 2 5
10:45:23 AM kbswpfree kbswpused  %swpused  kbswpcad   %swpcad
10:45:25 AM   2097148         0      0.00         0      0.00

# 메모리 통계 (상세)
$ sar -R 2 5
10:45:23 AM   frmpg/s   bufpg/s   campg/s
10:45:25 AM      0.00      0.00      0.00

# 페이징 통계
$ sar -B 2 5
10:45:23 AM  pgpgin/s pgpgout/s   fault/s  majflt/s  pgfree/s pgscank/s pgscand/s pgsteal/s    %vmeff
10:45:25 AM     12.34     23.45    123.45      0.00    234.56      0.00      0.00      0.00      0.00
```

### I/O 모니터링

```bash
# I/O 전송률
$ sar -b 2 5
10:45:23 AM       tps      rtps      wtps   bread/s   bwrtn/s
10:45:25 AM      5.67      2.34      3.33    123.45    234.56

# 블록 디바이스
$ sar -d 2 5
10:45:23 AM       DEV       tps     rkB/s     wkB/s   areq-sz    aqu-sz     await     svctm     %util
10:45:25 AM  dev8-0      5.67    123.45    234.56     63.21      0.02      3.45      1.23      0.70

# 확장 디스크 통계
$ sar -d -p 2 5  # 디바이스 이름 표시
```

### 네트워크 모니터링

```bash
# 네트워크 인터페이스
$ sar -n DEV 2 5
10:45:23 AM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
10:45:25 AM      eth0    123.45    234.56     12.34     23.45      0.00      0.00      0.00
10:45:25 AM        lo      5.67      5.67      0.56      0.56      0.00      0.00      0.00

# 네트워크 에러
$ sar -n EDEV 2 5
10:45:23 AM     IFACE   rxerr/s   txerr/s    coll/s  rxdrop/s  txdrop/s  txcarr/s  rxfram/s  rxfifo/s  txfifo/s
10:45:25 AM      eth0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00

# TCP 통계
$ sar -n TCP 2 5
10:45:23 AM  active/s passive/s    iseg/s    oseg/s
10:45:25 AM      2.34      1.23    123.45    234.56

# 소켓 통계
$ sar -n SOCK 2 5
10:45:23 AM    totsck    tcpsck    udpsck    rawsck   ip-frag    tcp-tw
10:45:25 AM       234        45        12         0         0        23

# IP 통계
$ sar -n IP 2 5

# 모든 네트워크 통계
$ sar -n ALL 2 5
```

### 부하 및 프로세스

```bash
# 시스템 부하 및 작업 큐
$ sar -q 2 5
10:45:23 AM   runq-sz  plist-sz   ldavg-1   ldavg-5  ldavg-15   blocked
10:45:25 AM         1       245      0.15      0.10      0.08         0

# 프로세스 생성률
$ sar -w 2 5
10:45:23 AM    proc/s   cswch/s
10:45:25 AM      2.34    456.78

# 컨텍스트 스위치 (상세)
$ sar -W 2 5
```

### sar 실전 활용

```bash
# 어제의 CPU 피크 시간 찾기
$ sar -u -f /var/log/sysstat/sa$(date -d yesterday +%d) | \
  sort -k4 -rn | head -20

# 오늘의 메모리 사용 추이
$ sar -r | grep -v "^$\|Linux\|Average"

# 네트워크 트래픽 피크
$ sar -n DEV | grep eth0 | sort -k5 -rn | head -10

# 전날 00:00-06:00 시간대 분석
$ sar -u -f /var/log/sysstat/sa$(date -d yesterday +%d) \
  -s 00:00:00 -e 06:00:00

# 종합 리포트 생성
$ sar -A > system_report_$(date +%Y%m%d).txt

# 실시간 모니터링 대시보드
#!/bin/bash
while true; do
    clear
    echo "=== System Monitor ==="
    echo "Time: $(date)"
    echo
    echo "=== CPU ==="
    sar -u 1 1 | grep Average | awk '{print "User: "$3"% System: "$5"% Idle: "$NF"%"}'
    echo
    echo "=== Memory ==="
    sar -r 1 1 | grep Average | awk '{print "Used: "$4"% Available: "$6" KB"}'
    echo
    echo "=== Disk I/O ==="
    sar -d -p 1 1 | grep Average | grep -v "^$\|DEV"
    echo
    echo "=== Network ==="
    sar -n DEV 1 1 | grep Average | grep eth0
    sleep 5
done
```

---

## 기타 모니터링 도구

### iotop - 프로세스별 I/O

```bash
# 설치
$ sudo apt install iotop

# 실행
$ sudo iotop

# 배치 모드
$ sudo iotop -b -n 5

# 프로세스만 (스레드 제외)
$ sudo iotop -P

# 누적 I/O
$ sudo iotop -a

# KB 단위
$ sudo iotop -k
```

### nethogs - 프로세스별 네트워크

```bash
# 설치
$ sudo apt install nethogs

# 실행
$ sudo nethogs

# 특정 인터페이스
$ sudo nethogs eth0

# 업데이트 간격
$ sudo nethogs -d 5
```

### dstat - 다목적 통계

```bash
# 설치
$ sudo apt install dstat

# 기본
$ dstat

# CPU, 디스크, 네트워크
$ dstat -cdn

# 상세
$ dstat -cdngy

# 5초마다
$ dstat 5

# 최상위 CPU 프로세스
$ dstat --top-cpu

# 최상위 I/O 프로세스
$ dstat --top-io

# 모든 디스크
$ dstat -D total,sda,sdb

# CSV 출력
$ dstat --output dstat.csv 5 60
```

### atop - 고급 시스템 모니터

```bash
# 설치
$ sudo apt install atop

# 실행
$ sudo atop

# 키 바인딩:
# g: 일반 정보
# m: 메모리 세부정보
# d: 디스크 세부정보
# n: 네트워크 세부정보
# c: 커맨드라인 전체

# 로깅 모드 (10분마다 저장)
$ sudo atop -w /tmp/atop.log 600

# 로그 재생
$ atop -r /tmp/atop.log
```

### nmon - 성능 모니터

```bash
# 설치
$ sudo apt install nmon

# 실행
$ nmon

# 키:
# c: CPU
# m: 메모리
# d: 디스크
# n: 네트워크
# t: 상위 프로세스
# q: 종료

# 레코딩 모드
$ nmon -f -s 10 -c 360
# -f: 파일에 저장
# -s 10: 10초 간격
# -c 360: 360번 (1시간)
```

---

## 실전 예제

### 예제 1: 성능 베이스라인 수집

```bash
#!/bin/bash
# collect_baseline.sh - 시스템 베이스라인 수집

OUTPUT_DIR="/var/log/performance_baseline"
DURATION=3600  # 1시간
INTERVAL=5

mkdir -p "$OUTPUT_DIR"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Collecting performance baseline..."

# CPU
mpstat -P ALL $INTERVAL $(($DURATION / $INTERVAL)) > "$OUTPUT_DIR/cpu_${DATE}.log" &

# 메모리
vmstat $INTERVAL $(($DURATION / $INTERVAL)) > "$OUTPUT_DIR/mem_${DATE}.log" &

# I/O
iostat -x $INTERVAL $(($DURATION / $INTERVAL)) > "$OUTPUT_DIR/io_${DATE}.log" &

# 네트워크
sar -n DEV $INTERVAL $(($DURATION / $INTERVAL)) > "$OUTPUT_DIR/net_${DATE}.log" &

# 프로세스
while true; do
    ps aux --sort=-%cpu | head -20 >> "$OUTPUT_DIR/processes_${DATE}.log"
    sleep $INTERVAL
done &
PROC_PID=$!

wait

echo "Baseline collection complete. Data saved to $OUTPUT_DIR/"
```

### 예제 2: 성능 문제 자동 감지

```bash
#!/bin/bash
# performance_alert.sh

CPU_THRESHOLD=80
MEM_THRESHOLD=80
IO_WAIT_THRESHOLD=20
DISK_UTIL_THRESHOLD=80

check_cpu() {
    cpu_usage=$(mpstat 1 1 | awk '/Average/ {print 100 - $NF}' | cut -d. -f1)
    if [ "$cpu_usage" -gt "$CPU_THRESHOLD" ]; then
        echo "ALERT: High CPU usage: ${cpu_usage}%"
        ps aux --sort=-%cpu | head -10
        return 1
    fi
    return 0
}

check_memory() {
    mem_usage=$(free | awk '/Mem/ {printf "%.0f", $3/$2 * 100}')
    if [ "$mem_usage" -gt "$MEM_THRESHOLD" ]; then
        echo "ALERT: High memory usage: ${mem_usage}%"
        ps aux --sort=-%mem | head -10
        return 1
    fi
    return 0
}

check_io() {
    io_wait=$(vmstat 1 2 | tail -1 | awk '{print $16}')
    if [ "$io_wait" -gt "$IO_WAIT_THRESHOLD" ]; then
        echo "ALERT: High I/O wait: ${io_wait}%"
        iostat -x 1 1
        return 1
    fi
    return 0
}

check_disk() {
    iostat -x 1 2 | grep -v "^$\|Linux\|Device" | tail -n +2 | while read line; do
        device=$(echo $line | awk '{print $1}')
        util=$(echo $line | awk '{print $NF}' | cut -d. -f1)
        if [ "$util" -gt "$DISK_UTIL_THRESHOLD" ] 2>/dev/null; then
            echo "ALERT: High disk utilization on $device: ${util}%"
            return 1
        fi
    done
}

while true; do
    echo "=== Performance Check: $(date) ==="
    check_cpu
    check_memory
    check_io
    check_disk
    echo "---"
    sleep 60
done
```

### 예제 3: 일일 리포트 생성

```bash
#!/bin/bash
# daily_report.sh

REPORT_DIR="/var/log/daily_reports"
DATE=$(date +%Y%m%d)
YESTERDAY=$(date -d yesterday +%d)

mkdir -p "$REPORT_DIR"
REPORT_FILE="$REPORT_DIR/report_${DATE}.txt"

{
    echo "========================================="
    echo "Daily Performance Report"
    echo "Date: $(date)"
    echo "========================================="
    echo

    echo "=== System Info ==="
    uname -a
    echo "Uptime: $(uptime)"
    echo

    echo "=== CPU Summary ==="
    sar -u -f /var/log/sysstat/sa$YESTERDAY | grep Average
    echo

    echo "=== Memory Summary ==="
    sar -r -f /var/log/sysstat/sa$YESTERDAY | grep Average
    echo

    echo "=== Disk I/O Summary ==="
    sar -d -p -f /var/log/sysstat/sa$YESTERDAY | grep Average
    echo

    echo "=== Network Summary ==="
    sar -n DEV -f /var/log/sysstat/sa$YESTERDAY | grep Average | grep -v "lo"
    echo

    echo "=== Load Average Peaks ==="
    sar -q -f /var/log/sysstat/sa$YESTERDAY | grep -v "^$\|Linux\|Average" | \
        sort -k5 -rn | head -10
    echo

    echo "=== Top CPU Consumers (current) ==="
    ps aux --sort=-%cpu | head -11
    echo

    echo "=== Top Memory Consumers (current) ==="
    ps aux --sort=-%mem | head -11
    echo

    echo "=== Disk Usage ==="
    df -h
    echo

} > "$REPORT_FILE"

echo "Report generated: $REPORT_FILE"
```

### 예제 4: 실시간 대시보드

```bash
#!/bin/bash
# dashboard.sh

while true; do
    clear
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║          SYSTEM PERFORMANCE DASHBOARD                ║"
    echo "║          $(date)                     ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    echo

    echo "┌─ CPU ────────────────────────────────────────────────┐"
    mpstat 1 1 | grep Average | \
        awk '{printf "  User: %5.1f%%  System: %5.1f%%  Idle: %5.1f%%\n", $3, $5, $NF}'
    echo "└──────────────────────────────────────────────────────┘"
    echo

    echo "┌─ Memory ─────────────────────────────────────────────┐"
    free -h | awk '/Mem/ {printf "  Total: %6s  Used: %6s  Free: %6s  Avail: %6s\n", $2, $3, $4, $7}'
    echo "└──────────────────────────────────────────────────────┘"
    echo

    echo "┌─ Disk I/O ───────────────────────────────────────────┐"
    iostat -x 1 1 | grep -E "^(sd|nvme)" | \
        awk '{printf "  %-8s  Read: %6.1f KB/s  Write: %6.1f KB/s  Util: %5.1f%%\n", $1, $4, $5, $NF}'
    echo "└──────────────────────────────────────────────────────┘"
    echo

    echo "┌─ Network ────────────────────────────────────────────┐"
    sar -n DEV 1 1 | grep Average | grep -v "lo\|IFACE" | \
        awk '{printf "  %-8s  RX: %7.1f KB/s  TX: %7.1f KB/s\n", $2, $5, $6}'
    echo "└──────────────────────────────────────────────────────┘"
    echo

    echo "┌─ Load Average ───────────────────────────────────────┐"
    uptime | awk -F'load average:' '{printf "  %s\n", $2}'
    echo "└──────────────────────────────────────────────────────┘"

    sleep 5
done
```

---

## 문제 해결

### 데이터 수집 안 될 때

```bash
# sysstat 서비스 확인
$ systemctl status sysstat

# cron 확인
$ cat /etc/cron.d/sysstat

# 수동 수집
$ sudo /usr/lib/sysstat/sa1
$ sudo /usr/lib/sysstat/sa2

# 로그 위치 확인
$ ls -l /var/log/sysstat/
```

### 높은 I/O wait

```bash
# 어떤 프로세스가 I/O 하는지
$ sudo iotop -oa

# 어떤 디스크가 병목인지
$ iostat -x 1

# 디스크 큐 확인
$ cat /sys/block/sda/queue/nr_requests
```

---

## 요약

시스템 모니터링 도구:

1. **vmstat** - 가상 메모리, 전반적 시스템 상태
2. **iostat** - 디스크 I/O 성능
3. **mpstat** - CPU별 성능
4. **sar** - 포괄적 시스템 통계, 과거 데이터
5. **기타** - iotop, nethogs, dstat, atop, nmon

---

[다음: 네트워크 설정 →](../08-networking/configuration.md)

[← 시그널로 돌아가기](signals.md)

[← 목차로 돌아가기](../README.md)

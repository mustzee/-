# 프로세스 제어

## 목차
- [포그라운드와 백그라운드](#포그라운드와-백그라운드)
- [작업 제어](#작업-제어)
- [프로세스 종료](#프로세스-종료)
- [프로세스 우선순위](#프로세스-우선순위)
- [프로세스 제한](#프로세스-제한)
- [실전 예제](#실전-예제)

---

## 포그라운드와 백그라운드

### 기본 개념

```bash
# 포그라운드 (Foreground):
# - 터미널을 점유하는 프로세스
# - 입력을 받고 출력을 화면에 표시
# - Ctrl+C로 종료, Ctrl+Z로 일시정지

# 백그라운드 (Background):
# - 터미널에서 분리되어 실행
# - 사용자 상호작용 없이 실행
# - 터미널을 계속 사용 가능
```

### 백그라운드 실행

```bash
# 명령어 끝에 & 추가
$ long_running_command &
[1] 12345

# 여러 명령어
$ command1 & command2 & command3 &

# 출력 리다이렉션과 함께
$ command > output.log 2>&1 &
[1] 12346

# nohup으로 터미널 종료 후에도 계속 실행
$ nohup command &
$ nohup command > output.log 2>&1 &

# nohup 없이 disown 사용
$ command &
$ disown

# 특정 작업만 disown
$ disown %1

# 모든 작업 disown
$ disown -a

# 실행 중인 프로세스를 백그라운드로
# 1. Ctrl+Z로 일시정지
# 2. bg 명령어로 백그라운드 재개
$ long_command
^Z
[1]+  Stopped                 long_command
$ bg
[1]+ long_command &
```

### 백그라운드 프로세스 관리

```bash
# 백그라운드 작업 목록
$ jobs
[1]   Running                 command1 &
[2]-  Running                 command2 &
[3]+  Stopped                 command3

# 작업 상태 기호:
# + : 현재 작업 (fg, bg 기본 대상)
# - : 이전 작업
# 숫자 : 작업 번호

# 자세한 정보
$ jobs -l
[1]  12345 Running                 command1 &
[2]  12346 Running                 command2 &

# 실행 중인 작업만
$ jobs -r

# 정지된 작업만
$ jobs -s

# PID만 표시
$ jobs -p
```

---

## 작업 제어

### fg - 포그라운드로 가져오기

```bash
# 최근 작업 (+ 표시된 작업)
$ fg
command1

# 작업 번호로
$ fg %1
$ fg %2

# 작업 이름으로
$ fg %command1
$ fg %?comm    # 부분 매칭

# 이전 작업 (- 표시)
$ fg %-

# 현재 작업
$ fg %+
```

### bg - 백그라운드로 재개

```bash
# 정지된 작업을 백그라운드로
$ bg
[1]+ command1 &

# 작업 번호로
$ bg %1
$ bg %2

# 모든 정지된 작업을 백그라운드로
$ for job in $(jobs -sp); do bg %$job; done
```

### Ctrl 키 조합

```bash
# Ctrl+C : SIGINT (인터럽트, 종료)
$ long_command
^C

# Ctrl+Z : SIGTSTP (일시정지)
$ long_command
^Z
[1]+  Stopped                 long_command

# Ctrl+D : EOF (입력 종료)
# 표준 입력을 받는 프로그램 종료
$ cat
(텍스트 입력)
^D

# Ctrl+\ : SIGQUIT (종료 + 코어덤프)
$ problematic_program
^\Quit (core dumped)
```

### wait - 프로세스 대기

```bash
# 모든 백그라운드 작업 대기
$ command1 &
$ command2 &
$ wait
# 모든 작업이 끝날 때까지 대기

# 특정 PID 대기
$ command &
$ wait $!  # $!는 마지막 백그라운드 프로세스 PID

# 특정 작업 대기
$ command1 &
$ command2 &
$ wait %1
$ wait %2

# 스크립트에서 활용
#!/bin/bash
command1 &
pid1=$!
command2 &
pid2=$!

wait $pid1
echo "Command1 completed"

wait $pid2
echo "Command2 completed"
```

---

## 프로세스 종료

### kill - 시그널 전송

```bash
# 기본 시그널 (SIGTERM, 15)
$ kill 12345

# 시그널 번호로
$ kill -9 12345   # SIGKILL (강제 종료)
$ kill -15 12345  # SIGTERM (정상 종료)

# 시그널 이름으로
$ kill -TERM 12345
$ kill -KILL 12345
$ kill -HUP 12345

# 여러 프로세스
$ kill 12345 12346 12347

# 작업 번호로
$ kill %1
$ kill %2

# 모든 시그널 목록
$ kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL
 5) SIGTRAP      6) SIGABRT      7) SIGBUS       8) SIGFPE
 9) SIGKILL     10) SIGUSR1     11) SIGSEGV     12) SIGUSR2
13) SIGPIPE     14) SIGALRM     15) SIGTERM     16) SIGSTKFLT
17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
...

# 시그널 번호 확인
$ kill -l TERM
15
$ kill -l 9
KILL
```

### 주요 시그널

```bash
# SIGTERM (15) - 정상 종료 요청
$ kill -15 12345
$ kill -TERM 12345
# 프로세스가 정리 작업 후 종료 가능
# 기본 시그널

# SIGKILL (9) - 강제 종료
$ kill -9 12345
$ kill -KILL 12345
# 즉시 종료, 정리 불가
# 최후의 수단

# SIGHUP (1) - 설정 재로드
$ kill -1 12345
$ kill -HUP 12345
# 많은 데몬이 설정 재로드에 사용
$ sudo kill -HUP $(cat /var/run/nginx.pid)

# SIGINT (2) - 인터럽트 (Ctrl+C)
$ kill -2 12345
$ kill -INT 12345

# SIGQUIT (3) - 종료 + 코어덤프 (Ctrl+\)
$ kill -3 12345
$ kill -QUIT 12345

# SIGSTOP (19) - 일시정지 (막을 수 없음)
$ kill -STOP 12345

# SIGCONT (18) - 재개
$ kill -CONT 12345

# SIGUSR1 (10), SIGUSR2 (12) - 사용자 정의
$ kill -USR1 12345
$ kill -USR2 12345
```

### killall - 이름으로 종료

```bash
# 프로세스 이름으로 종료
$ killall firefox
$ killall nginx

# 시그널 지정
$ killall -9 chrome
$ killall -HUP nginx

# 대화형 (확인)
$ killall -i firefox
Kill firefox(12345) ? (y/N) y

# 특정 사용자의 프로세스만
$ killall -u username firefox

# 프로세스 이름 정확히 매칭
$ killall -e exact_process_name

# 정규식으로
$ killall -r 'chrome.*'

# 실행 시간 기준
$ killall -o 1h firefox    # 1시간 이상 실행된 것만
$ killall -y 5m chrome      # 5분 미만 실행된 것만

# 조용히 (에러 메시지 없음)
$ killall -q process_name

# 대기
$ killall -w process_name  # 프로세스 종료까지 대기
```

### pkill - 패턴으로 종료

```bash
# 이름 패턴으로
$ pkill firefox
$ pkill chrome

# 전체 커맨드라인 매칭
$ pkill -f "python.*myapp.py"

# 특정 사용자
$ pkill -u username
$ pkill -u www-data nginx

# 시그널 지정
$ pkill -9 firefox
$ pkill -HUP nginx

# 정확한 매칭
$ pkill -x bash

# 최신 프로세스만
$ pkill -n chrome

# 가장 오래된 프로세스만
$ pkill -o chrome

# 터미널 지정
$ pkill -t pts/0

# 부모 프로세스 지정
$ pkill -P 1234

# 그룹 ID로
$ pkill -g 1000
```

### timeout - 시간 제한

```bash
# 10초 후 종료
$ timeout 10 command

# 10초 후 SIGKILL
$ timeout -s KILL 10 command

# 2분 후 종료
$ timeout 2m command

# 1시간 후 종료
$ timeout 1h command

# 종료 전 30초 대기 후 SIGKILL
$ timeout -k 30 10m command

# 종료 시그널 지정
$ timeout -s TERM 5m command

# 반환값 확인
$ timeout 10 command
$ echo $?
# 124: 타임아웃
# 0-123: 명령어 정상 종료
# 125-: 타임아웃 오류
```

---

## 프로세스 우선순위

### nice - 우선순위 설정하여 실행

```bash
# nice 값 범위: -20 (최고) ~ 19 (최저)
# 기본값: 0
# 일반 사용자는 0-19만 설정 가능
# root는 -20-19 설정 가능

# 기본 (nice = 10)
$ nice command

# nice 값 지정
$ nice -n 10 command
$ nice -10 command

# 최저 우선순위
$ nice -n 19 command

# 높은 우선순위 (root 필요)
$ sudo nice -n -20 command
$ sudo nice --20 command

# 백그라운드와 함께
$ nice -n 15 long_command &

# 현재 프로세스의 nice 값 확인
$ nice
0
```

### renice - 실행 중인 프로세스 우선순위 변경

```bash
# PID로 변경
$ renice 10 -p 12345
$ renice -n 10 -p 12345

# 여러 프로세스
$ renice 10 -p 12345 12346 12347

# 사용자의 모든 프로세스
$ renice 10 -u username
$ sudo renice -5 -u www-data

# 그룹의 모든 프로세스
$ renice 10 -g 1000

# 우선순위 높이기 (root 필요)
$ sudo renice -10 -p 12345

# 자신의 프로세스 우선순위 낮추기
$ renice 5 -p $$  # $$는 현재 셸 PID

# 실행 중인 명령어
$ renice 15 -p $(pgrep firefox)

# top에서 변경
# r 키 누르고 PID와 nice 값 입력

# htop에서 변경
# F7/F8 키로 nice 값 증가/감소
```

### ionice - IO 우선순위

```bash
# IO 스케줄링 클래스:
# 0 - None (기본)
# 1 - Real-time (높음, root만)
# 2 - Best-effort (보통)
# 3 - Idle (낮음)

# Idle 클래스로 실행
$ ionice -c 3 command

# Best-effort, 우선순위 7
$ ionice -c 2 -n 7 command

# Real-time (root 필요)
$ sudo ionice -c 1 -n 0 command

# 실행 중인 프로세스 변경
$ ionice -c 3 -p 12345

# 현재 프로세스 확인
$ ionice -p $$
best-effort: prio 4

# 백업 작업 (낮은 IO 우선순위)
$ ionice -c 3 tar czf backup.tar.gz /data/ &

# 조합
$ nice -n 19 ionice -c 3 heavy_task &
```

### chrt - 실시간 스케줄링

```bash
# 스케줄링 정책:
# SCHED_FIFO: First-in, First-out
# SCHED_RR: Round-robin
# SCHED_OTHER: 일반 (기본)
# SCHED_BATCH: 배치 작업
# SCHED_IDLE: 유휴

# 실시간 우선순위로 실행 (root 필요)
$ sudo chrt -f 99 command  # FIFO, 우선순위 99

# Round-robin
$ sudo chrt -r 50 command

# 일반 스케줄링
$ chrt -o 0 command

# 배치
$ chrt -b 0 command

# Idle
$ chrt -i 0 command

# 실행 중인 프로세스 변경
$ sudo chrt -f -p 99 12345

# 현재 설정 확인
$ chrt -p 12345
pid 12345's current scheduling policy: SCHED_OTHER
pid 12345's current scheduling priority: 0

# 범위 확인
$ chrt -m
SCHED_OTHER min/max priority    : 0/0
SCHED_FIFO min/max priority     : 1/99
SCHED_RR min/max priority       : 1/99
SCHED_BATCH min/max priority    : 0/0
SCHED_IDLE min/max priority     : 0/0
```

---

## 프로세스 제한

### ulimit - 리소스 제한

```bash
# 모든 제한 확인
$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 15733
max locked memory       (kbytes, -l) 65536
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 15733
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited

# 열린 파일 수 제한
$ ulimit -n
1024

# 열린 파일 수 늘리기 (soft limit)
$ ulimit -n 4096

# Hard limit (영구 변경은 /etc/security/limits.conf)
$ ulimit -Hn
1048576

# 코어덤프 크기
$ ulimit -c unlimited  # 무제한
$ ulimit -c 0          # 비활성화

# 스택 크기
$ ulimit -s 16384

# 프로세스 수
$ ulimit -u 10000

# CPU 시간 (초)
$ ulimit -t 3600  # 1시간

# 가상 메모리
$ ulimit -v 1048576  # 1GB

# 명령어와 함께 적용
$ bash -c "ulimit -n 4096; ./myapp"
```

### /etc/security/limits.conf

```bash
# 영구적인 제한 설정
$ sudo vi /etc/security/limits.conf

# 형식: <domain> <type> <item> <value>
# domain: 사용자명, @그룹명, *
# type: soft, hard
# item: nofile, nproc, cpu, etc.

# 예제:
*               soft    nofile          4096
*               hard    nofile          65536
@developers     soft    nproc           100
@developers     hard    nproc           200
username        soft    cpu             60
username        hard    cpu             120

# 적용 (재로그인 필요)
# 또는 PAM 설정 확인
$ cat /etc/pam.d/common-session | grep limits
session required pam_limits.so
```

### cgroups - 컨트롤 그룹

```bash
# cgroup v1 확인
$ mount | grep cgroup
cgroup on /sys/fs/cgroup/cpu type cgroup (rw,cpu)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,memory)

# cgroup v2 확인
$ mount | grep cgroup2

# systemd로 리소스 제한 (cgroup 사용)
$ systemd-run --unit=myapp --scope -p MemoryLimit=1G -p CPUQuota=50% ./myapp

# Docker는 cgroup 사용
$ docker run --memory=512m --cpus=1.5 myimage

# 수동 cgroup 생성 (고급)
$ sudo cgcreate -g memory,cpu:mygroup
$ sudo cgset -r memory.limit_in_bytes=1073741824 mygroup  # 1GB
$ sudo cgset -r cpu.shares=512 mygroup
$ sudo cgexec -g memory,cpu:mygroup command
```

---

## 실전 예제

### 예제 1: 안전한 프로세스 종료

```bash
# 순서대로 시도
#!/bin/bash
PID=12345

# 1. SIGTERM (정상 종료)
kill -TERM $PID
sleep 5

# 2. 아직 살아있으면 SIGKILL
if ps -p $PID > /dev/null; then
    echo "Process still alive, sending SIGKILL"
    kill -KILL $PID
fi

# 함수로 만들기
graceful_kill() {
    local pid=$1
    local timeout=${2:-10}

    kill -TERM $pid 2>/dev/null || return 1

    for i in $(seq 1 $timeout); do
        if ! ps -p $pid > /dev/null 2>&1; then
            echo "Process $pid terminated gracefully"
            return 0
        fi
        sleep 1
    done

    echo "Timeout, force killing $pid"
    kill -KILL $pid 2>/dev/null
    return 0
}

# 사용
graceful_kill 12345 15
```

### 예제 2: 프로세스 모니터링 및 재시작

```bash
#!/bin/bash
# process_monitor.sh

PROCESS_NAME="myapp"
START_COMMAND="/usr/local/bin/myapp"
CHECK_INTERVAL=60

while true; do
    if ! pgrep -x "$PROCESS_NAME" > /dev/null; then
        echo "$(date): $PROCESS_NAME not running, starting..."
        $START_COMMAND &

        # 로그 기록
        echo "$(date): Started $PROCESS_NAME" >> /var/log/process_monitor.log
    fi

    sleep $CHECK_INTERVAL
done
```

### 예제 3: 무거운 작업 nice하게 실행

```bash
# CPU 집약적 작업
$ nice -n 19 ionice -c 3 tar czf backup.tar.gz /data/ &

# 야간 배치 작업
#!/bin/bash
# night_batch.sh

# 낮은 우선순위로 실행
renice 19 -p $$ > /dev/null
ionice -c 3 -p $$ > /dev/null

# 무거운 작업들
process_logs
generate_reports
cleanup_old_files

# cron에 등록
# 0 2 * * * /usr/local/bin/night_batch.sh
```

### 예제 4: 병렬 작업 관리

```bash
#!/bin/bash
# parallel_tasks.sh

MAX_JOBS=4
JOBS=()

# 작업 함수
process_file() {
    local file=$1
    echo "Processing $file..."
    # 작업 수행
    sleep 10
    echo "Done: $file"
}

# 파일 목록
FILES=(file1 file2 file3 file4 file5 file6 file7 file8)

for file in "${FILES[@]}"; do
    # 백그라운드로 실행
    process_file "$file" &
    JOBS+=($!)

    # 최대 작업 수 제한
    while [ $(jobs -r | wc -l) -ge $MAX_JOBS ]; do
        sleep 1
    done
done

# 모든 작업 완료 대기
for job in "${JOBS[@]}"; do
    wait $job
done

echo "All tasks completed"
```

### 예제 5: 메모리 제한된 프로세스 실행

```bash
# systemd-run 사용
$ systemd-run --scope -p MemoryLimit=512M -p CPUQuota=50% ./memory_intensive_app

# ulimit 사용
$ bash -c 'ulimit -v 524288; ./app'  # 512MB 가상 메모리

# cgroup 사용 (수동)
$ sudo cgcreate -g memory:limited_app
$ sudo cgset -r memory.limit_in_bytes=536870912 limited_app  # 512MB
$ sudo cgexec -g memory:limited_app ./app

# timeout과 조합
$ timeout -s KILL 10m bash -c 'ulimit -v 1048576; ./app'
```

### 예제 6: 세션 유지하며 작업 실행

```bash
# screen 사용
$ screen -S mysession
$ long_running_command
# Ctrl+A, D로 detach
$ screen -r mysession  # 다시 attach

# tmux 사용
$ tmux new -s mysession
$ long_running_command
# Ctrl+B, D로 detach
$ tmux attach -t mysession

# nohup + disown
$ nohup command > output.log 2>&1 &
$ disown

# systemd-run (일회성 서비스)
$ systemd-run --user --scope command
```

---

## 문제 해결

### 프로세스가 종료되지 않을 때

```bash
# 1. 상태 확인
$ ps aux | grep process_name

# 2. 열린 파일 확인
$ lsof -p 12345

# 3. 스택 트레이스
$ sudo cat /proc/12345/stack

# 4. strace로 시스템 콜 확인
$ sudo strace -p 12345

# 5. SIGTERM 시도
$ kill -TERM 12345

# 6. 5초 대기 후 SIGKILL
$ sleep 5 && kill -KILL 12345

# 7. 부모 프로세스 확인
$ ps -o ppid= -p 12345
$ ps -p <ppid>

# 8. 마지막 수단: 재부팅
```

### 좀비 프로세스

```bash
# 좀비 찾기
$ ps aux | awk '$8=="Z"'

# 부모 프로세스에 SIGCHLD
$ kill -CHLD <parent_pid>

# 부모가 init(1)이면 자동 정리됨
# 그렇지 않으면 부모 재시작 필요
```

### "Cannot allocate memory" 오류

```bash
# 프로세스 수 확인
$ ps aux | wc -l

# 제한 확인
$ ulimit -u

# 제한 늘리기
$ ulimit -u 10000

# 또는 /etc/security/limits.conf 수정
```

---

## 요약

프로세스 제어 핵심:

1. **작업 제어**
   - `&` - 백그라운드 실행
   - `Ctrl+Z`, `bg`, `fg` - 작업 전환
   - `jobs` - 작업 목록

2. **프로세스 종료**
   - `kill` - 시그널 전송
   - `killall` - 이름으로 종료
   - `pkill` - 패턴으로 종료

3. **우선순위**
   - `nice` - 실행 시 우선순위 설정
   - `renice` - 실행 중 우선순위 변경
   - `ionice` - IO 우선순위

4. **리소스 제한**
   - `ulimit` - 셸 제한
   - `/etc/security/limits.conf` - 시스템 제한
   - `cgroups` - 세밀한 제어

---

[다음: 시그널 →](signals.md)

[← 프로세스 보기로 돌아가기](viewing-processes.md)

[← 목차로 돌아가기](../README.md)

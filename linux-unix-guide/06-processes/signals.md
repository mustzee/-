# 시그널 (Signals)

## 목차
- [시그널 기본 개념](#시그널-기본-개념)
- [주요 시그널](#주요-시그널)
- [시그널 전송](#시그널-전송)
- [시그널 처리](#시그널-처리)
- [스크립트에서 시그널 처리](#스크립트에서-시그널-처리)
- [실전 예제](#실전-예제)

---

## 시그널 기본 개념

### 시그널이란?

```bash
# 시그널(Signal):
# - 프로세스 간 통신(IPC) 메커니즘
# - 커널이나 다른 프로세스가 프로세스에 이벤트 알림
# - 비동기적 이벤트 처리
# - 소프트웨어 인터럽트

# 시그널 동작:
# 1. Default: 기본 동작 수행
# 2. Ignore: 시그널 무시
# 3. Catch: 사용자 정의 핸들러 실행
# 4. Block: 시그널을 보류 (나중에 처리)
```

### 시그널 목록

```bash
# 모든 시그널 보기
$ kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
 6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
...
64) SIGRTMAX

# 시그널 번호 찾기
$ kill -l TERM
15

$ kill -l 9
KILL

# man 페이지
$ man 7 signal
```

### 시그널 분류

```bash
# 표준 시그널:
# - 1-31: 전통적인 유닉스 시그널
# - 34-64: 실시간 시그널 (POSIX)

# 블록 불가능한 시그널:
# - SIGKILL (9): 강제 종료
# - SIGSTOP (19): 강제 일시정지

# 무시 가능한 시그널:
# - 대부분의 시그널은 무시하거나 처리 가능

# 기본 동작:
# - Term: 프로세스 종료
# - Core: 종료 + 코어덤프
# - Ign: 무시
# - Stop: 프로세스 정지
# - Cont: 정지된 프로세스 재개
```

---

## 주요 시그널

### SIGTERM (15) - 종료

```bash
# 정상 종료 요청
# - 가장 일반적인 종료 시그널
# - 프로세스가 정리 작업 수행 가능
# - kill의 기본 시그널

# 전송
$ kill 12345
$ kill -15 12345
$ kill -TERM 12345

# 사용 사례:
# - 서비스 정상 종료
# - 리소스 정리 필요한 프로세스
# - 로그 플러시, 파일 저장 등

# 예제
$ kill -TERM $(pgrep myapp)

# 모든 프로세스에
$ killall -TERM myapp

# systemd 서비스
$ systemctl stop myservice  # SIGTERM 전송
```

### SIGKILL (9) - 강제 종료

```bash
# 즉시 강제 종료
# - 무시하거나 처리할 수 없음
# - 정리 작업 불가
# - 최후의 수단

# 전송
$ kill -9 12345
$ kill -KILL 12345

# 주의사항:
# - 파일 손상 가능
# - 임시 파일 남을 수 있음
# - 락 파일 남을 수 있음
# - 데이터 손실 가능

# 사용 시나리오:
# - SIGTERM에 응답하지 않을 때
# - 프로세스가 멈춘 경우 (D state)
# - 응급 상황

# 예제
$ kill -TERM 12345
$ sleep 5
$ kill -KILL 12345  # 아직 살아있으면

# 스크립트로
#!/bin/bash
kill -TERM $1
for i in {1..10}; do
    if ! ps -p $1 > /dev/null 2>&1; then
        echo "Process terminated"
        exit 0
    fi
    sleep 1
done
kill -KILL $1
```

### SIGHUP (1) - Hangup

```bash
# 터미널 연결 끊김 또는 설정 재로드
# - 원래: 터미널 연결 끊김 시 전송
# - 현대: 설정 재로드 용도로 사용

# 전송
$ kill -1 12345
$ kill -HUP 12345

# 데몬 설정 재로드
$ sudo kill -HUP $(cat /var/run/nginx.pid)
$ sudo kill -HUP $(cat /var/run/syslogd.pid)

# systemctl에서
$ sudo systemctl reload nginx  # SIGHUP 전송

# 터미널 종료 시 프로세스 보호
$ nohup command &
# nohup은 SIGHUP을 무시하도록 함

# 또는 disown
$ command &
$ disown

# screen/tmux 사용
$ screen
$ command
# Ctrl+A, D로 detach
```

### SIGINT (2) - Interrupt

```bash
# 키보드 인터럽트 (Ctrl+C)
# - 사용자가 프로세스 중단 요청
# - 처리 가능 (graceful shutdown)

# 전송
$ kill -2 12345
$ kill -INT 12345

# Ctrl+C로 전송
$ long_running_command
^C

# 스크립트에서 처리
#!/bin/bash
trap 'echo "Interrupted!"; exit 1' INT

while true; do
    echo "Working..."
    sleep 1
done

# Ctrl+C 눌러도 메시지 출력 후 종료

# 무시하기
#!/bin/bash
trap '' INT  # SIGINT 무시

echo "Try Ctrl+C (won't work)"
sleep 10
echo "Done"
```

### SIGQUIT (3) - Quit

```bash
# 키보드 종료 (Ctrl+\)
# - 코어덤프 생성
# - 디버깅 목적

# 전송
$ kill -3 12345
$ kill -QUIT 12345

# Ctrl+\ 로 전송
$ problematic_program
^\Quit (core dumped)

# 코어덤프 활성화
$ ulimit -c unlimited

# 코어덤프 위치
$ cat /proc/sys/kernel/core_pattern
core

# systemd 시스템
$ cat /proc/sys/kernel/core_pattern
|/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %h

# Java 스레드 덤프
$ kill -3 <java_pid>
# 스레드 정보를 stdout에 출력
```

### SIGUSR1 (10), SIGUSR2 (12) - 사용자 정의

```bash
# 애플리케이션별 용도
# - 커스텀 동작 정의 가능
# - 재로드, 상태 토글 등

# 전송
$ kill -USR1 12345
$ kill -USR2 12345

# 일반적인 사용례:
# - 로그 레벨 변경
# - 통계 정보 출력
# - 디버그 모드 토글
# - 설정 재로드

# 예제: Apache
$ kill -USR1 <apache_pid>  # 로그 파일 재오픈

# 예제: Nginx
$ kill -USR1 <nginx_pid>   # 로그 파일 재오픈
$ kill -USR2 <nginx_pid>   # 바이너리 업그레이드

# 스크립트에서
#!/bin/bash
toggle=0

toggle_handler() {
    if [ $toggle -eq 0 ]; then
        toggle=1
        echo "Toggle ON"
    else
        toggle=0
        echo "Toggle OFF"
    fi
}

trap toggle_handler USR1

while true; do
    sleep 1
done
```

### SIGCHLD (17) - 자식 프로세스 종료

```bash
# 자식 프로세스 종료 시 부모에게 전송
# - 기본: 무시됨
# - wait() 시스템 콜과 연동

# 좀비 프로세스 방지
#!/bin/bash
# 자식 프로세스를 적절히 회수

reap_children() {
    wait
}

trap reap_children CHLD

for i in {1..10}; do
    (sleep $i; echo "Child $i done") &
done

wait
echo "All children done"
```

### SIGSTOP (19), SIGCONT (18) - 일시정지/재개

```bash
# SIGSTOP - 프로세스 일시정지
# - 처리/무시 불가
$ kill -STOP 12345

# SIGCONT - 프로세스 재개
$ kill -CONT 12345

# SIGTSTP - Ctrl+Z (처리 가능)
$ long_command
^Z
[1]+  Stopped                 long_command

$ bg  # 백그라운드로 재개 (SIGCONT)
$ fg  # 포그라운드로 재개

# 활용 예제: 일시적 리소스 제어
#!/bin/bash
# pause_resume.sh

PID=$1

while true; do
    echo "Pausing process $PID"
    kill -STOP $PID
    sleep 5

    echo "Resuming process $PID"
    kill -CONT $PID
    sleep 5
done
```

### SIGPIPE (13) - 파이프 끊김

```bash
# 파이프 읽는 쪽이 없을 때
# - 기본: 프로세스 종료

# 예제
$ yes | head -1
y
# yes는 SIGPIPE 받아 종료

# 처리하기
#!/bin/bash
trap 'echo "Pipe broken"; exit 1' PIPE

while true; do
    echo "data"
done

# 무시하기 (일부 애플리케이션)
trap '' PIPE
```

### SIGALRM (14) - 알람

```bash
# alarm() 시스템 콜로 설정된 타이머
# - timeout 구현에 사용

# 스크립트 타임아웃
#!/bin/bash
timeout_handler() {
    echo "Timeout!"
    exit 1
}

trap timeout_handler ALRM

# 시간 제한
(sleep 10; kill -ALRM $$) &
alarm_pid=$!

# 작업 수행
long_running_task

# 성공하면 알람 취소
kill $alarm_pid 2>/dev/null
```

### SIGWINCH (28) - 윈도우 크기 변경

```bash
# 터미널 크기 변경 시
# - 터미널 애플리케이션이 처리

# 처리 예제
#!/bin/bash
handle_resize() {
    echo "Terminal resized to $(tput cols)x$(tput lines)"
}

trap handle_resize WINCH

while true; do
    sleep 1
done
```

---

## 시그널 전송

### kill 명령어

```bash
# 기본 (SIGTERM)
$ kill 12345

# 시그널 번호
$ kill -9 12345
$ kill -15 12345

# 시그널 이름
$ kill -KILL 12345
$ kill -TERM 12345
$ kill -HUP 12345

# 여러 프로세스
$ kill 12345 12346 12347
$ kill -TERM 12345 12346 12347

# 음수 PID (프로세스 그룹)
$ kill -TERM -12345  # 프로세스 그룹 12345

# 현재 셸의 모든 작업
$ kill -TERM 0
```

### pkill / killall

```bash
# 이름으로
$ pkill -TERM firefox
$ killall -TERM firefox

# 시그널 종류
$ pkill -HUP syslogd
$ pkill -USR1 nginx

# 패턴
$ pkill -f "python.*myapp"

# 사용자별
$ pkill -u username -TERM
```

### 프로그래밍 방식

```bash
# Bash 스크립트
kill -TERM $PID

# Python
import os
import signal
os.kill(pid, signal.SIGTERM)

# C
#include <signal.h>
kill(pid, SIGTERM);

# 자신에게
kill -TERM $$  # Bash
os.kill(os.getpid(), signal.SIGTERM)  # Python
```

---

## 시그널 처리

### trap 명령어

```bash
# 기본 형식
trap 'commands' SIGNAL

# 여러 시그널
trap 'commands' SIGNAL1 SIGNAL2

# 기본 동작으로 복원
trap - SIGNAL

# 무시
trap '' SIGNAL

# 현재 trap 설정 보기
trap -p
trap -p SIGNAL
```

### 일반적인 패턴

```bash
# 정리 함수
#!/bin/bash
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/myapp.$$.*
    kill $child_pid 2>/dev/null
}

trap cleanup EXIT

# 작업 수행
echo "Running..."
sleep 100 &
child_pid=$!

wait

# EXIT 시그널은 스크립트 종료 시 항상 실행됨
```

### 시그널별 처리

```bash
#!/bin/bash

# SIGINT 처리
int_handler() {
    echo "Caught SIGINT (Ctrl+C)"
    exit 1
}

# SIGTERM 처리
term_handler() {
    echo "Caught SIGTERM"
    cleanup
    exit 0
}

# SIGHUP 처리
hup_handler() {
    echo "Caught SIGHUP, reloading config"
    reload_config
}

trap int_handler INT
trap term_handler TERM
trap hup_handler HUP

# 메인 루프
while true; do
    echo "Working... (PID: $$)"
    sleep 5
done
```

---

## 스크립트에서 시그널 처리

### 기본 템플릿

```bash
#!/bin/bash

# 전역 변수
RUNNING=1
RELOAD=0

# 정리 함수
cleanup() {
    echo "Cleaning up..."
    # 임시 파일 삭제
    rm -f /tmp/myapp.$$.*
    # 자식 프로세스 종료
    jobs -p | xargs -r kill
    echo "Cleanup done"
}

# 종료 핸들러
shutdown() {
    echo "Shutdown signal received"
    RUNNING=0
}

# 재로드 핸들러
reload() {
    echo "Reload signal received"
    RELOAD=1
}

# 시그널 설정
trap cleanup EXIT
trap shutdown INT TERM
trap reload HUP

# 메인 루프
while [ $RUNNING -eq 1 ]; do
    # 재로드 확인
    if [ $RELOAD -eq 1 ]; then
        echo "Reloading configuration..."
        # 설정 재로드 로직
        RELOAD=0
    fi

    # 작업 수행
    echo "Working... (PID: $$)"
    sleep 5
done

echo "Exiting..."
exit 0
```

### PID 파일 관리

```bash
#!/bin/bash

PIDFILE="/var/run/myapp.pid"

# PID 파일 생성
create_pidfile() {
    if [ -f "$PIDFILE" ]; then
        OLD_PID=$(cat "$PIDFILE")
        if ps -p $OLD_PID > /dev/null 2>&1; then
            echo "Already running (PID: $OLD_PID)"
            exit 1
        fi
    fi
    echo $$ > "$PIDFILE"
}

# PID 파일 삭제
remove_pidfile() {
    rm -f "$PIDFILE"
}

trap remove_pidfile EXIT

create_pidfile

# 메인 로직
while true; do
    echo "Running..."
    sleep 10
done
```

### 로그 로테이션

```bash
#!/bin/bash

LOGFILE="/var/log/myapp.log"

# 로그 재오픈
reopen_log() {
    exec 1>>"$LOGFILE"
    exec 2>>"$LOGFILE"
    echo "$(date): Log reopened"
}

# 초기 로그 설정
exec 1>>"$LOGFILE"
exec 2>>"$LOGFILE"

# USR1로 로그 재오픈
trap reopen_log USR1

echo "$(date): Application started (PID: $$)"

# 메인 루프
while true; do
    echo "$(date): Working..."
    sleep 60
done

# logrotate 설정 예:
# /var/log/myapp.log {
#     daily
#     rotate 7
#     compress
#     delaycompress
#     postrotate
#         kill -USR1 $(cat /var/run/myapp.pid)
#     endscript
# }
```

### 그레이스풀 셧다운

```bash
#!/bin/bash

WORKERS=()
SHUTDOWN=0

# 워커 프로세스 시작
start_worker() {
    while [ $SHUTDOWN -eq 0 ]; do
        echo "Worker $$: processing..."
        sleep 2
    done
    echo "Worker $$: shutting down"
}

# 그레이스풀 셧다운
graceful_shutdown() {
    echo "Graceful shutdown initiated"
    SHUTDOWN=1

    # 새 요청 거부
    echo "Stopping new requests..."

    # 기존 작업 완료 대기
    echo "Waiting for workers to finish..."
    for pid in "${WORKERS[@]}"; do
        wait $pid 2>/dev/null
    done

    echo "All workers finished"
    exit 0
}

trap graceful_shutdown TERM INT

# 워커 시작
for i in {1..3}; do
    start_worker &
    WORKERS+=($!)
done

# 메인 루프
while true; do
    sleep 1
done
```

---

## 실전 예제

### 예제 1: 데몬 스크립트

```bash
#!/bin/bash
# daemon.sh - 완전한 데몬 스크립트 예제

DAEMON_NAME="mydaemon"
PIDFILE="/var/run/${DAEMON_NAME}.pid"
LOGFILE="/var/log/${DAEMON_NAME}.log"
CONFIGFILE="/etc/${DAEMON_NAME}.conf"

# 로깅 함수
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}

# 설정 로드
load_config() {
    if [ -f "$CONFIGFILE" ]; then
        source "$CONFIGFILE"
        log "Configuration loaded"
    else
        log "WARNING: Config file not found"
    fi
}

# PID 파일 체크
check_pid() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Already running (PID: $PID)"
            exit 1
        fi
        rm -f "$PIDFILE"
    fi
}

# 정리
cleanup() {
    log "Cleaning up..."
    rm -f "$PIDFILE"
    log "Daemon stopped"
}

# 재로드
reload_handler() {
    log "Reloading configuration..."
    load_config
}

# 종료
shutdown_handler() {
    log "Shutdown signal received"
    cleanup
    exit 0
}

# 시그널 설정
trap shutdown_handler INT TERM
trap reload_handler HUP
trap cleanup EXIT

# 시작
check_pid
echo $$ > "$PIDFILE"
log "Daemon started (PID: $$)"
load_config

# 메인 루프
while true; do
    # 작업 수행
    log "Performing tasks..."

    # 실제 작업 코드
    # process_data
    # check_status
    # etc.

    sleep 60
done
```

### 예제 2: 시그널 기반 통신

```bash
# 서버 스크립트
#!/bin/bash
# server.sh

FIFO="/tmp/server_status.$$"
mkfifo "$FIFO"

cleanup() {
    rm -f "$FIFO"
}

trap cleanup EXIT

status_handler() {
    echo "Status: Running" > "$FIFO" &
}

trap status_handler USR1

echo "Server PID: $$"

while true; do
    sleep 1
done

# 클라이언트 스크립트
#!/bin/bash
# client.sh

SERVER_PID=$1

# 상태 요청
kill -USR1 $SERVER_PID

# 응답 읽기
timeout 2 cat /tmp/server_status.$SERVER_PID
```

### 예제 3: 프로세스 모니터링

```bash
#!/bin/bash
# monitor.sh - 프로세스 모니터링 및 자동 재시작

PROCESS_NAME="myapp"
PROCESS_CMD="/usr/local/bin/myapp"
CHECK_INTERVAL=10
MAX_RESTARTS=5
RESTART_WINDOW=60

restart_count=0
restart_time=0

start_process() {
    echo "$(date): Starting $PROCESS_NAME"
    $PROCESS_CMD &
    PID=$!
    echo $PID > "/var/run/${PROCESS_NAME}.pid"

    # 재시작 카운터 관리
    current_time=$(date +%s)
    if [ $((current_time - restart_time)) -gt $RESTART_WINDOW ]; then
        restart_count=0
    fi

    restart_count=$((restart_count + 1))
    restart_time=$current_time

    if [ $restart_count -gt $MAX_RESTARTS ]; then
        echo "$(date): ERROR: Too many restarts, giving up"
        exit 1
    fi
}

while true; do
    if ! pgrep -x "$PROCESS_NAME" > /dev/null; then
        echo "$(date): $PROCESS_NAME not running"
        start_process
    fi

    sleep $CHECK_INTERVAL
done
```

### 예제 4: 타임아웃 래퍼

```bash
#!/bin/bash
# timeout_wrapper.sh - 커스텀 타임아웃 구현

TIMEOUT=30
COMMAND="$@"

# 타임아웃 핸들러
timeout_handler() {
    echo "Timeout after ${TIMEOUT}s"
    kill -TERM $command_pid 2>/dev/null
    sleep 2
    kill -KILL $command_pid 2>/dev/null
    exit 124
}

# 알람 설정
trap timeout_handler ALRM

# 명령어 실행
$COMMAND &
command_pid=$!

# 타임아웃 타이머 시작
(sleep $TIMEOUT; kill -ALRM $$) &
timer_pid=$!

# 명령어 완료 대기
wait $command_pid
exit_code=$?

# 타이머 취소
kill $timer_pid 2>/dev/null

exit $exit_code
```

---

## 문제 해결

### 시그널이 무시될 때

```bash
# 프로세스 시그널 마스크 확인
$ cat /proc/12345/status | grep Sig
SigQ:   0/15733
SigPnd: 0000000000000000
SigBlk: 0000000000000000
SigIgn: 0000000000001000  # 무시되는 시그널
SigCgt: 0000000180004002  # 캐치되는 시그널

# strace로 확인
$ strace -e signal -p 12345
```

### 좀비 프로세스

```bash
# 부모에게 SIGCHLD 전송
$ ps -o ppid= -p <zombie_pid>
$ kill -CHLD <parent_pid>

# 부모 프로세스 재시작 필요할 수 있음
```

### trap이 작동하지 않을 때

```bash
# subshell에서는 trap 상속 안 됨
$ (trap 'echo trapped' INT; sleep 10)
# 새 프로세스에서는 별도 설정 필요

# 올바른 방법
$ trap 'echo trapped' INT
$ sleep 10
```

---

## 요약

시그널 핵심:

1. **필수 시그널**
   - SIGTERM(15): 정상 종료
   - SIGKILL(9): 강제 종료
   - SIGHUP(1): 재로드
   - SIGINT(2): Ctrl+C

2. **시그널 전송**
   - `kill -SIGNAL PID`
   - `pkill -SIGNAL name`
   - `killall -SIGNAL name`

3. **시그널 처리**
   - `trap 'command' SIGNAL`
   - 정리, 재로드, 그레이스풀 셧다운

4. **모범 사례**
   - 항상 정리 코드 작성
   - 그레이스풀 셧다운 구현
   - PID 파일 관리
   - 적절한 로깅

---

[다음: 모니터링 →](monitoring.md)

[← 프로세스 제어로 돌아가기](process-control.md)

[← 목차로 돌아가기](../README.md)

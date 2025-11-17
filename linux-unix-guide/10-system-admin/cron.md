# cron 작업 스케줄링

## 목차
- [소개](#소개)
- [crontab 기본](#crontab-기본)
- [cron 문법](#cron-문법)
- [시스템 cron](#시스템-cron)
- [anacron](#anacron)
- [at 명령](#at-명령)
- [환경 변수](#환경-변수)
- [로깅 및 디버깅](#로깅-및-디버깅)
- [보안](#보안)
- [실전 예제](#실전-예제)

---

## 소개

cron은 지정된 시간에 자동으로 작업을 실행하는 시간 기반 작업 스케줄러입니다.

### cron 개요

```bash
# cron 데몬 확인
$ systemctl status cron  # Debian/Ubuntu
$ systemctl status crond  # Red Hat/Fedora

# cron 데몬 시작
$ sudo systemctl start cron
$ sudo systemctl enable cron

# cron 프로세스
$ ps aux | grep cron
root      1234  0.0  0.1  cron

# cron 디렉토리 구조
/etc/crontab          # 시스템 crontab
/etc/cron.d/          # 시스템 cron 작업
/etc/cron.hourly/     # 시간별 스크립트
/etc/cron.daily/      # 일별 스크립트
/etc/cron.weekly/     # 주별 스크립트
/etc/cron.monthly/    # 월별 스크립트
/var/spool/cron/      # 사용자 crontab
```

### cron vs systemd timers

```bash
# cron 장점:
# - 간단하고 익숙한 문법
# - 이식성 (모든 Unix/Linux 시스템)
# - 가벼움

# systemd timers 장점:
# - 더 정확한 타이밍
# - 로깅 통합 (journald)
# - 의존성 관리
# - 부팅 시 놓친 작업 실행 (Persistent)

# 둘 다 사용 가능하며 상황에 따라 선택
```

---

## crontab 기본

### crontab 명령

```bash
# 현재 사용자 crontab 보기
$ crontab -l
no crontab for user

# crontab 편집
$ crontab -e
# 기본 편집기로 열림 (EDITOR 환경 변수)

# 편집기 지정
$ EDITOR=vim crontab -e

# crontab 파일에서 로드
$ crontab mycron.txt

# crontab 삭제
$ crontab -r
$ crontab -r -i  # 확인 후 삭제

# 다른 사용자 crontab (root만)
$ sudo crontab -u john -l
$ sudo crontab -u john -e

# 사용자별 crontab 파일 위치
/var/spool/cron/crontabs/user  # Debian/Ubuntu
/var/spool/cron/user           # Red Hat/Fedora
```

### 첫 crontab 만들기

```bash
# crontab 편집
$ crontab -e

# 예제 작업 추가
# 매일 오전 3시에 백업 스크립트 실행
0 3 * * * /home/user/backup.sh

# 매시간 로그 정리
0 * * * * /home/user/cleanup-logs.sh

# 매주 월요일 9시에 보고서 생성
0 9 * * 1 /home/user/weekly-report.sh

# 저장 및 종료
# cron이 자동으로 새 설정 로드
```

### crontab 형식

```bash
# 기본 형식
# * * * * * command
# │ │ │ │ │
# │ │ │ │ └─── 요일 (0-7, 0과 7은 일요일)
# │ │ │ └───── 월 (1-12)
# │ │ └─────── 일 (1-31)
# │ └───────── 시 (0-23)
# └─────────── 분 (0-59)

# 주석
# This is a comment

# 환경 변수 설정
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=user@example.com

# 작업 정의
0 3 * * * /home/user/backup.sh
```

---

## cron 문법

### 시간 지정 방법

```bash
# 매분
* * * * * command

# 매시간 (정각)
0 * * * * command

# 매일 자정
0 0 * * * command

# 매일 오전 3시 30분
30 3 * * * command

# 매주 일요일 오전 2시
0 2 * * 0 command
0 2 * * 7 command  # 같은 의미

# 매월 1일 오전 6시
0 6 1 * * command

# 1월 1일 자정 (새해)
0 0 1 1 * command

# 특정 월의 특정 일
0 0 15 6 * command  # 6월 15일

# 특정 요일과 날짜 조합
0 9 * * 1-5 command  # 평일 오전 9시
```

### 범위 및 간격

```bash
# 범위 (-)
0 9-17 * * * command  # 9시부터 17시까지 매시간

# 목록 (,)
0 9,12,18 * * * command  # 9시, 12시, 18시

# 간격 (/)
*/15 * * * * command  # 15분마다
0 */2 * * * command   # 2시간마다
0 0 */3 * * command   # 3일마다

# 조합
0,30 9-17 * * 1-5 command  # 평일 9-17시, 0분과 30분
*/10 9-17 * * 1-5 command  # 평일 9-17시, 10분마다

# 복잡한 예제
0 9-17/2 * * 1-5 command  # 평일 9,11,13,15,17시
```

### 특수 문자열

```bash
# @reboot - 부팅 시
@reboot command

# @yearly, @annually - 매년 (1월 1일 0시)
@yearly command
# 같은 의미: 0 0 1 1 *

# @monthly - 매월 (1일 0시)
@monthly command
# 같은 의미: 0 0 1 * *

# @weekly - 매주 (일요일 0시)
@weekly command
# 같은 의미: 0 0 * * 0

# @daily, @midnight - 매일 (0시)
@daily command
# 같은 의미: 0 0 * * *

# @hourly - 매시간
@hourly command
# 같은 의미: 0 * * * *

# 예제
@reboot /home/user/startup.sh
@daily /home/user/backup.sh
@weekly /home/user/weekly-report.sh
```

### 실전 예제 모음

```bash
# 매 5분마다
*/5 * * * * command

# 매일 새벽 2시 30분
30 2 * * * command

# 평일 오전 9시부터 오후 6시까지 매시간
0 9-18 * * 1-5 command

# 매월 첫째 날 오전 8시
0 8 1 * * command

# 매주 월요일과 목요일 오후 3시
0 15 * * 1,4 command

# 12월을 제외한 매월 15일
0 0 15 1-11 * command

# 주말 (토요일, 일요일)
0 10 * * 6,0 command

# 분기별 (1, 4, 7, 10월)
0 0 1 1,4,7,10 * command

# 영업일 오전 (월-금 9-12시)
0 9-12 * * 1-5 command

# 30분마다 (0분, 30분)
0,30 * * * * command
*/30 * * * * command  # 같은 의미
```

---

## 시스템 cron

### /etc/crontab

```bash
# /etc/crontab 보기
$ cat /etc/crontab
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )

# 사용자 지정 추가
0 2 * * * root /usr/local/bin/system-backup.sh

# 주의: /etc/crontab는 사용자 필드 포함!
# 분 시 일 월 요일 사용자 명령
0 3 * * * root /backup.sh
```

### /etc/cron.d/

```bash
# /etc/cron.d/ 디렉토리에 파일 생성
$ sudo vi /etc/cron.d/myapp

# 파일 내용 (사용자 필드 포함)
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=admin@example.com

# 매시간 로그 정리
0 * * * * myapp /opt/myapp/cleanup-logs.sh

# 매일 새벽 데이터베이스 백업
0 3 * * * root /opt/myapp/db-backup.sh

# 권한 설정
$ sudo chmod 644 /etc/cron.d/myapp

# cron이 자동으로 읽음 (재시작 불필요)
```

### cron.{hourly,daily,weekly,monthly}

```bash
# 스크립트를 해당 디렉토리에 배치
$ sudo cp backup.sh /etc/cron.daily/
$ sudo chmod +x /etc/cron.daily/backup.sh

# 시간별
$ ls /etc/cron.hourly/
.placeholder

# 일별
$ ls /etc/cron.daily/
apt-compat  dpkg  logrotate  man-db

# 주별
$ ls /etc/cron.weekly/
man-db

# 월별
$ ls /etc/cron.monthly/
.placeholder

# 실행 시간 설정 (anacron 사용)
$ cat /etc/anacrontab
# period  delay  job-identifier  command
1         5      cron.daily      run-parts /etc/cron.daily
7         10     cron.weekly     run-parts /etc/cron.weekly
@monthly  15     cron.monthly    run-parts /etc/cron.monthly

# 주의사항:
# - 파일 이름에 확장자 없어야 함 (backup.sh ❌, backup ✅)
# - 또는 run-parts 설정 확인
```

### run-parts

```bash
# run-parts - 디렉토리 내 모든 실행 파일 실행

# 수동 실행
$ sudo run-parts /etc/cron.daily/
$ sudo run-parts --report /etc/cron.daily/

# 테스트 (실제 실행 안 함)
$ sudo run-parts --test /etc/cron.daily/
backup
logrotate
man-db

# 정규식 필터
$ sudo run-parts --regex='^backup' /etc/cron.daily/

# run-parts 규칙
# - 실행 권한 필요
# - 특수 문자 없는 파일명 (., ~, 등)
# - 디렉토리 제외
```

---

## anacron

### anacron 소개

```bash
# anacron - 항상 켜져있지 않은 시스템용
# 놓친 작업을 부팅 시 실행

# anacron 설치 확인
$ dpkg -l | grep anacron
$ rpm -q cronie-anacron

# anacron 설정
$ cat /etc/anacrontab
# /etc/anacrontab: configuration file for anacron

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
RANDOM_DELAY=45
START_HOURS_RANGE=3-22

# period  delay  job-identifier  command
1         5      cron.daily      nice run-parts /etc/cron.daily
7         10     cron.weekly     nice run-parts /etc/cron.weekly
@monthly  15     cron.monthly    nice run-parts /etc/cron.monthly

# period: 일 단위 (1=매일, 7=매주, @monthly=매월)
# delay: 시작 전 지연 (분)
# job-identifier: 작업 이름
# command: 실행 명령
```

### anacron 사용

```bash
# anacron 수동 실행
$ sudo anacron -f  # 강제 실행
$ sudo anacron -n  # 즉시 실행 (지연 없이)
$ sudo anacron -d  # 디버그 모드

# 특정 작업만
$ sudo anacron -f cron.daily

# 테스트
$ sudo anacron -T  # 설정 파일 검증
$ sudo anacron -d -n  # 디버그 + 즉시 실행

# 마지막 실행 시간
$ cat /var/spool/anacron/cron.daily
20241117

# anacron vs cron
# cron: 정확한 시간에 실행
# anacron: 시스템이 켜져있을 때 실행 (데스크톱/노트북에 적합)
```

---

## at 명령

### at 기본 사용

```bash
# at - 일회성 작업 예약

# at 설치 확인
$ systemctl status atd

# 특정 시간에 작업 예약
$ at 15:30
at> /home/user/task.sh
at>
job 1 at Mon Nov 17 15:30:00 2024

# 상대 시간
$ at now + 1 hour
$ at now + 30 minutes
$ at now + 1 day
$ at now + 1 week

# 특정 날짜와 시간
$ at 10:00 AM tomorrow
$ at 14:30 Nov 20
$ at 8:00 PM Friday

# 예약된 작업 보기
$ atq
1       Mon Nov 17 15:30:00 2024 a user

# 작업 상세 보기
$ at -c 1

# 작업 삭제
$ atrm 1
$ at -r 1

# 파일에서 읽기
$ at -f script.sh now + 1 hour

# stdin으로 전달
$ echo "/home/user/backup.sh" | at now + 5 minutes
```

### batch 명령

```bash
# batch - 시스템 부하가 낮을 때 실행

# batch 사용
$ batch
at> /home/user/heavy-task.sh
at>

# 부하 임계값 설정 (atd 옵션)
# /etc/default/atd (Debian/Ubuntu)
LOADAVG_LIMIT=1.5

$ sudo systemctl restart atd

# batch 작업도 atq로 확인
$ atq
2       Mon Nov 17 16:00:00 2024 b user
```

---

## 환경 변수

### cron 환경

```bash
# cron은 최소한의 환경에서 실행
# PATH가 제한적

# crontab에서 환경 변수 설정
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
HOME=/home/user
MAILTO=user@example.com
EDITOR=vim

# 작업에서 사용
0 3 * * * /home/user/backup.sh

# 절대 경로 사용 (권장)
0 3 * * * /usr/bin/python3 /home/user/script.py

# 또는 스크립트 내에서 PATH 설정
#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin
/usr/local/bin/mycommand
```

### 사용자 환경 로드

```bash
# 사용자 환경 로드가 필요한 경우

# .bashrc 소싱
* * * * * . ~/.bashrc && /home/user/script.sh

# 로그인 쉘로 실행
* * * * * bash -l -c '/home/user/script.sh'

# 스크립트 내에서
#!/bin/bash
source ~/.bashrc
# 실제 작업...

# 환경 변수 파일 사용
# crontab
0 3 * * * /home/user/backup.sh

# backup.sh
#!/bin/bash
source /home/user/.env
# DATABASE_URL 등 사용
```

---

## 로깅 및 디버깅

### 출력 리디렉션

```bash
# stdout 저장
* * * * * /home/user/script.sh > /tmp/cron.log

# stderr 포함
* * * * * /home/user/script.sh > /tmp/cron.log 2>&1

# 추가 모드
* * * * * /home/user/script.sh >> /tmp/cron.log 2>&1

# 타임스탬프 포함
* * * * * echo "$(date): Starting" >> /tmp/cron.log && /home/user/script.sh >> /tmp/cron.log 2>&1

# /dev/null로 버리기 (출력 억제)
* * * * * /home/user/script.sh > /dev/null 2>&1

# stdout만 저장, stderr는 이메일
* * * * * /home/user/script.sh > /tmp/cron.log

# stderr만 저장
* * * * * /home/user/script.sh 2> /tmp/cron-error.log
```

### cron 로그

```bash
# Debian/Ubuntu
$ sudo tail -f /var/log/syslog | grep CRON
Nov 17 15:30:01 server CRON[1234]: (user) CMD (/home/user/script.sh)

# Red Hat/Fedora
$ sudo tail -f /var/log/cron

# journald 사용
$ sudo journalctl -u cron -f
$ sudo journalctl -u cron --since "1 hour ago"
$ sudo journalctl -u cron | grep user

# 특정 사용자 cron 로그
$ sudo journalctl -t CRON | grep "(user)"
```

### 디버깅 팁

```bash
# 1. 스크립트에 로깅 추가
#!/bin/bash
LOG="/tmp/script.log"
echo "$(date): Script started" >> "$LOG"
# 작업...
echo "$(date): Script finished" >> "$LOG"

# 2. set -x 사용 (디버그 모드)
#!/bin/bash
set -x  # 디버그 활성화
# 작업...
set +x  # 디버그 비활성화

# 3. 테스트 cron 작업
*/5 * * * * echo "Cron works: $(date)" >> /tmp/cron-test.log

# 4. 스크립트 직접 실행 테스트
$ /home/user/script.sh
# 오류 없이 실행되는지 확인

# 5. cron 환경 확인
* * * * * env > /tmp/cron-env.txt
# 5분 후
$ cat /tmp/cron-env.txt

# 6. MAILTO로 이메일 받기
MAILTO=user@localhost
* * * * * /home/user/script.sh
# 실패 시 이메일 수신
```

---

## 보안

### cron 접근 제어

```bash
# /etc/cron.allow - 허용 목록
$ sudo vi /etc/cron.allow
user1
user2
admin

# cron.allow가 있으면 이 파일에 있는 사용자만 crontab 사용 가능

# /etc/cron.deny - 거부 목록
$ sudo vi /etc/cron.deny
baduser
guest

# cron.deny에 있는 사용자는 crontab 사용 불가

# 우선순위:
# 1. cron.allow 존재 시: 이 파일에 있는 사용자만 허용
# 2. cron.allow 없고 cron.deny 존재: deny에 없는 모든 사용자 허용
# 3. 둘 다 없음: root만 허용 (배포판에 따라 다름)

# 테스트
$ crontab -e
You (baduser) are not allowed to use this program (crontab)
```

### 권한 관리

```bash
# crontab 파일 권한
$ ls -l /var/spool/cron/crontabs/
total 4
-rw------- 1 user crontab 1234 Nov 17 10:00 user

# /etc/cron.d/ 파일 권한
$ ls -l /etc/cron.d/
-rw-r--r-- 1 root root 123 Nov 17 10:00 myapp

# 스크립트 권한
$ chmod 700 /home/user/script.sh
$ chown user:user /home/user/script.sh

# 민감한 정보 처리
# 스크립트에 패스워드 하드코딩 금지
# 환경 파일 사용
$ chmod 600 ~/.env
$ cat ~/.env
DATABASE_PASSWORD=secret

# 스크립트
#!/bin/bash
source ~/.env
mysql -u user -p"$DATABASE_PASSWORD" ...
```

### 보안 모범 사례

```bash
# 1. 절대 경로 사용
0 3 * * * /usr/bin/python3 /home/user/script.py

# 2. 출력 제어 (민감한 정보 노출 방지)
0 3 * * * /home/user/backup.sh > /dev/null 2>&1

# 3. 별도 사용자로 실행
# /etc/cron.d/myapp
0 3 * * * myapp /opt/myapp/backup.sh

# 4. 스크립트 검증
# 실행 전 존재 여부 확인
0 3 * * * test -x /home/user/backup.sh && /home/user/backup.sh

# 5. 로깅 및 감사
0 3 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1

# 6. 이메일 알림
MAILTO=admin@example.com
0 3 * * * /home/user/critical-task.sh
```

---

## 실전 예제

### 시스템 백업

```bash
# crontab -e
# 매일 새벽 2시 백업
0 2 * * * /home/user/scripts/backup.sh >> /var/log/backup.log 2>&1

# backup.sh
#!/bin/bash
set -e

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d)
LOG="/var/log/backup.log"

echo "$(date): Starting backup" >> "$LOG"

# 데이터베이스 백업
mysqldump -u backup -p"$DB_PASSWORD" --all-databases | \
    gzip > "$BACKUP_DIR/db-$DATE.sql.gz"

# 파일 백업
tar czf "$BACKUP_DIR/files-$DATE.tar.gz" \
    /home \
    /etc \
    /var/www

# 7일 이상 된 백업 삭제
find "$BACKUP_DIR" -name "*.gz" -mtime +7 -delete

echo "$(date): Backup completed" >> "$LOG"
```

### 로그 정리

```bash
# crontab -e
# 매일 자정 로그 정리
0 0 * * * /home/user/scripts/cleanup-logs.sh

# cleanup-logs.sh
#!/bin/bash

# 30일 이상 된 로그 압축
find /var/log -name "*.log" -mtime +30 -exec gzip {} \;

# 90일 이상 된 압축 로그 삭제
find /var/log -name "*.log.gz" -mtime +90 -delete

# 특정 애플리케이션 로그
find /opt/myapp/logs -name "*.log" -mtime +7 -delete

# 디스크 사용량 확인
if [ $(df /var/log | tail -1 | awk '{print $5}' | sed 's/%//') -gt 80 ]; then
    echo "WARNING: /var/log disk usage above 80%" | \
        mail -s "Disk Space Alert" admin@example.com
fi
```

### 웹 스크래핑

```bash
# crontab -e
# 매시간 데이터 수집
0 * * * * /home/user/scraper/run.sh >> /var/log/scraper.log 2>&1

# run.sh
#!/bin/bash
cd /home/user/scraper
source venv/bin/activate

python3 scraper.py

# 실패 시 알림
if [ $? -ne 0 ]; then
    echo "Scraper failed at $(date)" | \
        mail -s "Scraper Alert" admin@example.com
fi
```

### 모니터링

```bash
# crontab -e
# 5분마다 모니터링
*/5 * * * * /home/user/monitor.sh

# monitor.sh
#!/bin/bash

# 서비스 확인
if ! systemctl is-active --quiet nginx; then
    echo "Nginx is down at $(date)" | \
        mail -s "CRITICAL: Nginx Down" admin@example.com
    systemctl restart nginx
fi

# 디스크 사용량
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $USAGE -gt 90 ]; then
    echo "Disk usage: $USAGE%" | \
        mail -s "WARNING: Disk Usage High" admin@example.com
fi

# CPU 온도 (Raspberry Pi 등)
TEMP=$(vcgencmd measure_temp | cut -d= -f2 | cut -d\' -f1)
if [ $(echo "$TEMP > 70" | bc) -eq 1 ]; then
    echo "CPU temperature: $TEMP°C" | \
        mail -s "WARNING: High Temperature" admin@example.com
fi
```

### 정기 보고서

```bash
# crontab -e
# 매주 월요일 오전 9시 보고서
0 9 * * 1 /home/user/reports/weekly.sh

# weekly.sh
#!/bin/bash

REPORT="/tmp/weekly-report.txt"
DATE=$(date +%Y-%m-%d)

cat > "$REPORT" << EOF
Weekly System Report - $DATE
================================

System Uptime:
$(uptime)

Disk Usage:
$(df -h)

Memory Usage:
$(free -h)

Top Processes:
$(ps aux --sort=-%mem | head -10)

Failed Services:
$(systemctl --failed)

Recent Logins:
$(last -10)

Security Updates:
$(apt list --upgradable 2>/dev/null | grep -i security)

EOF

# 이메일 전송
mail -s "Weekly System Report - $DATE" admin@example.com < "$REPORT"
```

### 데이터베이스 최적화

```bash
# crontab -e
# 매주 일요일 새벽 3시
0 3 * * 0 /home/user/scripts/optimize-db.sh >> /var/log/db-optimize.log 2>&1

# optimize-db.sh
#!/bin/bash

MYSQL="mysql -u root -p$DB_PASSWORD"

echo "$(date): Starting database optimization"

# 모든 테이블 최적화
$MYSQL -e "SELECT CONCAT('OPTIMIZE TABLE ', table_schema, '.', table_name, ';')
    FROM information_schema.tables
    WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema')" \
    | grep OPTIMIZE | $MYSQL

# 통계 업데이트
$MYSQL -e "ANALYZE TABLE mydb.users, mydb.posts, mydb.comments"

echo "$(date): Optimization completed"
```

---

## 요약

cron 핵심 개념:

1. **crontab**: 사용자별 작업 스케줄
2. **시스템 cron**: /etc/crontab, /etc/cron.d/
3. **anacron**: 항상 켜져있지 않은 시스템용
4. **at**: 일회성 작업

cron 문법:
```
분 시 일 월 요일 명령
*  *  *  *  *   command

*/5 * * * * - 5분마다
0 2 * * * - 매일 2시
0 0 * * 0 - 매주 일요일
```

모범 사례:
- 절대 경로 사용
- 출력 리디렉션
- 오류 처리 및 로깅
- 환경 변수 명시적 설정
- 보안 (권한, cron.allow/deny)

---

[다음: 로깅 →](logging.md)

[← systemd로 돌아가기](systemd.md)

[← 목차로 돌아가기](../README.md)

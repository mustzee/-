# 고급 명령어

## 목차
- [파이프와 리다이렉션](#파이프와-리다이렉션)
- [프로세스 대체](#프로세스-대체)
- [xargs와 병렬 실행](#xargs와-병렬-실행)
- [작업 제어](#작업-제어)
- [고급 find 활용](#고급-find-활용)

---

## 파이프와 리다이렉션

### 파이프 (|)

```bash
# 기본 파이프
$ ls -l | grep "\.txt$"

# 여러 파이프
$ cat /var/log/syslog | grep "ERROR" | wc -l

# 페이징
$ dmesg | less

# 정렬 및 중복 제거
$ cat file.txt | sort | uniq

# Top 10 대용량 파일
$ du -sh/* | sort -hr | head -10

# 프로세스 종료
$ ps aux | grep apache | awk '{print $2}' | xargs kill

# 실시간 로그 필터링
$ tail -f /var/log/nginx/access.log | grep "404"
```

### 리다이렉션

```bash
# 출력 리다이렉션
$ echo "Hello" > file.txt      # 덮어쓰기
$ echo "World" >> file.txt     # 추가

# 표준 에러 리다이렉션
$ command 2> error.log
$ command 2>> error.log

# 표준 출력과 에러 모두
$ command > output.log 2>&1
$ command &> output.log        # 간단한 방법

# 표준 출력과 에러 분리
$ command > output.log 2> error.log

# 에러만 /dev/null로
$ command 2> /dev/null

# 모두 버리기
$ command &> /dev/null

# 입력 리다이렉션
$ command < input.txt

# Here Document
$ cat << EOF > file.txt
Line 1
Line 2
EOF

# Here String
$ grep "pattern" <<< "string to search"

# 파일 디스크립터
$ exec 3> custom.log
$ echo "Message" >&3
$ exec 3>&-  # 닫기
```

### tee - 출력 분기

```bash
# 화면과 파일에 동시 출력
$ ls -l | tee output.txt

# 추가 모드
$ ls -l | tee -a output.txt

# 여러 파일
$ command | tee file1.txt file2.txt

# 표준 에러도 함께
$ command 2>&1 | tee output.txt

# sudo와 함께 사용
$ echo "content" | sudo tee /etc/file.conf

# 여러 명령 조합
$ make 2>&1 | tee build.log | grep -i error
```

---

## 프로세스 대체

### <() - Command Substitution

```bash
# 두 명령 출력 비교
$ diff <(ls dir1) <(ls dir2)

# 파일과 명령 비교
$ diff file.txt <(curl -s https://example.com/file.txt)

# 정렬 비교
$ diff <(sort file1.txt) <(sort file2.txt)

# 여러 소스 결합
$ paste <(cut -f1 file1.txt) <(cut -f2 file2.txt)

# 프로세스 모니터링
$ watch -n 1 "diff <(ps aux) <(sleep 1; ps aux)"
```

### $() vs ``

```bash
# 현대적 방법 - $()
$ echo "Today is $(date)"
$ files=$(ls *.txt)

# 레거시 방법 - ``
$ echo "Today is `date`"
$ files=`ls *.txt`

# 중첩 가능
$ echo "Kernel: $(uname -r), Files: $(ls | wc -l)"

# 실용 예제
$ for file in $(find . -name "*.log"); do
    echo "Processing $file"
done

# 백업 파일명 생성
$ cp important.txt important_$(date +%Y%m%d).txt
```

---

## xargs와 병렬 실행

### xargs - 인자 전달

```bash
# 기본 사용
$ echo "file1 file2 file3" | xargs rm

# 한 줄씩 처리
$ cat files.txt | xargs -I {} mv {} /backup/

# 여러 인자
$ ls *.txt | xargs -n 1 wc -l

# 대화형 확인
$ find . -name "*.tmp" | xargs -p rm

# 빈 입력 무시
$ find . -name "*.log" | xargs -r rm

# 병렬 실행
$ find . -name "*.jpg" | xargs -P 4 -I {} convert {} {}.png

# 공백 처리
$ find . -name "*.txt" -print0 | xargs -0 rm

# 여러 명령 실행
$ echo "server1 server2 server3" | xargs -n 1 -P 3 ssh

# 로그 파일 압축
$ find /var/log -name "*.log" -mtime +7 | xargs gzip

# 백업
$ ls *.conf | xargs -I {} cp {} {}.bak
```

### parallel - GNU parallel

```bash
# 설치
$ sudo apt install parallel

# 기본 사용
$ parallel echo ::: A B C

# 파일 처리
$ ls *.txt | parallel wc -l

# 여러 변수
$ parallel echo {1} {2} ::: A B ::: 1 2

# 작업 수 제한
$ parallel -j 4 command ::: inputs

# 진행 상황
$ parallel --progress command ::: inputs

# 드라이 런
$ parallel --dry-run command ::: inputs

# 로그
$ parallel --joblog log.txt command ::: inputs

# 이미지 처리
$ parallel convert {} -resize 50% small_{} ::: *.jpg

# SSH 병렬 실행
$ parallel -S server1,server2 command ::: data

# 재시도
$ parallel --retries 3 command ::: inputs

# 타임아웃
$ parallel --timeout 60 command ::: inputs
```

---

## 작업 제어

### bg / fg - 백그라운드 작업

```bash
# 백그라운드 실행
$ long_command &
[1] 12345

# 실행 중 작업을 백그라운드로
# Ctrl+Z로 일시 중지
# bg 명령으로 백그라운드 재개
$ bg

# 포그라운드로 가져오기
$ fg

# 작업 목록
$ jobs
[1]+  Running     long_command &
[2]-  Stopped     vim file.txt

# 특정 작업 제어
$ fg %1
$ bg %2
$ kill %1

# nohup - 로그아웃 후에도 실행
$ nohup long_command &
$ nohup long_command > output.log 2>&1 &

# disown - 작업 분리
$ long_command &
$ disown

# screen / tmux로 세션 관리
$ screen
$ tmux
```

### screen - 터미널 멀티플렉서

```bash
# 설치
$ sudo apt install screen

# 새 세션 시작
$ screen

# 이름 있는 세션
$ screen -S mysession

# 세션 분리 (Ctrl+A, D)

# 세션 목록
$ screen -ls

# 세션 재연결
$ screen -r
$ screen -r mysession

# 세션 종료
# exit 또는 Ctrl+D

# 주요 단축키 (Ctrl+A 후):
# c: 새 윈도우
# n: 다음 윈도우
# p: 이전 윈도우
# ": 윈도우 목록
# k: 윈도우 종료
# d: 세션 분리
```

### tmux - 현대적 멀티플렉서

```bash
# 설치
$ sudo apt install tmux

# 새 세션
$ tmux

# 이름 있는 세션
$ tmux new -s mysession

# 세션 분리 (Ctrl+B, D)

# 세션 목록
$ tmux ls

# 세션 재연결
$ tmux attach
$ tmux attach -t mysession

# 주요 단축키 (Ctrl+B 후):
# c: 새 윈도우
# ,: 윈도우 이름 변경
# n: 다음 윈도우
# p: 이전 윈도우
# %: 세로 분할
# ": 가로 분할
# 방향키: 패널 이동
# x: 패널 종료
# d: 세션 분리

# 설정 파일 (~/.tmux.conf)
$ cat > ~/.tmux.conf << EOF
# 마우스 지원
set -g mouse on

# 256 색상
set -g default-terminal "screen-256color"

# 상태바 색상
set -g status-bg blue
set -g status-fg white
EOF
```

---

## 고급 find 활용

### 복잡한 검색 조건

```bash
# AND 조건
$ find / -name "*.log" -size +10M

# OR 조건
$ find / \( -name "*.log" -o -name "*.txt" \)

# NOT 조건
$ find / -type f ! -name "*.log"

# 시간 범위
$ find / -newermt "2024-11-01" ! -newermt "2024-11-17"

# 복합 조건
$ find / -type f -name "*.log" -size +10M -mtime -7

# 권한 기반
$ find / -perm 777
$ find / -perm /u=s  # SUID
$ find / -perm /g=s  # SGID

# 빈 파일/디렉토리
$ find / -empty

# 소유자 없는 파일
$ find / -nouser -o -nogroup

# 하드링크
$ find / -links +1

# inode 번호
$ find / -inum 123456
```

### 고급 실행 패턴

```bash
# -exec로 명령 실행
$ find / -name "*.tmp" -exec rm -f {} \;

# 효율적인 방법 (+로 묶어서)
$ find / -name "*.tmp" -exec rm -f {} +

# 확인 후 실행
$ find / -name "*.tmp" -ok rm -f {} \;

# 여러 명령
$ find / -name "*.log" -exec gzip {} \; -exec mv {}.gz /backup/ \;

# bash 스크립트 실행
$ find / -name "*.txt" -exec bash -c 'echo "Processing: $1"' _ {} \;

# 파일 이름 활용
$ find . -name "*.txt" -exec bash -c 'mv "$1" "${1%.txt}.bak"' _ {} \;

# 병렬 실행
$ find . -name "*.jpg" -print0 | xargs -0 -P 4 -I {} convert {} {}.png

# 크기 기반 처리
$ find / -size +100M -exec ls -lh {} \; | sort -k5 -hr
```

### 실전 find 예제

```bash
# 오래된 로그 파일 정리
$ find /var/log -name "*.log" -mtime +30 -delete

# 대용량 파일 찾기
$ find / -type f -size +1G -exec ls -lh {} \; 2>/dev/null

# SUID/SGID 파일 보안 감사
$ find / -type f \( -perm -4000 -o -perm -2000 \) -exec ls -l {} \;

# 수정된 설정 파일 찾기
$ find /etc -name "*.conf" -mtime -7

# 중복 파일 찾기 (이름 기반)
$ find / -type f -printf '%f\n' | sort | uniq -d

# 디스크 공간 감사
$ find / -type f -size +100M -printf '%s %p\n' | sort -rn | head -20

# 특정 확장자 모두 백업
$ find . -name "*.conf" -exec tar -czf configs_$(date +%Y%m%d).tar.gz {} +

# 권한 일괄 수정
$ find /var/www -type d -exec chmod 755 {} \;
$ find /var/www -type f -exec chmod 644 {} \;

# 심볼릭 링크 끊어진 것 찾기
$ find / -xtype l

# 최근 변경 파일 모니터링
$ watch -n 60 'find /var/log -mmin -1'
```

---

## 실전 고급 예제

### 예제 1: 로그 분석 파이프라인

```bash
# 가장 빈번한 IP 주소 Top 10
$ cat /var/log/nginx/access.log \
  | awk '{print $1}' \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -10

# 404 에러 분석
$ grep "404" /var/log/nginx/access.log \
  | awk '{print $7}' \
  | sort \
  | uniq -c \
  | sort -rn

# 시간대별 요청 수
$ cat /var/log/nginx/access.log \
  | awk '{print $4}' \
  | cut -d: -f1-2 \
  | sort \
  | uniq -c
```

### 예제 2: 시스템 정리 스크립트

```bash
#!/bin/bash
# cleanup.sh - 시스템 정리 자동화

# 오래된 로그 압축
find /var/log -name "*.log" -mtime +7 -exec gzip {} \;

# 압축된 로그 삭제
find /var/log -name "*.gz" -mtime +30 -delete

# 임시 파일 정리
find /tmp -type f -atime +7 -delete

# 캐시 정리
find ~/.cache -type f -atime +30 -delete

# 패키지 캐시
sudo apt-get clean

# 고아 패키지
sudo apt-get autoremove

echo "Cleanup completed: $(date)"
```

### 예제 3: 병렬 백업

```bash
#!/bin/bash
# parallel_backup.sh

# 백업 대상 디렉토리
DIRS="/etc /home /var/www"

# 백업 위치
BACKUP_DIR="/backup/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# 병렬 백업
echo "$DIRS" | tr ' ' '\n' | parallel -j 3 \
  'tar -czf '"$BACKUP_DIR"'/{/.}.tar.gz {}'

echo "Backup completed"
```

---

## 요약

고급 명령어 테크닉:

- **파이프와 리다이렉션**: 명령어 조합의 핵심
- **프로세스 대체**: 유연한 데이터 처리
- **xargs/parallel**: 병렬 처리로 성능 향상
- **작업 제어**: screen/tmux로 세션 관리
- **고급 find**: 강력한 파일 검색과 처리

이러한 고급 기술을 마스터하면 복잡한 작업을 효율적으로 자동화할 수 있습니다.

---

[다음: 권한 기본 →](../05-permissions/basics.md)

[← 네트워크 명령어로 돌아가기](network.md)

[← 목차로 돌아가기](../README.md)

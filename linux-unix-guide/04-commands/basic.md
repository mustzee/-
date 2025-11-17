# 기본 명령어

## 목차
- [파일 및 디렉토리 탐색](#파일-및-디렉토리-탐색)
- [파일 조작](#파일-조작)
- [텍스트 표시](#텍스트-표시)
- [시스템 정보](#시스템-정보)
- [도움말](#도움말)

---

## 파일 및 디렉토리 탐색

### ls - 디렉토리 내용 표시

```bash
# 기본 목록
$ ls
Documents  Downloads  Pictures  Videos

# 자세한 정보 (-l)
$ ls -l
drwxr-xr-x 2 user user 4096 Nov 17 12:00 Documents
drwxr-xr-x 5 user user 4096 Nov 17 11:30 Downloads

# 숨김 파일 포함 (-a)
$ ls -a
.  ..  .bashrc  .profile  Documents  Downloads

# 숨김 파일 포함, . 과 .. 제외 (-A)
$ ls -A

# 자세한 정보 + 숨김 파일
$ ls -la

# 사람이 읽기 쉬운 크기 (-h)
$ ls -lh
-rw-r--r-- 1 user user 1.5M Nov 17 12:00 file.txt
drwxr-xr-x 2 user user 4.0K Nov 17 11:30 directory

# 최신 파일 먼저 (-t)
$ ls -lt

# 역순 정렬 (-r)
$ ls -lr

# 재귀적 표시 (-R)
$ ls -R
./directory:
file1.txt  file2.txt

./directory/subdirectory:
file3.txt

# 한 줄에 하나씩 (-1)
$ ls -1
Documents
Downloads
Pictures

# 파일 타입 표시 (-F)
$ ls -F
Documents/  script.sh*  link@  file.txt

# inode 번호 표시 (-i)
$ ls -i
123456 file.txt  234567 directory

# 크기 순 정렬 (-S)
$ ls -lhS

# 확장자별 정렬 (-X)
$ ls -X

# 색상 표시
$ ls --color=auto

# 디렉토리만 표시
$ ls -ld */

# 특정 패턴
$ ls *.txt
$ ls file[0-9].txt
$ ls file?.txt
```

### cd - 디렉토리 변경

```bash
# 절대 경로로 이동
$ cd /home/user/Documents

# 상대 경로로 이동
$ cd Documents

# 홈 디렉토리로
$ cd
$ cd ~

# 부모 디렉토리로
$ cd ..

# 이전 디렉토리로
$ cd -

# 두 단계 위로
$ cd ../..

# 특정 사용자 홈으로
$ cd ~username

# 경로에 공백이 있을 때
$ cd "My Documents"
$ cd My\ Documents

# CDPATH 환경변수 사용
$ export CDPATH=.:~:/usr/local
$ cd projects  # ~/projects나 /usr/local/projects 검색
```

### pwd - 현재 디렉토리 표시

```bash
# 현재 경로
$ pwd
/home/user/Documents

# 심볼릭 링크 해석
$ pwd -P
/home/user/real/path

# 논리적 경로
$ pwd -L
```

### tree - 디렉토리 트리

```bash
# 설치
$ sudo apt install tree

# 기본 트리
$ tree
.
├── dir1
│   ├── file1.txt
│   └── file2.txt
└── dir2
    └── file3.txt

# 깊이 제한
$ tree -L 2

# 디렉토리만
$ tree -d

# 숨김 파일 포함
$ tree -a

# 파일 크기 표시
$ tree -h

# 패턴 매칭
$ tree -P "*.txt"

# 제외
$ tree -I "node_modules|.git"
```

---

## 파일 조작

### touch - 파일 생성/타임스탬프 수정

```bash
# 빈 파일 생성
$ touch file.txt

# 여러 파일 생성
$ touch file1.txt file2.txt file3.txt

# 범위로 생성
$ touch file{1..10}.txt
$ ls
file1.txt  file2.txt  ... file10.txt

# 타임스탬프 현재 시간으로 업데이트
$ touch existing_file.txt

# 특정 시간 설정
$ touch -t 202411171200.00 file.txt

# 다른 파일과 같은 타임스탬프
$ touch -r reference.txt newfile.txt

# 접근 시간만
$ touch -a file.txt

# 수정 시간만
$ touch -m file.txt

# 파일이 없어도 생성하지 않음
$ touch -c file.txt
```

### mkdir - 디렉토리 생성

```bash
# 디렉토리 생성
$ mkdir mydir

# 여러 디렉토리
$ mkdir dir1 dir2 dir3

# 중첩 디렉토리
$ mkdir -p /path/to/deep/directory

# 권한 지정
$ mkdir -m 755 mydir

# 상위 디렉토리도 생성하며 권한 지정
$ mkdir -p -m 755 /path/to/directory

# 프로젝트 구조 생성
$ mkdir -p project/{src,tests,docs,config}
$ mkdir -p project/src/{main,utils}

# verbose 모드
$ mkdir -v mydir
mkdir: created directory 'mydir'
```

### cp - 복사

```bash
# 파일 복사
$ cp source.txt dest.txt

# 디렉토리 복사
$ cp -r source_dir dest_dir

# 대화형 (덮어쓰기 확인)
$ cp -i file.txt /tmp/

# 강제 (확인 없이)
$ cp -f file.txt /tmp/

# 속성 보존
$ cp -p file.txt /backup/

# 아카이브 모드 (모든 속성 보존)
$ cp -a /source/ /dest/

# 업데이트 (최신 파일만)
$ cp -u source.txt dest.txt

# 백업 생성
$ cp --backup=numbered file.txt /tmp/

# 심볼릭 링크 그대로 복사
$ cp -d link.txt /tmp/

# verbose
$ cp -v file.txt /tmp/
'file.txt' -> '/tmp/file.txt'

# 여러 파일을 디렉토리로
$ cp file1.txt file2.txt file3.txt /destination/

# 와일드카드
$ cp *.txt /backup/

# 제외하고 복사 (rsync 사용)
$ rsync -av --exclude='*.log' source/ dest/
```

### mv - 이동/이름변경

```bash
# 파일 이동
$ mv file.txt /tmp/

# 이름 변경
$ mv oldname.txt newname.txt

# 디렉토리 이동
$ mv mydir /opt/

# 여러 파일 이동
$ mv file1.txt file2.txt /destination/

# 대화형
$ mv -i file.txt /tmp/

# 강제
$ mv -f file.txt /tmp/

# 업데이트만
$ mv -u source.txt dest.txt

# 백업 생성
$ mv --backup=numbered file.txt /tmp/

# verbose
$ mv -v old.txt new.txt
'old.txt' -> 'new.txt'

# 확장자 일괄 변경
$ for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# 공백을 언더스코어로
$ for f in *\ *; do mv "$f" "${f// /_}"; done

# 소문자로 변환
$ for f in *; do mv "$f" "$(echo $f | tr 'A-Z' 'a-z')"; done
```

### rm - 삭제

```bash
# 파일 삭제
$ rm file.txt

# 여러 파일
$ rm file1.txt file2.txt

# 디렉토리와 내용
$ rm -r directory/

# 강제 삭제
$ rm -f file.txt

# 강제 재귀 삭제
$ rm -rf directory/

# 대화형
$ rm -i file.txt

# 3개 이상 삭제 시만 확인
$ rm -I *.txt

# verbose
$ rm -v file.txt
removed 'file.txt'

# 빈 디렉토리 삭제
$ rmdir empty_dir/

# 와일드카드
$ rm *.log
$ rm *~

# 안전한 삭제 (복구 불가능하게)
$ shred -vfz -n 3 sensitive.txt

# 특정 파일만 제외하고 삭제
$ rm !(keep.txt)  # bash extglob 필요
```

---

## 텍스트 표시

### cat - 파일 내용 출력

```bash
# 파일 내용
$ cat file.txt

# 여러 파일
$ cat file1.txt file2.txt

# 파일 연결
$ cat file1.txt file2.txt > combined.txt

# 줄 번호
$ cat -n file.txt

# 비어있지 않은 줄만 번호
$ cat -b file.txt

# 탭을 ^I로 표시
$ cat -T file.txt

# 줄 끝 표시
$ cat -E file.txt

# 모든 특수문자 표시
$ cat -A file.txt

# 파일 생성 (여기 문서)
$ cat > newfile.txt << EOF
This is line 1
This is line 2
EOF

# 추가
$ cat >> file.txt << EOF
New line
EOF
```

### head - 파일 시작 부분

```bash
# 기본 (10줄)
$ head file.txt

# 줄 수 지정
$ head -n 20 file.txt
$ head -20 file.txt

# 바이트 수
$ head -c 100 file.txt

# 여러 파일
$ head file1.txt file2.txt

# 파일 이름 표시 안 함
$ head -q file1.txt file2.txt

# 마지막 N줄 제외
$ head -n -10 file.txt  # 마지막 10줄 제외한 모든 줄
```

### tail - 파일 끝 부분

```bash
# 기본 (10줄)
$ tail file.txt

# 줄 수 지정
$ tail -n 20 file.txt

# 실시간 로그 감시 (가장 많이 사용)
$ tail -f /var/log/syslog

# 여러 파일 감시
$ tail -f /var/log/nginx/*.log

# N번째 줄부터 끝까지
$ tail -n +50 file.txt  # 50번째 줄부터

# 파일 재생성 시에도 계속 감시
$ tail -F /var/log/app.log

# PID 저장 (스크립트에서 kill하기 위해)
$ tail -f --pid=1234 file.txt

# 바이트 수
$ tail -c 100 file.txt
```

### less - 페이지 단위 보기

```bash
# 파일 보기
$ less file.txt

# 내부 명령어:
# 스페이스: 다음 페이지
# b: 이전 페이지
# /pattern: 검색
# n: 다음 검색 결과
# N: 이전 검색 결과
# g: 파일 시작
# G: 파일 끝
# q: 종료

# 줄 번호 표시
$ less -N file.txt

# 실시간 업데이트 (tail -f와 유사)
$ less +F /var/log/syslog

# 압축 파일 보기
$ zless file.txt.gz

# 여러 파일
$ less file1.txt file2.txt
# :n (다음 파일), :p (이전 파일)

# 특정 줄부터
$ less +100 file.txt

# 특정 패턴부터
$ less +/ERROR file.txt
```

---

## 시스템 정보

### uname - 시스템 정보

```bash
# 커널 이름
$ uname
Linux

# 모든 정보
$ uname -a
Linux hostname 5.15.0-78-generic #85-Ubuntu SMP x86_64 GNU/Linux

# 커널 이름
$ uname -s

# 노드 이름 (호스트명)
$ uname -n

# 커널 릴리스
$ uname -r
5.15.0-78-generic

# 커널 버전
$ uname -v

# 하드웨어 플랫폼
$ uname -m
x86_64

# 프로세서 타입
$ uname -p

# 운영체제
$ uname -o
GNU/Linux
```

### hostname - 호스트명

```bash
# 호스트명 확인
$ hostname
myserver

# 도메인 포함
$ hostname -f
myserver.example.com

# 도메인만
$ hostname -d
example.com

# IP 주소
$ hostname -I
192.168.1.100 10.0.0.5

# 모든 IP
$ hostname -A

# 호스트명 변경 (임시)
$ sudo hostname newname

# 영구 변경
$ sudo hostnamectl set-hostname newname
```

### whoami - 현재 사용자

```bash
$ whoami
user

# 사용자 ID
$ id
uid=1000(user) gid=1000(user) groups=1000(user),4(adm),24(cdrom),27(sudo)

# 사용자 이름만
$ id -un

# 그룹 이름만
$ id -gn

# 모든 그룹
$ groups
user adm cdrom sudo

# 특정 사용자의 그룹
$ groups alice
```

### uptime - 가동 시간

```bash
$ uptime
 12:34:56 up 5 days,  3:21,  2 users,  load average: 0.15, 0.10, 0.08

# 가동 시간만
$ uptime -p
up 5 days, 3 hours, 21 minutes

# 부팅 시각
$ uptime -s
2024-11-12 09:13:42
```

### date - 날짜와 시간

```bash
# 현재 날짜/시간
$ date
Fri Nov 17 12:34:56 KST 2024

# 형식 지정
$ date +%Y-%m-%d
2024-11-17

$ date +%H:%M:%S
12:34:56

$ date +%Y%m%d_%H%M%S
20241117_123456

# 다양한 형식
$ date +"%Y-%m-%d %H:%M:%S"
2024-11-17 12:34:56

$ date +%s  # Unix timestamp
1700195696

# UTC 시간
$ date -u

# 특정 시간 표시
$ date -d "2024-12-25"
Wed Dec 25 00:00:00 KST 2024

$ date -d "next Monday"
$ date -d "2 days ago"
$ date -d "last week"
$ date -d "+3 hours"

# 타임스탬프에서 변환
$ date -d @1700195696
Fri Nov 17 12:34:56 KST 2024

# 시간 설정 (root)
$ sudo date -s "2024-11-17 12:00:00"
```

### which - 명령어 위치

```bash
# 실행 파일 경로
$ which python3
/usr/bin/python3

# 모든 경로
$ which -a python
/usr/bin/python
/usr/local/bin/python

# 여러 명령어
$ which ls cd pwd
/usr/bin/ls
/usr/bin/cd
/usr/bin/pwd
```

---

## 도움말

### man - 매뉴얼 페이지

```bash
# 매뉴얼 보기
$ man ls

# 섹션 지정
$ man 1 printf  # 명령어
$ man 3 printf  # 라이브러리 함수

# 매뉴얼 검색
$ man -k keyword
$ apropos keyword

# 짧은 설명
$ whatis ls
ls (1) - list directory contents

# 모든 매뉴얼 업데이트
$ sudo mandb

# 매뉴얼 위치
$ man -w ls
/usr/share/man/man1/ls.1.gz

# 페이지 출력
$ man ls | cat
```

### help - 내장 명령어 도움말

```bash
# bash 내장 명령어
$ help cd

# 모든 내장 명령어
$ help

# 간단한 도움말
$ help -d cd
```

### --help 옵션

```bash
# 대부분의 명령어
$ ls --help
$ cp --help
$ rm --help

# 짧은 형식
$ command -h
```

### info - 정보 페이지

```bash
# GNU info 시스템
$ info ls

# 특정 노드
$ info coreutils 'ls invocation'
```

---

## 실전 예제

### 예제 1: 파일 백업

```bash
# 날짜가 포함된 백업
$ cp important.txt important_$(date +%Y%m%d).txt.bak

# 디렉토리 전체 백업
$ cp -a /home/user /backup/user_$(date +%Y%m%d)/
```

### 예제 2: 로그 확인

```bash
# 실시간 에러 로그
$ tail -f /var/log/syslog | grep ERROR

# 최근 100줄 확인
$ tail -n 100 /var/log/nginx/access.log
```

### 예제 3: 대량 파일 작업

```bash
# 모든 .txt 파일을 backup/ 디렉토리로
$ mkdir -p backup
$ cp *.txt backup/

# 빈 파일 생성
$ touch file{1..100}.txt

# 특정 패턴 파일만 삭제
$ rm *_temp.txt
```

---

## 요약

기본 명령어 마스터하기:

- **ls**: 파일 목록
- **cd**: 디렉토리 이동
- **cp/mv/rm**: 파일 조작
- **cat/head/tail/less**: 파일 내용 보기
- **man/help**: 도움말

이 명령어들은 리눅스 사용의 기초이며, 매일 사용하게 됩니다.

---

[다음: 텍스트 처리 명령어 →](text.md)

[← 파일시스템 마운팅으로 돌아가기](../03-filesystem/mounting.md)

[← 목차로 돌아가기](../README.md)

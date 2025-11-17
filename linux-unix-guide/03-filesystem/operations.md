# 파일시스템 작업

## 목차
- [파일 및 디렉토리 기본 작업](#파일-및-디렉토리-기본-작업)
- [파일 검색](#파일-검색)
- [파일 내용 처리](#파일-내용-처리)
- [파일 압축 및 아카이브](#파일-압축-및-아카이브)
- [링크 (하드링크와 심볼릭링크)](#링크-하드링크와-심볼릭링크)
- [파일 시스템 검사 및 복구](#파일-시스템-검사-및-복구)

---

## 파일 및 디렉토리 기본 작업

### 파일 생성

```bash
# 빈 파일 생성
$ touch file.txt

# 여러 파일 한번에 생성
$ touch file1.txt file2.txt file3.txt

# 타임스탬프 변경
$ touch -t 202411171200.00 file.txt  # YYYYMMDDhhmm.ss

# 파일 존재 시 타임스탬프만 업데이트
$ touch existing_file.txt

# 접근 시간만 변경
$ touch -a file.txt

# 수정 시간만 변경
$ touch -m file.txt

# 특정 파일의 타임스탬프 복사
$ touch -r reference.txt newfile.txt
```

### 디렉토리 생성

```bash
# 단일 디렉토리 생성
$ mkdir mydir

# 여러 디렉토리 생성
$ mkdir dir1 dir2 dir3

# 중첩 디렉토리 생성 (-p: parent)
$ mkdir -p /path/to/deep/nested/directory

# 권한 지정하며 생성
$ mkdir -m 755 mydir

# 프로젝트 구조 한번에 생성
$ mkdir -p project/{src,tests,docs,config}
$ tree project/
project/
├── config
├── docs
├── src
└── tests
```

### 파일 복사

```bash
# 기본 복사
$ cp source.txt destination.txt

# 디렉토리 복사 (-r: recursive)
$ cp -r source_dir/ dest_dir/

# 대화형 복사 (-i: interactive)
$ cp -i file.txt /tmp/
cp: overwrite '/tmp/file.txt'? y

# 강제 덮어쓰기
$ cp -f file.txt /tmp/

# 속성 보존 (-p: preserve)
$ cp -p file.txt /backup/
# 권한, 소유자, 타임스탬프 유지

# 전체 속성 보존 (-a: archive)
$ cp -a /home/user/ /backup/user/
# -a = -dR --preserve=all

# 심볼릭 링크 복사 시 원본 파일 복사하지 않음
$ cp -d link.txt /tmp/

# 진행 상황 표시 (-v: verbose)
$ cp -v source.txt dest.txt
'source.txt' -> 'dest.txt'

# 업데이트된 파일만 복사 (-u: update)
$ cp -u source.txt dest.txt

# 백업 생성하며 복사
$ cp --backup=numbered file.txt /tmp/
$ ls /tmp/
file.txt  file.txt.~1~  file.txt.~2~

# 특정 파일만 제외하고 복사
$ rsync -av --exclude='*.log' source/ dest/
```

### 파일 이동 및 이름 변경

```bash
# 파일 이동
$ mv file.txt /tmp/

# 파일 이름 변경
$ mv oldname.txt newname.txt

# 디렉토리 이동
$ mv mydir/ /opt/

# 대화형 이동
$ mv -i file.txt /tmp/
mv: overwrite '/tmp/file.txt'?

# 강제 덮어쓰기
$ mv -f file.txt /tmp/

# 업데이트된 파일만 이동
$ mv -u source.txt dest.txt

# 백업 생성하며 이동
$ mv --backup=numbered file.txt /tmp/

# 여러 파일을 디렉토리로 이동
$ mv file1.txt file2.txt file3.txt /destination/

# 확장자 일괄 변경
$ for file in *.txt; do mv "$file" "${file%.txt}.md"; done
```

### 파일 삭제

```bash
# 파일 삭제
$ rm file.txt

# 대화형 삭제
$ rm -i file.txt
rm: remove regular file 'file.txt'? y

# 강제 삭제
$ rm -f file.txt

# 디렉토리와 내용 전체 삭제
$ rm -r directory/

# 강제로 디렉토리 삭제
$ rm -rf directory/

# 주의! 절대 실행하지 말 것
$ rm -rf /  # 시스템 전체 삭제 (현대 시스템은 보호됨)

# 안전하게 삭제 (확인 요청)
$ rm -rI directory/  # 3개 이상 파일 삭제 시 확인

# 빈 디렉토리만 삭제
$ rmdir empty_directory/

# 상위 디렉토리도 비어있으면 함께 삭제
$ rmdir -p path/to/empty/directory/

# 특정 패턴의 파일 삭제
$ rm *.log
$ rm *~  # 백업 파일 삭제

# 오래된 파일 삭제
$ find /var/log/ -name "*.log" -mtime +30 -delete

# 안전한 삭제 (덮어쓰기)
$ shred -vfz -n 3 sensitive_file.txt
# -v: verbose, -f: 권한 변경 후 삭제, -z: 0으로 덮어쓰기, -n: 반복 횟수
```

---

## 파일 검색

### find 명령어

```bash
# 이름으로 검색
$ find /home -name "*.txt"
$ find /home -iname "*.TXT"  # 대소문자 무시

# 타입으로 검색
$ find /var -type f  # 파일
$ find /var -type d  # 디렉토리
$ find /var -type l  # 심볼릭 링크

# 크기로 검색
$ find / -size +100M  # 100MB 이상
$ find / -size -10k   # 10KB 이하
$ find / -size 50M    # 정확히 50MB

# 시간으로 검색
$ find /home -mtime -7      # 최근 7일 이내 수정
$ find /home -mtime +30     # 30일 이전 수정
$ find /home -atime -1      # 최근 1일 이내 접근
$ find /home -ctime -2      # 최근 2일 이내 상태 변경

# 분 단위
$ find /tmp -mmin -60       # 최근 60분 이내 수정

# 권한으로 검색
$ find / -perm 777          # 정확히 777
$ find / -perm -644         # 최소한 644
$ find / -perm /u+x         # 사용자 실행 권한 있음

# 소유자로 검색
$ find /home -user alice
$ find /home -group developers

# 여러 조건 조합
$ find /var/log -name "*.log" -size +10M -mtime -7

# 실행 권한 있는 파일
$ find /usr/bin -type f -executable

# SUID 파일 찾기
$ find / -perm -4000 2>/dev/null

# 빈 파일/디렉토리
$ find /tmp -empty

# 검색 결과에 명령 실행
$ find /home -name "*.bak" -delete
$ find /var/log -name "*.log" -exec gzip {} \;
$ find /home -name "*.txt" -exec cat {} \; > all.txt

# 확인 후 실행
$ find /tmp -name "*.tmp" -ok rm {} \;
< rm ... /tmp/file.tmp > ? y

# 여러 파일을 한번에 처리
$ find /home -name "*.jpg" -exec cp {} /backup/ +

# 검색 깊이 제한
$ find /home -maxdepth 2 -name "*.conf"
$ find /home -mindepth 3 -name "*.txt"

# 다른 파일시스템 제외
$ find / -xdev -name "large_file"

# 심볼릭 링크 따라가기
$ find / -follow -name "file.txt"

# 정규표현식 사용
$ find /etc -regex ".*conf"

# 파일 수 세기
$ find /home -type f | wc -l
```

### locate 명령어

```bash
# 데이터베이스 업데이트
$ sudo updatedb

# 파일 찾기 (훨씬 빠름)
$ locate filename.txt

# 대소문자 무시
$ locate -i FILENAME.txt

# 정규표현식 사용
$ locate -r '/home/.*/\.bashrc$'

# 기존 파일만 표시
$ locate -e filename

# 파일 수 제한
$ locate -l 10 "*.log"

# 통계 표시
$ locate -S
Database /var/lib/mlocate/mlocate.db:
    11,234 directories
    98,765 files
    5,678,901 bytes in file names
    2,345,678 bytes used to store database
```

### which / whereis

```bash
# 실행 파일 경로
$ which python3
/usr/bin/python3

$ which -a python  # 모든 경로
/usr/bin/python
/usr/local/bin/python

# 바이너리, 소스, 매뉴얼 위치
$ whereis ls
ls: /usr/bin/ls /usr/share/man/man1/ls.1.gz

$ whereis -b ls  # 바이너리만
ls: /usr/bin/ls

$ whereis -m ls  # 매뉴얼만
ls: /usr/share/man/man1/ls.1.gz
```

---

## 파일 내용 처리

### 파일 내용 보기

```bash
# 전체 내용
$ cat file.txt

# 여러 파일 연결
$ cat file1.txt file2.txt > combined.txt

# 줄 번호 표시
$ cat -n file.txt
     1  First line
     2  Second line
     3  Third line

# 비어있지 않은 줄만 번호
$ cat -b file.txt

# 처음 몇 줄
$ head file.txt         # 기본 10줄
$ head -n 5 file.txt    # 5줄
$ head -c 100 file.txt  # 100바이트

# 마지막 몇 줄
$ tail file.txt         # 기본 10줄
$ tail -n 20 file.txt   # 20줄

# 실시간 로그 보기
$ tail -f /var/log/syslog

# 특정 줄부터 끝까지
$ tail -n +50 file.txt  # 50번째 줄부터

# 페이지 단위로 보기
$ less file.txt         # 위아래 스크롤, 검색 가능
$ more file.txt         # 아래로만 스크롤

# 바이너리 파일 보기
$ hexdump -C file.bin
$ xxd file.bin

# 문자열 추출
$ strings binary_file
```

### 파일 비교

```bash
# 텍스트 파일 비교
$ diff file1.txt file2.txt
3c3
< Old line
---
> New line

# 나란히 비교
$ diff -y file1.txt file2.txt

# 통합 형식
$ diff -u file1.txt file2.txt

# 디렉토리 비교
$ diff -r dir1/ dir2/

# 간단한 비교 (다른지 여부만)
$ diff -q file1.txt file2.txt
Files file1.txt and file2.txt differ

# 패치 파일 생성
$ diff -u original.txt modified.txt > changes.patch

# 패치 적용
$ patch original.txt < changes.patch

# 바이너리 파일 비교
$ cmp file1.bin file2.bin
file1.bin file2.bin differ: byte 45, line 3

# 대화형 비교 (vimdiff)
$ vimdiff file1.txt file2.txt
```

### 파일 내용 수정

```bash
# sed - 스트림 에디터
# 문자열 치환 (첫 번째)
$ sed 's/old/new/' file.txt

# 전체 치환
$ sed 's/old/new/g' file.txt

# 파일 직접 수정
$ sed -i 's/old/new/g' file.txt

# 백업 생성 후 수정
$ sed -i.bak 's/old/new/g' file.txt

# 특정 줄만 치환
$ sed '5s/old/new/' file.txt      # 5번째 줄
$ sed '1,10s/old/new/g' file.txt  # 1~10번째 줄

# 줄 삭제
$ sed '5d' file.txt               # 5번째 줄 삭제
$ sed '/pattern/d' file.txt       # 패턴 매칭 줄 삭제
$ sed '1,5d' file.txt             # 1~5번째 줄 삭제

# 줄 추가
$ sed '5a\New line' file.txt      # 5번째 줄 뒤에 추가
$ sed '5i\New line' file.txt      # 5번째 줄 앞에 추가

# awk - 텍스트 처리
# 특정 열 출력
$ awk '{print $1}' file.txt       # 첫 번째 필드
$ awk '{print $1, $3}' file.txt   # 1, 3번째 필드

# 조건부 출력
$ awk '$3 > 100 {print $1}' file.txt

# 합계 계산
$ awk '{sum += $1} END {print sum}' numbers.txt

# CSV 처리
$ awk -F',' '{print $2}' data.csv

# tr - 문자 변환
# 대소문자 변환
$ cat file.txt | tr 'a-z' 'A-Z'

# 문자 삭제
$ cat file.txt | tr -d '0-9'      # 숫자 삭제

# 압축 (연속 문자)
$ cat file.txt | tr -s ' '        # 연속 공백을 하나로
```

---

## 파일 압축 및 아카이브

### gzip / gunzip

```bash
# 압축 (원본 파일 삭제됨)
$ gzip file.txt
$ ls
file.txt.gz

# 압축 해제
$ gunzip file.txt.gz

# 원본 유지하며 압축
$ gzip -k file.txt

# 압축률 지정 (1-9, 기본 6)
$ gzip -9 file.txt  # 최대 압축

# 압축된 파일 내용 보기
$ zcat file.txt.gz
$ zless file.txt.gz
$ zgrep "pattern" file.txt.gz

# 여러 파일 압축
$ gzip file1.txt file2.txt file3.txt

# 재귀적 압축
$ gzip -r directory/
```

### bzip2 / bunzip2

```bash
# bzip2 압축 (gzip보다 높은 압축률)
$ bzip2 file.txt

# 압축 해제
$ bunzip2 file.txt.bz2

# 원본 유지
$ bzip2 -k file.txt

# 압축된 파일 보기
$ bzcat file.txt.bz2
$ bzless file.txt.bz2
$ bzgrep "pattern" file.txt.bz2
```

### xz / unxz

```bash
# xz 압축 (가장 높은 압축률)
$ xz file.txt

# 압축 해제
$ unxz file.txt.xz

# 원본 유지
$ xz -k file.txt

# 압축률 지정
$ xz -9 file.txt  # 최대 압축

# 압축된 파일 보기
$ xzcat file.txt.xz
$ xzless file.txt.xz
```

### tar (아카이브)

```bash
# 아카이브 생성
$ tar -cf archive.tar directory/

# 압축 아카이브 생성
$ tar -czf archive.tar.gz directory/    # gzip
$ tar -cjf archive.tar.bz2 directory/   # bzip2
$ tar -cJf archive.tar.xz directory/    # xz

# verbose 모드
$ tar -czvf archive.tar.gz directory/

# 아카이브 내용 확인
$ tar -tf archive.tar.gz

# 아카이브 압축 해제
$ tar -xzf archive.tar.gz

# 특정 디렉토리에 압축 해제
$ tar -xzf archive.tar.gz -C /destination/

# 특정 파일만 추출
$ tar -xzf archive.tar.gz file.txt

# 아카이브에 파일 추가
$ tar -rf archive.tar newfile.txt

# 특정 파일 제외
$ tar -czf backup.tar.gz --exclude='*.log' /home/user/

# 증분 백업
$ tar -czf full_backup.tar.gz -g snapshot.file /data/
$ tar -czf incremental.tar.gz -g snapshot.file /data/

# 아카이브 검증
$ tar -tzf archive.tar.gz > /dev/null && echo "OK" || echo "Corrupted"
```

### zip / unzip

```bash
# zip 아카이브 생성
$ zip archive.zip file1.txt file2.txt

# 디렉토리 압축
$ zip -r archive.zip directory/

# 암호화
$ zip -e secure.zip file.txt
Enter password:

# 압축 해제
$ unzip archive.zip

# 특정 디렉토리에 압축 해제
$ unzip archive.zip -d /destination/

# 내용 확인
$ unzip -l archive.zip

# 테스트
$ unzip -t archive.zip

# 특정 파일만 압축 해제
$ unzip archive.zip file.txt
```

---

## 링크 (하드링크와 심볼릭링크)

### 하드링크

```bash
# 하드링크 생성
$ ln original.txt hardlink.txt

# 확인
$ ls -li
123456 -rw-r--r-- 2 user user 1024 Nov 17 12:00 original.txt
123456 -rw-r--r-- 2 user user 1024 Nov 17 12:00 hardlink.txt
# 같은 inode 번호 (123456)

# 하드링크 개수 확인
$ stat original.txt
  File: original.txt
  Size: 1024       Links: 2
  Inode: 123456

# 한 파일 삭제해도 다른 파일은 유지
$ rm original.txt
$ cat hardlink.txt  # 여전히 접근 가능

# 하드링크의 제한
# - 같은 파일시스템 내에서만 가능
# - 디렉토리에는 생성 불가
```

### 심볼릭링크 (소프트링크)

```bash
# 심볼릭 링크 생성
$ ln -s /path/to/original.txt symlink.txt

# 확인
$ ls -l
lrwxrwxrwx 1 user user 24 Nov 17 12:00 symlink.txt -> /path/to/original.txt

# 절대 경로 vs 상대 경로
$ ln -s /home/user/file.txt absolute_link
$ ln -s ../file.txt relative_link

# 디렉토리 심볼릭 링크
$ ln -s /var/www/html webroot

# 링크 덮어쓰기
$ ln -sf new_target symlink.txt

# 링크 타겟 확인
$ readlink symlink.txt
/path/to/original.txt

# 실제 경로 확인
$ readlink -f symlink.txt
/home/user/path/to/original.txt

# 끊어진 링크 찾기
$ find /home -type l ! -exec test -e {} \; -print

# 원본 파일 삭제 시 링크는 끊어짐
$ rm original.txt
$ cat symlink.txt
cat: symlink.txt: No such file or directory

# 시스템 전체에서 많이 사용
$ ls -l /bin
lrwxrwxrwx 1 root root 7 /bin -> usr/bin
```

---

## 파일 시스템 검사 및 복구

### fsck (파일시스템 체크)

```bash
# 파일시스템 체크 (언마운트 상태에서!)
$ sudo fsck /dev/sdb1

# 자동 복구 시도
$ sudo fsck -y /dev/sdb1

# 체크만 (수정 안 함)
$ sudo fsck -n /dev/sdb1

# 강제 체크
$ sudo fsck -f /dev/sdb1

# ext4 전용
$ sudo fsck.ext4 /dev/sdb1

# 모든 파일시스템 체크
$ sudo fsck -A

# 진행 상황 표시
$ sudo fsck -C /dev/sdb1

# 대체 슈퍼블록 사용 (손상 시)
$ sudo fsck.ext4 -b 8193 /dev/sdb1
```

### e2fsck (ext 전용)

```bash
# 체크 및 복구
$ sudo e2fsck /dev/sdb1

# 강제 체크
$ sudo e2fsck -f /dev/sdb1

# 자동 복구
$ sudo e2fsck -p /dev/sdb1

# 대화형 복구
$ sudo e2fsck /dev/sdb1
/dev/sdb1: Inode 12345 has illegal block(s). Clear? yes

# 불량 블록 스캔
$ sudo e2fsck -c /dev/sdb1

# 철저한 불량 블록 스캔
$ sudo e2fsck -cc /dev/sdb1
```

### badblocks (불량 섹터 검사)

```bash
# 읽기 전용 테스트
$ sudo badblocks -v /dev/sdb1
Checking blocks 0 to 10485759
Checking for bad blocks (read-only test)

# 비파괴 읽기-쓰기 테스트
$ sudo badblocks -n -v /dev/sdb1

# 파괴적 쓰기 테스트 (주의!)
$ sudo badblocks -w -v /dev/sdb1

# 결과를 파일로 저장
$ sudo badblocks -v /dev/sdb1 > badblocks.txt

# fsck와 함께 사용
$ sudo e2fsck -l badblocks.txt /dev/sdb1
```

### 디스크 사용량 분석

```bash
# 파일시스템 사용량
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       465G  123G  320G  28% /
/dev/sda1       511M  5.3M  506M   2% /boot/efi

# inode 사용량
$ df -i
Filesystem      Inodes  IUsed   IFree IUse% Mounted on
/dev/sda2      30597120 234567 30362553    1% /

# 디렉토리 크기
$ du -h /home/user/
123M    /home/user/Documents
456M    /home/user/Downloads
789M    /home/user/

# 요약
$ du -sh /home/user/
789M    /home/user/

# 깊이 제한
$ du -h --max-depth=1 /var/

# 크기 순 정렬
$ du -h /var/ | sort -hr | head -10

# 특정 타입 제외
$ du -h --exclude='*.log' /var/

# ncdu - 대화형 디스크 사용량 분석
$ sudo apt install ncdu
$ ncdu /home
```

---

## 실전 예제

### 예제 1: 로그 파일 관리

```bash
# 30일 이상 된 로그 파일 압축
$ find /var/log -name "*.log" -mtime +30 -exec gzip {} \;

# 압축된 로그 파일 검색
$ zgrep "ERROR" /var/log/syslog.*.gz

# 로그 순환 (로그 파일이 커지는 것 방지)
$ cat > /etc/logrotate.d/myapp <<EOF
/var/log/myapp/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

### 예제 2: 백업 스크립트

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d)

# 전체 백업
tar -czf "$BACKUP_DIR/home_$DATE.tar.gz" /home/

# 오래된 백업 삭제 (30일 이상)
find "$BACKUP_DIR" -name "home_*.tar.gz" -mtime +30 -delete

# 백업 검증
if tar -tzf "$BACKUP_DIR/home_$DATE.tar.gz" > /dev/null; then
    echo "Backup successful: $DATE"
else
    echo "Backup failed: $DATE"
fi
```

### 예제 3: 중복 파일 찾기

```bash
# fdupes 사용
$ sudo apt install fdupes

# 중복 파일 찾기
$ fdupes -r /home/user/

# 중복 파일 삭제 (대화형)
$ fdupes -rd /home/user/

# 크기가 같은 파일 찾기 (수동)
$ find /home -type f -exec md5sum {} + | sort | uniq -w32 -D
```

---

## 요약

파일시스템 작업의 핵심:

1. **기본 작업**: cp, mv, rm, mkdir
2. **검색**: find, locate, which
3. **압축**: gzip, bzip2, xz, tar, zip
4. **링크**: 하드링크 (동일 파일), 심볼릭링크 (참조)
5. **검사**: fsck, e2fsck, badblocks

안전한 작업을 위해 항상 백업을 유지하고, 중요한 작업 전에는 테스트를 수행하세요.

---

[다음: 마운팅 및 언마운팅 →](mounting.md)

[← 파일시스템 타입으로 돌아가기](types.md)

[← 목차로 돌아가기](../README.md)

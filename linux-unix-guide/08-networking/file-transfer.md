# 파일 전송

## 목차
- [SCP](#scp)
- [rsync](#rsync)
- [SFTP](#sftp)
- [wget](#wget)
- [curl](#curl)
- [FTP/FTPS](#ftpftps)
- [실전 예제](#실전-예제)

---

## SCP

### 기본 사용법

```bash
# 로컬 → 원격
$ scp file.txt user@host:/path/to/destination/
$ scp /local/file.txt user@192.168.1.100:/remote/path/

# 원격 → 로컬
$ scp user@host:/path/to/file.txt /local/destination/
$ scp user@192.168.1.100:/remote/file.txt ./

# 현재 디렉토리로
$ scp user@host:/path/to/file.txt .

# 파일명 변경하며 복사
$ scp user@host:/remote/old.txt /local/new.txt

# 여러 파일
$ scp file1.txt file2.txt file3.txt user@host:/destination/
$ scp *.txt user@host:/destination/
$ scp {file1,file2,file3}.txt user@host:/destination/

# 디렉토리 복사 (재귀)
$ scp -r directory/ user@host:/destination/
$ scp -r user@host:/remote/dir/ /local/destination/

# 권한 및 타임스탬프 보존
$ scp -p file.txt user@host:/destination/
$ scp -rp directory/ user@host:/destination/
```

### SCP 옵션

```bash
# 포트 지정
$ scp -P 2222 file.txt user@host:/destination/
$ scp -P 2222 user@host:/file.txt ./

# 대역폭 제한 (KB/s)
$ scp -l 1000 largefile.iso user@host:/destination/
$ scp -l 500 user@host:/largefile.iso ./

# 압축 전송
$ scp -C file.txt user@host:/destination/
$ scp -C user@host:/largefile.tar ./

# Verbose (상세 정보)
$ scp -v file.txt user@host:/destination/

# Quiet (출력 숨기기)
$ scp -q file.txt user@host:/destination/

# SSH 설정 파일 지정
$ scp -F ~/.ssh/custom_config file.txt user@host:/destination/

# SSH 키 지정
$ scp -i ~/.ssh/custom_key file.txt user@host:/destination/

# 암호화 알고리즘 지정
$ scp -c aes128-ctr file.txt user@host:/destination/
$ scp -c blowfish file.txt user@host:/destination/

# IPv4/IPv6 강제
$ scp -4 file.txt user@host:/destination/
$ scp -6 file.txt user@host:/destination/

# 조합
$ scp -P 2222 -i ~/.ssh/key -C -l 1000 file.txt user@host:/destination/
```

### 고급 사용

```bash
# 원격 → 원격 (현재 호스트를 통해)
$ scp user1@host1:/file.txt user2@host2:/destination/

# 와일드카드 사용 (따옴표 필요)
$ scp 'user@host:/path/*.txt' /local/destination/
$ scp user@host:'/path/{file1,file2,file3}.txt' ./

# 프록시 점프를 통한 전송
$ scp -o ProxyJump=bastion user@internal:/file.txt ./

# 진행 상황 표시 (rsync 사용 권장)
$ rsync --progress -avz -e ssh file.txt user@host:/destination/

# 백그라운드 전송
$ nohup scp large_file.iso user@host:/destination/ &

# 전송 재개는 불가 (rsync 사용 권장)
```

---

## rsync

### 기본 사용법

```bash
# 로컬 → 원격
$ rsync file.txt user@host:/destination/
$ rsync -avz source/ user@host:/destination/

# 원격 → 로컬
$ rsync user@host:/source/ /local/destination/
$ rsync -avz user@host:/source/ /local/destination/

# 주요 옵션:
# -a: archive (권한, 타임스탬프, 심볼릭 링크 보존)
# -v: verbose
# -z: 압축
# -h: 사람이 읽기 쉬운 형식

# 디렉토리 동기화
$ rsync -avz source/ user@host:/destination/
# 주의: source/와 source는 다름!
# source/  : source 내용물을 destination으로
# source   : source 자체를 destination으로
```

### rsync 주요 옵션

```bash
# 진행 상황 표시
$ rsync -avzP source/ user@host:/destination/
$ rsync -avz --progress source/ user@host:/destination/

# 부분 전송 보존 (중단된 전송 재개)
$ rsync -avzP source/ user@host:/destination/
$ rsync -avz --partial --progress source/ user@host:/destination/

# 삭제 동기화 (목적지에서 소스에 없는 파일 삭제)
$ rsync -avz --delete source/ user@host:/destination/

# Dry run (실제로 수행하지 않고 확인)
$ rsync -avzn source/ user@host:/destination/
$ rsync -avz --dry-run source/ user@host:/destination/

# 통계 정보
$ rsync -avz --stats source/ user@host:/destination/

# 대역폭 제한 (KB/s)
$ rsync -avz --bwlimit=1000 source/ user@host:/destination/

# 기존 파일만 업데이트
$ rsync -avz --existing source/ user@host:/destination/

# 새 파일만 복사
$ rsync -avz --ignore-existing source/ user@host:/destination/

# 파일 크기만 비교
$ rsync -avz --size-only source/ user@host:/destination/

# 체크섬으로 비교
$ rsync -avzc source/ user@host:/destination/

# 심볼릭 링크 보존
$ rsync -avzl source/ user@host:/destination/

# 하드 링크 보존
$ rsync -avzH source/ user@host:/destination/

# 권한 보존 안 함
$ rsync -rltvz source/ user@host:/destination/

# 소유자/그룹 보존
$ rsync -avz --chown=user:group source/ user@host:/destination/
```

### 필터링

```bash
# 특정 파일/디렉토리 제외
$ rsync -avz --exclude='*.log' source/ user@host:/destination/
$ rsync -avz --exclude='temp/' source/ user@host:/destination/

# 여러 패턴 제외
$ rsync -avz --exclude='*.log' --exclude='*.tmp' --exclude='cache/' \
    source/ user@host:/destination/

# 파일에서 제외 패턴 읽기
$ rsync -avz --exclude-from='exclude.txt' source/ user@host:/destination/

# exclude.txt 예:
*.log
*.tmp
.git/
node_modules/
__pycache__/

# 특정 파일만 포함
$ rsync -avz --include='*.txt' --exclude='*' source/ user@host:/destination/

# 복잡한 필터
$ rsync -avz \
    --include='*.php' \
    --include='*.html' \
    --include='*/' \
    --exclude='*' \
    source/ user@host:/destination/
```

### SSH 옵션

```bash
# 포트 지정
$ rsync -avz -e "ssh -p 2222" source/ user@host:/destination/

# SSH 키 지정
$ rsync -avz -e "ssh -i ~/.ssh/custom_key" source/ user@host:/destination/

# SSH 옵션 조합
$ rsync -avz -e "ssh -p 2222 -i ~/.ssh/key -o StrictHostKeyChecking=no" \
    source/ user@host:/destination/

# 압축 레벨 조정
$ rsync -avz -e "ssh -C" source/ user@host:/destination/

# ProxyJump 사용
$ rsync -avz -e "ssh -J bastion" source/ user@internal:/destination/
```

### 백업 용도

```bash
# 백업 (변경된 파일은 .bak으로)
$ rsync -avz --backup --suffix=.bak source/ /backup/

# 타임스탬프 접미사
$ rsync -avz --backup --suffix=.$(date +%Y%m%d) source/ /backup/

# 백업 디렉토리 지정
$ rsync -avz --backup --backup-dir=/backup/old source/ /backup/current/

# 증분 백업 (Hard link)
$ rsync -avz --link-dest=/backup/previous source/ /backup/current/

# 스냅샷 백업 스크립트
#!/bin/bash
DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/backup"
LATEST="$BACKUP_DIR/latest"
NEW="$BACKUP_DIR/$DATE"

rsync -avz --delete --link-dest="$LATEST" source/ "$NEW/"
rm -f "$LATEST"
ln -s "$DATE" "$LATEST"
```

### 실시간 동기화

```bash
# inotify-tools 사용
$ sudo apt install inotify-tools

# 실시간 감시 스크립트
#!/bin/bash
SOURCE="/path/to/source/"
DEST="user@host:/destination/"

while inotifywait -r -e modify,create,delete,move "$SOURCE"; do
    rsync -avz --delete "$SOURCE" "$DEST"
done

# lsyncd 사용 (더 효율적)
$ sudo apt install lsyncd

# /etc/lsyncd/lsyncd.conf.lua
settings {
    logfile = "/var/log/lsyncd/lsyncd.log",
    statusFile = "/var/log/lsyncd/lsyncd.status"
}

sync {
    default.rsync,
    source = "/path/to/source/",
    target = "user@host:/destination/",
    rsync = {
        archive = true,
        compress = true
    }
}
```

---

## SFTP

### 대화형 SFTP

```bash
# 연결
$ sftp user@hostname
$ sftp -P 2222 user@hostname

sftp> help
Available commands:
bye                                Quit sftp
cd path                            Change remote directory to 'path'
chgrp grp path                     Change group of file 'path' to 'grp'
chmod mode path                    Change permissions of file 'path' to 'mode'
chown own path                     Change owner of file 'path' to 'own'
df [-hi] [path]                    Display statistics for current directory or
                                   filesystem containing 'path'
exit                               Quit sftp
get [-afPpRr] remote [local]       Download file
reget [-fPpRr] remote [local]      Resume download file
help                               Display this help text
lcd path                           Change local directory to 'path'
lls [ls-options [path]]            Display local directory listing
lmkdir path                        Create local directory
ln [-s] oldpath newpath            Link remote file (-s for symlink)
lpwd                               Print local working directory
ls [-1afhlnrSt] [path]             Display remote directory listing
lumask umask                       Set local umask to 'umask'
mkdir path                         Create remote directory
progress                           Toggle display of progress meter
put [-afPpRr] local [remote]       Upload file
pwd                                Display remote working directory
quit                               Quit sftp
reput [-fPpRr] local [remote]      Resume upload file
rename oldpath newpath             Rename remote file
rm path                            Delete remote file
rmdir path                         Remove remote directory
symlink oldpath newpath            Symlink remote file
version                            Show SFTP version
!command                           Execute 'command' in local shell
!                                  Escape to local shell
?                                  Synonym for help

# 파일 다운로드
sftp> get remote_file.txt
sftp> get remote_file.txt local_file.txt

# 여러 파일 다운로드
sftp> mget *.txt
sftp> mget file1.txt file2.txt file3.txt

# 디렉토리 다운로드
sftp> get -r remote_directory

# 파일 업로드
sftp> put local_file.txt
sftp> put local_file.txt remote_file.txt

# 여러 파일 업로드
sftp> mput *.txt
sftp> mput file1.txt file2.txt file3.txt

# 디렉토리 업로드
sftp> put -r local_directory

# 진행 상황 토글
sftp> progress

# 디렉토리 작업
sftp> ls
sftp> ls -la
sftp> cd /remote/path
sftp> pwd
sftp> mkdir newdir
sftp> rmdir olddir

# 파일 작업
sftp> rm file.txt
sftp> rename old.txt new.txt
sftp> chmod 644 file.txt
sftp> chown 1000 file.txt

# 로컬 작업
sftp> lls
sftp> lcd /local/path
sftp> lpwd
sftp> lmkdir newdir
sftp> !ls -la

# 종료
sftp> bye
sftp> exit
sftp> quit
```

### 배치 SFTP

```bash
# 배치 파일 사용
$ sftp -b batch.txt user@host

# batch.txt:
cd /remote/directory
get file1.txt
get file2.txt
mget *.log
put local_file.txt
put -r local_directory
bye

# 표준 입력으로
$ echo "get /remote/file.txt" | sftp user@host

# 여러 명령
$ cat <<EOF | sftp user@host
cd /remote/path
get file1.txt
get file2.txt
bye
EOF

# 스크립트에서
#!/bin/bash
sftp user@host <<EOF
cd /uploads
put file1.txt
put file2.txt
chmod 644 file1.txt
chmod 644 file2.txt
bye
EOF
```

### SFTP 옵션

```bash
# 포트 지정
$ sftp -P 2222 user@host

# 대역폭 제한 (KB/s)
$ sftp -l 1000 user@host

# SSH 옵션
$ sftp -o "Port=2222" user@host
$ sftp -o "IdentityFile=~/.ssh/key" user@host

# 버퍼 크기
$ sftp -B 32768 user@host

# Verbose
$ sftp -v user@host

# 조합
$ sftp -P 2222 -o "IdentityFile=~/.ssh/key" -l 1000 user@host
```

---

## wget

### 기본 사용법

```bash
# 파일 다운로드
$ wget http://example.com/file.iso
$ wget https://example.com/archive.tar.gz

# 다른 이름으로 저장
$ wget -O filename.zip http://example.com/download.zip

# 표준 출력으로
$ wget -O - http://example.com/file.txt

# 디렉토리 지정
$ wget -P /path/to/directory http://example.com/file.iso

# 재개 (이어받기)
$ wget -c http://example.com/large_file.iso

# 백그라운드
$ wget -b http://example.com/file.iso
# 로그: wget-log

# Quiet
$ wget -q http://example.com/file.txt

# Verbose
$ wget -v http://example.com/file.txt

# 진행 표시 유형
$ wget --progress=bar http://example.com/file.iso
$ wget --progress=dot http://example.com/file.iso
```

### 여러 파일 다운로드

```bash
# 파일 목록에서
$ wget -i urls.txt

# urls.txt:
http://example.com/file1.zip
http://example.com/file2.tar.gz
http://example.com/file3.iso

# 와일드카드 (FTP)
$ wget ftp://ftp.example.com/pub/*.iso

# 재귀 다운로드
$ wget -r http://example.com/directory/
$ wget -r -np http://example.com/directory/  # 상위 안 올라감
$ wget -r -l 2 http://example.com/  # 깊이 2까지

# 전체 웹사이트 미러링
$ wget --mirror http://example.com/
$ wget -m -k -p -E http://example.com/
# -m: mirror
# -k: convert links
# -p: 페이지 필수 파일들
# -E: HTML 확장자 조정
```

### 인증 및 헤더

```bash
# HTTP 인증
$ wget --user=username --password=password http://example.com/file.zip
$ wget --http-user=username --http-password=password http://example.com/file.zip

# FTP 인증
$ wget --ftp-user=username --ftp-password=password ftp://ftp.example.com/file.tar

# 헤더 추가
$ wget --header="Authorization: Bearer TOKEN" http://api.example.com/data

# User-Agent 변경
$ wget --user-agent="Mozilla/5.0" http://example.com/file.zip

# Referer 설정
$ wget --referer="http://example.com/" http://example.com/protected.zip

# 쿠키
$ wget --load-cookies=cookies.txt http://example.com/file.zip
$ wget --save-cookies=cookies.txt http://example.com/file.zip
```

### 속도 및 재시도

```bash
# 속도 제한 (KB/s)
$ wget --limit-rate=500k http://example.com/file.iso

# 재시도 횟수
$ wget --tries=10 http://example.com/file.iso
$ wget -t 10 http://example.com/file.iso

# 무한 재시도
$ wget -t 0 http://example.com/file.iso

# 타임아웃
$ wget --timeout=30 http://example.com/file.iso
$ wget --dns-timeout=10 --connect-timeout=10 --read-timeout=30 http://example.com/file.iso

# 대기 시간
$ wget --wait=2 -i urls.txt  # 파일 간 2초 대기
$ wget --random-wait -i urls.txt  # 랜덤 대기
```

### 필터링

```bash
# 특정 파일 타입만
$ wget -r -A "*.pdf" http://example.com/

# 제외
$ wget -r -R "*.gif,*.png" http://example.com/

# 도메인 제한
$ wget -r -D example.com http://example.com/

# 특정 디렉토리 제외
$ wget -r -X /cgi-bin,/tmp http://example.com/
```

---

## curl

### 기본 다운로드

```bash
# 파일 다운로드 (원격 파일명 사용)
$ curl -O http://example.com/file.zip

# 다른 이름으로 저장
$ curl -o filename.zip http://example.com/download.zip

# 여러 파일
$ curl -O http://example.com/file1.zip -O http://example.com/file2.tar.gz

# 진행 표시
$ curl -# -O http://example.com/file.iso

# 재개
$ curl -C - -O http://example.com/large_file.iso

# 리다이렉트 따라가기
$ curl -L -O http://example.com/file.zip

# Verbose
$ curl -v -O http://example.com/file.zip

# Silent
$ curl -s -O http://example.com/file.zip
```

### HTTP 요청

```bash
# GET
$ curl http://api.example.com/users
$ curl -X GET http://api.example.com/users

# POST
$ curl -X POST -d "key1=value1&key2=value2" http://example.com/api
$ curl -X POST -d @data.txt http://example.com/api

# JSON POST
$ curl -X POST -H "Content-Type: application/json" \
    -d '{"key":"value"}' http://example.com/api

# PUT
$ curl -X PUT -d "data" http://example.com/api/resource/1

# DELETE
$ curl -X DELETE http://example.com/api/resource/1

# 파일 업로드
$ curl -F "file=@/path/to/file.pdf" http://example.com/upload
$ curl -F "file=@document.pdf" -F "title=Document" http://example.com/upload
```

### 헤더 및 인증

```bash
# 헤더 추가
$ curl -H "Authorization: Bearer TOKEN" http://api.example.com/data
$ curl -H "Content-Type: application/json" -H "Accept: application/json" \
    http://api.example.com/

# 헤더 보기
$ curl -I http://example.com/
$ curl --head http://example.com/

# HTTP 인증
$ curl -u username:password http://example.com/protected
$ curl --user username:password http://example.com/protected

# Bearer 토큰
$ curl -H "Authorization: Bearer YOUR_TOKEN" http://api.example.com/

# 쿠키
$ curl -b cookies.txt http://example.com/
$ curl -c cookies.txt http://example.com/
$ curl -b "name=value" http://example.com/

# User-Agent
$ curl -A "Mozilla/5.0" http://example.com/
$ curl --user-agent "Custom Agent" http://example.com/

# Referer
$ curl -e "http://google.com" http://example.com/
$ curl --referer "http://google.com" http://example.com/
```

### 성능 측정

```bash
# 응답 시간
$ curl -w "@-" -o /dev/null -s http://example.com/ <<'EOF'
    time_namelookup:  %{time_namelookup}s\n
       time_connect:  %{time_connect}s\n
    time_appconnect:  %{time_appconnect}s\n
   time_pretransfer:  %{time_pretransfer}s\n
      time_redirect:  %{time_redirect}s\n
 time_starttransfer:  %{time_starttransfer}s\n
                    ----------\n
         time_total:  %{time_total}s\n

# HTTP 상태 코드
$ curl -o /dev/null -s -w "%{http_code}\n" http://example.com/

# 다운로드 속도
$ curl -o /dev/null -w "Speed: %{speed_download} bytes/sec\n" http://example.com/file.zip

# 속도 제한
$ curl --limit-rate 100K -O http://example.com/file.iso
```

---

## FTP/FTPS

### FTP 클라이언트

```bash
# ftp 명령어
$ ftp ftp.example.com

ftp> open ftp.example.com
ftp> user username
Password: ****
ftp> ls
ftp> cd directory
ftp> get file.txt
ftp> mget *.txt
ftp> put local_file.txt
ftp> mput *.txt
ftp> binary  # 바이너리 모드
ftp> ascii   # ASCII 모드
ftp> bye

# lftp (더 강력)
$ sudo apt install lftp

$ lftp ftp://username:password@ftp.example.com
lftp> ls
lftp> get file.txt
lftp> mirror  # 미러링
lftp> mirror -R  # 역방향 미러링
lftp> bye
```

---

## 실전 예제

### 예제 1: 대용량 파일 안전 전송

```bash
#!/bin/bash
# safe_transfer.sh

SOURCE=$1
DEST=$2

# 체크섬 계산
CHECKSUM=$(md5sum "$SOURCE" | awk '{print $1}')

# 전송
rsync -avzP --partial "$SOURCE" "$DEST"

# 검증
REMOTE_CHECKSUM=$(ssh user@host "md5sum $DEST" | awk '{print $1}')

if [ "$CHECKSUM" == "$REMOTE_CHECKSUM" ]; then
    echo "Transfer successful"
else
    echo "Transfer failed - checksum mismatch"
    exit 1
fi
```

### 예제 2: 백업 스크립트

```bash
#!/bin/bash
# backup.sh

BACKUP_SRC="/data"
BACKUP_DEST="user@backup-server:/backups/$(hostname)"
LOG_FILE="/var/log/backup.log"

echo "$(date): Starting backup" >> "$LOG_FILE"

rsync -avz --delete \
    --exclude='*.tmp' \
    --exclude='cache/' \
    --log-file="$LOG_FILE" \
    "$BACKUP_SRC/" "$BACKUP_DEST/"

echo "$(date): Backup completed" >> "$LOG_FILE"
```

---

## 요약

파일 전송 도구:

1. **scp**: 단순 파일 복사
2. **rsync**: 동기화, 증분 백업
3. **sftp**: 대화형 파일 전송
4. **wget**: 웹에서 다운로드
5. **curl**: HTTP API, 다양한 프로토콜

---

[다음: 방화벽 →](firewall.md)

[← SSH로 돌아가기](ssh.md)

[← 목차로 돌아가기](../README.md)

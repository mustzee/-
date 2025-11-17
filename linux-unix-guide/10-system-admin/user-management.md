# 사용자 관리

## 목차
- [소개](#소개)
- [사용자 계정 관리](#사용자-계정-관리)
- [그룹 관리](#그룹-관리)
- [패스워드 정책](#패스워드-정책)
- [사용자 정보 조회](#사용자-정보-조회)
- [권한 및 sudo](#권한-및-sudo)
- [사용자 환경](#사용자-환경)
- [계정 보안](#계정-보안)
- [배치 작업](#배치-작업)
- [감사 및 모니터링](#감사-및-모니터링)
- [실전 예제](#실전-예제)

---

## 소개

Linux에서 사용자 및 그룹 관리는 시스템 보안과 리소스 관리의 핵심입니다.

### 사용자 유형

```bash
# 1. 루트 사용자 (UID 0)
# - 시스템의 모든 권한 보유
# - 시스템 관리 작업 수행

# 2. 시스템 사용자 (UID 1-999 또는 1-499)
# - 서비스 및 데몬 실행용
# - 로그인 불가능

# 3. 일반 사용자 (UID 1000+)
# - 실제 사용자 계정
# - 제한된 권한

# 현재 사용자 확인
$ whoami
user

$ id
uid=1000(user) gid=1000(user) groups=1000(user),27(sudo),998(wheel)

# 모든 사용자 목록
$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
user:x:1000:1000:User Name:/home/user:/bin/bash

# 형식: username:password:UID:GID:comment:home:shell

# 그룹 목록
$ cat /etc/group
root:x:0:
sudo:x:27:user
users:x:100:

# 형식: groupname:password:GID:members
```

---

## 사용자 계정 관리

### 사용자 추가

```bash
# useradd - 기본 명령어
$ sudo useradd john
# 최소한의 설정만 생성

# 홈 디렉토리 포함
$ sudo useradd -m john

# 쉘 지정
$ sudo useradd -m -s /bin/bash john

# 그룹 지정
$ sudo useradd -m -g users -G sudo,docker john
# -g: 기본 그룹
# -G: 추가 그룹들

# UID 지정
$ sudo useradd -m -u 1500 john

# 코멘트 추가
$ sudo useradd -m -c "John Doe" john

# 홈 디렉토리 경로 지정
$ sudo useradd -m -d /custom/home/john john

# 만료일 설정
$ sudo useradd -m -e 2025-12-31 john

# 완전한 예제
$ sudo useradd -m -s /bin/bash -c "John Doe" \
    -g users -G sudo,docker john

# adduser - 대화형 (Debian/Ubuntu)
$ sudo adduser john
Adding user `john' ...
Adding new group `john' (1001) ...
Adding new user `john' (1001) with group `john' ...
Creating home directory `/home/john' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
Full Name []: John Doe
Room Number []:
Work Phone []:
Home Phone []:
Other []:

# 시스템 사용자 생성
$ sudo useradd -r -s /usr/sbin/nologin service_user
# -r: 시스템 사용자
```

### 사용자 수정

```bash
# usermod - 사용자 속성 수정

# 그룹 추가
$ sudo usermod -aG sudo john
$ sudo usermod -aG docker,www-data john
# -a: append (기존 그룹 유지)
# 주의: -a 없이 -G 사용 시 기존 그룹에서 제거됨

# 기본 쉘 변경
$ sudo usermod -s /bin/zsh john

# 홈 디렉토리 변경
$ sudo usermod -d /new/home john
$ sudo usermod -d /new/home -m john  # 파일도 이동

# 사용자 이름 변경
$ sudo usermod -l newname oldname

# UID 변경
$ sudo usermod -u 2000 john

# 계정 잠금
$ sudo usermod -L john
$ sudo usermod --lock john

# 계정 잠금 해제
$ sudo usermod -U john
$ sudo usermod --unlock john

# 만료일 설정
$ sudo usermod -e 2025-12-31 john

# 만료일 해제
$ sudo usermod -e "" john

# 코멘트 변경
$ sudo usermod -c "John Smith" john
```

### 사용자 삭제

```bash
# userdel - 사용자 삭제

# 기본 삭제 (홈 디렉토리 유지)
$ sudo userdel john

# 홈 디렉토리도 삭제
$ sudo userdel -r john

# 강제 삭제 (로그인 중이어도)
$ sudo userdel -f john

# 완전 삭제
$ sudo userdel -r john
$ sudo rm -rf /var/mail/john  # 메일함 삭제
$ sudo rm -rf /var/spool/cron/john  # cron 작업 삭제

# deluser (Debian/Ubuntu)
$ sudo deluser john
$ sudo deluser --remove-home john
$ sudo deluser --remove-all-files john
```

### 패스워드 설정

```bash
# passwd - 패스워드 변경

# 자신의 패스워드 변경
$ passwd
Changing password for user.
Current password:
New password:
Retype new password:

# 다른 사용자 패스워드 변경 (root)
$ sudo passwd john

# 패스워드 잠금
$ sudo passwd -l john

# 패스워드 잠금 해제
$ sudo passwd -u john

# 패스워드 삭제 (위험!)
$ sudo passwd -d john

# 패스워드 만료
$ sudo passwd -e john
# 다음 로그인 시 패스워드 변경 강제

# 패스워드 정보 확인
$ sudo passwd -S john
john P 11/17/2024 0 99999 7 -1
# P: 사용 가능, L: 잠김, NP: 패스워드 없음

# 파이프로 패스워드 설정 (스크립트용)
$ echo "newpassword" | sudo passwd --stdin john  # Red Hat
$ echo "john:newpassword" | sudo chpasswd  # 모든 배포판

# 여러 사용자 패스워드 변경
$ cat passwords.txt
user1:pass1
user2:pass2
user3:pass3

$ sudo chpasswd < passwords.txt
```

---

## 그룹 관리

### 그룹 생성 및 삭제

```bash
# groupadd - 그룹 생성
$ sudo groupadd developers

# GID 지정
$ sudo groupadd -g 5000 developers

# 시스템 그룹
$ sudo groupadd -r sysgroup

# groupdel - 그룹 삭제
$ sudo groupdel developers

# addgroup (Debian/Ubuntu)
$ sudo addgroup developers
$ sudo addgroup --gid 5000 developers
```

### 그룹 수정

```bash
# groupmod - 그룹 수정

# 그룹 이름 변경
$ sudo groupmod -n newname oldname

# GID 변경
$ sudo groupmod -g 5001 developers
```

### 그룹 멤버 관리

```bash
# 사용자를 그룹에 추가
$ sudo usermod -aG developers john
$ sudo gpasswd -a john developers

# 여러 그룹에 추가
$ sudo usermod -aG developers,docker,sudo john

# 사용자를 그룹에서 제거
$ sudo gpasswd -d john developers
$ sudo deluser john developers  # Debian/Ubuntu

# 그룹 관리자 지정
$ sudo gpasswd -A admin developers

# 그룹 멤버 확인
$ getent group developers
developers:x:5000:john,jane,bob

$ groups john
john : john sudo developers docker

# 사용자의 모든 그룹
$ id john
uid=1001(john) gid=1001(john) groups=1001(john),27(sudo),5000(developers)

# 특정 그룹의 모든 멤버
$ getent group sudo
$ grep sudo /etc/group
```

### 기본 그룹 변경

```bash
# 사용자의 기본 그룹 변경
$ sudo usermod -g developers john

# 임시로 그룹 변경
$ newgrp developers
$ id
uid=1000(user) gid=5000(developers) ...

# 원래 그룹으로 복귀
$ exit
```

---

## 패스워드 정책

### chage - 패스워드 에이징

```bash
# 패스워드 정책 확인
$ sudo chage -l john
Last password change                    : Nov 17, 2024
Password expires                        : never
Password inactive                       : never
Account expires                         : never
Minimum number of days between password change : 0
Maximum number of days between password change : 99999
Number of days of warning before password expires : 7

# 패스워드 최대 사용 기간 (일)
$ sudo chage -M 90 john  # 90일마다 변경

# 패스워드 최소 사용 기간
$ sudo chage -m 7 john  # 변경 후 7일은 재변경 불가

# 경고 기간
$ sudo chage -W 14 john  # 만료 14일 전부터 경고

# 비활성 기간
$ sudo chage -I 30 john  # 만료 후 30일 유예

# 계정 만료일
$ sudo chage -E 2025-12-31 john
$ sudo chage -E -1 john  # 만료일 해제

# 대화형 설정
$ sudo chage john

# 다음 로그인 시 패스워드 변경 강제
$ sudo chage -d 0 john
```

### 패스워드 품질 설정

```bash
# PAM 설정 (Debian/Ubuntu)
$ sudo vi /etc/pam.d/common-password

# pam_pwquality.so 사용
password requisite pam_pwquality.so retry=3 \
    minlen=12 \
    dcredit=-1 \
    ucredit=-1 \
    ocredit=-1 \
    lcredit=-1

# minlen: 최소 길이
# dcredit: 숫자 필수 (-1)
# ucredit: 대문자 필수
# ocredit: 특수문자 필수
# lcredit: 소문자 필수

# pwquality 설정 파일
$ sudo vi /etc/security/pwquality.conf
minlen = 12
dcredit = -1
ucredit = -1
ocredit = -1
lcredit = -1
difok = 3
maxrepeat = 3
usercheck = 1
enforcing = 1

# Red Hat/Fedora
$ sudo authconfig --passminlen=12 --update
```

### login.defs 설정

```bash
# /etc/login.defs 편집
$ sudo vi /etc/login.defs

# 패스워드 에이징
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_WARN_AGE   14

# UID/GID 범위
UID_MIN         1000
UID_MAX         60000
SYS_UID_MIN     100
SYS_UID_MAX     999

GID_MIN         1000
GID_MAX         60000
SYS_GID_MIN     100
SYS_GID_MAX     999

# 홈 디렉토리 생성
CREATE_HOME     yes

# umask
UMASK           077

# 암호화 방식
ENCRYPT_METHOD SHA512
```

---

## 사용자 정보 조회

### 사용자 목록 및 상태

```bash
# 로그인한 사용자
$ who
user     tty1         2024-11-17 09:00
admin    pts/0        2024-11-17 10:30 (192.168.1.100)

$ w
 10:45:37 up 2 days,  3:21,  2 users,  load average: 0.15, 0.20, 0.18
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
user     tty1     -                09:00    1:45m  0.05s  0.05s -bash
admin    pts/0    192.168.1.100    10:30    0.00s  0.12s  0.01s w

# 최근 로그인
$ last
user     pts/0        192.168.1.100    Mon Nov 17 10:00 - 11:00  (01:00)
admin    tty1         -                Mon Nov 17 09:00   still logged in

# 최근 로그인 (요약)
$ last -10  # 최근 10개
$ last user  # 특정 사용자
$ last reboot  # 재부팅 기록

# 실패한 로그인 시도
$ sudo lastb
$ sudo lastb | head -20

# 마지막 로그인
$ lastlog
Username         Port     From             Latest
root             pts/0                     Mon Nov 17 08:00:00 +0900 2024
user             pts/1    192.168.1.100    Mon Nov 17 10:00:00 +0900 2024

# 특정 사용자
$ lastlog -u john

# 현재 사용자 정보
$ id
$ id john
$ groups
$ groups john
```

### 사용자 계정 정보

```bash
# /etc/passwd 조회
$ getent passwd john
john:x:1001:1001:John Doe:/home/john:/bin/bash

# 모든 일반 사용자
$ getent passwd | awk -F: '$3 >= 1000 {print $1}'

# /etc/shadow 조회 (root만)
$ sudo getent shadow john
john:$6$random...:19320:0:99999:7:::

# /etc/group 조회
$ getent group developers

# 홈 디렉토리 확인
$ eval echo ~john
/home/john

# 사용자 프로세스
$ ps -u john
$ pgrep -u john
```

### 디스크 사용량

```bash
# 사용자별 디스크 사용량
$ sudo du -sh /home/*
1.2G    /home/john
856M    /home/jane
2.1G    /home/bob

# 상세 정보
$ sudo du -h --max-depth=1 /home/john | sort -h

# quota 설정 (quota 패키지 필요)
$ sudo apt install quota

# 파일시스템에 quota 활성화
$ sudo vi /etc/fstab
/dev/sda1 /home ext4 defaults,usrquota,grpquota 0 2

$ sudo mount -o remount /home
$ sudo quotacheck -cum /home
$ sudo quotaon /home

# 사용자 quota 설정
$ sudo edquota -u john
Disk quotas for user john (uid 1001):
  Filesystem    blocks   soft   hard  inodes  soft  hard
  /dev/sda1      10000  50000  60000     100  5000  6000

# quota 확인
$ quota -u john
$ sudo repquota /home
```

---

## 권한 및 sudo

### sudo 설정

```bash
# sudo 그룹에 추가
$ sudo usermod -aG sudo john  # Debian/Ubuntu
$ sudo usermod -aG wheel john  # Red Hat/Fedora

# sudoers 파일 편집 (안전)
$ sudo visudo

# 특정 사용자에게 모든 권한
john    ALL=(ALL:ALL) ALL

# 패스워드 없이
john    ALL=(ALL) NOPASSWD: ALL

# 특정 명령만 허용
john    ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx

# 여러 명령
john    ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/journalctl

# 그룹에 권한
%developers    ALL=(ALL:ALL) ALL

# 특정 호스트에서만
john    webserver=(ALL) ALL

# 별칭 사용
# Command Aliases
Cmnd_Alias SERVICES = /usr/bin/systemctl, /usr/sbin/service
Cmnd_Alias NETWORKING = /sbin/ifconfig, /sbin/route

# User Aliases
User_Alias ADMINS = john, jane, bob

# 적용
ADMINS    ALL=(ALL) SERVICES, NETWORKING

# sudoers.d 사용 (권장)
$ sudo vi /etc/sudoers.d/developers
%developers ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx

# 권한 확인
$ sudo chmod 0440 /etc/sudoers.d/developers
```

### sudo 사용

```bash
# 명령 실행
$ sudo command

# 다른 사용자로 실행
$ sudo -u john command

# 환경 변수 유지
$ sudo -E command

# 쉘 시작
$ sudo -i  # 루트 로그인 쉘
$ sudo -s  # 현재 쉘

# 패스워드 캐시 업데이트
$ sudo -v

# 패스워드 캐시 무효화
$ sudo -k

# 허용된 명령 확인
$ sudo -l

# 명령 실행 로그
$ sudo journalctl -u sudo
$ sudo cat /var/log/auth.log | grep sudo
```

### su - 사용자 전환

```bash
# 루트로 전환
$ su
$ su -  # 로그인 쉘

# 다른 사용자로 전환
$ su john
$ su - john  # 로그인 쉘

# 명령 실행 후 복귀
$ su -c "command" john

# 특정 쉘 사용
$ su -s /bin/bash john

# 그룹만 변경
$ su -g developers

# 원래 사용자로 복귀
$ exit
```

---

## 사용자 환경

### 홈 디렉토리 설정

```bash
# /etc/skel - 새 사용자 템플릿
$ ls -la /etc/skel/
.bash_logout
.bashrc
.profile

# 템플릿 수정
$ sudo vi /etc/skel/.bashrc
# 모든 새 사용자에게 적용됨

# 사용자별 설정 파일
~/.bashrc       # bash 설정
~/.bash_profile # 로그인 쉘 설정
~/.bash_logout  # 로그아웃 시 실행
~/.profile      # 로그인 프로파일

# 환경 변수 설정
$ vi ~/.bashrc
export PATH=$HOME/bin:$PATH
export EDITOR=vim
alias ll='ls -la'

$ source ~/.bashrc
```

### 쉘 변경

```bash
# 사용 가능한 쉘
$ cat /etc/shells
/bin/sh
/bin/bash
/bin/zsh
/bin/fish

# 현재 쉘 확인
$ echo $SHELL

# 쉘 변경
$ chsh -s /bin/zsh
$ chsh -s /bin/zsh john  # root가 다른 사용자 변경

# 또는
$ sudo usermod -s /bin/zsh john
```

### umask 설정

```bash
# 현재 umask
$ umask
0022

# umask 설정
$ umask 0077  # 파일 600, 디렉토리 700

# 영구 설정
$ vi ~/.bashrc
umask 0077

# 시스템 전체
$ sudo vi /etc/profile
umask 0022
```

---

## 계정 보안

### 계정 잠금 및 비활성화

```bash
# 계정 잠금 (패스워드 로그인 차단)
$ sudo usermod -L john
$ sudo passwd -l john

# 계정 만료 (완전 차단)
$ sudo usermod -e 1 john  # 1970-01-02로 설정

# 쉘 변경으로 차단
$ sudo usermod -s /usr/sbin/nologin john
$ sudo usermod -s /bin/false john

# 잠금 해제
$ sudo usermod -U john
$ sudo passwd -u john
$ sudo usermod -e -1 john
$ sudo usermod -s /bin/bash john

# 계정 상태 확인
$ sudo passwd -S john
john L 11/17/2024 0 99999 7 -1
# L = 잠김

$ sudo chage -l john
```

### PAM 설정

```bash
# /etc/pam.d/ 디렉토리
$ ls /etc/pam.d/
common-account
common-auth
common-password
common-session
sudo
login
sshd

# 로그인 실패 잠금 (faillock)
$ sudo vi /etc/pam.d/common-auth
auth required pam_faillock.so preauth
auth required pam_faillock.so authfail
auth sufficient pam_unix.so

account required pam_faillock.so

# faillock 설정
$ sudo vi /etc/security/faillock.conf
deny = 5
unlock_time = 600
fail_interval = 900

# 잠긴 사용자 확인
$ faillock --user john

# 잠금 해제
$ sudo faillock --user john --reset

# 접근 제어 (pam_access)
$ sudo vi /etc/security/access.conf
+ : root : LOCAL
+ : @admins : ALL
- : ALL : ALL

# 시간 기반 접근
$ sudo vi /etc/security/time.conf
login;*;john;Al0800-1800
```

### SSH 키 관리

```bash
# SSH 키 생성
$ ssh-keygen -t ed25519 -C "john@example.com"
$ ssh-keygen -t rsa -b 4096 -C "john@example.com"

# 공개 키 복사
$ ssh-copy-id john@server
$ cat ~/.ssh/id_ed25519.pub | ssh john@server \
    "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# authorized_keys 권한
$ chmod 700 ~/.ssh
$ chmod 600 ~/.ssh/authorized_keys

# SSH 키만 허용 (패스워드 비활성화)
$ sudo vi /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes

$ sudo systemctl restart sshd
```

---

## 배치 작업

### 여러 사용자 생성

```bash
# 사용자 목록 파일
$ cat users.txt
john:John Doe:developers
jane:Jane Smith:developers,sudo
bob:Bob Johnson:users

# 스크립트로 생성
$ cat create-users.sh
#!/bin/bash
while IFS=: read -r username fullname groups; do
    echo "Creating user: $username"
    sudo useradd -m -c "$fullname" -s /bin/bash "$username"
    echo "$username:changeme" | sudo chpasswd
    sudo chage -d 0 "$username"  # 첫 로그인 시 패스워드 변경

    IFS=',' read -ra GROUPARR <<< "$groups"
    for group in "${GROUPARR[@]}"; do
        sudo usermod -aG "$group" "$username"
    done
done < users.txt

$ chmod +x create-users.sh
$ ./create-users.sh
```

### 사용자 일괄 수정

```bash
# 모든 일반 사용자 패스워드 만료 설정
#!/bin/bash
for user in $(getent passwd | awk -F: '$3 >= 1000 && $3 < 65534 {print $1}'); do
    echo "Setting password policy for $user"
    sudo chage -M 90 -m 7 -W 14 "$user"
done

# 모든 사용자에게 그룹 추가
$ for user in john jane bob; do
    sudo usermod -aG docker "$user"
done

# CSV에서 사용자 생성
$ cat users.csv
username,fullname,department,groups
alice,Alice Wonder,IT,"sudo,developers"
charlie,Charlie Brown,HR,"users"

$ cat import-users.sh
#!/bin/bash
tail -n +2 users.csv | while IFS=, read -r username fullname dept groups; do
    sudo useradd -m -c "$fullname - $dept" "$username"
    IFS=',' read -ra GROUPARR <<< "$groups"
    for group in "${GROUPARR[@]}"; do
        sudo usermod -aG "$group" "$username"
    done
done
```

### 사용자 백업

```bash
# 사용자 정보 백업
#!/bin/bash
BACKUP_DIR="/backup/users-$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# 시스템 파일 백업
sudo cp /etc/passwd "$BACKUP_DIR/"
sudo cp /etc/group "$BACKUP_DIR/"
sudo cp /etc/shadow "$BACKUP_DIR/"
sudo cp /etc/gshadow "$BACKUP_DIR/"

# 홈 디렉토리 백업
for user in $(getent passwd | awk -F: '$3 >= 1000 && $3 < 65534 {print $1}'); do
    echo "Backing up /home/$user"
    sudo tar czf "$BACKUP_DIR/$user-home.tar.gz" \
        -C /home "$user"
done

# 압축
sudo tar czf "/backup/users-$(date +%Y%m%d).tar.gz" "$BACKUP_DIR"
sudo rm -rf "$BACKUP_DIR"
```

---

## 감사 및 모니터링

### 로그인 감사

```bash
# 로그인 기록
$ sudo cat /var/log/auth.log | grep "Accepted"
$ sudo cat /var/log/secure | grep "Accepted"  # Red Hat

# 실패한 로그인
$ sudo cat /var/log/auth.log | grep "Failed password"

# su 사용 기록
$ sudo cat /var/log/auth.log | grep "su\["

# sudo 사용 기록
$ sudo cat /var/log/auth.log | grep "sudo"
$ sudo journalctl -u sudo

# 특정 사용자
$ sudo journalctl _UID=1001
$ sudo journalctl _COMM=sudo | grep john
```

### 활성 사용자 모니터링

```bash
# 현재 로그인 사용자
$ who -a
$ w
$ users

# 사용자 프로세스
$ ps aux | grep "^john"
$ ps -u john

# 사용자 세션 종료
$ sudo pkill -u john
$ sudo pkill -9 -u john  # 강제 종료

# 특정 터미널 세션 종료
$ sudo pkill -t pts/1
```

### 보안 감사

```bash
# 패스워드 없는 계정
$ sudo awk -F: '$2 == "" {print $1}' /etc/shadow

# UID 0 계정 (root 권한)
$ awk -F: '$3 == 0 {print $1}' /etc/passwd

# 쉘이 있는 시스템 계정
$ awk -F: '$3 < 1000 && $7 !~ /nologin|false/ {print $1,$7}' /etc/passwd

# 90일 이상 로그인하지 않은 사용자
$ sudo lastlog -b 90

# sudo 권한 사용자
$ getent group sudo
$ getent group wheel

# sudoers 검증
$ sudo visudo -c
/etc/sudoers: parsed OK

# 중복 UID/GID
$ sudo awk -F: '{print $3}' /etc/passwd | sort -n | uniq -d
$ sudo awk -F: '{print $3}' /etc/group | sort -n | uniq -d
```

---

## 실전 예제

### 개발팀 사용자 설정

```bash
#!/bin/bash
# setup-dev-team.sh

# 그룹 생성
sudo groupadd -g 5000 developers
sudo groupadd -g 5001 devops

# 공용 디렉토리
sudo mkdir -p /opt/projects
sudo chown root:developers /opt/projects
sudo chmod 2775 /opt/projects

# 사용자 생성
declare -A users=(
    ["alice"]="Alice Wonder:developers,devops,sudo"
    ["bob"]="Bob Builder:developers"
    ["charlie"]="Charlie Code:developers,docker"
)

for username in "${!users[@]}"; do
    IFS=: read -r fullname groups <<< "${users[$username]}"

    # 사용자 생성
    sudo useradd -m -c "$fullname" -s /bin/bash \
        -G "$groups" "$username"

    # 임시 패스워드
    temp_pass=$(openssl rand -base64 12)
    echo "$username:$temp_pass" | sudo chpasswd
    sudo chage -d 0 "$username"

    # SSH 키 설정
    sudo -u "$username" ssh-keygen -t ed25519 -N "" \
        -f /home/$username/.ssh/id_ed25519 -C "$username@company.com"

    echo "User: $username, Temporary password: $temp_pass"
done

# 패스워드 정책
for username in "${!users[@]}"; do
    sudo chage -M 90 -m 7 -W 14 -I 30 "$username"
done

echo "Dev team setup complete!"
```

### 사용자 감사 스크립트

```bash
#!/bin/bash
# user-audit.sh

echo "=== User Security Audit ==="
echo "Date: $(date)"
echo

# 1. 패스워드 없는 계정
echo "## Accounts without password:"
sudo awk -F: '$2 == "" {print $1}' /etc/shadow
echo

# 2. UID 0 계정
echo "## Accounts with UID 0:"
awk -F: '$3 == 0 {print $1}' /etc/passwd
echo

# 3. sudo 권한
echo "## Users with sudo privileges:"
getent group sudo | cut -d: -f4
getent group wheel | cut -d: -f4
echo

# 4. 오래된 로그인
echo "## Users not logged in for 90+ days:"
sudo lastlog -b 90 | grep -v "Never logged in"
echo

# 5. 만료된 계정
echo "## Expired accounts:"
for user in $(getent passwd | awk -F: '$3 >= 1000 && $3 < 65534 {print $1}'); do
    expiry=$(sudo chage -l "$user" | grep "Account expires" | cut -d: -f2)
    if [[ "$expiry" != *"never"* ]] && [[ -n "$expiry" ]]; then
        if [[ $(date -d "$expiry" +%s 2>/dev/null) -lt $(date +%s) ]]; then
            echo "$user: $expiry"
        fi
    fi
done
echo

# 6. 잠긴 계정
echo "## Locked accounts:"
for user in $(getent passwd | awk -F: '$3 >= 1000 {print $1}'); do
    status=$(sudo passwd -S "$user" | awk '{print $2}')
    if [[ "$status" == "L" ]]; then
        echo "$user"
    fi
done
```

### 사용자 프로비저닝 자동화

```bash
#!/bin/bash
# provision-user.sh

set -e

USERNAME=$1
FULLNAME=$2
DEPARTMENT=$3
GROUPS=$4

if [ $# -lt 3 ]; then
    echo "Usage: $0 <username> <fullname> <department> [groups]"
    exit 1
fi

echo "Provisioning user: $USERNAME"

# 1. 사용자 생성
sudo useradd -m -c "$FULLNAME - $DEPARTMENT" -s /bin/bash "$USERNAME"

# 2. 그룹 추가
if [ -n "$GROUPS" ]; then
    IFS=',' read -ra GROUP_ARRAY <<< "$GROUPS"
    for group in "${GROUP_ARRAY[@]}"; do
        sudo usermod -aG "$group" "$USERNAME"
    done
fi

# 3. 패스워드 생성 및 설정
TEMP_PASS=$(openssl rand -base64 16)
echo "$USERNAME:$TEMP_PASS" | sudo chpasswd
sudo chage -d 0 "$USERNAME"

# 4. SSH 키 생성
sudo -u "$USERNAME" mkdir -p /home/$USERNAME/.ssh
sudo -u "$USERNAME" chmod 700 /home/$USERNAME/.ssh
sudo -u "$USERNAME" ssh-keygen -t ed25519 -N "" \
    -f /home/$USERNAME/.ssh/id_ed25519 -C "$USERNAME@company.com"

# 5. 기본 설정
sudo -u "$USERNAME" tee /home/$USERNAME/.bashrc > /dev/null << 'EOF'
# Custom bashrc
export EDITOR=vim
alias ll='ls -la'
alias gs='git status'
EOF

# 6. 패스워드 정책
sudo chage -M 90 -m 7 -W 14 -I 30 "$USERNAME"

# 7. 로그
echo "$(date): User $USERNAME created" | sudo tee -a /var/log/user-provisioning.log

# 8. 이메일 알림 (mail 명령 필요)
# echo "Your account has been created. Temporary password: $TEMP_PASS" | \
#     mail -s "New Account" $USERNAME@company.com

echo "User $USERNAME provisioned successfully!"
echo "Temporary password: $TEMP_PASS"
echo "Public SSH key:"
sudo cat /home/$USERNAME/.ssh/id_ed25519.pub
```

---

## 요약

사용자 관리 핵심 명령어:

1. **생성**: `useradd`, `adduser`
2. **수정**: `usermod`, `passwd`, `chage`
3. **삭제**: `userdel`, `deluser`
4. **그룹**: `groupadd`, `groupmod`, `groupdel`, `gpasswd`
5. **조회**: `id`, `groups`, `who`, `w`, `last`
6. **권한**: `sudo`, `visudo`, `su`

보안 모범 사례:
- 강력한 패스워드 정책 설정
- 정기적인 패스워드 변경 강제
- sudo 사용 (직접 root 로그인 금지)
- 사용하지 않는 계정 비활성화
- 정기적인 감사 수행

---

[다음: systemd →](systemd.md)

[← 소스 빌드로 돌아가기](../09-package-management/building-from-source.md)

[← 목차로 돌아가기](../README.md)

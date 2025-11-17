# 권한 기본

## 목차
- [권한 시스템 이해](#권한-시스템-이해)
- [권한 확인](#권한-확인)
- [권한 변경 chmod](#권한-변경-chmod)
- [기본 권한 umask](#기본-권한-umask)
- [실전 예제](#실전 예제)

---

## 권한 시스템 이해

Linux는 파일과 디렉토리에 대한 접근을 세밀하게 제어합니다.

### 권한 구성 요소

```
-rwxr-xr-x 1 user group 4096 Nov 17 12:00 file.txt
│└┬─┘└┬─┘└┬─┘
│ │   │   └─ 기타(others) 권한: r-x (읽기, 실행)
│ │   └───── 그룹(group) 권한: r-x (읽기, 실행)
│ └───────── 소유자(user) 권한: rwx (읽기, 쓰기, 실행)
└─────────── 파일 타입: - (일반 파일)
```

### 파일 타입

```bash
-  일반 파일
d  디렉토리
l  심볼릭 링크
b  블록 디바이스
c  문자 디바이스
p  파이프 (FIFO)
s  소켓
```

### 권한 의미

```
읽기(r, 4):
- 파일: 내용 읽기 가능
- 디렉토리: 목록 조회 가능 (ls)

쓰기(w, 2):
- 파일: 내용 수정 가능
- 디렉토리: 파일 생성/삭제 가능

실행(x, 1):
- 파일: 실행 가능
- 디렉토리: 진입 가능 (cd)
```

---

## 권한 확인

### ls로 권한 확인

```bash
# 자세한 정보
$ ls -l
drwxr-xr-x 2 user group 4096 Nov 17 12:00 Documents
-rw-r--r-- 1 user group 1234 Nov 17 11:30 file.txt

# 숨김 파일 포함
$ ls -la

# 숫자 형식으로
$ stat file.txt
  File: file.txt
  Size: 1234       Blocks: 8          IO Block: 4096   regular file
Device: 801h/2049d Inode: 123456      Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/   user)   Gid: ( 1000/  group)

# 권한만 간단히
$ stat -c "%a %n" file.txt
644 file.txt

# 여러 파일
$ stat -c "%a %U:%G %n" *
755 user:group script.sh
644 user:group file.txt
```

### find로 권한 검색

```bash
# 특정 권한
$ find / -perm 777

# 최소 권한
$ find / -perm -644

# 권한 포함
$ find / -perm /u=x

# 쓰기 가능 파일
$ find / -writable

# 실행 가능 파일
$ find / -executable

# 소유자별
$ find / -user username

# 그룹별
$ find / -group groupname
```

---

## 권한 변경 chmod

### 기호 모드

```bash
# 소유자에게 실행 권한 추가
$ chmod u+x file.txt

# 그룹에서 쓰기 권한 제거
$ chmod g-w file.txt

# 기타에게 읽기 권한 추가
$ chmod o+r file.txt

# 모두에게 실행 권한
$ chmod a+x script.sh
$ chmod +x script.sh  # 동일

# 여러 권한
$ chmod u+rwx,g+rx,o+r file.txt

# 정확히 설정
$ chmod u=rwx,g=rx,o=r file.txt

# 재귀적 적용
$ chmod -R 755 directory/

# verbose
$ chmod -v 755 file.txt
mode of 'file.txt' changed from 0644 (rw-r--r--) to 0755 (rwxr-xr-x)
```

### 숫자 모드

```bash
# 8진수 권한
$ chmod 644 file.txt   # rw-r--r--
$ chmod 755 script.sh  # rwxr-xr-x
$ chmod 600 secret.txt # rw-------
$ chmod 777 public.txt # rwxrwxrwx

# 계산 방법:
# r=4, w=2, x=1
# rwx = 4+2+1 = 7
# rw- = 4+2+0 = 6
# r-x = 4+0+1 = 5
# r-- = 4+0+0 = 4

# 일반적인 권한 값들
644  # 파일: 소유자 읽기/쓰기, 나머지 읽기
755  # 실행 파일 및 디렉토리
600  # 개인 파일 (소유자만)
700  # 개인 디렉토리
666  # 모두 읽기/쓰기
777  # 모두 전체 권한 (보안상 위험!)
```

### 참조 모드

```bash
# 다른 파일과 같은 권한 설정
$ chmod --reference=file1.txt file2.txt

# stat와 조합
$ chmod $(stat -c %a file1.txt) file2.txt
```

---

## 기본 권한 umask

umask는 새로 생성되는 파일의 기본 권한을 결정합니다.

### umask 이해

```bash
# 현재 umask 확인
$ umask
0022

# 기호로 확인
$ umask -S
u=rwx,g=rx,o=rx

# umask 계산:
# 파일 기본: 666 (rw-rw-rw-)
# 디렉토리 기본: 777 (rwxrwxrwx)
#
# umask 022를 빼면:
# 파일: 666 - 022 = 644 (rw-r--r--)
# 디렉토리: 777 - 022 = 755 (rwxr-xr-x)
```

### umask 설정

```bash
# 일시적 변경
$ umask 027
# 파일: 666 - 027 = 640 (rw-r-----)
# 디렉토리: 777 - 027 = 750 (rwxr-x---)

# 영구 변경 (~/.bashrc)
$ echo "umask 027" >> ~/.bashrc

# 일반적인 umask 값:
022  # 기본 (파일 644, 디렉토리 755)
002  # 그룹 협업 (파일 664, 디렉토리 775)
077  # 엄격한 보안 (파일 600, 디렉토리 700)
```

### 실제 테스트

```bash
# 현재 umask
$ umask
0022

# 파일 생성
$ touch newfile.txt
$ ls -l newfile.txt
-rw-r--r-- 1 user group 0 Nov 17 12:00 newfile.txt

# 디렉토리 생성
$ mkdir newdir
$ ls -ld newdir
drwxr-xr-x 2 user group 4096 Nov 17 12:00 newdir

# umask 변경 후
$ umask 077
$ touch private.txt
$ ls -l private.txt
-rw------- 1 user group 0 Nov 17 12:01 private.txt
```

---

## 실전 예제

### 예제 1: 웹 서버 권한 설정

```bash
# 웹 루트 디렉토리
$ sudo chown -R www-data:www-data /var/www/html

# 디렉토리 권한
$ sudo find /var/www/html -type d -exec chmod 755 {} \;

# 파일 권한
$ sudo find /var/www/html -type f -exec chmod 644 {} \;

# 업로드 디렉토리
$ sudo chmod 775 /var/www/html/uploads
$ sudo chmod g+s /var/www/html/uploads  # SGID
```

### 예제 2: 스크립트 실행 권한

```bash
# 스크립트 생성
$ cat > script.sh << 'EOF'
#!/bin/bash
echo "Hello, World!"
EOF

# 실행 권한 부여
$ chmod +x script.sh

# 확인
$ ls -l script.sh
-rwxr-xr-x 1 user group 31 Nov 17 12:00 script.sh

# 실행
$ ./script.sh
Hello, World!
```

### 예제 3: 공유 디렉토리

```bash
# 팀 프로젝트 디렉토리
$ sudo mkdir /shared/project
$ sudo chgrp developers /shared/project
$ sudo chmod 775 /shared/project
$ sudo chmod g+s /shared/project  # SGID

# 이제 developers 그룹 멤버가 파일 생성 가능
# 생성된 파일의 그룹이 자동으로 developers가 됨
```

### 예제 4: 개인 파일 보호

```bash
# SSH 키 권한
$ chmod 700 ~/.ssh
$ chmod 600 ~/.ssh/id_rsa
$ chmod 644 ~/.ssh/id_rsa.pub
$ chmod 644 ~/.ssh/authorized_keys

# GPG 키
$ chmod 700 ~/.gnupg

# 비밀번호 파일
$ chmod 600 ~/.netrc
$ chmod 600 ~/.my.cnf
```

### 예제 5: 로그 파일 권한

```bash
# 로그 디렉토리
$ sudo chmod 755 /var/log

# 로그 파일 (읽기 전용)
$ sudo chmod 644 /var/log/*.log

# 시스템 로그 (root만)
$ sudo chmod 600 /var/log/auth.log
$ sudo chmod 600 /var/log/secure
```

---

## 보안 권장사항

### 파일 권한

```bash
# 설정 파일
644  # 일반 설정 파일
640  # 비밀번호 포함 파일

# 실행 파일
755  # 일반 실행 파일
750  # 관리 스크립트
700  # 개인 스크립트

# 데이터 파일
644  # 공개 데이터
640  # 제한된 데이터
600  # 개인 데이터
```

### 디렉토리 권한

```bash
755  # 일반 디렉토리
750  # 그룹 접근 디렉토리
700  # 개인 디렉토리
1777 # 공용 임시 디렉토리 (/tmp)
```

### 위험한 권한

```bash
# 피해야 할 권한
777  # 모두 전체 권한 - 매우 위험!
666  # 모두 쓰기 가능 - 위험
o+w  # 기타 사용자 쓰기 - 위험

# 특히 주의
/  # 루트 디렉토리
/etc  # 시스템 설정
/home  # 사용자 홈
```

---

## 권한 문제 해결

### 권한 거부 문제

```bash
# 1. 현재 권한 확인
$ ls -l file.txt

# 2. 현재 사용자 확인
$ whoami
$ id

# 3. 파일 소유자 확인
$ stat file.txt

# 4. 권한 수정
$ chmod 644 file.txt
$ sudo chown user:group file.txt

# 5. 디렉토리 권한 확인
$ ls -ld /path/to/directory
```

### 일괄 권한 수정

```bash
# 모든 파일을 644로
$ find . -type f -exec chmod 644 {} \;

# 모든 디렉토리를 755로
$ find . -type d -exec chmod 755 {} \;

# 스크립트만 실행 권한
$ find . -name "*.sh" -exec chmod +x {} \;

# 소유자 일괄 변경
$ find . -user olduser -exec sudo chown newuser {} \;
```

---

## 요약

권한 시스템의 핵심:

- **권한 구조**: User, Group, Others - Read, Write, Execute
- **chmod**: 권한 변경 (기호/숫자 모드)
- **umask**: 기본 권한 설정
- **보안**: 최소 권한 원칙 적용

올바른 권한 설정은 시스템 보안의 기초입니다.

---

[다음: 소유권 관리 →](ownership.md)

[← 고급 명령어로 돌아가기](../04-commands/advanced.md)

[← 목차로 돌아가기](../README.md)

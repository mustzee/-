# 소유권 관리

## 목차
- [소유권 개념](#소유권-개념)
- [chown - 소유자 변경](#chown---소유자-변경)
- [chgrp - 그룹 변경](#chgrp---그룹-변경)
- [그룹 관리](#그룹-관리)
- [실전 예제](#실전-예제)

---

## 소유권 개념

모든 파일과 디렉토리는 소유자(user)와 그룹(group)을 가집니다.

```bash
$ ls -l file.txt
-rw-r--r-- 1 user group 1234 Nov 17 12:00 file.txt
           │ └──┘ └───┘
           │  │     └─── 그룹
           │  └───────── 소유자  
           └──────────── 하드링크 수
```

---

## chown - 소유자 변경

```bash
# 소유자만 변경
$ sudo chown alice file.txt

# 소유자와 그룹 모두 변경
$ sudo chown alice:developers file.txt

# 그룹만 변경 (콜론 앞 생략)
$ sudo chown :developers file.txt

# 재귀적 변경
$ sudo chown -R alice:developers directory/

# 참조 파일과 동일하게
$ sudo chown --reference=file1.txt file2.txt

# verbose 모드
$ sudo chown -v alice file.txt
changed ownership of 'file.txt' from user to alice

# 심볼릭 링크 자체 변경 (대상 아님)
$ sudo chown -h alice symlink

# 변경 내역만 표시
$ sudo chown -c alice file.txt  # 변경된 경우만 출력
```

---

## chgrp - 그룹 변경

```bash
# 그룹 변경
$ sudo chgrp developers file.txt

# 재귀적 변경
$ sudo chgrp -R developers directory/

# verbose
$ sudo chgrp -v developers file.txt

# 참조 파일 사용
$ sudo chgrp --reference=file1.txt file2.txt
```

---

## 그룹 관리

```bash
# 현재 사용자가 속한 그룹
$ groups
user adm cdrom sudo dip plugdev

# 특정 사용자의 그룹
$ groups alice

# 그룹에 사용자 추가
$ sudo usermod -aG developers alice

# 그룹에서 사용자 제거
$ sudo gpasswd -d alice developers

# 새 그룹 생성
$ sudo groupadd developers

# 그룹 삭제
$ sudo groupdel developers

# 그룹 정보 확인
$ getent group developers
developers:x:1001:alice,bob,carol
```

---

## 실전 예제

### 예제 1: 웹 서버 파일 소유권

```bash
# Apache/Nginx 사용자로 변경
$ sudo chown -R www-data:www-data /var/www/html

# 확인
$ ls -ld /var/www/html
drwxr-xr-x 2 www-data www-data 4096 Nov 17 12:00 /var/www/html
```

### 예제 2: 공유 프로젝트 디렉토리

```bash
# 그룹 생성
$ sudo groupadd developers

# 사용자 추가
$ sudo usermod -aG developers alice
$ sudo usermod -aG developers bob

# 디렉토리 소유권 설정
$ sudo chown -R :developers /shared/project
$ sudo chmod -R 775 /shared/project
$ sudo chmod g+s /shared/project  # SGID 설정
```

### 예제 3: 데이터베이스 파일

```bash
# MySQL 파일
$ sudo chown -R mysql:mysql /var/lib/mysql
$ sudo chmod 750 /var/lib/mysql

# PostgreSQL 파일
$ sudo chown -R postgres:postgres /var/lib/postgresql
$ sudo chmod 700 /var/lib/postgresql
```

---

[다음: 특수 권한 →](special.md)

[← 권한 기본으로 돌아가기](basics.md)

[← 목차로 돌아가기](../README.md)

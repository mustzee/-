# 특수 권한

## 목차
- [SUID - Set User ID](#suid---set-user-id)
- [SGID - Set Group ID](#sgid---set-group-id)
- [Sticky Bit](#sticky-bit)
- [보안 고려사항](#보안-고려사항)

---

## SUID - Set User ID

파일 실행 시 소유자의 권한으로 실행됩니다.

```bash
# SUID 설정
$ chmod u+s file
$ chmod 4755 file  # 4는 SUID

# 확인 (소유자 실행 권한에 s)
$ ls -l
-rwsr-xr-x 1 root root 12345 file

# SUID 제거
$ chmod u-s file

# SUID 파일 찾기
$ find / -perm -4000 2>/dev/null

# 시스템의 SUID 파일 예제
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 /usr/bin/passwd

# passwd는 root 소유이지만 일반 사용자도 실행 가능
# 실행 시 root 권한으로 /etc/shadow 수정
```

---

## SGID - Set Group ID

### 파일에 적용

```bash
# SGID 설정
$ chmod g+s file
$ chmod 2755 file  # 2는 SGID

# 확인 (그룹 실행 권한에 s)
$ ls -l
-rwxr-sr-x 1 user group 12345 file
```

### 디렉토리에 적용 (더 유용)

```bash
# 디렉토리에 SGID 설정
$ chmod g+s /shared/project

# 효과: 디렉토리 내 생성되는 파일의 그룹이
# 사용자 그룹이 아닌 디렉토리 그룹을 상속

# 예제
$ sudo mkdir /shared/team
$ sudo chgrp developers /shared/team
$ sudo chmod 2775 /shared/team

# alice (developers 그룹 멤버)가 파일 생성
$ touch /shared/team/file.txt
$ ls -l /shared/team/file.txt
-rw-r--r-- 1 alice developers 0 file.txt  # 그룹이 developers!
```

---

## Sticky Bit

디렉토리의 Sticky Bit: 소유자만 자신의 파일을 삭제할 수 있습니다.

```bash
# Sticky Bit 설정
$ chmod +t directory
$ chmod 1777 directory  # 1은 Sticky Bit

# 확인 (others 실행 권한에 t)
$ ls -ld directory
drwxrwxrwt 2 root root 4096 directory

# /tmp 디렉토리가 대표적 예제
$ ls -ld /tmp
drwxrwxrwt 15 root root 4096 /tmp

# 효과:
# - 누구나 /tmp에 파일 생성 가능 (rwx for all)
# - 하지만 자신의 파일만 삭제 가능 (t)

# Sticky Bit 제거
$ chmod -t directory
```

---

## 특수 권한 조합

```bash
# 숫자 표기법:
# [특수권한][소유자][그룹][기타]
# 특수권한: 4(SUID) + 2(SGID) + 1(Sticky)

4755  # SUID + 755
2755  # SGID + 755
1777  # Sticky + 777
6755  # SUID + SGID + 755
7777  # SUID + SGID + Sticky + 777

# 예제
$ chmod 4755 executable   # SUID
$ chmod 2775 directory    # SGID
$ chmod 1777 /tmp         # Sticky Bit
```

---

## 보안 고려사항

```bash
# 위험한 SUID 파일 찾기
$ find / -perm -4000 -user root 2>/dev/null

# 새로운 SUID 파일 모니터링
$ find / -perm -4000 -mtime -7 2>/dev/null

# SUID/SGID 제거 (마운트 시)
$ sudo mount -o nosuid /dev/sdb1 /mnt

# 정기 감사
$ sudo find / -type f \( -perm -4000 -o -perm -2000 \) -ls 2>/dev/null
```

---

[다음: ACL →](acl.md)

[← 소유권 관리로 돌아가기](ownership.md)

[← 목차로 돌아가기](../README.md)

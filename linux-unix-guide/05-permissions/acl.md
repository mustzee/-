# Access Control Lists (ACL)

## 목차
- [ACL 개요](#acl-개요)
- [ACL 확인](#acl-확인)
- [ACL 설정](#acl-설정)
- [ACL 고급 활용](#acl-고급-활용)

---

## ACL 개요

ACL은 기본 권한(rwx)보다 세밀한 접근 제어를 제공합니다.

```bash
# ACL 지원 확인
$ mount | grep acl
/dev/sda1 on / type ext4 (rw,relatime,acl)

# ACL 도구 설치
$ sudo apt install acl
```

---

## ACL 확인

```bash
# ACL 확인
$ getfacl file.txt
# file: file.txt
# owner: user
# group: group
user::rw-
group::r--
other::r--

# ACL이 설정된 파일 (ls에서 + 표시)
$ ls -l
-rw-r--r--+ 1 user group 1234 file.txt
           ↑ ACL 있음
```

---

## ACL 설정

```bash
# 특정 사용자에게 권한 부여
$ setfacl -m u:alice:rw file.txt

# 특정 그룹에게 권한 부여
$ setfacl -m g:developers:rx directory/

# 여러 ACL 동시 설정
$ setfacl -m u:alice:rw,g:developers:rx file.txt

# ACL 제거
$ setfacl -x u:alice file.txt

# 모든 ACL 제거
$ setfacl -b file.txt

# 재귀적 설정
$ setfacl -R -m u:alice:rwx directory/

# 기본 ACL (새 파일에 적용)
$ setfacl -d -m u:alice:rw directory/
```

---

## ACL 고급 활용

```bash
# 마스크 설정
$ setfacl -m m::rx file.txt

# ACL 복사
$ getfacl file1.txt | setfacl --set-file=- file2.txt

# 백업 및 복원
$ getfacl -R /data > acl_backup.txt
$ setfacl --restore=acl_backup.txt

# 예제: 공유 디렉토리
$ mkdir /shared
$ setfacl -m u:alice:rwx /shared
$ setfacl -m u:bob:rx /shared
$ setfacl -d -m u:alice:rwx /shared
```

---

[다음: 셸 스크립팅 기초 →](../07-shell-scripting/basics.md)

[← 특수 권한으로 돌아가기](special.md)

[← 목차로 돌아가기](../README.md)

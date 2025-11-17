# 셸 스크립팅 기초

## 목차
- [셸 스크립트란](#셸-스크립트란)
- [첫 스크립트 작성](#첫-스크립트-작성)
- [변수 사용](#변수-사용)
- [사용자 입력](#사용자-입력)
- [기본 명령어 활용](#기본-명령어-활용)

---

## 셸 스크립트란

셸 스크립트는 셸 명령어들을 모아 놓은 프로그램입니다.

```bash
# 장점:
- 반복 작업 자동화
- 시스템 관리 효율화
- 복잡한 작업 단순화
```

---

## 첫 스크립트 작성

```bash
#!/bin/bash
# hello.sh - 첫 번째 스크립트

echo "Hello, World!"
```

```bash
# 실행 권한 부여
$ chmod +x hello.sh

# 실행
$ ./hello.sh
Hello, World!
```

---

## 변수 사용

```bash
#!/bin/bash
# variables.sh

# 변수 선언
NAME="Alice"
AGE=30
PI=3.14

# 변수 사용
echo "Name: $NAME"
echo "Age: $AGE"
echo "Pi: ${PI}"

# 명령 결과 저장
DATE=$(date)
FILES=$(ls -1 | wc -l)

echo "Today: $DATE"
echo "Files: $FILES"
```

---

## 사용자 입력

```bash
#!/bin/bash
# input.sh

echo "What is your name?"
read NAME

echo "Hello, $NAME!"

# 옵션과 함께
read -p "Enter your age: " AGE
read -s -p "Enter password: " PASS
echo

echo "Age: $AGE"
```

---

## 기본 명령어 활용

```bash
#!/bin/bash
# commands.sh

# 파일 작업
if [ -f "file.txt" ]; then
    echo "File exists"
    cat file.txt
else
    echo "File not found"
fi

# 디렉토리 작업
mkdir -p backup
cp *.txt backup/

# 날짜 기반 백업
BACKUP_DIR="backup_$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
cp important.txt "$BACKUP_DIR/"
```

---

[다음: 제어 구조 →](control-flow.md)

[← ACL로 돌아가기](../05-permissions/acl.md)

[← 목차로 돌아가기](../README.md)

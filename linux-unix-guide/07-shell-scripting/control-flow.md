# 제어 구조

## 목차
- [조건문 if](#조건문-if)
- [case 문](#case-문)
- [for 루프](#for-루프)
- [while 루프](#while-루프)

---

## 조건문 if

```bash
#!/bin/bash

# 기본 if
if [ "$USER" = "root" ]; then
    echo "You are root"
fi

# if-else
if [ -f "file.txt" ]; then
    echo "File exists"
else
    echo "File not found"
fi

# if-elif-else
if [ $# -eq 0 ]; then
    echo "No arguments"
elif [ $# -eq 1 ]; then
    echo "One argument"
else
    echo "Multiple arguments"
fi

# 파일 테스트
if [ -e "$FILE" ]; then echo "Exists"; fi
if [ -f "$FILE" ]; then echo "Regular file"; fi
if [ -d "$FILE" ]; then echo "Directory"; fi
if [ -r "$FILE" ]; then echo "Readable"; fi
if [ -w "$FILE" ]; then echo "Writable"; fi
if [ -x "$FILE" ]; then echo "Executable"; fi

# 문자열 테스트
if [ -z "$VAR" ]; then echo "Empty"; fi
if [ -n "$VAR" ]; then echo "Not empty"; fi
if [ "$A" = "$B" ]; then echo "Equal"; fi
if [ "$A" != "$B" ]; then echo "Not equal"; fi

# 숫자 비교
if [ $A -eq $B ]; then echo "Equal"; fi
if [ $A -ne $B ]; then echo "Not equal"; fi
if [ $A -lt $B ]; then echo "Less than"; fi
if [ $A -le $B ]; then echo "Less or equal"; fi
if [ $A -gt $B ]; then echo "Greater than"; fi
if [ $A -ge $B ]; then echo "Greater or equal"; fi

# 논리 연산
if [ $A -gt 0 ] && [ $A -lt 10 ]; then
    echo "Between 0 and 10"
fi

if [ $A -eq 0 ] || [ $A -eq 10 ]; then
    echo "0 or 10"
fi
```

---

## case 문

```bash
#!/bin/bash

read -p "Enter option (start/stop/restart): " OPTION

case $OPTION in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        echo "Restarting service..."
        ;;
    *)
        echo "Invalid option"
        ;;
esac
```

---

## for 루프

```bash
#!/bin/bash

# 리스트 반복
for item in apple banana cherry; do
    echo "Fruit: $item"
done

# 범위
for i in {1..10}; do
    echo "Number: $i"
done

# C 스타일
for ((i=0; i<10; i++)); do
    echo "Index: $i"
done

# 파일 처리
for file in *.txt; do
    echo "Processing $file"
    wc -l "$file"
done

# 배열 반복
FILES=(file1.txt file2.txt file3.txt)
for file in "${FILES[@]}"; do
    echo "$file"
done
```

---

## while 루프

```bash
#!/bin/bash

# 기본 while
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    ((count++))
done

# 파일 읽기
while read line; do
    echo "Line: $line"
done < file.txt

# 무한 루프
while true; do
    echo "Press Ctrl+C to stop"
    sleep 1
done

# until (while의 반대)
count=0
until [ $count -ge 5 ]; do
    echo "Count: $count"
    ((count++))
done
```

---

[다음: 함수 →](functions.md)

[← 셸 스크립팅 기초로 돌아가기](basics.md)

[← 목차로 돌아가기](../README.md)

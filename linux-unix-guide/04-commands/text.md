# 텍스트 처리 명령어

## 목차
- [텍스트 검색](#텍스트-검색)
- [텍스트 필터링](#텍스트-필터링)
- [텍스트 변환](#텍스트-변환)
- [텍스트 편집](#텍스트-편집)
- [텍스트 비교](#텍스트-비교)

---

## 텍스트 검색

### grep - 패턴 검색

```bash
# 기본 검색
$ grep "pattern" file.txt

# 대소문자 무시
$ grep -i "pattern" file.txt

# 단어 단위 매칭
$ grep -w "word" file.txt

# 줄 번호 표시
$ grep -n "pattern" file.txt

# 매칭된 줄 개수
$ grep -c "pattern" file.txt

# 매칭되지 않은 줄
$ grep -v "pattern" file.txt

# 여러 파일 검색
$ grep "pattern" *.txt

# 재귀 검색
$ grep -r "pattern" /path/

# 파일 이름만 표시
$ grep -l "pattern" *.txt

# 매칭 부분만 표시
$ grep -o "pattern" file.txt

# 컨텍스트 표시 (전후 줄)
$ grep -C 3 "pattern" file.txt  # 전후 3줄
$ grep -A 2 "pattern" file.txt  # 이후 2줄
$ grep -B 2 "pattern" file.txt  # 이전 2줄

# 정규표현식
$ grep "^start" file.txt  # 줄 시작
$ grep "end$" file.txt    # 줄 끝
$ grep "[0-9]" file.txt   # 숫자 포함
$ grep "a\{3\}" file.txt  # aaa

# Extended 정규표현식
$ grep -E "pattern1|pattern2" file.txt
$ egrep "pattern1|pattern2" file.txt

# 바이너리 파일 제외
$ grep -I "pattern" *

# 숨김 파일 포함 검색
$ grep -r --include=".*" "pattern" .

# 특정 파일만 검색
$ grep -r --include="*.py" "def " .

# 특정 파일 제외
$ grep -r --exclude="*.log" "pattern" .

# 디렉토리 제외
$ grep -r --exclude-dir=".git" "pattern" .

# 색상 표시
$ grep --color=auto "pattern" file.txt

# Perl 정규표현식
$ grep -P "\d{3}-\d{4}" file.txt

# 고정 문자열 (정규표현식 아님)
$ grep -F "literal.string" file.txt
$ fgrep "literal.string" file.txt
```

### awk - 텍스트 처리 및 패턴 스캔

```bash
# 특정 열 출력
$ awk '{print $1}' file.txt       # 첫 번째 필드
$ awk '{print $1, $3}' file.txt   # 1,3번째 필드

# 구분자 지정
$ awk -F: '{print $1}' /etc/passwd
$ awk -F',' '{print $2}' data.csv

# 조건부 출력
$ awk '$3 > 100' file.txt
$ awk '$1 == "admin"' file.txt

# 패턴 매칭
$ awk '/pattern/ {print $0}' file.txt

# 합계 계산
$ awk '{sum += $1} END {print sum}' numbers.txt

# 평균 계산
$ awk '{sum += $1; count++} END {print sum/count}' numbers.txt

# 조건과 액션
$ awk '$3 > 50 {print $1, $2}' file.txt

# BEGIN과 END 블록
$ awk 'BEGIN {print "Start"} {print $1} END {print "End"}' file.txt

# 여러 조건
$ awk '$1 == "error" || $2 > 100' file.txt

# 필드 개수
$ awk '{print NF}' file.txt

# 레코드 번호 (줄 번호)
$ awk '{print NR, $0}' file.txt

# 출력 형식 지정
$ awk '{printf "%-10s %5d\n", $1, $2}' file.txt

# 복잡한 예제
$ ps aux | awk 'NR>1 {sum += $3} END {print "Total CPU:", sum"%"}'
```

### sed - 스트림 에디터

```bash
# 문자열 치환
$ sed 's/old/new/' file.txt         # 첫 번째만
$ sed 's/old/new/g' file.txt        # 전체
$ sed 's/old/new/2' file.txt        # 두 번째

# 파일 직접 수정
$ sed -i 's/old/new/g' file.txt

# 백업 생성 후 수정
$ sed -i.bak 's/old/new/g' file.txt

# 특정 줄만 치환
$ sed '5s/old/new/' file.txt
$ sed '1,10s/old/new/g' file.txt

# 줄 삭제
$ sed '5d' file.txt                 # 5번째 줄
$ sed '1,5d' file.txt               # 1~5번째 줄
$ sed '/pattern/d' file.txt         # 패턴 매칭 줄

# 줄 추가
$ sed '5a\New line' file.txt        # 5번째 줄 뒤
$ sed '5i\New line' file.txt        # 5번째 줄 앞

# 패턴 매칭 줄 뒤에 추가
$ sed '/pattern/a\New line' file.txt

# 줄 치환
$ sed '5c\Replacement line' file.txt

# 줄 범위 출력
$ sed -n '10,20p' file.txt

# 패턴 매칭 줄만 출력
$ sed -n '/pattern/p' file.txt

# 다중 명령
$ sed -e 's/old/new/g' -e 's/foo/bar/g' file.txt

# 또는
$ sed 's/old/new/g; s/foo/bar/g' file.txt

# 정규표현식
$ sed 's/[0-9]\{3\}-[0-9]\{4\}/XXX-XXXX/g' file.txt

# 그룹 참조
$ sed 's/\([0-9]\{3\}\)-\([0-9]\{4\}\)/\2-\1/g' file.txt

# 주소 범위
$ sed '/start/,/end/d' file.txt     # start부터 end까지 삭제

# 여러 파일
$ sed 's/old/new/g' file1.txt file2.txt
```

---

## 텍스트 필터링

### cut - 열 추출

```bash
# 특정 필드
$ cut -f1 file.txt                  # 첫 번째 필드
$ cut -f1,3 file.txt                # 1,3번째 필드
$ cut -f1-5 file.txt                # 1~5번째 필드

# 구분자 지정
$ cut -d: -f1 /etc/passwd           # : 구분자
$ cut -d',' -f2 data.csv

# 문자 위치
$ cut -c1-10 file.txt               # 1~10번째 문자
$ cut -c1,5,10 file.txt

# 탭 대신 다른 출력 구분자
$ cut -d: -f1,3 --output-delimiter=, /etc/passwd
```

### sort - 정렬

```bash
# 기본 정렬 (알파벳순)
$ sort file.txt

# 역순
$ sort -r file.txt

# 숫자 정렬
$ sort -n numbers.txt

# 고유한 줄만
$ sort -u file.txt

# 특정 필드로 정렬
$ sort -k2 file.txt                 # 2번째 필드
$ sort -t: -k3 -n /etc/passwd       # : 구분, 3번째 필드, 숫자

# 여러 필드
$ sort -k1,1 -k2,2n file.txt

# 대소문자 무시
$ sort -f file.txt

# 월 이름 정렬
$ sort -M months.txt

# 사람이 읽기 쉬운 숫자 (1K, 2M 등)
$ du -sh * | sort -h

# 무작위 정렬
$ sort -R file.txt

# 정렬 확인
$ sort -c file.txt

# 안정 정렬
$ sort -s file.txt

# 병렬 정렬 (빠름)
$ sort --parallel=4 largefile.txt

# 임시 디렉토리 지정
$ sort -T /tmp largefile.txt
```

### uniq - 중복 제거

```bash
# 인접한 중복 제거 (보통 sort와 함께 사용)
$ sort file.txt | uniq

# 중복 개수
$ sort file.txt | uniq -c

# 중복된 줄만
$ sort file.txt | uniq -d

# 고유한 줄만
$ sort file.txt | uniq -u

# 대소문자 무시
$ sort file.txt | uniq -i

# 특정 필드 무시
$ uniq -f 1 file.txt

# 특정 문자 무시
$ uniq -s 5 file.txt

# 중복 개수로 정렬
$ sort file.txt | uniq -c | sort -rn

# 가장 빈번한 10개
$ sort file.txt | uniq -c | sort -rn | head -10
```

### wc - 단어/줄/바이트 세기

```bash
# 줄 수
$ wc -l file.txt

# 단어 수
$ wc -w file.txt

# 문자 수
$ wc -c file.txt

# 바이트 수
$ wc -m file.txt

# 모든 정보
$ wc file.txt
 100  500 3000 file.txt
# 줄  단어 바이트

# 여러 파일
$ wc *.txt

# 파일 수 세기
$ ls | wc -l

# 가장 긴 줄 길이
$ wc -L file.txt
```

---

## 텍스트 변환

### tr - 문자 변환/삭제

```bash
# 대문자로 변환
$ cat file.txt | tr 'a-z' 'A-Z'
$ tr 'a-z' 'A-Z' < file.txt

# 소문자로 변환
$ cat file.txt | tr 'A-Z' 'a-z'

# 문자 치환
$ echo "hello" | tr 'el' 'ip'
hippo

# 문자 삭제
$ cat file.txt | tr -d '0-9'        # 숫자 삭제
$ cat file.txt | tr -d ' '          # 공백 삭제

# 연속 문자 압축
$ cat file.txt | tr -s ' '          # 연속 공백을 하나로
$ cat file.txt | tr -s '\n'         # 빈 줄 제거

# 보완 (complement)
$ cat file.txt | tr -cd '0-9'       # 숫자만 남김

# 개행 문자 변환
$ cat file.txt | tr '\n' ' '        # 모든 줄을 한 줄로

# 탭을 공백으로
$ cat file.txt | tr '\t' ' '

# Windows 줄바꿈을 Unix로
$ cat windows.txt | tr -d '\r' > unix.txt

# ROT13 암호화
$ echo "hello" | tr 'a-zA-Z' 'n-za-mN-ZA-M'
uryyb
```

### expand / unexpand - 탭 변환

```bash
# 탭을 공백으로
$ expand file.txt

# 탭 크기 지정
$ expand -t 4 file.txt

# 공백을 탭으로
$ unexpand file.txt

# 초기 공백만
$ unexpand -a file.txt
```

### join - 파일 결합

```bash
# 공통 필드로 결합
$ join file1.txt file2.txt

# 구분자 지정
$ join -t: file1.txt file2.txt

# 특정 필드로 결합
$ join -1 2 -2 1 file1.txt file2.txt

# 매칭되지 않은 줄 포함
$ join -a 1 file1.txt file2.txt     # file1의 모든 줄
$ join -a 2 file1.txt file2.txt     # file2의 모든 줄
$ join -a 1 -a 2 file1.txt file2.txt # 모든 줄 (outer join)
```

### paste - 파일 병합

```bash
# 세로로 병합
$ paste file1.txt file2.txt

# 구분자 지정
$ paste -d: file1.txt file2.txt

# 한 파일을 여러 열로
$ paste -s file.txt

# 여러 파일
$ paste file1.txt file2.txt file3.txt
```

### column - 열 정렬

```bash
# 자동 정렬
$ column file.txt

# 테이블 형식
$ column -t file.txt

# 구분자 지정
$ column -t -s: /etc/passwd

# 출력 구분자
$ column -t -s: -o, /etc/passwd

# 특정 너비
$ column -c 80 file.txt
```

---

## 텍스트 편집

### vi / vim

```bash
# 파일 열기
$ vi file.txt
$ vim file.txt

# 읽기 전용
$ view file.txt

# 복구
$ vim -r file.txt

# 여러 파일
$ vim file1.txt file2.txt

# 차이 보기
$ vimdiff file1.txt file2.txt

# 기본 명령 (명령 모드)
i     # 삽입 모드
a     # 커서 뒤 삽입
o     # 아래 줄 추가
O     # 위 줄 추가
Esc   # 명령 모드로
:w    # 저장
:q    # 종료
:wq   # 저장 후 종료
:q!   # 강제 종료
dd    # 줄 삭제
yy    # 줄 복사
p     # 붙여넣기
u     # 실행 취소
/     # 검색
n     # 다음 검색
:%s/old/new/g  # 전체 치환
```

### nano

```bash
# 파일 열기
$ nano file.txt

# 기본 단축키
^X    # 종료
^O    # 저장
^W    # 검색
^K    # 줄 잘라내기
^U    # 붙여넣기
^J    # 정렬
^T    # 맞춤법 검사
```

---

## 텍스트 비교

### diff - 파일 차이

```bash
# 기본 비교
$ diff file1.txt file2.txt

# 나란히 비교
$ diff -y file1.txt file2.txt

# 통합 형식 (패치 파일용)
$ diff -u file1.txt file2.txt

# 컨텍스트 형식
$ diff -c file1.txt file2.txt

# 디렉토리 비교
$ diff -r dir1/ dir2/

# 간단한 출력 (다른지 여부만)
$ diff -q file1.txt file2.txt

# 대소문자 무시
$ diff -i file1.txt file2.txt

# 공백 무시
$ diff -w file1.txt file2.txt

# 색상 표시
$ diff --color file1.txt file2.txt

# 패치 파일 생성
$ diff -u original.txt modified.txt > changes.patch

# 패치 적용
$ patch original.txt < changes.patch
```

### comm - 정렬된 파일 비교

```bash
# 세 열로 출력: file1만, file2만, 공통
$ comm file1.txt file2.txt

# file1만
$ comm -12 file1.txt file2.txt

# file2만
$ comm -13 file1.txt file2.txt

# 공통 줄만
$ comm -23 file1.txt file2.txt

# 파일은 먼저 정렬되어야 함
$ sort file1.txt > sorted1.txt
$ sort file2.txt > sorted2.txt
$ comm sorted1.txt sorted2.txt
```

---

## 실전 예제

### 예제 1: 로그 분석

```bash
# 에러 로그만 추출
$ grep -i "error" /var/log/syslog

# 가장 빈번한 에러 top 10
$ grep -i "error" /var/log/syslog | awk '{print $5}' | sort | uniq -c | sort -rn | head -10

# 특정 시간대 로그
$ awk '/Nov 17 12:/' /var/log/syslog
```

### 예제 2: CSV 처리

```bash
# 두 번째 열만 추출
$ cut -d',' -f2 data.csv

# 특정 조건 필터링
$ awk -F',' '$3 > 100 {print $1,$2}' data.csv

# 합계 계산
$ awk -F',' '{sum += $2} END {print sum}' data.csv
```

### 예제 3: 텍스트 정제

```bash
# 중복 제거
$ sort file.txt | uniq > cleaned.txt

# 빈 줄 제거
$ grep -v "^$" file.txt

# 공백 정리
$ cat file.txt | tr -s ' ' | sed 's/^ //;s/ $//'

# 소문자 변환
$ cat file.txt | tr 'A-Z' 'a-z'
```

---

## 요약

텍스트 처리의 강력한 도구들:

- **grep/awk/sed**: 검색, 필터링, 편집
- **sort/uniq/wc**: 정렬, 중복 제거, 통계
- **cut/paste/join**: 열 조작
- **tr**: 문자 변환
- **diff/comm**: 파일 비교

이 도구들을 조합하면 복잡한 텍스트 처리 작업을 쉽게 수행할 수 있습니다.

---

[다음: 시스템 관리 명령어 →](system.md)

[← 기본 명령어로 돌아가기](basic.md)

[← 목차로 돌아가기](../README.md)

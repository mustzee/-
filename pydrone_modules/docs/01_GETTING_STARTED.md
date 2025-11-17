# pyDrone 시작하기 - 완전 기초 가이드

> pyDrone을 개봉부터 Claude Code 연동까지 단계별 완벽 가이드

## 📦 Step 1: 개봉 및 하드웨어 확인

### 박스 안 구성품

```
✅ pyDrone 메인보드 (ESP32-S3)
✅ 프로펠러 4개 (A형 2개, B형 2개)
✅ 모터 4개 (이미 장착됨)
✅ 배터리 (400mAh 3.7V)
✅ USB-C 케이블
✅ 예비 프로펠러
✅ 드라이버 (선택)
```

### 하드웨어 점검

```bash
# 점검 체크리스트
□ 프로펠러가 손상되지 않았는지 확인
□ 모터가 4개 모두 단단히 고정되었는지 확인
□ 배터리 커넥터 확인
□ USB-C 포트가 깨끗한지 확인
□ LED가 보드에 있는지 확인
```

---

## 🔌 Step 2: 첫 전원 켜기

### 배터리 충전 (매우 중요!)

```
1. USB-C 케이블을 pyDrone에 연결
2. 컴퓨터나 5V 충전기에 연결
3. 충전 LED 확인:
   - 빨간색 LED: 충전 중
   - 녹색 LED: 충전 완료
4. 첫 충전은 최소 1시간 이상!
```

⚠️ **주의사항:**
- 과방전된 배터리는 충전하지 마세요
- 충전 중에는 비행하지 마세요
- 배터리가 부풀어 오르면 즉시 사용 중지

### 전원 켜기

```
1. 배터리를 pyDrone에 연결 (커넥터 확인)
2. 전원 스위치 ON
3. LED가 깜빡이는지 확인
4. WiFi AP가 생성되는지 확인 (약 10초 소요)
```

---

## 📡 Step 3: WiFi 연동 (핵심!)

### 방법 1: AP 모드 (기본 모드, 가장 쉬움!)

pyDrone이 WiFi 공유기처럼 동작합니다.

```
1. pyDrone 전원 ON
2. 스마트폰/노트북의 WiFi 설정 열기
3. WiFi 네트워크 검색
4. "pyDrone-XXXX" 또는 "ESP32-XXXX" 찾기
5. 연결 (비밀번호: 기본값은 "12345678" 또는 없음)
6. 연결 완료!

pyDrone IP: 192.168.4.1 (기본값)
```

#### 📱 스마트폰으로 연결 테스트

```bash
# WiFi 연결 후 브라우저에서:
http://192.168.4.1

# 또는 ping 테스트 (터미널 앱 사용)
ping 192.168.4.1
```

성공하면 응답이 옵니다!

### 방법 2: Station 모드 (집 WiFi에 연결)

pyDrone이 집 WiFi에 연결됩니다.

```python
# main.py에 추가할 코드
import network

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f'WiFi 연결 중: {ssid}')
        wlan.connect(ssid, password)

        # 연결 대기 (최대 10초)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print('.', end='')
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print(f'\nWiFi 연결 완료!')
        print(f'IP 주소: {wlan.ifconfig()[0]}')
        return wlan.ifconfig()[0]
    else:
        print('\nWiFi 연결 실패!')
        return None

# 사용 예제
ip = connect_wifi('YourWiFiName', 'YourPassword')
```

⚠️ **처음에는 AP 모드를 추천합니다!**
- 설정이 쉽고 확실합니다
- IP 주소를 찾을 필요가 없습니다
- 연결이 안정적입니다

---

## 💻 Step 4: 로컬 컴퓨터와 연결

### 연결 방식 비교

| 방식 | 장점 | 단점 | 추천도 |
|------|------|------|--------|
| **USB 케이블** | 가장 안정적, 빠름 | 케이블 필요, 비행 중 불가 | ⭐⭐⭐⭐⭐ |
| **WiFi (AP)** | 무선, 비행 중 가능 | 약간 느림, 거리 제한 | ⭐⭐⭐⭐ |
| **WiFi (Station)** | 집 네트워크 사용 | 설정 복잡, IP 찾기 필요 | ⭐⭐⭐ |

### Option A: USB 케이블 연결 (권장!)

#### Windows

```bash
1. USB-C 케이블로 pyDrone과 컴퓨터 연결
2. 장치 관리자 열기 (Win + X → 장치 관리자)
3. "포트 (COM & LPT)" 확인
4. "USB Serial Port (COM3)" 같은 항목 찾기
5. COM 포트 번호 기억 (예: COM3)
```

드라이버가 없다면:
```bash
# CP210x USB to UART Bridge 드라이버 설치
https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
```

#### macOS

```bash
# 터미널에서 확인
ls /dev/tty.*

# 출력 예시:
/dev/tty.usbserial-0001
/dev/tty.SLAB_USBtoUART

# 이 경로를 기억하세요!
```

#### Linux

```bash
# 터미널에서 확인
ls /dev/ttyUSB*

# 출력 예시:
/dev/ttyUSB0

# 권한 설정 (중요!)
sudo usermod -a -G dialout $USER
# 로그아웃 후 다시 로그인 필요
```

### Option B: WiFi 연결

```bash
1. pyDrone WiFi에 연결 (위 Step 3 참고)
2. IP 주소 확인: 192.168.4.1 (AP 모드)
3. WebREPL 활성화 (아래 설명 참고)
```

---

## 🛠️ Step 5: 개발 환경 설정

### 필수 소프트웨어 설치

#### 1. Python 설치 (필수)

```bash
# Python 3.8 이상 필요
python3 --version

# 없다면 설치:
# Windows: https://python.org
# macOS: brew install python3
# Linux: sudo apt install python3
```

#### 2. MicroPython 도구 설치

```bash
# esptool (펌웨어 업로드용)
pip3 install esptool

# mpremote (MicroPython 원격 제어)
pip3 install mpremote

# rshell (파일 전송)
pip3 install rshell
```

#### 3. IDE 선택

**Option A: Thonny (초보자 추천!)**

```bash
# 설치
# Windows/macOS: https://thonny.org 에서 다운로드
# Linux:
sudo apt install thonny

# Thonny 설정:
1. Thonny 실행
2. 우측 하단 "Python 3.x" 클릭
3. "MicroPython (ESP32)" 선택
4. Port 선택 (COM3 또는 /dev/ttyUSB0)
5. 연결 완료!
```

**Option B: VS Code (고급)**

```bash
# VS Code 설치
# https://code.visualstudio.com

# 확장 설치:
1. Pymakr 또는 MicroPico 확장
2. Python 확장
```

---

## 🚀 Step 6: MicroPython 펌웨어 설치

### 펌웨어 다운로드

```bash
# pyDrone 공식 펌웨어
https://github.com/01studio-lab/pyDrone/releases

# 또는
https://download.01studio.cc/project/pyDrone/pyDrone.html

# 파일 이름 예시:
pydrone_firmware_v1.0.bin
```

### 펌웨어 업로드

#### 방법 1: esptool 사용 (권장)

```bash
# 1. 플래시 메모리 지우기 (최초 1회)
esptool.py --chip esp32s3 --port COM3 erase_flash

# 2. 펌웨어 업로드
esptool.py --chip esp32s3 \
  --port COM3 \
  --baud 460800 \
  write_flash -z 0x0 pydrone_firmware_v1.0.bin

# macOS/Linux:
esptool.py --chip esp32s3 \
  --port /dev/ttyUSB0 \
  --baud 460800 \
  write_flash -z 0x0 pydrone_firmware_v1.0.bin
```

성공 메시지:
```
Hash of data verified.
Leaving...
Hard resetting via RTS pin...
```

#### 방법 2: Thonny 사용 (GUI)

```
1. Thonny 열기
2. Tools → Options → Interpreter
3. "Install or update MicroPython (esptool)"
4. Port 선택
5. "Install" 클릭
6. 펌웨어 파일 선택
7. 완료 대기
```

### 연결 테스트

```python
# Thonny의 Shell에서 입력:
>>> print("Hello pyDrone!")
Hello pyDrone!

>>> import sys
>>> sys.platform
'esp32'

# 성공!
```

---

## 📝 Step 7: 첫 코드 업로드

### 간단한 LED 깜빡이기

```python
# blink.py
from machine import Pin
import time

# LED 핀 설정 (pyDrone 보드에 따라 다를 수 있음)
led = Pin(2, Pin.OUT)  # GPIO 2

print("LED 깜빡이기 시작!")

for i in range(10):
    led.value(1)  # LED ON
    print(f"깜빡 {i+1}: ON")
    time.sleep(0.5)

    led.value(0)  # LED OFF
    print(f"깜빡 {i+1}: OFF")
    time.sleep(0.5)

print("완료!")
```

### 파일 업로드 방법

#### Thonny 사용

```
1. blink.py 파일 열기
2. File → Save As...
3. "MicroPython device" 선택
4. 파일명: main.py (자동 실행됨)
5. Save 클릭
6. 재부팅하면 자동 실행!
```

#### rshell 사용

```bash
# rshell 연결
rshell -p COM3  # Windows
rshell -p /dev/ttyUSB0  # Linux/macOS

# pyDrone에 연결됨
> ls /pyboard
# 파일 목록 표시

> cp blink.py /pyboard/main.py
# 파일 복사

> repl
# REPL 모드로 전환 (Ctrl+X로 나가기)
```

---

## 🎮 Step 8: pyDrone 기본 테스트

### 모터 테스트 (프로펠러 제거 필수!)

⚠️ **프로펠러를 반드시 제거하세요!**

```python
# motor_test.py
from machine import Pin, PWM
import time

# 모터 핀 (pyDrone 하드웨어 확인 필요)
# 예시 핀 번호 - 실제 하드웨어 매뉴얼 참고!
motor1 = PWM(Pin(25), freq=50)
motor2 = PWM(Pin(26), freq=50)
motor3 = PWM(Pin(27), freq=50)
motor4 = PWM(Pin(14), freq=50)

def set_motor_speed(motor, speed):
    """
    모터 속도 설정
    speed: 0 (정지) ~ 100 (최대)
    """
    # PWM duty: 대략 0 ~ 1023
    duty = int(speed * 10.23)
    motor.duty(duty)

print("모터 테스트 시작!")
print("⚠️ 프로펠러가 제거되었는지 확인하세요!")
time.sleep(3)

# 각 모터를 순서대로 테스트
motors = [motor1, motor2, motor3, motor4]

for i, motor in enumerate(motors, 1):
    print(f"모터 {i} 테스트...")

    # 천천히 속도 증가
    for speed in range(0, 31, 10):
        set_motor_speed(motor, speed)
        print(f"  속도: {speed}%")
        time.sleep(1)

    # 정지
    set_motor_speed(motor, 0)
    print(f"  모터 {i} 정지")
    time.sleep(1)

print("모터 테스트 완료!")
```

### 센서 테스트

```python
# sensor_test.py
import time

# pyDrone의 센서 모듈 import
# (펌웨어에 포함되어 있어야 함)
try:
    from mpu6050 import MPU6050
    from spl06 import SPL06
    from qmc5883l import QMC5883L
except ImportError:
    print("센서 라이브러리가 없습니다!")
    print("pyDrone 펌웨어를 확인하세요.")

# 센서 초기화
print("센서 초기화 중...")

try:
    mpu = MPU6050()
    print("✓ MPU6050 (가속도/자이로) 초기화 완료")
except:
    print("✗ MPU6050 초기화 실패")

try:
    baro = SPL06()
    print("✓ SPL06 (기압계) 초기화 완료")
except:
    print("✗ SPL06 초기화 실패")

try:
    mag = QMC5883L()
    print("✓ QMC5883L (나침반) 초기화 완료")
except:
    print("✗ QMC5883L 초기화 실패")

print("\n센서 데이터 읽기 (10초)...")

for i in range(10):
    # 가속도/자이로 데이터
    accel = mpu.get_accel()
    gyro = mpu.get_gyro()

    # 기압 데이터
    pressure = baro.get_pressure()
    temperature = baro.get_temperature()

    # 나침반 데이터
    mag_data = mag.get_data()

    print(f"\n[{i+1}/10]")
    print(f"  가속도: X={accel['x']:.2f}, Y={accel['y']:.2f}, Z={accel['z']:.2f} g")
    print(f"  자이로: X={gyro['x']:.2f}, Y={gyro['y']:.2f}, Z={gyro['z']:.2f} °/s")
    print(f"  기압: {pressure:.2f} Pa, 온도: {temperature:.2f} °C")
    print(f"  나침반: X={mag_data['x']}, Y={mag_data['y']}, Z={mag_data['z']}")

    time.sleep(1)

print("\n센서 테스트 완료!")
```

---

## 📊 정리: 연결 방법 요약

```
┌─────────────────────────────────────────────────────┐
│                  연결 방법 선택                      │
└─────────────────────────────────────────────────────┘

1️⃣ 개발/디버깅 단계 (코드 작성 중)
   ├─ USB 케이블 연결 ✅ 추천!
   ├─ Thonny 또는 VS Code 사용
   ├─ 빠르고 안정적
   └─ 실시간 디버깅 가능

2️⃣ 무선 테스트 단계 (비행 테스트)
   ├─ WiFi AP 모드 ✅ 추천!
   ├─ IP: 192.168.4.1
   ├─ WebREPL 사용
   └─ 비행 중 데이터 확인 가능

3️⃣ 프로덕션 배포 (완성된 코드)
   ├─ main.py에 코드 저장
   ├─ 자동 실행
   └─ USB 연결 필요 없음
```

---

## 다음 단계

다음 가이드를 참고하세요:

- `02_CLAUDE_CODE_WORKFLOW.md` - Claude Code와 함께 개발하는 방법
- `03_WIFI_ADVANCED.md` - WiFi 고급 설정 및 WebREPL
- `04_DEBUGGING.md` - 디버깅 및 문제 해결

---

## 🆘 문제 해결

### Q: pyDrone이 켜지지 않아요
```
✓ 배터리가 충전되었는지 확인
✓ 배터리 커넥터가 제대로 연결되었는지 확인
✓ 전원 스위치가 ON인지 확인
```

### Q: WiFi가 보이지 않아요
```
✓ 전원 켜고 10초 대기
✓ pyDrone-XXXX 또는 ESP32-XXXX 검색
✓ 2.4GHz WiFi 대역 확인 (5GHz 불가)
```

### Q: USB 연결이 안 돼요
```
✓ USB 케이블 확인 (데이터 케이블인지)
✓ 드라이버 설치 (CP210x)
✓ 다른 USB 포트 시도
```

### Q: 펌웨어 업로드가 실패해요
```
✓ esptool 최신 버전인지 확인
✓ 보드레이트 낮추기 (115200)
✓ Flash 지우기 먼저 실행
```

---

**축하합니다! pyDrone 기본 설정을 완료했습니다!** 🎉

이제 Claude Code와 함께 본격적인 개발을 시작할 준비가 되었습니다!

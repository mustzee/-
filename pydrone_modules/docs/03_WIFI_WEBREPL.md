# WiFi & WebREPL 고급 가이드

> pyDrone 무선 개발을 위한 완벽 가이드

## 🌐 WebREPL이란?

WebREPL = Web-based REPL (Read-Eval-Print Loop)

```
브라우저에서 pyDrone에 접속해서:
- Python 코드 실행
- 파일 업로드/다운로드
- 실시간 디버깅

USB 케이블 없이 무선으로 개발 가능!
```

---

## 🚀 WebREPL 설정 (한 번만!)

### Step 1: pyDrone에 USB 연결

```bash
# Thonny 또는 rshell로 연결
rshell -p /dev/ttyUSB0

# REPL 모드로 진입
> repl
>>>
```

### Step 2: WebREPL 설정

```python
>>> import webrepl_setup

# 출력:
WebREPL daemon auto-start status: disabled

Would you like to (E)nable or (D)isable it running on boot?
(Empty line to quit)
> E  # Enable 입력

To enable WebREPL, you must set password for it
New password (4-9 chars): ********  # 비밀번호 입력 (예: pydrone)
Confirm password: ********  # 다시 입력

Changes will be activated after reboot
Would you like to reboot now? (y/n)
> y  # 재부팅
```

### Step 3: WiFi 정보 확인

재부팅 후:

```python
>>> import network
>>> ap = network.WLAN(network.AP_IF)
>>> ap.active()
True
>>> ap.ifconfig()
('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8')

# IP 주소: 192.168.4.1 (기본값)
```

---

## 💻 WebREPL 사용하기

### 방법 1: 웹 브라우저 (가장 쉬움!)

```
1. pyDrone WiFi에 연결
   - SSID: pyDrone-XXXX 또는 ESP32-XXXX
   - 비밀번호: 12345678 (기본값)

2. 브라우저 열기
   - Chrome, Firefox, Edge 등

3. WebREPL 접속
   - http://micropython.org/webrepl/
   또는
   - https://github.com/micropython/webrepl
     다운로드 후 webrepl.html 열기

4. 연결
   - ws://192.168.4.1:8266 입력
   - Connect 클릭
   - 비밀번호 입력 (위에서 설정한 비밀번호)

5. 연결 완료!
   >>>
```

### 방법 2: webrepl CLI (고급 사용자)

```bash
# webrepl CLI 설치
pip3 install webrepl

# 연결
webrepl
# 또는
webrepl 192.168.4.1

# 비밀번호 입력
Password: ********

# 연결 완료
>>>
```

---

## 📤 WebREPL로 파일 업로드

### GUI 방법 (webrepl.html)

```
1. WebREPL 웹페이지에서
2. "Send a file" 섹션 찾기
3. "Choose File" 클릭
4. 업로드할 파일 선택 (예: lib/pid_controller.py)
5. "Send to device" 클릭
6. 업로드 진행률 표시
7. 완료!

확인:
>>> import os
>>> os.listdir()
['boot.py', 'webrepl_cfg.py', 'pid_controller.py']
```

### CLI 방법

```python
# Python 스크립트로 업로드

import webrepl
import sys

# 파일 업로드
webrepl.send_file('local_file.py', 'remote_file.py', '192.168.4.1', 'password')
```

또는 전용 스크립트:

```bash
# upload.py
import sys
import os

sys.path.append('/path/to/webrepl')
import websocket_helper

def upload_file(local_path, remote_path, ip='192.168.4.1', password='pydrone'):
    """파일 업로드"""
    print(f"Uploading {local_path} → {remote_path}")
    # WebREPL 파일 전송 프로토콜 사용
    # (구현 생략 - webrepl 라이브러리 참고)
    print("Upload complete!")

if __name__ == '__main__':
    upload_file('lib/pid_controller.py', '/lib/pid_controller.py')
```

---

## 🔧 고급 WiFi 설정

### Station 모드로 전환 (집 WiFi 사용)

```python
# boot.py 또는 main.py에 추가

import network
import time

def connect_to_wifi(ssid, password, timeout=10):
    """집 WiFi에 연결"""
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if not sta.isconnected():
        print(f'WiFi 연결 중: {ssid}')
        sta.connect(ssid, password)

        # 연결 대기
        start = time.time()
        while not sta.isconnected():
            if time.time() - start > timeout:
                print('WiFi 연결 타임아웃!')
                return None
            print('.', end='')
            time.sleep(0.5)

    print(f'\nWiFi 연결 완료!')
    print(f'IP: {sta.ifconfig()[0]}')
    print(f'Gateway: {sta.ifconfig()[2]}')
    print(f'DNS: {sta.ifconfig()[3]}')

    return sta.ifconfig()[0]

# 사용
ip = connect_to_wifi('YourWiFiName', 'YourPassword')

# WebREPL 시작
import webrepl
webrepl.start()

print(f'\nWebREPL 접속 주소: ws://{ip}:8266')
```

### AP + Station 동시 사용 (추천!)

```python
# dual_wifi.py

import network
import time

def setup_dual_wifi(sta_ssid, sta_password):
    """AP 모드와 Station 모드 동시 활성화"""

    # AP 모드 (항상 켜짐)
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='pyDrone-MyDrone', password='12345678')
    print(f'AP 모드: {ap.ifconfig()[0]}')

    # Station 모드 (집 WiFi)
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    if sta_ssid:
        sta.connect(sta_ssid, sta_password)
        timeout = 10
        while not sta.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

        if sta.isconnected():
            print(f'Station 모드: {sta.ifconfig()[0]}')
        else:
            print('Station 모드: 연결 실패')

    return ap.ifconfig()[0], sta.ifconfig()[0] if sta.isconnected() else None

# 사용
ap_ip, sta_ip = setup_dual_wifi('YourWiFi', 'YourPassword')

# WebREPL 시작
import webrepl
webrepl.start()

print('\n접속 방법:')
print(f'1. pyDrone WiFi 연결 → ws://{ap_ip}:8266')
if sta_ip:
    print(f'2. 집 WiFi 사용 → ws://{sta_ip}:8266')
```

이렇게 하면:
- pyDrone WiFi로 직접 연결 가능 (항상)
- 집 WiFi로도 연결 가능 (인터넷 사용 가능)

### WiFi 신호 강도 확인

```python
>>> import network
>>> sta = network.WLAN(network.STA_IF)
>>> sta.status('rssi')
-45  # dBm (높을수록 좋음, -30이 최고)

# 신호 강도 해석:
# -30 dBm: 최고 (excellent)
# -67 dBm: 좋음 (very good)
# -70 dBm: 보통 (okay)
# -80 dBm: 약함 (not good)
# -90 dBm: 매우 약함 (unusable)
```

---

## 🚁 비행 중 무선 모니터링

### 실시간 텔레메트리

```python
# telemetry_server.py - pyDrone에서 실행

import socket
import json
import time
from lib.sensor_fusion import SensorFusion

# 센서 초기화
sensors = SensorFusion()

# UDP 서버 설정
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 9999)
print(f'텔레메트리 서버 시작: {server_address}')

try:
    while True:
        # 센서 데이터 읽기
        data = sensors.read_all()

        # JSON으로 변환
        telemetry = {
            'time': time.ticks_ms(),
            'roll': data['roll'],
            'pitch': data['pitch'],
            'yaw': data['yaw'],
            'altitude': data['altitude'],
            'battery': data.get('battery', 0)
        }

        # UDP로 전송 (브로드캐스트)
        message = json.dumps(telemetry).encode()
        sock.sendto(message, ('192.168.4.255', 9999))

        time.sleep(0.1)  # 10Hz

except KeyboardInterrupt:
    print('서버 종료')
    sock.close()
```

PC에서 수신:

```python
# receive_telemetry.py - PC에서 실행

import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999))
sock.settimeout(1.0)

print("텔레메트리 수신 중...")

try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            telemetry = json.loads(data.decode())

            print(f"\r[{telemetry['time']/1000:.1f}s] "
                  f"Roll: {telemetry['roll']:6.2f}° "
                  f"Pitch: {telemetry['pitch']:6.2f}° "
                  f"Yaw: {telemetry['yaw']:6.2f}° "
                  f"Alt: {telemetry['altitude']:5.1f}cm "
                  f"Bat: {telemetry['battery']}%", end='')

        except socket.timeout:
            print("\n연결 끊김...")

except KeyboardInterrupt:
    print("\n수신 종료")
    sock.close()
```

### 실시간 그래프

```python
# real_time_plot.py - PC에서 실행

import socket
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# 데이터 버퍼
max_points = 200
times = deque(maxlen=max_points)
rolls = deque(maxlen=max_points)
pitches = deque(maxlen=max_points)
yaws = deque(maxlen=max_points)

# 그래프 설정
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))

line_roll, = ax1.plot([], [], 'r-', label='Roll')
line_pitch, = ax2.plot([], [], 'g-', label='Pitch')
line_yaw, = ax3.plot([], [], 'b-', label='Yaw')

ax1.set_ylabel('Roll (°)')
ax2.set_ylabel('Pitch (°)')
ax3.set_ylabel('Yaw (°)')
ax3.set_xlabel('Time (s)')

for ax in [ax1, ax2, ax3]:
    ax.grid(True)
    ax.legend()

# UDP 소켓
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 9999))
sock.settimeout(0.01)

def update_plot(frame):
    """그래프 업데이트"""
    try:
        data, _ = sock.recvfrom(1024)
        telemetry = json.loads(data.decode())

        t = telemetry['time'] / 1000.0
        times.append(t)
        rolls.append(telemetry['roll'])
        pitches.append(telemetry['pitch'])
        yaws.append(telemetry['yaw'])

        # 그래프 업데이트
        line_roll.set_data(times, rolls)
        line_pitch.set_data(times, pitches)
        line_yaw.set_data(times, yaws)

        # 축 범위 자동 조정
        for ax, data in [(ax1, rolls), (ax2, pitches), (ax3, yaws)]:
            if len(data) > 0:
                ax.set_xlim(min(times), max(times))
                ax.set_ylim(min(data) - 5, max(data) + 5)

    except socket.timeout:
        pass

    return line_roll, line_pitch, line_yaw

# 애니메이션 시작
ani = animation.FuncAnimation(fig, update_plot, interval=50, blit=True)
plt.tight_layout()
plt.show()

sock.close()
```

---

## 🔐 보안 설정

### WebREPL 비밀번호 변경

```python
>>> import webrepl
>>> webrepl.password('new_strong_password')
Password updated. Restart to apply changes.

>>> import machine
>>> machine.reset()
```

### WiFi AP 보안 강화

```python
# boot.py

import network

ap = network.WLAN(network.AP_IF)
ap.active(True)

# 강력한 설정
ap.config(
    essid='MyDrone-Secret',      # SSID 변경
    password='VeryStr0ngP@ss!',  # 강력한 비밀번호
    authmode=network.AUTH_WPA2_PSK,  # WPA2
    hidden=False                 # True로 하면 SSID 숨김
)

print(f'AP 설정 완료: {ap.config("essid")}')
```

### MAC 필터링 (고급)

```python
# 특정 디바이스만 연결 허용
ALLOWED_MACS = [
    'AA:BB:CC:DD:EE:FF',  # 내 노트북
    '11:22:33:44:55:66',  # 내 스마트폰
]

# 연결 시도 시 MAC 확인
# (MicroPython은 기본 지원 안 함, 펌웨어 수정 필요)
```

---

## 📊 WiFi 성능 최적화

### 전송 속도 테스트

```python
# speed_test.py - pyDrone에서 실행

import socket
import time

def speed_test():
    """WiFi 전송 속도 측정"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(1)

    print('속도 테스트 서버 시작...')
    print('PC에서 연결하세요: nc 192.168.4.1 8080')

    conn, addr = sock.accept()
    print(f'연결됨: {addr}')

    # 1MB 데이터 전송
    data = b'X' * 1024  # 1KB
    total_sent = 0
    start = time.ticks_ms()

    for _ in range(1024):  # 1024 * 1KB = 1MB
        conn.send(data)
        total_sent += len(data)

    elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000.0
    speed = total_sent / elapsed / 1024  # KB/s

    print(f'전송 완료: {total_sent} bytes')
    print(f'시간: {elapsed:.2f}s')
    print(f'속도: {speed:.2f} KB/s')

    conn.close()
    sock.close()

speed_test()
```

PC에서:
```bash
# 데이터 수신 및 속도 측정
nc 192.168.4.1 8080 > /dev/null
```

### 거리별 성능

```
0-5m:   최고 (Full speed, -30 dBm)
5-10m:  좋음 (Good, -50 dBm)
10-15m: 보통 (Okay, -70 dBm)
15-20m: 약함 (Weak, -80 dBm)
20m+:   불안정 (Unstable)

장애물 (벽, 문):
- 나무 벽: -5 dBm 손실
- 콘크리트 벽: -10~15 dBm 손실
- 금속: -20+ dBm 손실
```

---

## 🛠️ 문제 해결

### Q: WebREPL이 연결 안 돼요

```python
# 1. WebREPL 상태 확인
>>> import webrepl
>>> webrepl.start()  # 수동 시작

# 2. 방화벽 확인 (PC)
# 포트 8266 허용 확인

# 3. WiFi 연결 확인
>>> import network
>>> ap = network.WLAN(network.AP_IF)
>>> ap.active()
True  # False면 ap.active(True)

# 4. IP 확인
>>> ap.ifconfig()
('192.168.4.1', ...)

# 5. 재부팅
>>> import machine
>>> machine.reset()
```

### Q: 파일 업로드가 실패해요

```
원인:
- 파일이 너무 큼 (>100KB)
- 메모리 부족
- 연결 불안정

해결:
1. 파일을 작게 나누기
2. pyDrone 재부팅 후 재시도
3. USB로 업로드
```

### Q: WiFi 신호가 약해요

```
해결책:
1. 거리 줄이기 (10m 이내)
2. 장애물 제거
3. 외부 안테나 추가 (하드웨어 수정)
4. 2.4GHz 채널 변경:

>>> ap.config(channel=6)  # 1~13
```

---

## 요약

```
┌─────────────────────────────────────────┐
│         WiFi 개발 베스트 프랙티스        │
└─────────────────────────────────────────┘

개발 단계:
✓ USB 케이블로 개발 (빠르고 안정적)

테스트 단계:
✓ WebREPL로 무선 디버깅

비행 단계:
✓ UDP 텔레메트리로 실시간 모니터링

프로덕션:
✓ 독립 실행 (main.py 자동 실행)
```

**무선 개발의 자유를 누리세요!** 🚀

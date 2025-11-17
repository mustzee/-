# pyDrone 빠른 시작 가이드 (5분!)

> 드론을 구매하고 처음 시작하는 분들을 위한 초간단 가이드

## ⚡ 5분 만에 시작하기

### 1단계: 하드웨어 준비 (1분)

```
□ 프로펠러 제거하고 보관 (나중에 장착!)
□ 배터리 충전 (USB-C 케이블)
□ 충전 중 LED 확인 (빨강 → 녹색)
```

### 2단계: USB 연결 (1분)

```
□ USB-C 케이블로 PC 연결
□ 포트 확인:
  - Windows: 장치 관리자에서 COM3 등 확인
  - Mac: /dev/tty.usbserial* 확인
  - Linux: /dev/ttyUSB0 확인
```

### 3단계: Thonny 설치 (2분)

```
1. https://thonny.org 접속
2. 다운로드 및 설치
3. Thonny 실행
4. 우측 하단에서 "MicroPython (ESP32)" 선택
5. 포트 선택 (COM3 또는 /dev/ttyUSB0)
```

### 4단계: 첫 코드 실행 (1분)

Thonny Shell에서:

```python
>>> print("Hello pyDrone!")
Hello pyDrone!

>>> from machine import Pin
>>> led = Pin(2, Pin.OUT)
>>> led.value(1)  # LED 켜기
>>> led.value(0)  # LED 끄기
```

LED가 깜빡이면 성공! 🎉

---

## 🚀 다음 단계

### 초보자 (1-2주차)

```
1. 센서 테스트
   → docs/01_GETTING_STARTED.md

2. 모터 테스트 (프로펠러 없이!)
   → examples/motor_test.py

3. LED 깜빡이기
   → examples/blink.py
```

### 중급자 (3-4주차)

```
1. PID 컨트롤러 학습
   → lib/pid_controller.py

2. 센서 퓨전 이해
   → lib/sensor_fusion.py

3. WiFi 연결
   → docs/03_WIFI_WEBREPL.md
```

### 고급자 (5주 이상)

```
1. 자율 비행 개발
   → lib/waypoint_navigation.py

2. Claude Code 연동
   → docs/02_CLAUDE_CODE_WORKFLOW.md

3. 커스텀 기능 개발
   → examples/custom_flight_modes.py
```

---

## ❓ 자주 묻는 질문

### Q: 드론이 켜지지 않아요

```
A: 배터리 충전 확인
   - USB 연결 시 LED 깜빡이는지 확인
   - 최소 30분 충전 후 재시도
```

### Q: USB가 인식 안 돼요

```
A: 드라이버 설치
   - Windows: CP210x 드라이버 필요
   - https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
```

### Q: 비행 테스트는 언제 하나요?

```
A: 충분히 연습한 후!
   1. 센서 테스트 완료 (2주)
   2. 모터 제어 이해 (2주)
   3. PID 튜닝 완료 (1주)
   4. 안전한 환경에서 테스트
```

### Q: Claude Code는 어떻게 사용하나요?

```
A: docs/02_CLAUDE_CODE_WORKFLOW.md 참고
   - Claude에게 코드 요청
   - 로컬 PC에서 개발
   - pyDrone에 업로드
   - 테스트 및 피드백
```

---

## 📚 전체 문서

```
docs/
├── QUICK_START.md           ← 지금 보고 있는 문서
├── 01_GETTING_STARTED.md    ← 상세 시작 가이드
├── 02_CLAUDE_CODE_WORKFLOW.md ← Claude와 개발하기
├── 03_WIFI_WEBREPL.md       ← 무선 개발
└── 04_DEBUGGING_TIPS.md     ← 문제 해결
```

---

## 🆘 도움이 필요하면

1. **문서 확인**: `docs/` 폴더의 상세 가이드
2. **예제 실행**: `examples/` 폴더의 샘플 코드
3. **Claude에게 질문**: "pyDrone에서 ~하는 방법을 알려줘"
4. **커뮤니티**: https://forum.01studio.cc

---

## ✅ 체크리스트

시작 전:
```
□ 배터리 충전 완료
□ USB 연결 확인
□ Thonny 설치 완료
□ 첫 코드 실행 성공
```

다음 단계:
```
□ 센서 테스트 (examples/sensor_test.py)
□ 모터 테스트 (examples/motor_test.py)
□ PID 학습 (lib/pid_controller.py)
□ WiFi 설정 (docs/03_WIFI_WEBREPL.md)
```

---

**축하합니다! pyDrone 여정의 시작입니다!** 🚁

Claude Code와 함께 재미있게 개발하세요! 🤖✨

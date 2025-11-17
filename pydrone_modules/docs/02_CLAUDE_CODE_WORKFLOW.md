# Claude Code와 pyDrone 개발 워크플로우

> Claude Code를 활용한 효율적인 pyDrone 개발 방법

## 🎯 개발 흐름 개요

```
┌─────────────────────────────────────────────────────────┐
│          Claude Code + pyDrone 개발 사이클              │
└─────────────────────────────────────────────────────────┘

1. 💬 Claude Code에게 기능 설명
   "PID 컨트롤러를 개선해줘"

2. 📝 Claude가 코드 작성 (로컬 PC)
   /home/user/pydrone_project/pid_controller.py

3. 🧪 로컬에서 문법 검사 및 시뮬레이션

4. 📤 pyDrone에 업로드
   USB 또는 WiFi로 전송

5. ✈️ 실제 하드웨어에서 테스트
   모터, 센서 등 실제 동작 확인

6. 📊 결과 분석 및 피드백
   "Roll 값이 불안정해" → Claude에게 피드백

7. 🔄 반복 개선
```

---

## 🚀 실전 워크플로우

### Phase 1: 프로젝트 셋업

#### Step 1: 로컬 개발 디렉토리 생성

```bash
# 프로젝트 디렉토리 만들기
mkdir ~/pydrone_project
cd ~/pydrone_project

# Git 초기화 (선택)
git init
git add .
git commit -m "Initial commit"

# 기본 구조 생성
mkdir -p {lib,config,tests,logs}

# 구조:
pydrone_project/
├── lib/                    # pyDrone에 업로드할 라이브러리
│   ├── pid_controller.py
│   ├── sensor_fusion.py
│   └── navigation.py
├── config/                 # 설정 파일
│   └── drone_config.py
├── tests/                  # 테스트 코드
│   └── test_pid.py
├── logs/                   # 비행 로그
├── main.py                # pyDrone 메인 파일
└── README.md
```

#### Step 2: Claude Code와 대화 시작

```
당신: "pyDrone 프로젝트를 시작하려고 해.
       PID 컨트롤러부터 만들어줄래?"

Claude: "네! pyDrone용 PID 컨트롤러를 만들어드리겠습니다.
        먼저 몇 가지 질문드릴게요..."
```

### Phase 2: 코드 개발 (Claude와 협업)

#### 패턴 1: 새 기능 개발

```
┌──────────────────────────────────────┐
│  당신 → Claude Code                  │
└──────────────────────────────────────┘

"pyDrone용 PID 컨트롤러를 만들어줘.
 - Roll, Pitch, Yaw, Throttle 4축
 - 실시간 게인 튜닝 가능
 - 안티 와인드업 기능
 - MicroPython으로 작성"

┌──────────────────────────────────────┐
│  Claude Code → 당신                  │
└──────────────────────────────────────┘

Claude가 다음 파일을 생성:
✓ lib/pid_controller.py
✓ tests/test_pid.py
✓ 사용 예제 포함

코드 설명:
- PID 클래스 구조
- 각 메서드 설명
- 사용법 예제
```

#### 패턴 2: 기존 코드 개선

```
┌──────────────────────────────────────┐
│  당신 → Claude Code                  │
└──────────────────────────────────────┘

"lib/pid_controller.py를 읽어보고
 다음을 개선해줘:
 1. 메모리 사용량 최적화
 2. 실행 속도 개선
 3. 주석 추가"

┌──────────────────────────────────────┐
│  Claude Code → 당신                  │
└──────────────────────────────────────┘

Claude가:
1. 파일 읽기
2. 문제점 분석
3. 개선된 코드 제시
4. 변경 사항 설명
```

#### 패턴 3: 버그 수정

```
┌──────────────────────────────────────┐
│  당신 → Claude Code                  │
└──────────────────────────────────────┘

"드론 테스트 중 이런 에러가 났어:

Traceback:
  File 'main.py', line 45
  ZeroDivisionError: division by zero

lib/pid_controller.py에서 dt가 0이 되는 것 같아"

┌──────────────────────────────────────┐
│  Claude Code → 당신                  │
└──────────────────────────────────────┘

Claude가:
1. 에러 원인 분석
2. 코드 검토
3. 수정 제안
4. 추가 방어 코드 제시
```

---

## 📤 pyDrone에 코드 업로드

### 방법 1: rshell 사용 (권장)

```bash
# Claude가 작성한 코드를 pyDrone에 업로드

# 1. rshell 연결
rshell -p /dev/ttyUSB0  # 또는 COM3

# 2. 디렉토리 생성
/home/user/pydrone_project> mkdir /pyboard/lib

# 3. 파일 복사
/home/user/pydrone_project> cp lib/pid_controller.py /pyboard/lib/
/home/user/pydrone_project> cp lib/sensor_fusion.py /pyboard/lib/
/home/user/pydrone_project> cp main.py /pyboard/

# 4. 파일 확인
/home/user/pydrone_project> ls /pyboard/lib
pid_controller.py
sensor_fusion.py

# 5. REPL로 테스트
/home/user/pydrone_project> repl
>>> from lib.pid_controller import PIDController
>>> pid = PIDController(kp=1.0, ki=0.1, kd=0.01)
>>> print(pid.get_gains())
{'kp': 1.0, 'ki': 0.1, 'kd': 0.01}
>>>
# Ctrl+X로 나가기
```

### 방법 2: mpremote 사용

```bash
# 한 번에 전체 프로젝트 업로드

# 파일 복사
mpremote cp lib/pid_controller.py :lib/pid_controller.py
mpremote cp lib/sensor_fusion.py :lib/sensor_fusion.py
mpremote cp main.py :main.py

# 실행 테스트
mpremote run main.py
```

### 방법 3: Thonny (GUI)

```
1. Thonny에서 파일 열기 (예: lib/pid_controller.py)
2. File → Save As...
3. "MicroPython device" 선택
4. 경로: /lib/pid_controller.py
5. Save
```

### 방법 4: 자동화 스크립트

Claude Code에게 요청:

```
"pyDrone에 코드를 자동으로 업로드하는
 스크립트를 만들어줘"
```

Claude가 만들어주는 스크립트:

```bash
#!/bin/bash
# upload_to_pydrone.sh

PORT="/dev/ttyUSB0"  # 또는 COM3

echo "pyDrone에 코드 업로드 중..."

# lib 디렉토리 업로드
echo "1. 라이브러리 업로드..."
mpremote cp -r lib :lib

# 설정 파일 업로드
echo "2. 설정 파일 업로드..."
mpremote cp config/drone_config.py :config.py

# 메인 파일 업로드
echo "3. 메인 파일 업로드..."
mpremote cp main.py :main.py

echo "✓ 업로드 완료!"

# 재부팅
echo "pyDrone 재부팅 중..."
mpremote reset

echo "✓ 완료!"
```

사용법:
```bash
chmod +x upload_to_pydrone.sh
./upload_to_pydrone.sh
```

---

## 🧪 테스트 워크플로우

### 1. 로컬 시뮬레이션 테스트

```python
# Claude에게 요청:
"PID 컨트롤러를 시뮬레이션으로 테스트하는
 코드를 만들어줘"

# Claude가 만들어주는 코드:
# tests/simulate_pid.py

import sys
sys.path.append('../lib')

from pid_controller import PIDController
import matplotlib.pyplot as plt
import numpy as np

def simulate_pid():
    """PID 컨트롤러 시뮬레이션"""
    pid = PIDController(kp=2.0, ki=0.1, kd=0.5)

    # 시뮬레이션 파라미터
    setpoint = 0  # 목표 각도
    current_value = 10  # 초기 각도 (10도 기울어짐)
    dt = 0.01  # 10ms

    # 기록용
    time_points = []
    values = []
    outputs = []

    # 5초 시뮬레이션
    for t in np.arange(0, 5, dt):
        # PID 출력 계산
        output = pid.update(setpoint, current_value, int(t * 1000))

        # 간단한 드론 모델 (1차 시스템)
        current_value += output * dt

        # 기록
        time_points.append(t)
        values.append(current_value)
        outputs.append(output)

    # 그래프 그리기
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_points, values, label='Current Value')
    plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
    plt.ylabel('Angle (degrees)')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(time_points, outputs, label='PID Output', color='orange')
    plt.xlabel('Time (s)')
    plt.ylabel('Control Output')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('pid_simulation.png')
    print("그래프 저장: pid_simulation.png")
    plt.show()

if __name__ == '__main__':
    simulate_pid()
```

실행:
```bash
cd tests
python3 simulate_pid.py
```

결과를 Claude에게 보여주고 피드백:
```
"시뮬레이션 결과를 봤는데 오버슈트가 심해.
 PID 게인을 조정해줄래?"
```

### 2. pyDrone 하드웨어 테스트

```python
# main.py - pyDrone에서 실행

from lib.pid_controller import AttitudePIDController
from lib.sensor_fusion import SensorFusion
import time

# 초기화
print("시스템 초기화...")
pid = AttitudePIDController()
sensors = SensorFusion()

# 센서 캘리브레이션
print("센서 캘리브레이션 중... (5초간 움직이지 마세요)")
sensors.calibrate_gyro(samples=50)
print("캘리브레이션 완료!")

# 테스트 루프
print("테스트 시작! (10초)")
for i in range(100):  # 10초 (100 * 0.1초)
    # 센서 데이터 읽기
    sensor_data = sensors.read_all()

    # 목표 자세 (수평 유지)
    target = {'roll': 0, 'pitch': 0, 'yaw': 0}

    # PID 제어 계산
    control = pid.update(
        target,
        sensor_data,
        time.ticks_ms()
    )

    # 결과 출력
    print(f"[{i}] Roll: {sensor_data['roll']:.2f}° → {control['rol']}")

    time.sleep(0.1)

print("테스트 완료!")
```

### 3. 데이터 로깅 및 분석

```python
# Claude에게 요청:
"비행 데이터를 SD 카드에 로깅하는 코드를 만들어줘"

# Claude가 만들어주는 코드:
# lib/data_logger.py

import os
import time

class FlightDataLogger:
    def __init__(self, filename=None):
        if filename is None:
            # 타임스탬프로 파일명 생성
            timestamp = time.time()
            filename = f"flight_{int(timestamp)}.csv"

        self.filename = f"/sd/{filename}"
        self.file = None

        # CSV 헤더 작성
        self._write_header()

    def _write_header(self):
        """CSV 헤더 작성"""
        try:
            self.file = open(self.filename, 'w')
            self.file.write("time,roll,pitch,yaw,altitude,")
            self.file.write("pid_roll,pid_pitch,pid_yaw,pid_thr\n")
            self.file.close()
        except Exception as e:
            print(f"로거 초기화 실패: {e}")

    def log(self, data):
        """데이터 로깅"""
        try:
            self.file = open(self.filename, 'a')
            line = f"{data['time']},{data['roll']},{data['pitch']},"
            line += f"{data['yaw']},{data['altitude']},"
            line += f"{data['pid_roll']},{data['pid_pitch']},"
            line += f"{data['pid_yaw']},{data['pid_thr']}\n"
            self.file.write(line)
            self.file.close()
        except Exception as e:
            print(f"로깅 실패: {e}")

    def close(self):
        """로거 종료"""
        if self.file:
            self.file.close()
        print(f"로그 저장 완료: {self.filename}")
```

사용:
```python
# main.py
from lib.data_logger import FlightDataLogger

logger = FlightDataLogger()

# 비행 중
while flying:
    # ... 센서 읽기, PID 계산 ...

    # 로깅
    logger.log({
        'time': time.ticks_ms(),
        'roll': sensor_data['roll'],
        'pitch': sensor_data['pitch'],
        'yaw': sensor_data['yaw'],
        'altitude': sensor_data['altitude'],
        'pid_roll': control['rol'],
        'pid_pitch': control['pit'],
        'pid_yaw': control['yaw'],
        'pid_thr': control['thr']
    })

logger.close()
```

비행 후 데이터 다운로드:
```bash
# rshell로 로그 다운로드
rshell -p /dev/ttyUSB0
> cp /pyboard/sd/flight_*.csv logs/
```

Claude에게 분석 요청:
```
"logs/flight_123456.csv를 분석해서
 PID 튜닝을 개선해줘"
```

---

## 🔄 반복 개선 사이클

### 실전 예시: Roll 제어 개선

#### Iteration 1: 초기 구현

```
당신: "Roll 제어를 위한 PID를 구현해줘"

Claude: [PID 코드 생성]

당신: [pyDrone에 업로드 → 테스트]
```

결과: Roll 값이 진동함

#### Iteration 2: 문제 피드백

```
당신: "Roll 값이 계속 진동해. 로그 파일을 첨부할게.
      [flight_log.csv 첨부]"

Claude: "로그를 분석해보니 D 게인이 너무 높습니다.
        다음과 같이 수정하세요:
        - Kd: 0.5 → 0.2
        - 저역통과 필터 추가"

당신: [수정된 코드 업로드 → 재테스트]
```

결과: 진동 감소, but 느린 반응

#### Iteration 3: 최적화

```
당신: "진동은 줄었는데 반응이 느려. 어떻게 개선할까?"

Claude: "P 게인을 약간 높이고, I 게인을 추가하세요:
        - Kp: 1.5 → 2.0
        - Ki: 0 → 0.05"

당신: [수정 → 테스트]
```

결과: 완벽! ✅

---

## 💻 Claude Code 활용 팁

### Tip 1: 명확한 요구사항 전달

❌ 나쁜 예:
```
"드론 코드 만들어줘"
```

✅ 좋은 예:
```
"pyDrone용 고도 유지 기능을 만들어줘.
 요구사항:
 - SPL06 기압계 사용
 - 칼만 필터로 노이즈 제거
 - PID로 스로틀 제어
 - 목표 고도 ±5cm 정밀도
 - MicroPython으로 작성
 - 메모리 효율적으로"
```

### Tip 2: 컨텍스트 제공

```
"lib/pid_controller.py를 읽어보고,
 이것과 호환되는 고도 제어기를 만들어줘.
 기존 PID 인터페이스를 그대로 사용해야 해."
```

### Tip 3: 단계별 진행

```
단계 1: "먼저 센서 읽기 모듈만 만들어줘"
        [테스트]

단계 2: "이제 칼만 필터를 추가해줘"
        [테스트]

단계 3: "PID 제어를 통합해줘"
        [테스트]
```

### Tip 4: 에러 메시지 공유

```
"이런 에러가 났어:

Traceback (most recent call last):
  File "main.py", line 23, in <module>
    from lib.sensor_fusion import SensorFusion
ImportError: no module named 'lib.sensor_fusion'

어떻게 해결할까?"
```

### Tip 5: 성능 데이터 공유

```
"PID 컨트롤러의 성능을 측정했어:
- 실행 시간: 15ms (목표: 10ms 이하)
- 메모리: 8KB (목표: 5KB 이하)

최적화해줄 수 있어?"
```

---

## 🛠️ 개발 도구 통합

### VS Code + Claude Code 설정

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "/usr/bin/python3",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,

  // MicroPython 설정
  "python.autoComplete.extraPaths": [
    "/home/user/.micropython/stubs"
  ],

  // 파일 자동 업로드 (Pymakr)
  "pymakr.autoConnect": false,
  "pymakr.address": "/dev/ttyUSB0",
  "pymakr.syncFolder": "",
  "pymakr.openOnStart": false
}
```

### Git + Claude Code 워크플로우

```bash
# 새 기능 개발
git checkout -b feature/altitude-hold

# Claude에게 요청
"고도 유지 기능을 구현해줘"

# 코드 작성 완료 후
git add lib/altitude_controller.py
git commit -m "Add altitude hold controller"

# 테스트 후
git push origin feature/altitude-hold
```

---

## 📚 다음 단계

- `03_WIFI_ADVANCED.md` - WiFi WebREPL 고급 사용법
- `04_DEBUGGING.md` - 실시간 디버깅 기법
- `05_ADVANCED_PROJECTS.md` - 고급 프로젝트 예제

---

## 요약

```
┌─────────────────────────────────────────────┐
│   Claude Code + pyDrone = 강력한 조합!      │
└─────────────────────────────────────────────┘

1. Claude에게 명확한 요구사항 전달
2. 로컬 PC에서 코드 개발 및 시뮬레이션
3. pyDrone에 업로드
4. 실제 하드웨어 테스트
5. 결과를 Claude에게 피드백
6. 반복 개선

이 사이클을 통해 빠르게 고품질 드론 코드 개발!
```

**Claude Code는 당신의 드론 개발 파트너입니다!** 🚀

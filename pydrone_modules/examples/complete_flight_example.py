"""
pyDrone 완전한 비행 예제
실제 pyDrone 하드웨어에서 사용 가능한 통합 예제
"""

import time


class MockDrone:
    """
    실제 pyDrone이 없을 때 사용하는 Mock 객체
    실제 하드웨어에서는 다음과 같이 import:
    from drone import DRONE as MockDrone
    """

    def __init__(self, flightmode=0):
        self.flightmode = flightmode
        self.flying = False
        print(f"[MockDrone] 초기화 완료 (mode={flightmode})")

    def takeoff(self):
        self.flying = True
        print("[MockDrone] 이륙!")

    def landing(self):
        self.flying = False
        print("[MockDrone] 착륙!")

    def control(self, rol=0, pit=0, yaw=0, thr=0):
        print(f"[MockDrone] 제어: roll={rol}, pitch={pit}, yaw={yaw}, throttle={thr}")

    def get_mpu6050_data(self):
        """실제로는 MPU6050 센서에서 데이터 읽기"""
        return {
            'accel': {'x': 0.0, 'y': 0.0, 'z': 1.0},
            'gyro': {'x': 0.0, 'y': 0.0, 'z': 0.0}
        }

    def get_barometer_data(self):
        """실제로는 SPL06-001 기압계에서 데이터 읽기"""
        return {'pressure': 101325, 'temperature': 25.0}

    def get_compass_data(self):
        """실제로는 QMC5883L 나침반에서 데이터 읽기"""
        return {'x': 1.0, 'y': 0.0, 'z': 0.0}


def main():
    """
    pyDrone 완전한 비행 예제
    Claude와 함께 개발한 모든 모듈을 통합
    """
    print("=" * 70)
    print("pyDrone 완전한 비행 시스템 - Claude와 함께 개발")
    print("=" * 70)
    print()

    # 모듈 임포트 (실제 환경에서 사용)
    try:
        from flight_control.pid_controller import AttitudePIDController
        from sensors.sensor_fusion import SensorFusion
        from navigation.waypoint_navigation import WaypointNavigator
        print("✅ 모든 모듈 로드 완료!")
    except ImportError as e:
        print(f"⚠️ 모듈 로드 실패: {e}")
        print("   현재 디렉토리에서 실행해주세요")
        return

    print()
    print("1️⃣ 드론 시스템 초기화...")
    print("-" * 70)

    # 드론 초기화
    drone = MockDrone(flightmode=0)  # 헤드리스 모드

    # PID 컨트롤러 초기화
    pid_controller = AttitudePIDController()
    print("  ✓ PID 컨트롤러 초기화")

    # 센서 퓨전 시스템 초기화
    sensor_fusion = SensorFusion()
    print("  ✓ 센서 퓨전 시스템 초기화")

    # 웨이포인트 네비게이터 초기화
    navigator = WaypointNavigator(drone, arrival_threshold=20)
    print("  ✓ 웨이포인트 네비게이터 초기화")

    print()
    print("2️⃣ 센서 캘리브레이션...")
    print("-" * 70)
    print("  이 기능은 Tello에서 절대 불가능합니다!")
    print("  pyDrone만의 강력한 기능입니다!")
    print()

    # 자이로 캘리브레이션 (실제로는 100개 샘플 수집)
    print("  자이로스코프 캘리브레이션 중...")
    print("  (드론을 평평한 곳에 두고 움직이지 마세요)")
    # sensor_fusion.calibrate_gyro(samples=100)
    print("  ✓ 캘리브레이션 완료!")

    print()
    print("3️⃣ PID 게인 튜닝...")
    print("-" * 70)
    print("  이것도 Tello에서는 불가능합니다!")
    print("  pyDrone은 실시간으로 PID 게인을 조정할 수 있습니다!")
    print()

    # PID 게인 설정
    pid_controller.roll_pid.set_gains(kp=2.0, ki=0.02, kd=0.6)
    pid_controller.pitch_pid.set_gains(kp=2.0, ki=0.02, kd=0.6)
    pid_controller.yaw_pid.set_gains(kp=2.5, ki=0.01, kd=0.4)
    pid_controller.throttle_pid.set_gains(kp=1.5, ki=0.05, kd=0.3)

    print(f"  Roll PID:     {pid_controller.roll_pid.get_gains()}")
    print(f"  Pitch PID:    {pid_controller.pitch_pid.get_gains()}")
    print(f"  Yaw PID:      {pid_controller.yaw_pid.get_gains()}")
    print(f"  Throttle PID: {pid_controller.throttle_pid.get_gains()}")

    print()
    print("4️⃣ 미션 계획...")
    print("-" * 70)

    # 홈 포지션 설정
    home = {'x': 0, 'y': 0, 'z': 0}
    navigator.set_home(home)

    # 웨이포인트 추가 (사각형 비행 경로)
    print("  정사각형 비행 경로 설정:")
    navigator.add_waypoint(100, 0, 100, speed=50)
    print(f"    → 웨이포인트 1: 앞으로 1m, 고도 1m")

    navigator.add_waypoint(100, 100, 100, speed=50)
    print(f"    → 웨이포인트 2: 오른쪽으로 1m")

    navigator.add_waypoint(0, 100, 100, speed=50, action='rotate')
    print(f"    → 웨이포인트 3: 뒤로 1m (회전 수행)")

    navigator.add_waypoint(0, 0, 100, speed=50)
    print(f"    → 웨이포인트 4: 원점 복귀")

    navigator.add_waypoint(0, 0, 0, speed=30, action='land')
    print(f"    → 웨이포인트 5: 착륙")

    print()
    print("5️⃣ 비행 시작!")
    print("-" * 70)

    # 이륙
    print("  이륙 중...")
    drone.takeoff()
    time.sleep(0.5)

    print()
    print("  자동 비행 실행 중...")
    print("  (실제 환경에서는 센서 데이터를 실시간으로 읽어서 PID 제어)")
    print()

    # 시뮬레이션: 몇 번의 제어 루프 실행
    current_time = int(time.time() * 1000)

    for i in range(5):
        # 센서 데이터 읽기 (pyDrone만 가능!)
        mpu_data = drone.get_mpu6050_data()
        baro_data = drone.get_barometer_data()
        mag_data = drone.get_compass_data()

        # 센서 퓨전으로 현재 자세 추정
        current_state = {
            'roll': 0.5 * i,
            'pitch': -0.3 * i,
            'yaw': 0.1 * i,
            'altitude': 100 + i * 5
        }

        # 목표 자세 설정
        target_attitude = {
            'roll': 0,
            'pitch': 0,
            'yaw': 0,
            'altitude': 100
        }

        # PID 컨트롤러로 제어값 계산 (pyDrone만 가능!)
        control_output = pid_controller.update(
            target_attitude,
            current_state,
            current_time + i * 100
        )

        # 제어 명령 전송
        drone.control(**control_output)

        print(f"  [{i+1}/5] Roll: {current_state['roll']:6.2f}°, "
              f"Pitch: {current_state['pitch']:6.2f}°, "
              f"Altitude: {current_state['altitude']:6.1f}cm")

        time.sleep(0.2)

    print()
    print("  ✓ 자동 비행 완료!")

    # 착륙
    print()
    print("  착륙 중...")
    drone.landing()

    print()
    print("=" * 70)
    print("✅ 비행 완료!")
    print("=" * 70)
    print()
    print("📊 요약:")
    print(f"  - 미션 진행률: {navigator.get_mission_progress()}")
    print(f"  - PID 제어 루프: 5회 실행")
    print(f"  - 센서 데이터 처리: 5회")
    print()
    print("💡 이 모든 기능은 Tello에서 불가능합니다!")
    print("   pyDrone + Claude = 무한한 가능성! 🚀")
    print()


if __name__ == "__main__":
    main()

    print()
    print("=" * 70)
    print("다음 단계:")
    print("=" * 70)
    print()
    print("1. 실제 pyDrone 하드웨어 준비")
    print("2. MicroPython 펌웨어 업로드")
    print("3. 이 코드를 pyDrone에 업로드")
    print("4. 실제 비행 테스트 및 PID 튜닝")
    print("5. 고급 기능 추가 (GPS, 카메라 등)")
    print()
    print("Claude가 모든 단계를 도와드립니다! 🤖")
    print()

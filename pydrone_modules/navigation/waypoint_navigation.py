"""
웨이포인트 네비게이션 시스템 - pyDrone 전용
고급 자율 비행 기능 구현
"""

import math
from enum import Enum


class FlightMode(Enum):
    """비행 모드"""
    MANUAL = 0
    STABILIZE = 1
    ALTITUDE_HOLD = 2
    POSITION_HOLD = 3
    AUTO = 4
    RTH = 5  # Return to Home


class Waypoint:
    """3D 웨이포인트"""

    def __init__(self, x, y, z, speed=50, action=None):
        """
        Args:
            x, y: 수평 위치 (cm)
            z: 고도 (cm)
            speed: 이동 속도 (cm/s)
            action: 도착 시 실행할 동작 (예: 'hover', 'photo', 'rotate')
        """
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.action = action
        self.reached = False

    def distance_to(self, current_pos):
        """현재 위치로부터의 거리 계산"""
        dx = self.x - current_pos['x']
        dy = self.y - current_pos['y']
        dz = self.z - current_pos['z']
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def __repr__(self):
        return f"Waypoint(x={self.x}, y={self.y}, z={self.z}, speed={self.speed})"


class WaypointNavigator:
    """
    자율 웨이포인트 네비게이션
    pyDrone의 저수준 제어를 활용한 정밀 비행!
    """

    def __init__(self, drone_controller, arrival_threshold=20):
        """
        Args:
            drone_controller: 드론 제어 객체
            arrival_threshold: 웨이포인트 도착 판정 거리 (cm)
        """
        self.drone = drone_controller
        self.waypoints = []
        self.current_waypoint_idx = 0
        self.arrival_threshold = arrival_threshold
        self.mission_active = False
        self.home_position = None

    def add_waypoint(self, x, y, z, speed=50, action=None):
        """웨이포인트 추가"""
        wp = Waypoint(x, y, z, speed, action)
        self.waypoints.append(wp)
        print(f"웨이포인트 추가: {wp}")

    def load_mission(self, mission_file):
        """
        미션 파일에서 웨이포인트 로드
        Tello도 가능하지만 pyDrone은 더 정밀한 제어 가능!
        """
        print(f"미션 로딩: {mission_file}")
        # 실제 구현에서는 JSON/YAML 파일 파싱
        pass

    def set_home(self, position):
        """홈 포지션 설정"""
        self.home_position = position
        print(f"홈 설정: {position}")

    def calculate_trajectory(self, start, end, dt=0.1):
        """
        두 지점 사이의 궤적 계산
        pyDrone: 부드러운 곡선 비행 가능
        Tello: 직선 이동만 가능 (go 명령)
        """
        distance = math.sqrt(
            (end.x - start['x'])**2 +
            (end.y - start['y'])**2 +
            (end.z - start['z'])**2
        )

        # 이동 시간 계산
        travel_time = distance / end.speed

        # 궤적 포인트 생성
        trajectory = []
        num_points = int(travel_time / dt)

        for i in range(num_points + 1):
            t = i / num_points if num_points > 0 else 1.0

            # S-커브 가속/감속 프로파일 (Tello는 불가능!)
            s = self._s_curve(t)

            point = {
                'x': start['x'] + (end.x - start['x']) * s,
                'y': start['y'] + (end.y - start['y']) * s,
                'z': start['z'] + (end.z - start['z']) * s,
                'time': t * travel_time
            }
            trajectory.append(point)

        return trajectory

    def _s_curve(self, t):
        """
        S-커브 함수 (부드러운 가속/감속)
        pyDrone의 저수준 제어로만 가능!
        """
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - 2 * (1 - t) * (1 - t)

    def navigate_to_waypoint(self, waypoint, current_pos, pid_controller):
        """
        웨이포인트로 이동
        pyDrone: PID 제어로 정밀한 위치 제어
        Tello: go x y z 명령으로 대략적 이동만 가능
        """
        # 목표까지의 벡터 계산
        dx = waypoint.x - current_pos['x']
        dy = waypoint.y - current_pos['y']
        dz = waypoint.z - current_pos['z']

        # 거리 및 방향 계산
        distance = math.sqrt(dx**2 + dy**2 + dz**2)

        if distance < self.arrival_threshold:
            waypoint.reached = True
            print(f"웨이포인트 도착: {waypoint}")
            if waypoint.action:
                self._execute_action(waypoint.action)
            return True

        # 정규화된 방향 벡터
        if distance > 0:
            dx /= distance
            dy /= distance
            dz /= distance

        # 목표 자세 계산 (pyDrone 전용!)
        target_roll = dy * 30  # 최대 30도 기울기
        target_pitch = dx * 30
        target_altitude = waypoint.z

        # PID 컨트롤러로 제어값 계산
        # 이것이 pyDrone의 핵심 장점!
        control_output = pid_controller.update(
            target_attitude={
                'roll': target_roll,
                'pitch': target_pitch,
                'yaw': 0,
                'altitude': target_altitude
            },
            current_attitude=current_pos,
            current_time=self._get_time_ms()
        )

        # 드론에 제어값 전송
        self.drone.control(**control_output)

        return False

    def execute_mission(self):
        """
        자율 미션 실행
        pyDrone: 완전한 자율 비행 가능
        Tello: 고수준 명령어만 가능
        """
        if not self.waypoints:
            print("미션이 비어있습니다!")
            return

        print("미션 시작!")
        self.mission_active = True
        self.current_waypoint_idx = 0

        # 실제 구현에서는 비동기 루프에서 실행
        print(f"총 {len(self.waypoints)}개의 웨이포인트")

    def return_to_home(self):
        """
        자동 귀환 (RTH)
        pyDrone: 정밀한 위치 제어로 정확한 착륙
        Tello: 대략적인 귀환만 가능
        """
        if self.home_position:
            print("홈으로 귀환 중...")
            self.add_waypoint(
                self.home_position['x'],
                self.home_position['y'],
                self.home_position['z'],
                speed=30,
                action='land'
            )
        else:
            print("홈 포지션이 설정되지 않았습니다!")

    def _execute_action(self, action):
        """웨이포인트 도착 시 동작 실행"""
        print(f"동작 실행: {action}")
        if action == 'hover':
            # 제자리 비행
            pass
        elif action == 'photo':
            # 사진 촬영 (카메라 모듈 필요)
            pass
        elif action == 'rotate':
            # 360도 회전
            pass
        elif action == 'land':
            self.drone.landing()

    def _get_time_ms(self):
        """현재 시간 (ms) - 실제 구현에서는 time.ticks_ms() 사용"""
        import time
        return int(time.time() * 1000)

    def get_mission_progress(self):
        """미션 진행 상황 반환"""
        if not self.waypoints:
            return "미션 없음"

        completed = sum(1 for wp in self.waypoints if wp.reached)
        total = len(self.waypoints)
        percentage = (completed / total) * 100

        return f"{completed}/{total} 완료 ({percentage:.1f}%)"


# 사용 예제
if __name__ == "__main__":
    print("=" * 60)
    print("pyDrone 웨이포인트 네비게이션 시스템")
    print("=" * 60)
    print()

    # 예제 미션 생성
    class MockDrone:
        def control(self, **kwargs):
            pass
        def landing(self):
            pass

    navigator = WaypointNavigator(MockDrone())

    # 홈 설정
    navigator.set_home({'x': 0, 'y': 0, 'z': 0})

    # 미션 웨이포인트 추가
    navigator.add_waypoint(100, 0, 100, speed=50)  # 앞으로 1m, 고도 1m
    navigator.add_waypoint(100, 100, 100, speed=50)  # 오른쪽으로 1m
    navigator.add_waypoint(0, 100, 100, speed=50, action='rotate')  # 뒤로
    navigator.add_waypoint(0, 0, 100, speed=50)  # 원점
    navigator.add_waypoint(0, 0, 0, speed=30, action='land')  # 착륙

    print()
    print("✅ pyDrone 장점:")
    print("  - PID 제어로 정밀한 위치 제어")
    print("  - S-커브 가속/감속으로 부드러운 비행")
    print("  - 실시간 궤적 계산 및 조정")
    print("  - 커스텀 동작 실행")
    print()
    print("❌ Tello 제한사항:")
    print("  - go 명령으로 직선 이동만 가능")
    print("  - 위치 정밀도 낮음")
    print("  - 부드러운 가속/감속 불가")
    print()

    print(navigator.get_mission_progress())

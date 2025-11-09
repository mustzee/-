#!/usr/bin/env python3
"""
Order-3 Heptagonal Tiling {7,3} - Poincaré Disk Model
쌍곡 기하학 시각화 - 파이썬 구현
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Wedge
from matplotlib.collections import PatchCollection
from matplotlib.widgets import Slider, Button, CheckButtons
import math

# ===================================================================
# Möbius 변환과 쌍곡 기하학 함수들
# ===================================================================

class MobiusTransform:
    """Möbius 변환: z -> (az + b) / (cz + d)"""

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def apply(self, z):
        """복소수 z에 Möbius 변환 적용"""
        return (self.a * z + self.b) / (self.c * z + self.d)

    @staticmethod
    def identity():
        """항등 변환"""
        return MobiusTransform(1+0j, 0+0j, 0+0j, 1+0j)


def hyperbolic_distance(z1, z2):
    """두 점 사이의 쌍곡 거리 계산"""
    diff = abs(z1 - z2)
    z1_abs = abs(z1)
    z2_abs = abs(z2)

    numerator = 2 * diff * diff
    denominator = (1 - z1_abs * z1_abs) * (1 - z2_abs * z2_abs)

    if denominator <= 0:
        return float('inf')

    return np.arccosh(1 + numerator / denominator)


def find_geodesic_circle(z1, z2):
    """
    두 점을 잇는 측지선을 나타내는 원의 중심과 반지름 찾기
    Poincaré disk에서 측지선은 단위원과 직교하는 원의 호
    """
    z1_abs_sq = abs(z1) ** 2
    z2_abs_sq = abs(z2) ** 2

    denom = 2 * (z1.real * z2.imag - z1.imag * z2.real)

    if abs(denom) < 1e-10:
        return None  # 직선

    center_x = (z2.imag * z1_abs_sq - z1.imag * z2_abs_sq) / denom
    center_y = (z1.real * z2_abs_sq - z2.real * z1_abs_sq) / denom

    center = complex(center_x, center_y)
    radius = abs(center - z1)

    return center, radius


def interpolate_geodesic(z1, z2, num_points=50):
    """측지선을 따라 두 점 사이를 보간"""
    # 간단한 유클리드 보간 (근사)
    t = np.linspace(0, 1, num_points)
    points = []
    for ti in t:
        point = z1 + (z2 - z1) * ti
        points.append(point)
    return points


# ===================================================================
# Poincaré Disk 렌더러
# ===================================================================

class PoincareRenderer:
    """Poincaré disk 모델 렌더링"""

    def __init__(self, ax):
        self.ax = ax
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # 배경색
        self.ax.set_facecolor('#0f0f1e')

        self.view_transform = MobiusTransform.identity()

    def draw_disk_boundary(self):
        """단위원 경계 그리기"""
        circle = Circle((0, 0), 1, fill=False, edgecolor='#00ff88',
                       linewidth=2.5, zorder=1000)
        self.ax.add_patch(circle)

    def draw_geodesic(self, z1, z2, color='#00ff88', linewidth=1.5, zorder=1):
        """두 점을 잇는 측지선(곡선) 그리기"""
        # View transform 적용
        z1 = self.view_transform.apply(z1)
        z2 = self.view_transform.apply(z2)

        # 원점을 지나는지 확인
        cross = z1.real * z2.imag - z1.imag * z2.real

        if abs(cross) < 1e-10:
            # 직선
            self.ax.plot([z1.real, z2.real], [z1.imag, z2.imag],
                        color=color, linewidth=linewidth, zorder=zorder)
        else:
            # 원호
            result = find_geodesic_circle(z1, z2)
            if result:
                center, radius = result

                # 각도 계산
                angle1 = np.degrees(np.arctan2(z1.imag - center.imag,
                                               z1.real - center.real))
                angle2 = np.degrees(np.arctan2(z2.imag - center.imag,
                                               z2.real - center.real))

                # 더 짧은 호 선택
                angle_diff = angle2 - angle1
                while angle_diff > 180:
                    angle_diff -= 360
                while angle_diff < -180:
                    angle_diff += 360

                if angle_diff < 0:
                    angle1, angle2 = angle2, angle1

                arc = Arc((center.real, center.imag), 2*radius, 2*radius,
                         angle=0, theta1=angle1, theta2=angle2,
                         color=color, linewidth=linewidth, zorder=zorder)
                self.ax.add_patch(arc)

    def draw_polygon(self, vertices, fill_color=None, edge_color='#00ff88',
                    linewidth=1.5, alpha=0.6):
        """다각형(칠각형) 그리기"""
        if len(vertices) < 3:
            return

        # 채우기를 위한 경로 생성 (측지선 보간)
        if fill_color:
            all_points = []
            for i in range(len(vertices)):
                v1 = vertices[i]
                v2 = vertices[(i + 1) % len(vertices)]

                # 측지선 보간
                points = interpolate_geodesic(v1, v2, num_points=20)
                points = [self.view_transform.apply(p) for p in points]
                all_points.extend(points)

            # 다각형 채우기
            xs = [p.real for p in all_points]
            ys = [p.imag for p in all_points]
            self.ax.fill(xs, ys, color=fill_color, alpha=alpha, zorder=2)

        # 외곽선
        if edge_color:
            for i in range(len(vertices)):
                v1 = vertices[i]
                v2 = vertices[(i + 1) % len(vertices)]
                self.draw_geodesic(v1, v2, color=edge_color,
                                 linewidth=linewidth, zorder=3)


# ===================================================================
# Order-3 Heptagonal Tiling 생성기
# ===================================================================

class HeptagonalTiling:
    """Order-3 heptagonal tiling {7,3} 생성"""

    def __init__(self):
        self.tiles = []
        self.p = 7  # 다각형 변 개수
        self.q = 3  # 한 꼭짓점에 모이는 다각형 개수

        # 쌍곡 반지름 계산
        self.hyperbolic_radius = self.calculate_hyperbolic_radius()

        # 색상 팔레트
        self.colors = [
            '#FF6B6B', '#4ECDC4', '#FFC371', '#C77DFF',
            '#FF9FF3', '#84FAB0', '#FFDA79', '#95E1D3'
        ]

    def calculate_hyperbolic_radius(self):
        """{7,3} 타일링에서 정칠각형의 반지름 계산"""
        p = self.p
        q = self.q

        # 쌍곡 기하학 공식
        r = np.arctanh(np.cos(np.pi / p) /
                      np.cos(np.pi / q - np.pi / p))

        # Poincaré disk에서의 유클리드 반지름
        return np.tanh(r / 2) * 0.95

    def generate_heptagon(self, center, radius, rotation=0):
        """정칠각형의 꼭짓점 생성"""
        vertices = []
        for i in range(7):
            angle = rotation + (2 * np.pi * i) / 7
            vertex = center + radius * np.exp(1j * angle)
            vertices.append(vertex)
        return vertices

    def create_adjacent_tile(self, tile, edge_index):
        """인접한 타일 생성"""
        vertices = tile['vertices']
        v1 = vertices[edge_index]
        v2 = vertices[(edge_index + 1) % 7]

        # 변의 중점
        midpoint = (v1 + v2) / 2

        # 중심에서 중점으로의 벡터
        to_midpoint = midpoint - tile['center']

        # 법선 방향 (90도 회전)
        normal = to_midpoint * 1j

        if abs(normal) < 1e-10:
            return None

        # 새 중심 위치
        distance = self.hyperbolic_radius * 1.8
        new_center = midpoint + (normal / abs(normal)) * distance

        # 회전각
        angle = np.angle(to_midpoint)
        rotation = angle + np.pi

        new_vertices = self.generate_heptagon(new_center,
                                              self.hyperbolic_radius,
                                              rotation)

        return {
            'center': new_center,
            'vertices': new_vertices
        }

    def generate(self, depth=4):
        """타일링 생성 (BFS)"""
        self.tiles = []

        # 중앙 칠각형
        center_tile = {
            'center': 0+0j,
            'vertices': self.generate_heptagon(0+0j, self.hyperbolic_radius, 0),
            'depth': 0,
            'id': '0'
        }

        self.tiles.append(center_tile)

        # BFS 큐
        queue = [center_tile]
        visited = {'0'}

        while queue and len(self.tiles) < 1000:
            tile = queue.pop(0)

            if tile['depth'] >= depth:
                continue

            # 각 변에 대해 인접 타일 생성
            for i in range(7):
                edge_id = f"{tile['id']}-{i}"
                if edge_id in visited:
                    continue

                new_tile = self.create_adjacent_tile(tile, i)

                if new_tile and abs(new_tile['center']) < 0.98:
                    new_tile['depth'] = tile['depth'] + 1
                    new_tile['id'] = edge_id

                    self.tiles.append(new_tile)
                    queue.append(new_tile)
                    visited.add(edge_id)

        return self.tiles

    def render(self, renderer, show_edges=True, color_mode=True):
        """타일링 렌더링"""
        for i, tile in enumerate(self.tiles):
            fill_color = self.colors[i % len(self.colors)] if color_mode else '#323250'
            edge_color = '#00ff88' if show_edges else None

            renderer.draw_polygon(
                tile['vertices'],
                fill_color=fill_color,
                edge_color=edge_color,
                linewidth=1.5,
                alpha=0.6
            )


# ===================================================================
# 메인 애플리케이션
# ===================================================================

class HyperbolicVisualization:
    """인터랙티브 시각화"""

    def __init__(self):
        # Figure 설정
        self.fig = plt.figure(figsize=(12, 10), facecolor='#1a1a2e')

        # 메인 축
        self.ax = plt.axes([0.1, 0.25, 0.8, 0.7])

        # 렌더러와 타일링
        self.renderer = PoincareRenderer(self.ax)
        self.tiling = HeptagonalTiling()

        # 현재 설정
        self.current_depth = 4
        self.show_edges = True
        self.color_mode = True

        # UI 요소 설정
        self.setup_ui()

        # 초기 렌더링
        self.update()

    def setup_ui(self):
        """UI 컨트롤 설정"""
        # Depth 슬라이더
        ax_depth = plt.axes([0.2, 0.12, 0.6, 0.03], facecolor='#2a2a4e')
        self.slider_depth = Slider(
            ax_depth, 'Depth', 1, 6,
            valinit=self.current_depth,
            valstep=1,
            color='#00ff88'
        )
        self.slider_depth.on_changed(self.update_depth)

        # Reset 버튼
        ax_reset = plt.axes([0.4, 0.05, 0.2, 0.04])
        self.btn_reset = Button(ax_reset, 'Reset View',
                               color='#00ff88', hovercolor='#00cc6a')
        self.btn_reset.on_clicked(self.reset_view)

        # 체크박스
        ax_check = plt.axes([0.02, 0.4, 0.15, 0.15], facecolor='#1a1a2e')
        self.check = CheckButtons(
            ax_check,
            ['Show Edges', 'Color Tiles'],
            [self.show_edges, self.color_mode]
        )
        self.check.on_clicked(self.update_options)

        # 제목
        self.ax.set_title('Order-3 Heptagonal Tiling {7,3}\nPoincaré Disk Model',
                         fontsize=16, color='#00ff88', pad=20)

    def update_depth(self, val):
        """Depth 슬라이더 업데이트"""
        self.current_depth = int(val)
        self.update()

    def update_options(self, label):
        """체크박스 업데이트"""
        if label == 'Show Edges':
            self.show_edges = not self.show_edges
        elif label == 'Color Tiles':
            self.color_mode = not self.color_mode
        self.update()

    def reset_view(self, event):
        """뷰 리셋"""
        self.renderer.view_transform = MobiusTransform.identity()
        self.update()

    def update(self):
        """화면 업데이트"""
        # 축 클리어
        self.ax.clear()

        # 렌더러 재설정
        self.renderer = PoincareRenderer(self.ax)

        # 타일링 생성
        self.tiling.generate(self.current_depth)

        # 렌더링
        self.renderer.draw_disk_boundary()
        self.tiling.render(self.renderer, self.show_edges, self.color_mode)

        # 타일 개수 표시
        self.ax.text(0, -1.25, f'Tiles: {len(self.tiling.tiles)}',
                    ha='center', fontsize=12, color='#888888')

        # 제목
        self.ax.set_title('Order-3 Heptagonal Tiling {7,3}\nPoincaré Disk Model',
                         fontsize=16, color='#00ff88', pad=20)

        # 다시 그리기
        self.fig.canvas.draw_idle()

    def show(self):
        """창 표시"""
        plt.show()


# ===================================================================
# 실행
# ===================================================================

if __name__ == '__main__':
    print("Order-3 Heptagonal Tiling {7,3} - Poincaré Disk Model")
    print("=" * 60)
    print("쌍곡 기하학 시각화")
    print("\n컨트롤:")
    print("  - Depth 슬라이더: 타일링 깊이 조절 (1-6)")
    print("  - Show Edges: 타일 경계선 표시/숨김")
    print("  - Color Tiles: 타일 색상 모드 전환")
    print("  - Reset View: 초기 뷰로 복귀")
    print("\n창을 닫으면 프로그램이 종료됩니다.")
    print("=" * 60)

    viz = HyperbolicVisualization()
    viz.show()

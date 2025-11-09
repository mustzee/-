// ===================================================================
// Complex Number Class - 복소수 연산
// ===================================================================
class Complex {
    constructor(re, im) {
        this.re = re;
        this.im = im;
    }

    add(z) {
        return new Complex(this.re + z.re, this.im + z.im);
    }

    sub(z) {
        return new Complex(this.re - z.re, this.im - z.im);
    }

    mul(z) {
        return new Complex(
            this.re * z.re - this.im * z.im,
            this.re * z.im + this.im * z.re
        );
    }

    div(z) {
        const denom = z.re * z.re + z.im * z.im;
        return new Complex(
            (this.re * z.re + this.im * z.im) / denom,
            (this.im * z.re - this.re * z.im) / denom
        );
    }

    conjugate() {
        return new Complex(this.re, -this.im);
    }

    abs() {
        return Math.sqrt(this.re * this.re + this.im * this.im);
    }

    arg() {
        return Math.atan2(this.im, this.re);
    }

    scale(s) {
        return new Complex(this.re * s, this.im * s);
    }

    static fromPolar(r, theta) {
        return new Complex(r * Math.cos(theta), r * Math.sin(theta));
    }

    static zero() {
        return new Complex(0, 0);
    }

    static one() {
        return new Complex(1, 0);
    }
}

// ===================================================================
// Hyperbolic Geometry Functions - 쌍곡 기하학
// ===================================================================

// Möbius 변환: z -> (az + b) / (cz + d)
class MobiusTransform {
    constructor(a, b, c, d) {
        this.a = a;
        this.b = b;
        this.c = c;
        this.d = d;
    }

    apply(z) {
        const numerator = this.a.mul(z).add(this.b);
        const denominator = this.c.mul(z).add(this.d);
        return numerator.div(denominator);
    }

    compose(other) {
        return new MobiusTransform(
            this.a.mul(other.a).add(this.b.mul(other.c)),
            this.a.mul(other.b).add(this.b.mul(other.d)),
            this.c.mul(other.a).add(this.d.mul(other.c)),
            this.c.mul(other.b).add(this.d.mul(other.d))
        );
    }

    // 쌍곡 회전: Poincaré disk에서의 회전
    static rotation(angle) {
        const cos = Math.cos(angle / 2);
        const sin = Math.sin(angle / 2);
        return new MobiusTransform(
            new Complex(cos, sin),
            new Complex(0, 0),
            new Complex(0, 0),
            new Complex(cos, -sin)
        );
    }

    // 쌍곡 이동: 원점을 z로 이동
    static translation(z) {
        const zConj = z.conjugate();
        const oneMinusZZ = Complex.one().sub(z.mul(zConj));
        const denom = Math.sqrt(oneMinusZZ.re);

        return new MobiusTransform(
            new Complex(1, 0),
            z.scale(-1),
            zConj.scale(-1),
            new Complex(1, 0)
        );
    }
}

// ===================================================================
// Poincaré Disk Rendering
// ===================================================================

class PoincareRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        this.center = { x: this.width / 2, y: this.height / 2 };
        this.radius = Math.min(this.width, this.height) / 2 - 20;

        this.viewTransform = new MobiusTransform(
            Complex.one(), Complex.zero(),
            Complex.zero(), Complex.one()
        );
    }

    // 복소수를 캔버스 좌표로 변환
    complexToCanvas(z) {
        return {
            x: this.center.x + z.re * this.radius,
            y: this.center.y - z.im * this.radius
        };
    }

    // 캔버스 좌표를 복소수로 변환
    canvasToComplex(x, y) {
        return new Complex(
            (x - this.center.x) / this.radius,
            -(y - this.center.y) / this.radius
        );
    }

    // Poincaré disk에서 두 점을 잇는 측지선(geodesic) 그리기
    drawGeodesic(z1, z2, strokeStyle = '#00ff88', lineWidth = 2) {
        z1 = this.viewTransform.apply(z1);
        z2 = this.viewTransform.apply(z2);

        const p1 = this.complexToCanvas(z1);
        const p2 = this.complexToCanvas(z2);

        this.ctx.strokeStyle = strokeStyle;
        this.ctx.lineWidth = lineWidth;

        // 두 점이 거의 같은 경우
        const dist = Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
        if (dist < 0.5) return;

        // 원점을 지나는 직선인지 확인
        const cross = z1.re * z2.im - z1.im * z2.re;

        if (Math.abs(cross) < 1e-10) {
            // 직선
            this.ctx.beginPath();
            this.ctx.moveTo(p1.x, p1.y);
            this.ctx.lineTo(p2.x, p2.y);
            this.ctx.stroke();
        } else {
            // 원호로 그리기
            const circle = this.findGeodesicCircle(z1, z2);
            if (circle) {
                this.drawArc(z1, z2, circle, p1, p2);
            }
        }
    }

    // 측지선을 나타내는 원 찾기
    findGeodesicCircle(z1, z2) {
        // 쌍곡 측지선은 단위원과 직교하는 원
        const z1AbsSq = z1.re * z1.re + z1.im * z1.im;
        const z2AbsSq = z2.re * z2.re + z2.im * z2.im;

        const denom = 2 * (z1.re * z2.im - z1.im * z2.re);
        if (Math.abs(denom) < 1e-10) return null;

        const centerX = (z2.im * z1AbsSq - z1.im * z2AbsSq) / denom;
        const centerY = (z1.re * z2AbsSq - z2.re * z1AbsSq) / denom;

        const center = new Complex(centerX, centerY);
        const radius = center.sub(z1).abs();

        return { center, radius };
    }

    // 원호 그리기
    drawArc(z1, z2, circle, p1, p2) {
        const centerCanvas = this.complexToCanvas(circle.center);
        const radiusCanvas = circle.radius * this.radius;

        const angle1 = Math.atan2(p1.y - centerCanvas.y, p1.x - centerCanvas.x);
        const angle2 = Math.atan2(p2.y - centerCanvas.y, p2.x - centerCanvas.x);

        // 더 짧은 호를 선택
        let angleDiff = angle2 - angle1;
        while (angleDiff > Math.PI) angleDiff -= 2 * Math.PI;
        while (angleDiff < -Math.PI) angleDiff += 2 * Math.PI;

        const anticlockwise = angleDiff < 0;

        this.ctx.beginPath();
        this.ctx.arc(centerCanvas.x, centerCanvas.y, radiusCanvas,
                     angle1, angle2, anticlockwise);
        this.ctx.stroke();
    }

    // 다각형 그리기
    drawPolygon(vertices, fillStyle, strokeStyle = '#00ff88', lineWidth = 2) {
        if (vertices.length < 3) return;

        // 채우기를 위한 경로
        if (fillStyle) {
            this.ctx.fillStyle = fillStyle;
            this.ctx.beginPath();

            // 복잡한 곡선 경로를 만들어야 하므로 근사
            const segments = 20;
            for (let i = 0; i < vertices.length; i++) {
                const v1 = vertices[i];
                const v2 = vertices[(i + 1) % vertices.length];

                // 두 점 사이를 측지선으로 보간
                for (let t = 0; t <= segments; t++) {
                    const s = t / segments;
                    const point = this.interpolateGeodesic(v1, v2, s);
                    const p = this.complexToCanvas(this.viewTransform.apply(point));

                    if (t === 0 && i === 0) {
                        this.ctx.moveTo(p.x, p.y);
                    } else {
                        this.ctx.lineTo(p.x, p.y);
                    }
                }
            }

            this.ctx.closePath();
            this.ctx.fill();
        }

        // 외곽선
        if (strokeStyle) {
            for (let i = 0; i < vertices.length; i++) {
                this.drawGeodesic(
                    vertices[i],
                    vertices[(i + 1) % vertices.length],
                    strokeStyle,
                    lineWidth
                );
            }
        }
    }

    // 측지선을 따라 두 점 사이를 보간
    interpolateGeodesic(z1, z2, t) {
        // 쌍곡 선형 보간
        const d = this.hyperbolicDistance(z1, z2);
        const targetDist = d * t;

        // z1에서 z2 방향으로 targetDist만큼 이동
        if (d < 1e-10) return z1;

        // 간단한 유클리드 보간 (근사)
        // 정확한 구현은 더 복잡하지만, 시각화에는 충분
        return new Complex(
            z1.re + (z2.re - z1.re) * t,
            z1.im + (z2.im - z1.im) * t
        );
    }

    // 쌍곡 거리 계산
    hyperbolicDistance(z1, z2) {
        const diff = z1.sub(z2).abs();
        const z1Abs = z1.abs();
        const z2Abs = z2.abs();

        const numerator = 2 * diff * diff;
        const denominator = (1 - z1Abs * z1Abs) * (1 - z2Abs * z2Abs);

        if (denominator <= 0) return Infinity;

        return Math.acosh(1 + numerator / denominator);
    }

    // 디스크 경계 그리기
    drawDiskBoundary() {
        this.ctx.strokeStyle = '#00ff88';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.arc(this.center.x, this.center.y, this.radius, 0, 2 * Math.PI);
        this.ctx.stroke();
    }

    clear() {
        this.ctx.fillStyle = '#0f0f1e';
        this.ctx.fillRect(0, 0, this.width, this.height);
    }
}

// ===================================================================
// Order-3 Heptagonal Tiling Generator
// ===================================================================

class HeptagonalTiling {
    constructor(renderer) {
        this.renderer = renderer;
        this.tiles = [];
        this.maxDepth = 4;

        // {7,3} 타일링의 기하학적 매개변수
        this.p = 7; // 다각형의 변 개수
        this.q = 3; // 한 꼭짓점에 모이는 다각형 개수

        // 쌍곡 기하학에서 정칠각형의 크기 계산
        // 각 꼭짓점 각도
        const vertexAngle = 2 * Math.PI / this.q;
        // 정칠각형의 내각
        const polygonAngle = (this.p - 2) * Math.PI / this.p;

        // 쌍곡 반지름 계산
        // cos(π/q) = cos(π/p) / sin((p-2)π/(2p))
        this.hyperbolicRadius = this.calculateHyperbolicRadius();

        this.colors = [
            'rgba(255, 107, 107, 0.6)',
            'rgba(78, 205, 196, 0.6)',
            'rgba(255, 195, 113, 0.6)',
            'rgba(199, 125, 255, 0.6)',
            'rgba(255, 159, 243, 0.6)',
            'rgba(132, 250, 176, 0.6)',
            'rgba(255, 218, 121, 0.6)',
        ];
    }

    calculateHyperbolicRadius() {
        // {7,3} 타일링에서 중심에서 꼭짓점까지의 쌍곡 거리
        const p = this.p;
        const q = this.q;

        // tan(r) 계산 (r은 Poincaré disk에서의 반지름)
        const numerator = Math.cos(Math.PI / q);
        const denominator = Math.sin(Math.PI / p);
        const cotValue = numerator / denominator;

        // 쌍곡 기하학 공식
        const r = Math.atanh(Math.cos(Math.PI / p) / Math.cos(Math.PI / q - Math.PI / p));

        // Poincaré disk에서의 유클리드 반지름
        return Math.tanh(r / 2) * 0.95;
    }

    // 정칠각형의 꼭짓점 생성
    generateHeptagon(center, radius, rotation = 0) {
        const vertices = [];
        for (let i = 0; i < 7; i++) {
            const angle = rotation + (2 * Math.PI * i) / 7;
            const vertex = new Complex(
                center.re + radius * Math.cos(angle),
                center.im + radius * Math.sin(angle)
            );
            vertices.push(vertex);
        }
        return vertices;
    }

    // 타일링 생성
    generate(depth = 4) {
        this.maxDepth = depth;
        this.tiles = [];

        // 중앙 칠각형
        const centerHeptagon = {
            center: Complex.zero(),
            vertices: this.generateHeptagon(Complex.zero(), this.hyperbolicRadius, 0),
            depth: 0,
            id: '0'
        };

        this.tiles.push(centerHeptagon);

        // BFS로 타일 확장
        const queue = [centerHeptagon];
        const visited = new Set(['0']);

        while (queue.length > 0 && this.tiles.length < 1000) {
            const tile = queue.shift();

            if (tile.depth >= this.maxDepth) continue;

            // 각 변에 대해 인접한 칠각형 생성
            for (let i = 0; i < 7; i++) {
                const edgeId = `${tile.id}-${i}`;
                if (visited.has(edgeId)) continue;

                const newTile = this.createAdjacentTile(tile, i);

                if (newTile && newTile.center.abs() < 0.98) {
                    newTile.depth = tile.depth + 1;
                    newTile.id = edgeId;

                    this.tiles.push(newTile);
                    queue.push(newTile);
                    visited.add(edgeId);
                }
            }
        }
    }

    // 인접한 타일 생성
    createAdjacentTile(tile, edgeIndex) {
        const v1 = tile.vertices[edgeIndex];
        const v2 = tile.vertices[(edgeIndex + 1) % 7];

        // 변의 중점
        const midpoint = new Complex(
            (v1.re + v2.re) / 2,
            (v1.im + v2.im) / 2
        );

        // 중심에서 중점으로의 벡터
        const toMidpoint = new Complex(
            midpoint.re - tile.center.re,
            midpoint.im - tile.center.im
        );

        // 법선 방향 (90도 회전)
        const normal = new Complex(-toMidpoint.im, toMidpoint.re);
        const normalLength = normal.abs();

        if (normalLength < 1e-10) return null;

        // 새 중심 위치 (쌍곡 기하학에서의 이동)
        const distance = this.hyperbolicRadius * 1.8; // 경험적 값
        const newCenter = new Complex(
            midpoint.re + (normal.re / normalLength) * distance,
            midpoint.im + (normal.im / normalLength) * distance
        );

        // 회전각 계산
        const angle = Math.atan2(
            midpoint.im - tile.center.im,
            midpoint.re - tile.center.re
        );
        const rotation = angle + Math.PI;

        const vertices = this.generateHeptagon(newCenter, this.hyperbolicRadius, rotation);

        return {
            center: newCenter,
            vertices: vertices
        };
    }

    // 렌더링
    render(showEdges = true, colorMode = true) {
        for (let i = 0; i < this.tiles.length; i++) {
            const tile = this.tiles[i];
            const color = colorMode ? this.colors[i % this.colors.length] : 'rgba(50, 50, 80, 0.6)';
            const strokeStyle = showEdges ? '#00ff88' : null;
            const lineWidth = showEdges ? 1.5 : 0;

            this.renderer.drawPolygon(tile.vertices, color, strokeStyle, lineWidth);
        }
    }
}

// ===================================================================
// Main Application
// ===================================================================

let renderer, tiling;
let isDragging = false;
let lastMousePos = null;

function init() {
    const canvas = document.getElementById('canvas');
    renderer = new PoincareRenderer(canvas);
    tiling = new HeptagonalTiling(renderer);

    const depthSlider = document.getElementById('depth');
    const depthValue = document.getElementById('depthValue');
    const resetButton = document.getElementById('reset');
    const showEdgesCheckbox = document.getElementById('showEdges');
    const colorModeCheckbox = document.getElementById('colorMode');
    const stats = document.getElementById('stats');

    // 초기 생성
    generateAndRender();

    // 이벤트 리스너
    depthSlider.addEventListener('input', (e) => {
        depthValue.textContent = e.target.value;
        generateAndRender();
    });

    resetButton.addEventListener('click', () => {
        renderer.viewTransform = new MobiusTransform(
            Complex.one(), Complex.zero(),
            Complex.zero(), Complex.one()
        );
        generateAndRender();
    });

    showEdgesCheckbox.addEventListener('change', () => {
        renderScene();
    });

    colorModeCheckbox.addEventListener('change', () => {
        renderScene();
    });

    // 마우스 이벤트 (간단한 팬 기능)
    canvas.addEventListener('mousedown', (e) => {
        isDragging = true;
        lastMousePos = { x: e.clientX, y: e.clientY };
    });

    canvas.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const dx = e.clientX - lastMousePos.x;
        const dy = e.clientY - lastMousePos.y;

        // 간단한 팬 (정확한 쌍곡 변환은 더 복잡함)
        const shift = new Complex(dx / renderer.radius * 0.1, -dy / renderer.radius * 0.1);
        const translation = MobiusTransform.translation(shift);
        renderer.viewTransform = translation.compose(renderer.viewTransform);

        lastMousePos = { x: e.clientX, y: e.clientY };
        renderScene();
    });

    canvas.addEventListener('mouseup', () => {
        isDragging = false;
    });

    canvas.addEventListener('mouseleave', () => {
        isDragging = false;
    });

    // 휠 줌 (간단한 구현)
    canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        const zoomFactor = e.deltaY > 0 ? 1.1 : 0.9;
        const scale = new MobiusTransform(
            new Complex(zoomFactor, 0), Complex.zero(),
            Complex.zero(), Complex.one()
        );
        renderer.viewTransform = scale.compose(renderer.viewTransform);
        renderScene();
    });

    function generateAndRender() {
        const depth = parseInt(depthSlider.value);
        tiling.generate(depth);
        renderScene();

        stats.textContent = `Tiles: ${tiling.tiles.length}`;
    }

    function renderScene() {
        renderer.clear();
        renderer.drawDiskBoundary();

        const showEdges = showEdgesCheckbox.checked;
        const colorMode = colorModeCheckbox.checked;

        tiling.render(showEdges, colorMode);
    }
}

// 초기화
window.addEventListener('load', init);

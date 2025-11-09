// ===================================================================
// Complex Number Class - 복소수 연산
// ===================================================================
export class Complex {
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

    static zero() {
        return new Complex(0, 0);
    }

    static one() {
        return new Complex(1, 0);
    }
}

// ===================================================================
// Möbius Transform
// ===================================================================
export class MobiusTransform {
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

    static translation(z) {
        const zConj = z.conjugate();
        return new MobiusTransform(
            new Complex(1, 0),
            z.scale(-1),
            zConj.scale(-1),
            new Complex(1, 0)
        );
    }
}

// ===================================================================
// Poincaré Disk Renderer
// ===================================================================
export class PoincareRenderer {
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

    complexToCanvas(z) {
        return {
            x: this.center.x + z.re * this.radius,
            y: this.center.y - z.im * this.radius
        };
    }

    drawGeodesic(z1, z2, strokeStyle = '#00ff88', lineWidth = 2) {
        z1 = this.viewTransform.apply(z1);
        z2 = this.viewTransform.apply(z2);

        const p1 = this.complexToCanvas(z1);
        const p2 = this.complexToCanvas(z2);

        this.ctx.strokeStyle = strokeStyle;
        this.ctx.lineWidth = lineWidth;

        const dist = Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
        if (dist < 0.5) return;

        const cross = z1.re * z2.im - z1.im * z2.re;

        if (Math.abs(cross) < 1e-10) {
            this.ctx.beginPath();
            this.ctx.moveTo(p1.x, p1.y);
            this.ctx.lineTo(p2.x, p2.y);
            this.ctx.stroke();
        } else {
            const circle = this.findGeodesicCircle(z1, z2);
            if (circle) {
                this.drawArc(z1, z2, circle, p1, p2);
            }
        }
    }

    findGeodesicCircle(z1, z2) {
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

    drawArc(z1, z2, circle, p1, p2) {
        const centerCanvas = this.complexToCanvas(circle.center);
        const radiusCanvas = circle.radius * this.radius;

        const angle1 = Math.atan2(p1.y - centerCanvas.y, p1.x - centerCanvas.x);
        const angle2 = Math.atan2(p2.y - centerCanvas.y, p2.x - centerCanvas.x);

        let angleDiff = angle2 - angle1;
        while (angleDiff > Math.PI) angleDiff -= 2 * Math.PI;
        while (angleDiff < -Math.PI) angleDiff += 2 * Math.PI;

        const anticlockwise = angleDiff < 0;

        this.ctx.beginPath();
        this.ctx.arc(centerCanvas.x, centerCanvas.y, radiusCanvas,
                     angle1, angle2, anticlockwise);
        this.ctx.stroke();
    }

    drawPolygon(vertices, fillStyle, strokeStyle = '#00ff88', lineWidth = 2) {
        if (vertices.length < 3) return;

        if (fillStyle) {
            this.ctx.fillStyle = fillStyle;
            this.ctx.beginPath();

            const segments = 20;
            for (let i = 0; i < vertices.length; i++) {
                const v1 = vertices[i];
                const v2 = vertices[(i + 1) % vertices.length];

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

    interpolateGeodesic(z1, z2, t) {
        return new Complex(
            z1.re + (z2.re - z1.re) * t,
            z1.im + (z2.im - z1.im) * t
        );
    }

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
// Heptagonal Tiling Generator
// ===================================================================
export class HeptagonalTiling {
    constructor(renderer) {
        this.renderer = renderer;
        this.tiles = [];
        this.p = 7;
        this.q = 3;
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
        const r = Math.atanh(Math.cos(Math.PI / this.p) /
                            Math.cos(Math.PI / this.q - Math.PI / this.p));
        return Math.tanh(r / 2) * 0.95;
    }

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

    generate(depth = 4) {
        this.tiles = [];

        const centerHeptagon = {
            center: Complex.zero(),
            vertices: this.generateHeptagon(Complex.zero(), this.hyperbolicRadius, 0),
            depth: 0,
            id: '0'
        };

        this.tiles.push(centerHeptagon);

        const queue = [centerHeptagon];
        const visited = new Set(['0']);

        while (queue.length > 0 && this.tiles.length < 1000) {
            const tile = queue.shift();

            if (tile.depth >= depth) continue;

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

    createAdjacentTile(tile, edgeIndex) {
        const v1 = tile.vertices[edgeIndex];
        const v2 = tile.vertices[(edgeIndex + 1) % 7];

        const midpoint = new Complex(
            (v1.re + v2.re) / 2,
            (v1.im + v2.im) / 2
        );

        const toMidpoint = new Complex(
            midpoint.re - tile.center.re,
            midpoint.im - tile.center.im
        );

        const normal = new Complex(-toMidpoint.im, toMidpoint.re);
        const normalLength = normal.abs();

        if (normalLength < 1e-10) return null;

        const distance = this.hyperbolicRadius * 1.8;
        const newCenter = new Complex(
            midpoint.re + (normal.re / normalLength) * distance,
            midpoint.im + (normal.im / normalLength) * distance
        );

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
}

Complex.prototype.scale = function(s) {
    return new Complex(this.re * s, this.im * s);
};

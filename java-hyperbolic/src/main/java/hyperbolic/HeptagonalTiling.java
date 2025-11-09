package hyperbolic;

import java.util.*;

/**
 * Order-3 Heptagonal Tiling {7,3} 생성기
 */
public class HeptagonalTiling {
    private final int p = 7; // 다각형 변 개수
    private final int q = 3; // 한 꼭짓점에 모이는 다각형 개수
    private final double hyperbolicRadius;
    private final List<Tile> tiles;

    public static class Tile {
        public final Complex center;
        public final List<Complex> vertices;
        public final int depth;
        public final String id;

        public Tile(Complex center, List<Complex> vertices, int depth, String id) {
            this.center = center;
            this.vertices = vertices;
            this.depth = depth;
            this.id = id;
        }
    }

    public HeptagonalTiling() {
        this.hyperbolicRadius = calculateHyperbolicRadius();
        this.tiles = new ArrayList<>();
    }

    private double calculateHyperbolicRadius() {
        double r = Math.atanh(Math.cos(Math.PI / p) /
                             Math.cos(Math.PI / q - Math.PI / p));
        return Math.tanh(r / 2) * 0.95;
    }

    public List<Complex> generateHeptagon(Complex center, double radius, double rotation) {
        List<Complex> vertices = new ArrayList<>();
        for (int i = 0; i < 7; i++) {
            double angle = rotation + (2 * Math.PI * i) / 7;
            Complex vertex = new Complex(
                center.re + radius * Math.cos(angle),
                center.im + radius * Math.sin(angle)
            );
            vertices.add(vertex);
        }
        return vertices;
    }

    public void generate(int depth) {
        tiles.clear();

        // 중앙 칠각형
        Tile centerTile = new Tile(
            Complex.zero(),
            generateHeptagon(Complex.zero(), hyperbolicRadius, 0),
            0,
            "0"
        );

        tiles.add(centerTile);

        // BFS
        Queue<Tile> queue = new LinkedList<>();
        Set<String> visited = new HashSet<>();

        queue.add(centerTile);
        visited.add("0");

        while (!queue.isEmpty() && tiles.size() < 1000) {
            Tile tile = queue.poll();

            if (tile.depth >= depth) continue;

            // 각 변에 대해 인접 타일 생성
            for (int i = 0; i < 7; i++) {
                String edgeId = tile.id + "-" + i;
                if (visited.contains(edgeId)) continue;

                Tile newTile = createAdjacentTile(tile, i, edgeId);

                if (newTile != null && newTile.center.abs() < 0.98) {
                    tiles.add(newTile);
                    queue.add(newTile);
                    visited.add(edgeId);
                }
            }
        }
    }

    private Tile createAdjacentTile(Tile tile, int edgeIndex, String id) {
        Complex v1 = tile.vertices.get(edgeIndex);
        Complex v2 = tile.vertices.get((edgeIndex + 1) % 7);

        // 변의 중점
        Complex midpoint = new Complex(
            (v1.re + v2.re) / 2,
            (v1.im + v2.im) / 2
        );

        // 중심에서 중점으로의 벡터
        Complex toMidpoint = new Complex(
            midpoint.re - tile.center.re,
            midpoint.im - tile.center.im
        );

        // 법선 방향 (90도 회전)
        Complex normal = new Complex(-toMidpoint.im, toMidpoint.re);
        double normalLength = normal.abs();

        if (normalLength < 1e-10) return null;

        // 새 중심 위치
        double distance = hyperbolicRadius * 1.8;
        Complex newCenter = new Complex(
            midpoint.re + (normal.re / normalLength) * distance,
            midpoint.im + (normal.im / normalLength) * distance
        );

        // 회전각
        double angle = Math.atan2(
            midpoint.im - tile.center.im,
            midpoint.re - tile.center.re
        );
        double rotation = angle + Math.PI;

        List<Complex> vertices = generateHeptagon(newCenter, hyperbolicRadius, rotation);

        return new Tile(newCenter, vertices, tile.depth + 1, id);
    }

    public List<Tile> getTiles() {
        return tiles;
    }

    public int getTileCount() {
        return tiles.size();
    }
}

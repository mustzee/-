package hyperbolic;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.*;
import java.util.List;

/**
 * Poincaré Disk 렌더링 패널
 */
public class PoincarePanel extends JPanel {
    private static final int SIZE = 800;
    private static final Color BACKGROUND = new Color(15, 15, 30);
    private static final Color BOUNDARY_COLOR = new Color(0, 255, 136);
    private static final Color[] TILE_COLORS = {
        new Color(255, 107, 107, 150),
        new Color(78, 205, 196, 150),
        new Color(255, 195, 113, 150),
        new Color(199, 125, 255, 150),
        new Color(255, 159, 243, 150),
        new Color(132, 250, 176, 150),
        new Color(255, 218, 121, 150)
    };

    private HeptagonalTiling tiling;
    private boolean showEdges = true;
    private boolean colorMode = true;
    private int maxTileIndex = -1; // 애니메이션용: -1이면 모두 표시

    private final double centerX;
    private final double centerY;
    private final double radius;

    public PoincarePanel(HeptagonalTiling tiling) {
        this.tiling = tiling;
        this.centerX = SIZE / 2.0;
        this.centerY = SIZE / 2.0;
        this.radius = SIZE / 2.0 - 20;

        setPreferredSize(new Dimension(SIZE, SIZE));
        setBackground(BACKGROUND);
    }

    public void setTiling(HeptagonalTiling tiling) {
        this.tiling = tiling;
        repaint();
    }

    public void setShowEdges(boolean showEdges) {
        this.showEdges = showEdges;
        repaint();
    }

    public void setColorMode(boolean colorMode) {
        this.colorMode = colorMode;
        repaint();
    }

    public void setMaxTileIndex(int index) {
        this.maxTileIndex = index;
        repaint();
    }

    public void resetMaxTileIndex() {
        this.maxTileIndex = -1;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        // 안티앨리어싱
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                            RenderingHints.VALUE_ANTIALIAS_ON);
        g2d.setRenderingHint(RenderingHints.KEY_RENDERING,
                            RenderingHints.VALUE_RENDER_QUALITY);

        // 배경
        g2d.setColor(BACKGROUND);
        g2d.fillRect(0, 0, SIZE, SIZE);

        // 타일 그리기
        drawTiles(g2d);

        // 경계원 그리기
        drawBoundary(g2d);
    }

    private void drawTiles(Graphics2D g2d) {
        if (tiling == null) return;

        List<HeptagonalTiling.Tile> tiles = tiling.getTiles();
        int limit = maxTileIndex >= 0 ? Math.min(maxTileIndex + 1, tiles.size()) : tiles.size();

        for (int i = 0; i < limit; i++) {
            HeptagonalTiling.Tile tile = tiles.get(i);
            drawPolygon(g2d, tile.vertices, i);
        }
    }

    private void drawPolygon(Graphics2D g2d, List<Complex> vertices, int index) {
        if (vertices.size() < 3) return;

        // 채우기
        if (colorMode) {
            Color fillColor = TILE_COLORS[index % TILE_COLORS.length];
            g2d.setColor(fillColor);

            Path2D path = new Path2D.Double();
            boolean first = true;

            for (int i = 0; i < vertices.size(); i++) {
                Complex v1 = vertices.get(i);
                Complex v2 = vertices.get((i + 1) % vertices.size());

                // 측지선 보간
                for (int t = 0; t <= 20; t++) {
                    double s = t / 20.0;
                    Complex point = new Complex(
                        v1.re + (v2.re - v1.re) * s,
                        v1.im + (v2.im - v1.im) * s
                    );

                    Point2D.Double p = complexToCanvas(point);

                    if (first) {
                        path.moveTo(p.x, p.y);
                        first = false;
                    } else {
                        path.lineTo(p.x, p.y);
                    }
                }
            }

            path.closePath();
            g2d.fill(path);
        }

        // 외곽선
        if (showEdges) {
            g2d.setColor(BOUNDARY_COLOR);
            g2d.setStroke(new BasicStroke(1.5f));

            for (int i = 0; i < vertices.size(); i++) {
                Complex v1 = vertices.get(i);
                Complex v2 = vertices.get((i + 1) % vertices.size());
                drawGeodesic(g2d, v1, v2);
            }
        }
    }

    private void drawGeodesic(Graphics2D g2d, Complex z1, Complex z2) {
        Point2D.Double p1 = complexToCanvas(z1);
        Point2D.Double p2 = complexToCanvas(z2);

        double cross = z1.re * z2.im - z1.im * z2.re;

        if (Math.abs(cross) < 1e-10) {
            // 직선
            g2d.draw(new Line2D.Double(p1, p2));
        } else {
            // 원호
            GeodesicCircle circle = findGeodesicCircle(z1, z2);
            if (circle != null) {
                drawArc(g2d, z1, z2, circle);
            }
        }
    }

    private static class GeodesicCircle {
        Complex center;
        double radius;

        GeodesicCircle(Complex center, double radius) {
            this.center = center;
            this.radius = radius;
        }
    }

    private GeodesicCircle findGeodesicCircle(Complex z1, Complex z2) {
        double z1AbsSq = z1.re * z1.re + z1.im * z1.im;
        double z2AbsSq = z2.re * z2.re + z2.im * z2.im;

        double denom = 2 * (z1.re * z2.im - z1.im * z2.re);
        if (Math.abs(denom) < 1e-10) return null;

        double centerX = (z2.im * z1AbsSq - z1.im * z2AbsSq) / denom;
        double centerY = (z1.re * z2AbsSq - z2.re * z1AbsSq) / denom;

        Complex center = new Complex(centerX, centerY);
        double radius = center.sub(z1).abs();

        return new GeodesicCircle(center, radius);
    }

    private void drawArc(Graphics2D g2d, Complex z1, Complex z2, GeodesicCircle circle) {
        Point2D.Double centerCanvas = complexToCanvas(circle.center);
        double radiusCanvas = circle.radius * this.radius;

        Point2D.Double p1 = complexToCanvas(z1);
        Point2D.Double p2 = complexToCanvas(z2);

        double angle1 = Math.atan2(p1.y - centerCanvas.y, p1.x - centerCanvas.x);
        double angle2 = Math.atan2(p2.y - centerCanvas.y, p2.x - centerCanvas.x);

        double angleDiff = angle2 - angle1;
        while (angleDiff > Math.PI) angleDiff -= 2 * Math.PI;
        while (angleDiff < -Math.PI) angleDiff += 2 * Math.PI;

        double startAngle = Math.toDegrees(angle1);
        double extent = Math.toDegrees(angleDiff);

        Arc2D arc = new Arc2D.Double(
            centerCanvas.x - radiusCanvas,
            centerCanvas.y - radiusCanvas,
            2 * radiusCanvas,
            2 * radiusCanvas,
            startAngle,
            extent,
            Arc2D.OPEN
        );

        g2d.draw(arc);
    }

    private void drawBoundary(Graphics2D g2d) {
        g2d.setColor(BOUNDARY_COLOR);
        g2d.setStroke(new BasicStroke(3.0f));
        g2d.draw(new Ellipse2D.Double(
            centerX - radius,
            centerY - radius,
            2 * radius,
            2 * radius
        ));
    }

    private Point2D.Double complexToCanvas(Complex z) {
        return new Point2D.Double(
            centerX + z.re * radius,
            centerY - z.im * radius
        );
    }
}

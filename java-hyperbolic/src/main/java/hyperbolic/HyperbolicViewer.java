package hyperbolic;

import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

/**
 * Order-3 Heptagonal Tiling 메인 애플리케이션
 */
public class HyperbolicViewer extends JFrame {
    private static final Color BACKGROUND = new Color(26, 26, 46);
    private static final Color PANEL_BG = new Color(22, 33, 62);
    private static final Color TEXT_COLOR = new Color(170, 170, 170);
    private static final Color ACCENT_COLOR = new Color(0, 255, 136);

    private HeptagonalTiling tiling;
    private PoincarePanel canvas;
    private JSlider depthSlider;
    private JCheckBox edgesCheckbox;
    private JCheckBox colorCheckbox;
    private JCheckBox animateCheckbox;
    private JButton resetButton;
    private JButton playButton;
    private JLabel tileCountLabel;
    private JLabel progressLabel;

    private Timer animationTimer;
    private int currentAnimationIndex = 0;
    private boolean isAnimating = false;

    public HyperbolicViewer() {
        super("Order-3 Heptagonal Tiling {7,3}");

        tiling = new HeptagonalTiling();
        tiling.generate(4);

        setupUI();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        pack();
        setLocationRelativeTo(null);
        setResizable(false);
    }

    private void setupUI() {
        setLayout(new BorderLayout(10, 10));
        getContentPane().setBackground(BACKGROUND);

        // 헤더
        add(createHeader(), BorderLayout.NORTH);

        // 캔버스
        canvas = new PoincarePanel(tiling);
        add(canvas, BorderLayout.CENTER);

        // 컨트롤 패널
        add(createControlPanel(), BorderLayout.SOUTH);

        updateStats();
    }

    private JPanel createHeader() {
        JPanel header = new JPanel();
        header.setBackground(PANEL_BG);
        header.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        JLabel title = new JLabel("Order-3 Heptagonal Tiling {7,3}");
        title.setFont(new Font("SansSerif", Font.BOLD, 28));
        title.setForeground(ACCENT_COLOR);

        JLabel subtitle = new JLabel("Poincaré Disk Model - Java Swing Implementation");
        subtitle.setFont(new Font("SansSerif", Font.PLAIN, 14));
        subtitle.setForeground(TEXT_COLOR);

        header.setLayout(new BoxLayout(header, BoxLayout.Y_AXIS));
        title.setAlignmentX(Component.CENTER_ALIGNMENT);
        subtitle.setAlignmentX(Component.CENTER_ALIGNMENT);

        header.add(title);
        header.add(Box.createVerticalStrut(5));
        header.add(subtitle);

        return header;
    }

    private JPanel createControlPanel() {
        JPanel panel = new JPanel();
        panel.setBackground(PANEL_BG);
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));

        // Depth 슬라이더
        panel.add(createSliderPanel());
        panel.add(Box.createVerticalStrut(15));

        // 체크박스
        panel.add(createCheckboxPanel());
        panel.add(Box.createVerticalStrut(15));

        // 버튼
        panel.add(createButtonPanel());
        panel.add(Box.createVerticalStrut(15));

        // 통계
        panel.add(createStatsPanel());

        return panel;
    }

    private JPanel createSliderPanel() {
        JPanel panel = new JPanel(new BorderLayout(10, 5));
        panel.setBackground(PANEL_BG);

        JLabel label = new JLabel("Depth:");
        label.setForeground(TEXT_COLOR);
        label.setFont(new Font("SansSerif", Font.PLAIN, 14));

        depthSlider = new JSlider(1, 6, 4);
        depthSlider.setMajorTickSpacing(1);
        depthSlider.setPaintTicks(true);
        depthSlider.setPaintLabels(true);
        depthSlider.setBackground(PANEL_BG);
        depthSlider.setForeground(TEXT_COLOR);

        depthSlider.addChangeListener(e -> {
            if (!depthSlider.getValueIsAdjusting() && !isAnimating) {
                updateTiling();
            }
        });

        panel.add(label, BorderLayout.WEST);
        panel.add(depthSlider, BorderLayout.CENTER);

        return panel;
    }

    private JPanel createCheckboxPanel() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.LEFT, 20, 0));
        panel.setBackground(PANEL_BG);

        edgesCheckbox = new JCheckBox("Show Edges", true);
        styleCheckbox(edgesCheckbox);
        edgesCheckbox.addActionListener(e -> {
            canvas.setShowEdges(edgesCheckbox.isSelected());
        });

        colorCheckbox = new JCheckBox("Color Tiles", true);
        styleCheckbox(colorCheckbox);
        colorCheckbox.addActionListener(e -> {
            canvas.setColorMode(colorCheckbox.isSelected());
        });

        animateCheckbox = new JCheckBox("Animate Generation", false);
        styleCheckbox(animateCheckbox);
        animateCheckbox.addActionListener(e -> {
            boolean animate = animateCheckbox.isSelected();
            playButton.setEnabled(animate);
            if (!animate && animationTimer != null) {
                stopAnimation();
            }
        });

        panel.add(edgesCheckbox);
        panel.add(colorCheckbox);
        panel.add(animateCheckbox);

        return panel;
    }

    private void styleCheckbox(JCheckBox checkbox) {
        checkbox.setBackground(PANEL_BG);
        checkbox.setForeground(TEXT_COLOR);
        checkbox.setFont(new Font("SansSerif", Font.PLAIN, 14));
    }

    private JPanel createButtonPanel() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 0));
        panel.setBackground(PANEL_BG);

        resetButton = new JButton("Reset View");
        styleButton(resetButton, ACCENT_COLOR);
        resetButton.addActionListener(e -> resetView());

        playButton = new JButton("▶ Play");
        styleButton(playButton, new Color(78, 205, 196));
        playButton.setEnabled(false);
        playButton.addActionListener(e -> toggleAnimation());

        panel.add(resetButton);
        panel.add(playButton);

        return panel;
    }

    private void styleButton(JButton button, Color bg) {
        button.setBackground(bg);
        button.setForeground(new Color(26, 26, 46));
        button.setFont(new Font("SansSerif", Font.BOLD, 14));
        button.setFocusPainted(false);
        button.setBorderPainted(false);
        button.setPreferredSize(new Dimension(150, 40));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
    }

    private JPanel createStatsPanel() {
        JPanel panel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        panel.setBackground(PANEL_BG);
        panel.setBorder(BorderFactory.createMatteBorder(1, 0, 0, 0, new Color(42, 42, 78)));
        panel.setBorder(BorderFactory.createCompoundBorder(
            panel.getBorder(),
            BorderFactory.createEmptyBorder(10, 0, 0, 0)
        ));

        tileCountLabel = new JLabel("Tiles: 0");
        tileCountLabel.setForeground(new Color(136, 136, 136));
        tileCountLabel.setFont(new Font("Monospaced", Font.PLAIN, 12));

        progressLabel = new JLabel("");
        progressLabel.setForeground(ACCENT_COLOR);
        progressLabel.setFont(new Font("Monospaced", Font.BOLD, 12));

        panel.add(tileCountLabel);
        panel.add(Box.createHorizontalStrut(20));
        panel.add(progressLabel);

        return panel;
    }

    private void updateTiling() {
        int depth = depthSlider.getValue();

        if (animateCheckbox.isSelected()) {
            tiling.generate(depth);
            startAnimation();
        } else {
            tiling.generate(depth);
            canvas.setTiling(tiling);
            canvas.resetMaxTileIndex();
            updateStats();
        }
    }

    private void startAnimation() {
        if (animationTimer != null) {
            animationTimer.stop();
        }

        currentAnimationIndex = 0;
        isAnimating = true;
        playButton.setText("⏸ Pause");

        int totalTiles = tiling.getTileCount();
        int delay = Math.max(10, Math.min(100, 2000 / totalTiles));

        animationTimer = new Timer(delay, e -> {
            if (currentAnimationIndex < totalTiles) {
                canvas.setMaxTileIndex(currentAnimationIndex);
                updateAnimationStats();
                currentAnimationIndex++;
            } else {
                stopAnimation();
            }
        });

        animationTimer.start();
    }

    private void stopAnimation() {
        if (animationTimer != null) {
            animationTimer.stop();
        }
        isAnimating = false;
        playButton.setText("▶ Play");
        canvas.resetMaxTileIndex();
        updateStats();
    }

    private void toggleAnimation() {
        if (isAnimating) {
            stopAnimation();
        } else {
            startAnimation();
        }
    }

    private void resetView() {
        if (animationTimer != null) {
            animationTimer.stop();
        }
        isAnimating = false;
        currentAnimationIndex = 0;
        canvas.resetMaxTileIndex();
        updateTiling();
        playButton.setText("▶ Play");
    }

    private void updateStats() {
        tileCountLabel.setText("Tiles: " + tiling.getTileCount());
        progressLabel.setText("");
    }

    private void updateAnimationStats() {
        int total = tiling.getTileCount();
        int current = currentAnimationIndex + 1;
        int percent = (int) ((current / (double) total) * 100);

        tileCountLabel.setText("Tiles: " + current + " / " + total);
        progressLabel.setText("Progress: " + percent + "%");
    }

    public static void main(String[] args) {
        // Look and Feel 설정
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        SwingUtilities.invokeLater(() -> {
            HyperbolicViewer viewer = new HyperbolicViewer();
            viewer.setVisible(true);

            System.out.println("=".repeat(60));
            System.out.println("Order-3 Heptagonal Tiling {7,3}");
            System.out.println("Poincaré Disk Model - Java Swing");
            System.out.println("=".repeat(60));
            System.out.println("\n컨트롤:");
            System.out.println("  - Depth 슬라이더: 타일링 깊이 조절 (1-6)");
            System.out.println("  - Show Edges: 경계선 표시/숨김");
            System.out.println("  - Color Tiles: 색상 모드 전환");
            System.out.println("  - Animate Generation: 단계별 생성 애니메이션");
            System.out.println("  - Reset View: 초기 상태로 복귀");
            System.out.println("\n창을 닫으면 프로그램이 종료됩니다.");
            System.out.println("=".repeat(60));
        });
    }
}

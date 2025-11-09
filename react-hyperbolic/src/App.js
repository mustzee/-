import React, { useRef, useEffect, useState } from 'react';
import './App.css';
import { Complex, MobiusTransform, PoincareRenderer, HeptagonalTiling } from './hyperbolic';

function App() {
  const canvasRef = useRef(null);
  const [depth, setDepth] = useState(4);
  const [showEdges, setShowEdges] = useState(true);
  const [colorMode, setColorMode] = useState(true);
  const [animate, setAnimate] = useState(false);
  const [currentTileIndex, setCurrentTileIndex] = useState(0);
  const [tileCount, setTileCount] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  const rendererRef = useRef(null);
  const tilingRef = useRef(null);
  const animationFrameRef = useRef(null);

  // 초기화
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    rendererRef.current = new PoincareRenderer(canvas);
    tilingRef.current = new HeptagonalTiling(rendererRef.current);

    renderScene();
  }, []);

  // depth 변경 시
  useEffect(() => {
    if (!tilingRef.current) return;

    if (animate) {
      startAnimation();
    } else {
      tilingRef.current.generate(depth);
      setTileCount(tilingRef.current.tiles.length);
      renderScene();
    }
  }, [depth, animate]);

  // 렌더링 옵션 변경 시
  useEffect(() => {
    renderScene();
  }, [showEdges, colorMode, currentTileIndex]);

  const renderScene = () => {
    if (!rendererRef.current || !tilingRef.current) return;

    const renderer = rendererRef.current;
    const tiling = tilingRef.current;

    renderer.clear();
    renderer.drawDiskBoundary();

    // 애니메이션 모드: 현재 인덱스까지만 그리기
    if (isAnimating && animate) {
      const tilesToRender = tiling.tiles.slice(0, currentTileIndex + 1);
      renderTiles(tilesToRender);
    } else {
      renderTiles(tiling.tiles);
    }

    setTileCount(isAnimating ? currentTileIndex + 1 : tiling.tiles.length);
  };

  const renderTiles = (tiles) => {
    const renderer = rendererRef.current;
    const tiling = tilingRef.current;

    for (let i = 0; i < tiles.length; i++) {
      const tile = tiles[i];
      const color = colorMode ? tiling.colors[i % tiling.colors.length] : 'rgba(50, 50, 80, 0.6)';
      const strokeStyle = showEdges ? '#00ff88' : null;
      const lineWidth = showEdges ? 1.5 : 0;

      renderer.drawPolygon(tile.vertices, color, strokeStyle, lineWidth);
    }
  };

  const startAnimation = () => {
    if (!tilingRef.current) return;

    // 타일 생성
    tilingRef.current.generate(depth);
    const totalTiles = tilingRef.current.tiles.length;

    setCurrentTileIndex(0);
    setIsAnimating(true);

    let index = 0;
    const animationSpeed = Math.max(10, Math.min(100, 2000 / totalTiles)); // 속도 조절

    const animateStep = () => {
      if (index < totalTiles) {
        setCurrentTileIndex(index);
        index++;
        animationFrameRef.current = setTimeout(animateStep, animationSpeed);
      } else {
        setIsAnimating(false);
      }
    };

    animateStep();
  };

  const handleReset = () => {
    if (animationFrameRef.current) {
      clearTimeout(animationFrameRef.current);
    }
    setIsAnimating(false);
    setCurrentTileIndex(0);
    rendererRef.current.viewTransform = new MobiusTransform(
      Complex.one(), Complex.zero(),
      Complex.zero(), Complex.one()
    );
    if (tilingRef.current) {
      tilingRef.current.generate(depth);
      setTileCount(tilingRef.current.tiles.length);
    }
    renderScene();
  };

  const handlePlayAnimation = () => {
    if (isAnimating) {
      // 정지
      if (animationFrameRef.current) {
        clearTimeout(animationFrameRef.current);
      }
      setIsAnimating(false);
    } else {
      // 재생
      startAnimation();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Order-3 Heptagonal Tiling {'{7,3}'}</h1>
        <p className="subtitle">Poincaré Disk Model - React Implementation</p>
      </header>

      <main className="App-main">
        <div className="canvas-container">
          <canvas
            ref={canvasRef}
            width={800}
            height={800}
            className="hyperbolic-canvas"
          />
        </div>

        <div className="controls">
          <div className="control-group">
            <label htmlFor="depth-slider">
              Depth: <span className="value">{depth}</span>
            </label>
            <input
              id="depth-slider"
              type="range"
              min="1"
              max="6"
              value={depth}
              onChange={(e) => setDepth(parseInt(e.target.value))}
              disabled={isAnimating}
            />
          </div>

          <div className="control-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={showEdges}
                onChange={(e) => setShowEdges(e.target.checked)}
              />
              Show Edges
            </label>
            <label>
              <input
                type="checkbox"
                checked={colorMode}
                onChange={(e) => setColorMode(e.target.checked)}
              />
              Color Tiles
            </label>
            <label>
              <input
                type="checkbox"
                checked={animate}
                onChange={(e) => setAnimate(e.target.checked)}
                disabled={isAnimating}
              />
              Animate Generation
            </label>
          </div>

          <div className="button-group">
            <button onClick={handleReset} className="btn btn-primary">
              Reset View
            </button>
            {animate && (
              <button onClick={handlePlayAnimation} className="btn btn-secondary">
                {isAnimating ? '⏸ Pause' : '▶ Play'}
              </button>
            )}
          </div>

          <div className="stats">
            <span>Tiles: {tileCount}</span>
            {isAnimating && (
              <span className="progress">
                Progress: {Math.round((currentTileIndex / tilingRef.current?.tiles.length) * 100)}%
              </span>
            )}
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>쌍곡 기하학에서의 정칠각형 타일링 시각화</p>
      </footer>
    </div>
  );
}

export default App;

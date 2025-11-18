/**
 * Tiny AI - 경량 신경망 구현체
 *
 * 특징:
 * - 순수 JavaScript (의존성 없음)
 * - 작은 메모리 footprint (~5KB)
 * - 빠른 추론 속도
 * - 간단한 API
 *
 * @version 1.0.0
 * @license MIT
 */

class TinyAI {
  /**
   * 경량 신경망 생성
   * @param {Array<number>} layers - 각 레이어의 뉴런 수 [입력, 은닉1, 은닉2, ..., 출력]
   * @param {string} activation - 활성화 함수 ('relu', 'sigmoid', 'tanh')
   */
  constructor(layers = [2, 4, 1], activation = 'relu') {
    this.layers = layers;
    this.activation = activation;
    this.weights = [];
    this.biases = [];

    // 가중치와 편향 초기화 (He initialization)
    for (let i = 0; i < layers.length - 1; i++) {
      const scale = Math.sqrt(2 / layers[i]); // He initialization
      const w = this.randomMatrix(layers[i + 1], layers[i], scale);
      const b = new Array(layers[i + 1]).fill(0);
      this.weights.push(w);
      this.biases.push(b);
    }
  }

  /**
   * 랜덤 행렬 생성
   */
  randomMatrix(rows, cols, scale = 1) {
    const matrix = [];
    for (let i = 0; i < rows; i++) {
      matrix[i] = [];
      for (let j = 0; j < cols; j++) {
        // Box-Muller 변환으로 정규분포 샘플링
        const u1 = Math.random();
        const u2 = Math.random();
        const gaussian = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        matrix[i][j] = gaussian * scale;
      }
    }
    return matrix;
  }

  /**
   * 활성화 함수
   */
  activate(x, derivative = false) {
    switch (this.activation) {
      case 'relu':
        return derivative ? (x > 0 ? 1 : 0) : Math.max(0, x);
      case 'sigmoid':
        const sig = 1 / (1 + Math.exp(-x));
        return derivative ? sig * (1 - sig) : sig;
      case 'tanh':
        const th = Math.tanh(x);
        return derivative ? 1 - th * th : th;
      default:
        return x;
    }
  }

  /**
   * 순전파 (Forward propagation)
   * @param {Array<number>} input - 입력 벡터
   * @returns {Array<number>} 출력 벡터
   */
  forward(input) {
    let activation = input;
    this.activations = [activation];
    this.zValues = []; // 활성화 전 값 저장

    for (let i = 0; i < this.weights.length; i++) {
      const z = this.matMul(this.weights[i], activation, this.biases[i]);
      this.zValues.push(z);
      activation = z.map(x => this.activate(x));
      this.activations.push(activation);
    }

    return activation;
  }

  /**
   * 예측
   * @param {Array<number>} input - 입력 데이터
   * @returns {Array<number>} 예측값
   */
  predict(input) {
    return this.forward(input);
  }

  /**
   * 학습 (경사하강법)
   * @param {Array<Array<number>>} X - 입력 데이터셋
   * @param {Array<Array<number>>} y - 정답 레이블
   * @param {Object} options - 학습 옵션
   */
  train(X, y, options = {}) {
    const {
      epochs = 1000,
      learningRate = 0.01,
      batchSize = 32,
      verbose = true
    } = options;

    const startTime = Date.now();

    for (let epoch = 0; epoch < epochs; epoch++) {
      let totalLoss = 0;

      // 미니배치 학습
      for (let i = 0; i < X.length; i += batchSize) {
        const batchX = X.slice(i, i + batchSize);
        const batchY = y.slice(i, i + batchSize);

        for (let j = 0; j < batchX.length; j++) {
          const input = batchX[j];
          const target = batchY[j];

          // Forward pass
          const output = this.forward(input);

          // 손실 계산 (MSE)
          const loss = output.reduce((sum, o, k) =>
            sum + Math.pow(o - target[k], 2), 0) / output.length;
          totalLoss += loss;

          // Backward pass
          this.backward(target, learningRate);
        }
      }

      // 로그 출력
      if (verbose && (epoch % 100 === 0 || epoch === epochs - 1)) {
        const avgLoss = (totalLoss / X.length).toFixed(6);
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
        console.log(`Epoch ${epoch + 1}/${epochs} - Loss: ${avgLoss} - Time: ${elapsed}s`);
      }
    }

    if (verbose) {
      const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);
      console.log(`✓ Training completed in ${totalTime}s`);
    }
  }

  /**
   * 역전파 (Backpropagation)
   */
  backward(target, learningRate) {
    const numLayers = this.weights.length;
    const deltas = new Array(numLayers);

    // 출력층 델타 계산
    const outputIdx = numLayers - 1;
    deltas[outputIdx] = [];
    for (let i = 0; i < this.activations[numLayers].length; i++) {
      const error = this.activations[numLayers][i] - target[i];
      const derivative = this.activate(this.zValues[outputIdx][i], true);
      deltas[outputIdx][i] = error * derivative;
    }

    // 은닉층 델타 역전파
    for (let layer = numLayers - 2; layer >= 0; layer--) {
      deltas[layer] = [];
      for (let i = 0; i < this.weights[layer].length; i++) {
        let error = 0;
        // 다음 층의 모든 뉴런으로부터 오차 역전파
        for (let j = 0; j < this.weights[layer + 1].length; j++) {
          error += this.weights[layer + 1][j][i] * deltas[layer + 1][j];
        }
        const derivative = this.activate(this.zValues[layer][i], true);
        deltas[layer][i] = error * derivative;
      }
    }

    // 가중치와 편향 업데이트
    for (let layer = 0; layer < numLayers; layer++) {
      for (let i = 0; i < this.weights[layer].length; i++) {
        // 가중치 업데이트
        for (let j = 0; j < this.weights[layer][i].length; j++) {
          const gradient = deltas[layer][i] * this.activations[layer][j];
          this.weights[layer][i][j] -= learningRate * gradient;
        }
        // 편향 업데이트
        this.biases[layer][i] -= learningRate * deltas[layer][i];
      }
    }
  }

  /**
   * 행렬-벡터 곱셈
   */
  matMul(matrix, vector, bias) {
    return matrix.map((row, i) => {
      const sum = row.reduce((acc, val, j) => acc + val * vector[j], 0);
      return sum + bias[i];
    });
  }

  /**
   * 모델 저장 (JSON)
   */
  save() {
    return JSON.stringify({
      layers: this.layers,
      activation: this.activation,
      weights: this.weights,
      biases: this.biases
    });
  }

  /**
   * 모델 불러오기 (JSON)
   */
  static load(jsonString) {
    const data = JSON.parse(jsonString);
    const model = new TinyAI(data.layers, data.activation);
    model.weights = data.weights;
    model.biases = data.biases;
    return model;
  }

  /**
   * 모델 정보 출력
   */
  summary() {
    console.log('='.repeat(50));
    console.log('Tiny AI Model Summary');
    console.log('='.repeat(50));
    console.log(`Architecture: ${this.layers.join(' → ')}`);
    console.log(`Activation: ${this.activation}`);

    let totalParams = 0;
    for (let i = 0; i < this.weights.length; i++) {
      const params = this.weights[i].length * this.weights[i][0].length + this.biases[i].length;
      totalParams += params;
      console.log(`Layer ${i + 1}: ${params} parameters`);
    }

    console.log(`Total parameters: ${totalParams}`);
    console.log(`Memory: ~${(totalParams * 8 / 1024).toFixed(2)} KB`);
    console.log('='.repeat(50));
  }
}

// 유틸리티 함수들

/**
 * 데이터 정규화
 */
function normalize(data) {
  const min = Math.min(...data.flat());
  const max = Math.max(...data.flat());
  return data.map(row =>
    Array.isArray(row)
      ? row.map(x => (x - min) / (max - min))
      : (row - min) / (max - min)
  );
}

/**
 * 정확도 계산 (분류 문제)
 */
function accuracy(model, X, y) {
  let correct = 0;
  for (let i = 0; i < X.length; i++) {
    const pred = model.predict(X[i]);
    const predicted = pred[0] > 0.5 ? 1 : 0;
    const actual = y[i][0];
    if (predicted === actual) correct++;
  }
  return (correct / X.length * 100).toFixed(2);
}

/**
 * 데이터 섞기
 */
function shuffle(X, y) {
  const indices = Array.from({ length: X.length }, (_, i) => i);
  for (let i = indices.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [indices[i], indices[j]] = [indices[j], indices[i]];
  }
  return {
    X: indices.map(i => X[i]),
    y: indices.map(i => y[i])
  };
}

// Node.js 환경 지원
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TinyAI, normalize, accuracy, shuffle };
}

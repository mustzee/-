/**
 * Tiny AI 테스트 스위트
 *
 * 실행 방법:
 * - 브라우저: tiny-ai-demo.html 사용
 * - Node.js: node test-tiny-ai.js
 */

// Node.js 환경 체크
const isNode = typeof module !== 'undefined' && module.exports;
if (isNode) {
  const { TinyAI, normalize, accuracy, shuffle } = require('./tiny-ai');
  global.TinyAI = TinyAI;
  global.normalize = normalize;
  global.accuracy = accuracy;
  global.shuffle = shuffle;
}

// 테스트 결과 저장
const testResults = {
  passed: 0,
  failed: 0,
  tests: []
};

// 테스트 헬퍼 함수
function assert(condition, message) {
  if (condition) {
    testResults.passed++;
    testResults.tests.push({ status: '✓', message });
    console.log(`✓ ${message}`);
  } else {
    testResults.failed++;
    testResults.tests.push({ status: '✗', message });
    console.error(`✗ ${message}`);
  }
}

function assertClose(a, b, tolerance, message) {
  const diff = Math.abs(a - b);
  assert(diff < tolerance, `${message} (차이: ${diff.toFixed(6)})`);
}

console.log('='.repeat(60));
console.log('🧪 Tiny AI 테스트 시작');
console.log('='.repeat(60));
console.log();

// ========================================
// 1. 모델 생성 테스트
// ========================================
console.log('📦 1. 모델 생성 테스트');
console.log('-'.repeat(60));

try {
  const model1 = new TinyAI([2, 4, 1], 'sigmoid');
  assert(model1.layers.length === 3, '레이어 개수 확인');
  assert(model1.weights.length === 2, '가중치 행렬 개수 확인');
  assert(model1.biases.length === 2, '편향 벡터 개수 확인');
  assert(model1.activation === 'sigmoid', '활성화 함수 확인');
} catch (e) {
  assert(false, `모델 생성 실패: ${e.message}`);
}

try {
  const model2 = new TinyAI([10, 20, 10, 5], 'relu');
  assert(model2.layers.length === 4, '다층 네트워크 생성');
  assert(model2.weights[0].length === 20, '첫 번째 가중치 행렬 크기');
  assert(model2.weights[0][0].length === 10, '첫 번째 가중치 행렬 크기');
} catch (e) {
  assert(false, `다층 모델 생성 실패: ${e.message}`);
}

console.log();

// ========================================
// 2. 활성화 함수 테스트
// ========================================
console.log('🔄 2. 활성화 함수 테스트');
console.log('-'.repeat(60));

const modelRelu = new TinyAI([1, 1], 'relu');
assertClose(modelRelu.activate(5), 5, 0.001, 'ReLU(5) = 5');
assertClose(modelRelu.activate(-5), 0, 0.001, 'ReLU(-5) = 0');

const modelSigmoid = new TinyAI([1, 1], 'sigmoid');
assertClose(modelSigmoid.activate(0), 0.5, 0.001, 'Sigmoid(0) = 0.5');
assert(modelSigmoid.activate(10) > 0.99, 'Sigmoid(10) > 0.99');
assert(modelSigmoid.activate(-10) < 0.01, 'Sigmoid(-10) < 0.01');

const modelTanh = new TinyAI([1, 1], 'tanh');
assertClose(modelTanh.activate(0), 0, 0.001, 'Tanh(0) = 0');
assert(modelTanh.activate(10) > 0.99, 'Tanh(10) > 0.99');
assert(modelTanh.activate(-10) < -0.99, 'Tanh(-10) < -0.99');

console.log();

// ========================================
// 3. 순전파 테스트
// ========================================
console.log('➡️  3. 순전파 테스트');
console.log('-'.repeat(60));

const model3 = new TinyAI([2, 3, 1], 'sigmoid');
const output3 = model3.predict([0.5, 0.5]);

assert(Array.isArray(output3), '출력이 배열인지 확인');
assert(output3.length === 1, '출력 크기 확인');
assert(output3[0] >= 0 && output3[0] <= 1, 'Sigmoid 출력 범위 확인');

console.log();

// ========================================
// 4. XOR 학습 테스트
// ========================================
console.log('🧠 4. XOR 학습 테스트');
console.log('-'.repeat(60));

const xorModel = new TinyAI([2, 4, 1], 'sigmoid');
const xorX = [[0, 0], [0, 1], [1, 0], [1, 1]];
const xorY = [[0], [1], [1], [0]];

console.log('XOR 학습 시작 (2000 epochs)...');
xorModel.train(xorX, xorY, {
  epochs: 2000,
  learningRate: 0.5,
  batchSize: 4,
  verbose: false
});

const pred00 = xorModel.predict([0, 0])[0];
const pred01 = xorModel.predict([0, 1])[0];
const pred10 = xorModel.predict([1, 0])[0];
const pred11 = xorModel.predict([1, 1])[0];

console.log(`  [0, 0] → ${pred00.toFixed(4)} (정답: 0)`);
console.log(`  [0, 1] → ${pred01.toFixed(4)} (정답: 1)`);
console.log(`  [1, 0] → ${pred10.toFixed(4)} (정답: 1)`);
console.log(`  [1, 1] → ${pred11.toFixed(4)} (정답: 0)`);

assert(pred00 < 0.2, 'XOR [0,0] 예측');
assert(pred01 > 0.8, 'XOR [0,1] 예측');
assert(pred10 > 0.8, 'XOR [1,0] 예측');
assert(pred11 < 0.2, 'XOR [1,1] 예측');

console.log();

// ========================================
// 5. AND 학습 테스트 (간단한 선형 분류)
// ========================================
console.log('🔗 5. AND 학습 테스트');
console.log('-'.repeat(60));

const andModel = new TinyAI([2, 1], 'sigmoid');
const andX = [[0, 0], [0, 1], [1, 0], [1, 1]];
const andY = [[0], [0], [0], [1]];

console.log('AND 학습 시작 (1000 epochs)...');
andModel.train(andX, andY, {
  epochs: 1000,
  learningRate: 0.5,
  batchSize: 4,
  verbose: false
});

const andAcc = accuracy(andModel, andX, andY);
console.log(`  정확도: ${andAcc}%`);
assert(parseFloat(andAcc) >= 75, 'AND 정확도 >= 75%');

console.log();

// ========================================
// 6. 모델 저장/불러오기 테스트
// ========================================
console.log('💾 6. 모델 저장/불러오기 테스트');
console.log('-'.repeat(60));

const saveModel = new TinyAI([3, 5, 2], 'relu');
const testInput = [0.1, 0.2, 0.3];
const originalOutput = saveModel.predict(testInput);

const saved = saveModel.save();
assert(typeof saved === 'string', '저장된 모델이 문자열인지 확인');
assert(saved.length > 0, '저장된 모델이 비어있지 않은지 확인');

const loadedModel = TinyAI.load(saved);
const loadedOutput = loadedModel.predict(testInput);

assertClose(
  originalOutput[0],
  loadedOutput[0],
  0.0001,
  '저장/불러오기 후 동일한 출력'
);

console.log();

// ========================================
// 7. 유틸리티 함수 테스트
// ========================================
console.log('🛠️  7. 유틸리티 함수 테스트');
console.log('-'.repeat(60));

// normalize 테스트
const data = [[1, 2], [3, 4], [5, 6]];
const normalized = normalize(data);
assert(normalized[0][0] === 0, '정규화 최솟값 = 0');
assert(normalized[2][1] === 1, '정규화 최댓값 = 1');

// shuffle 테스트
const X = [[1, 2], [3, 4], [5, 6], [7, 8]];
const y = [[1], [2], [3], [4]];
const { X: shuffledX, y: shuffledY } = shuffle(X, y);
assert(shuffledX.length === X.length, 'Shuffle 후 크기 유지');
assert(shuffledY.length === y.length, 'Shuffle 후 크기 유지');

console.log();

// ========================================
// 8. 함수 근사 테스트 (회귀)
// ========================================
console.log('📈 8. 함수 근사 테스트 (y = 2x)');
console.log('-'.repeat(60));

const regressionX = [];
const regressionY = [];
for (let i = 0; i < 50; i++) {
  const x = i / 50;
  regressionX.push([x]);
  regressionY.push([2 * x]); // y = 2x
}

const regressionModel = new TinyAI([1, 5, 1], 'relu');
console.log('회귀 학습 시작 (500 epochs)...');
regressionModel.train(regressionX, regressionY, {
  epochs: 500,
  learningRate: 0.01,
  verbose: false
});

const pred0 = regressionModel.predict([0])[0];
const pred05 = regressionModel.predict([0.5])[0];
const pred1 = regressionModel.predict([1])[0];

console.log(`  f(0) = ${pred0.toFixed(4)} (정답: 0)`);
console.log(`  f(0.5) = ${pred05.toFixed(4)} (정답: 1)`);
console.log(`  f(1) = ${pred1.toFixed(4)} (정답: 2)`);

assertClose(pred0, 0, 0.2, '회귀 f(0) 근사');
assertClose(pred05, 1, 0.2, '회귀 f(0.5) 근사');
assertClose(pred1, 2, 0.2, '회귀 f(1) 근사');

console.log();

// ========================================
// 9. 성능 테스트
// ========================================
console.log('⚡ 9. 성능 테스트');
console.log('-'.repeat(60));

const perfModel = new TinyAI([10, 20, 5], 'relu');
const perfX = Array.from({ length: 100 }, () =>
  Array.from({ length: 10 }, () => Math.random())
);
const perfY = Array.from({ length: 100 }, () =>
  Array.from({ length: 5 }, () => Math.random())
);

const startTime = Date.now();
perfModel.train(perfX, perfY, {
  epochs: 100,
  learningRate: 0.01,
  batchSize: 20,
  verbose: false
});
const elapsed = Date.now() - startTime;

console.log(`  100 샘플, 100 epochs: ${elapsed}ms`);
assert(elapsed < 5000, '성능: 100 epochs < 5초');

// 예측 속도 테스트
const predStart = Date.now();
for (let i = 0; i < 1000; i++) {
  perfModel.predict([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]);
}
const predElapsed = Date.now() - predStart;
console.log(`  1000회 예측: ${predElapsed}ms (${(predElapsed / 1000).toFixed(2)}ms/예측)`);

console.log();

// ========================================
// 10. 메모리 사용량 테스트
// ========================================
console.log('💾 10. 메모리 사용량 테스트');
console.log('-'.repeat(60));

function calculateParams(layers) {
  let total = 0;
  for (let i = 0; i < layers.length - 1; i++) {
    total += layers[i] * layers[i + 1] + layers[i + 1]; // W + b
  }
  return total;
}

const smallModel = new TinyAI([2, 4, 1], 'sigmoid');
const smallParams = calculateParams([2, 4, 1]);
console.log(`  작은 모델 [2, 4, 1]: ${smallParams} 파라미터 (~${(smallParams * 8 / 1024).toFixed(2)} KB)`);

const mediumModel = new TinyAI([10, 20, 10, 5], 'relu');
const mediumParams = calculateParams([10, 20, 10, 5]);
console.log(`  중간 모델 [10, 20, 10, 5]: ${mediumParams} 파라미터 (~${(mediumParams * 8 / 1024).toFixed(2)} KB)`);

const largeModel = new TinyAI([50, 100, 50, 10], 'relu');
const largeParams = calculateParams([50, 100, 50, 10]);
console.log(`  큰 모델 [50, 100, 50, 10]: ${largeParams} 파라미터 (~${(largeParams * 8 / 1024).toFixed(2)} KB)`);

assert(smallParams === 17, '작은 모델 파라미터 수');
assert(mediumParams === 485, '중간 모델 파라미터 수');
assert(largeParams === 10660, '큰 모델 파라미터 수');

console.log();

// ========================================
// 테스트 결과 요약
// ========================================
console.log('='.repeat(60));
console.log('📊 테스트 결과 요약');
console.log('='.repeat(60));
console.log(`총 테스트: ${testResults.passed + testResults.failed}개`);
console.log(`✓ 통과: ${testResults.passed}개`);
console.log(`✗ 실패: ${testResults.failed}개`);
console.log(`성공률: ${((testResults.passed / (testResults.passed + testResults.failed)) * 100).toFixed(1)}%`);
console.log('='.repeat(60));

if (testResults.failed === 0) {
  console.log('🎉 모든 테스트 통과!');
} else {
  console.log('⚠️  일부 테스트 실패');
  console.log('\n실패한 테스트:');
  testResults.tests
    .filter(t => t.status === '✗')
    .forEach(t => console.log(`  ${t.status} ${t.message}`));
}

console.log();

// Node.js 환경에서 종료 코드 설정
if (isNode) {
  process.exit(testResults.failed > 0 ? 1 : 0);
}

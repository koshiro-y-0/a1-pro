/** @type {import('jest').Config} */
const config = {
  // React用テスト環境
  testEnvironment: 'jsdom',
  
  // テストファイルのパターン
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)'
  ],
  
  // TypeScript + JSX対応
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  
  // モジュール解決
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    // CSS/スタイルのモック
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    // 画像のモック
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  
  // セットアップファイル
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  
  // カバレッジ設定
  collectCoverage: true,
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx',
    '!src/reportWebVitals.ts',
  ],
  
  // タイムアウト
  testTimeout: 10000,
  
  verbose: true,
};

module.exports = config;

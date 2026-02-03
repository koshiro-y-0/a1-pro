import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // テストディレクトリ
  testDir: './e2e',
  
  // テストファイルのパターン
  testMatch: '**/*.spec.ts',
  
  // 並列実行
  fullyParallel: true,
  
  // CI環境ではリトライしない
  retries: process.env.CI ? 2 : 0,
  
  // 並列ワーカー数
  workers: process.env.CI ? 1 : undefined,
  
  // レポーター
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
  
  // 共通設定
  use: {
    // ベースURL
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    
    // スクリーンショット（失敗時のみ）
    screenshot: 'only-on-failure',
    
    // 動画（失敗時のみ）
    video: 'retain-on-failure',
    
    // トレース（失敗時のみ）
    trace: 'retain-on-failure',
    
    // タイムアウト
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },
  
  // グローバルタイムアウト
  timeout: 60000,
  
  // ブラウザ設定
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    // モバイル
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  
  // ローカル開発サーバー（自動起動）
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});

-- Initialize A1-PRO Database
-- This script runs automatically when MySQL container starts for the first time

-- Set character set to UTF-8
ALTER DATABASE a1pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant all privileges to a1pro_user
GRANT ALL PRIVILEGES ON a1pro.* TO 'a1pro_user'@'%';
FLUSH PRIVILEGES;

-- Log initialization
SELECT 'A1-PRO Database initialized successfully!' AS message;

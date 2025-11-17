# LAMP 스택 개발 환경

Linux, Apache, MySQL, PHP로 구성된 전통적인 웹 개발 환경입니다.

## 포함된 내용

- Ubuntu 20.04 LTS
- Apache 2.4
- MySQL 8.0
- PHP 7.4 (주요 확장 포함)
- phpMyAdmin
- Composer

## 사용 방법

### 1. VM 시작

```bash
vagrant up
```

### 2. 웹 브라우저로 접속

- **PHP Info**: http://localhost:8080
- **Database Test**: http://localhost:8080/db-test.php
- **phpMyAdmin**: http://localhost:8080/phpmyadmin
- **샘플 앱**: http://localhost:8080/myapp/public/

## MySQL 정보

### Root 계정
- **Username**: root
- **Password**: root

### 애플리케이션 데이터베이스
- **Database**: myapp
- **Username**: myapp
- **Password**: myapp123

## 디렉토리 구조

```
/var/www/html/
├── index.php           # PHP info 페이지
├── db-test.php         # 데이터베이스 연결 테스트
└── myapp/              # 샘플 애플리케이션
    ├── public/
    ├── src/
    └── config/
```

## PHP 애플리케이션 개발

### 1. SSH 접속

```bash
vagrant ssh
cd /var/www/html
```

### 2. 새 프로젝트 생성

```bash
# Composer로 새 프로젝트 생성
cd /var/www/html
composer create-project --prefer-dist laravel/laravel mylaravel

# 권한 설정
sudo chown -R www-data:www-data mylaravel
sudo chmod -R 755 mylaravel
```

### 3. Apache 가상 호스트 설정

새 프로젝트를 위한 가상 호스트 생성:

```bash
sudo cat > /etc/apache2/sites-available/myproject.conf << 'EOF'
<VirtualHost *:80>
    ServerName myproject.local
    DocumentRoot /var/www/html/myproject/public

    <Directory /var/www/html/myproject/public>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/myproject_error.log
    CustomLog ${APACHE_LOG_DIR}/myproject_access.log combined
</VirtualHost>
EOF

# 사이트 활성화
sudo a2ensite myproject.conf
sudo systemctl reload apache2
```

## MySQL 사용

### 명령줄 접속

```bash
# Root로 접속
mysql -u root -p
# 비밀번호: root

# 앱 사용자로 접속
mysql -u myapp -p myapp
# 비밀번호: myapp123
```

### 데이터베이스 생성

```sql
CREATE DATABASE newapp;
GRANT ALL PRIVILEGES ON newapp.* TO 'myapp'@'localhost';
FLUSH PRIVILEGES;
```

### 샘플 테이블 생성

```sql
USE myapp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email) VALUES
    ('john', 'john@example.com'),
    ('jane', 'jane@example.com');

SELECT * FROM users;
```

## Composer 사용

```bash
# Composer 버전 확인
composer --version

# 패키지 설치
composer require vendor/package

# autoload 생성
composer dump-autoload

# 의존성 업데이트
composer update
```

## Apache 관리

```bash
# 상태 확인
sudo systemctl status apache2

# 재시작
sudo systemctl restart apache2

# 설정 테스트
sudo apache2ctl configtest

# 에러 로그 확인
sudo tail -f /var/log/apache2/error.log

# 접속 로그 확인
sudo tail -f /var/log/apache2/access.log
```

## PHP 설정

```bash
# php.ini 위치
/etc/php/7.4/apache2/php.ini

# 설정 변경 예시
sudo nano /etc/php/7.4/apache2/php.ini

# 주요 설정:
# upload_max_filesize = 20M
# post_max_size = 20M
# memory_limit = 256M
# max_execution_time = 300

# 변경 후 Apache 재시작 필요
sudo systemctl restart apache2
```

## 유용한 PHP 확장

```bash
# 설치된 확장 확인
php -m

# 추가 확장 설치 예시
sudo apt-get install php-redis
sudo apt-get install php-memcached
sudo apt-get install php-imagick

# 설치 후 Apache 재시작
sudo systemctl restart apache2
```

## phpMyAdmin

### 접속
- URL: http://localhost:8080/phpmyadmin
- Username: root
- Password: root

### 주요 기능
- 데이터베이스 관리
- SQL 쿼리 실행
- 테이블 구조 편집
- 데이터 import/export
- 사용자 권한 관리

## 데이터베이스 백업

### MySQL 덤프
```bash
# 단일 데이터베이스 백업
mysqldump -u root -p myapp > /vagrant/backup.sql

# 모든 데이터베이스 백업
mysqldump -u root -p --all-databases > /vagrant/all-databases.sql

# 압축 백업
mysqldump -u root -p myapp | gzip > /vagrant/backup.sql.gz
```

### 복원
```bash
# 복원
mysql -u root -p myapp < /vagrant/backup.sql

# 압축 파일 복원
gunzip < /vagrant/backup.sql.gz | mysql -u root -p myapp
```

## 외부 MySQL 클라이언트로 접속

MySQL Workbench, DBeaver, Sequel Pro 등에서:

- **Host**: localhost
- **Port**: 3306
- **Username**: root
- **Password**: root

## 샘플 PHP 코드

### PDO를 사용한 데이터베이스 연결

```php
<?php
$host = 'localhost';
$db = 'myapp';
$user = 'myapp';
$pass = 'myapp123';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 데이터 조회
    $stmt = $pdo->query("SELECT * FROM users");
    $users = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($users as $user) {
        echo $user['username'] . '<br>';
    }
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>
```

### mysqli를 사용한 연결

```php
<?php
$conn = new mysqli('localhost', 'myapp', 'myapp123', 'myapp');

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$result = $conn->query("SELECT * FROM users");

while ($row = $result->fetch_assoc()) {
    echo $row['username'] . '<br>';
}

$conn->close();
?>
```

## 트러블슈팅

### Apache가 시작되지 않는 경우

```bash
# 에러 확인
sudo systemctl status apache2
sudo apache2ctl configtest

# 포트 확인
sudo netstat -tlnp | grep :80
```

### MySQL 연결 오류

```bash
# MySQL 상태 확인
sudo systemctl status mysql

# 연결 테스트
mysql -u root -p -e "SELECT 1"

# 사용자 확인
mysql -u root -p -e "SELECT user, host FROM mysql.user"
```

### 파일 권한 문제

```bash
# 웹 디렉토리 권한 재설정
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html

# 특정 디렉토리 쓰기 권한
sudo chmod -R 775 /var/www/html/uploads
```

## VM 관리

```bash
# VM 중지
vagrant halt

# VM 재시작
vagrant reload

# VM 삭제
vagrant destroy
```

## 프레임워크 설치

### Laravel
```bash
composer create-project laravel/laravel mylaravel
cd mylaravel
php artisan serve --host=0.0.0.0 --port=8000
```

### Symfony
```bash
composer create-project symfony/skeleton mysymfony
cd mysymfony
composer require webapp
symfony server:start
```

### CodeIgniter
```bash
composer create-project codeigniter4/appstarter mycodeigniter
```

## 팁

- phpMyAdmin으로 데이터베이스를 쉽게 관리할 수 있습니다
- /vagrant 디렉토리는 호스트와 공유됩니다
- Composer로 현대적인 PHP 패키지 관리가 가능합니다
- Apache의 mod_rewrite가 활성화되어 있어 URL 재작성 사용 가능

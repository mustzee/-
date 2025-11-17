#!/bin/bash

echo "=========================================="
echo "LAMP 스택 설치 시작"
echo "=========================================="

# 시스템 업데이트
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y

# Apache 설치
echo "Apache 설치 중..."
apt-get install -y apache2

# Apache 모듈 활성화
a2enmod rewrite
a2enmod ssl
a2enmod headers

# MySQL 설치
echo "MySQL 설치 중..."
apt-get install -y mysql-server

# MySQL 기본 보안 설정
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"
mysql -e "DELETE FROM mysql.user WHERE User='';"
mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
mysql -e "DROP DATABASE IF EXISTS test;"
mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
mysql -e "FLUSH PRIVILEGES;"

# 개발용 데이터베이스 생성
mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS myapp;"
mysql -uroot -proot -e "CREATE USER IF NOT EXISTS 'myapp'@'localhost' IDENTIFIED BY 'myapp123';"
mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON myapp.* TO 'myapp'@'localhost';"
mysql -uroot -proot -e "FLUSH PRIVILEGES;"

# MySQL 외부 접속 허용
sed -i "s/bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
mysql -uroot -proot -e "CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'root';"
mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;"
mysql -uroot -proot -e "FLUSH PRIVILEGES;"
systemctl restart mysql

# PHP 설치
echo "PHP 설치 중..."
apt-get install -y php libapache2-mod-php php-mysql
apt-get install -y php-curl php-gd php-mbstring php-xml php-xmlrpc
apt-get install -y php-soap php-intl php-zip php-bcmath php-json

# phpMyAdmin 설치
echo "phpMyAdmin 설치 중..."
echo "phpmyadmin phpmyadmin/dbconfig-install boolean true" | debconf-set-selections
echo "phpmyadmin phpmyadmin/app-password-confirm password root" | debconf-set-selections
echo "phpmyadmin phpmyadmin/mysql/admin-pass password root" | debconf-set-selections
echo "phpmyadmin phpmyadmin/mysql/app-pass password root" | debconf-set-selections
echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2" | debconf-set-selections

apt-get install -y phpmyadmin

# phpMyAdmin Apache 설정
ln -sf /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
a2enconf phpmyadmin
systemctl reload apache2

# Composer 설치
echo "Composer 설치 중..."
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer
chmod +x /usr/local/bin/composer

# 샘플 PHP 파일 생성
cat > /var/www/html/index.php << 'EOF'
<?php
phpinfo();
?>
EOF

cat > /var/www/html/db-test.php << 'EOF'
<?php
$servername = "localhost";
$username = "myapp";
$password = "myapp123";
$database = "myapp";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "데이터베이스 연결 성공!";
} catch(PDOException $e) {
    echo "연결 실패: " . $e->getMessage();
}
?>
EOF

# Apache DocumentRoot에 샘플 프로젝트 구조 생성
mkdir -p /var/www/html/myapp/{public,src,config}
cat > /var/www/html/myapp/public/index.php << 'EOF'
<?php
echo "<h1>Welcome to My LAMP App</h1>";
echo "<p>PHP Version: " . phpversion() . "</p>";
echo "<ul>";
echo "<li><a href='/'>PHP Info</a></li>";
echo "<li><a href='/db-test.php'>Database Test</a></li>";
echo "<li><a href='/phpmyadmin'>phpMyAdmin</a></li>";
echo "</ul>";
?>
EOF

# 권한 설정
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html

# Apache 재시작
systemctl restart apache2
systemctl enable apache2
systemctl enable mysql

echo "=========================================="
echo "LAMP 스택 설치 완료!"
echo "=========================================="
echo ""
echo "설치된 버전:"
echo "  Apache: $(apache2 -v | head -n 1)"
echo "  MySQL: $(mysql --version)"
echo "  PHP: $(php -v | head -n 1)"
echo "=========================================="
echo ""
echo "MySQL 정보:"
echo "  Root 비밀번호: root"
echo "  앱 데이터베이스: myapp"
echo "  앱 사용자: myapp / myapp123"
echo "=========================================="
echo ""
echo "접속 주소:"
echo "  웹사이트: http://localhost:8080"
echo "  PHP Info: http://localhost:8080"
echo "  DB Test: http://localhost:8080/db-test.php"
echo "  phpMyAdmin: http://localhost:8080/phpmyadmin"
echo "    (root / root)"
echo "=========================================="

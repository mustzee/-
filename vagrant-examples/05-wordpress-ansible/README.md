# WordPress (Ansible 프로비저닝)

Ansible을 사용하여 자동으로 구성되는 WordPress 개발 환경입니다.

## 포함된 내용

- Ubuntu 20.04 LTS
- Apache 2.4
- MySQL 8.0
- PHP 7.4
- WordPress 6.4
- Ansible 프로비저닝

## 사용 방법

### 1. VM 시작

```bash
vagrant up
```

처음 시작 시 Ansible이 자동으로:
- LAMP 스택 설치
- WordPress 다운로드 및 설정
- 데이터베이스 생성
- Apache 설정

### 2. WordPress 설치 완료

브라우저에서 http://localhost:8080 접속

WordPress 초기 설정 화면이 나타나면:
1. 사이트 제목 입력
2. 관리자 계정 정보 입력
3. 설치 완료

### 3. WordPress 관리자 페이지

http://localhost:8080/wp-admin

## 데이터베이스 정보

- **Database**: wordpress
- **User**: wpuser
- **Password**: wppass123
- **Host**: localhost

## MySQL Root 비밀번호

- **Root Password**: rootpass123

## 디렉토리 구조

```
05-wordpress-ansible/
├── Vagrantfile
├── playbook.yml              # Ansible playbook
├── templates/
│   ├── wp-config.php.j2      # WordPress 설정 템플릿
│   └── wordpress.conf.j2     # Apache 가상 호스트 설정
└── README.md
```

## Ansible 변수 커스터마이징

`playbook.yml` 파일의 vars 섹션을 수정:

```yaml
vars:
  mysql_root_password: rootpass123
  wordpress_db_name: wordpress
  wordpress_db_user: wpuser
  wordpress_db_password: wppass123
  wordpress_version: "6.4"
```

변경 후:
```bash
vagrant provision
```

## 유용한 명령어

### SSH 접속
```bash
vagrant ssh
```

### Apache 관리
```bash
# Apache 재시작
sudo systemctl restart apache2

# Apache 상태 확인
sudo systemctl status apache2

# 에러 로그 확인
sudo tail -f /var/log/apache2/wordpress_error.log
```

### MySQL 관리
```bash
# MySQL 접속
mysql -u root

# WordPress 데이터베이스 접속
mysql -u wpuser -p wordpress
# 비밀번호: wppass123

# 데이터베이스 백업
mysqldump -u wpuser -p wordpress > /vagrant/backup.sql

# 데이터베이스 복원
mysql -u wpuser -p wordpress < /vagrant/backup.sql
```

### WordPress 디렉토리
```bash
cd /var/www/html/wordpress

# 파일 권한 확인
ls -la

# 테마 디렉토리
cd wp-content/themes

# 플러그인 디렉토리
cd wp-content/plugins
```

## WordPress 플러그인/테마 개발

### 1. 테마 개발

```bash
# 테마 디렉토리에 새 테마 생성
mkdir -p /var/www/html/wordpress/wp-content/themes/mytheme
cd /var/www/html/wordpress/wp-content/themes/mytheme

# style.css 생성
cat > style.css << 'EOF'
/*
Theme Name: My Theme
Author: Your Name
Version: 1.0
*/
EOF

# index.php 생성
cat > index.php << 'EOF'
<?php
get_header();
?>
<h1>My Custom Theme</h1>
<?php
get_footer();
?>
EOF
```

WordPress 관리자에서 테마 활성화

### 2. 플러그인 개발

```bash
# 플러그인 디렉토리에 새 플러그인 생성
mkdir -p /var/www/html/wordpress/wp-content/plugins/myplugin
cd /var/www/html/wordpress/wp-content/plugins/myplugin

# 플러그인 파일 생성
cat > myplugin.php << 'EOF'
<?php
/*
Plugin Name: My Plugin
Description: Custom plugin
Version: 1.0
Author: Your Name
*/

function my_plugin_function() {
    echo "Hello from my plugin!";
}
add_action('wp_footer', 'my_plugin_function');
?>
EOF
```

WordPress 관리자에서 플러그인 활성화

## 문제 해결

### WordPress가 표시되지 않는 경우

```bash
# Apache 상태 확인
sudo systemctl status apache2

# WordPress 디렉토리 권한 확인
ls -la /var/www/html/wordpress

# 권한 재설정
sudo chown -R www-data:www-data /var/www/html/wordpress
```

### 데이터베이스 연결 오류

```bash
# MySQL 상태 확인
sudo systemctl status mysql

# 데이터베이스 확인
mysql -u root -e "SHOW DATABASES;"

# 사용자 권한 확인
mysql -u root -e "SHOW GRANTS FOR 'wpuser'@'localhost';"
```

### Ansible 재실행

```bash
# 프로비저닝만 다시 실행
vagrant provision

# 특정 태스크만 실행하려면 playbook.yml에 tags 추가
```

## VM 관리

```bash
# VM 중지
vagrant halt

# VM 재시작
vagrant reload

# 재시작 + 프로비저닝
vagrant reload --provision

# VM 삭제
vagrant destroy
```

## 백업 및 복원

### 파일 백업
```bash
# WordPress 파일 백업
vagrant ssh -c "tar -czf /vagrant/wordpress-files.tar.gz -C /var/www/html wordpress"
```

### 데이터베이스 백업
```bash
vagrant ssh -c "mysqldump -u wpuser -pwppass123 wordpress > /vagrant/wordpress-db.sql"
```

### 복원
```bash
# 데이터베이스 복원
vagrant ssh -c "mysql -u wpuser -pwppass123 wordpress < /vagrant/wordpress-db.sql"

# 파일 복원
vagrant ssh -c "sudo tar -xzf /vagrant/wordpress-files.tar.gz -C /var/www/html"
vagrant ssh -c "sudo chown -R www-data:www-data /var/www/html/wordpress"
```

## 보안 강화 (프로덕션용)

1. **wp-config.php 보안 키 변경**
   - https://api.wordpress.org/secret-key/1.1/salt/ 에서 생성
   - `templates/wp-config.php.j2` 파일에 적용

2. **WP_DEBUG 비활성화**
   ```php
   define('WP_DEBUG', false);
   ```

3. **파일 권한 강화**
   ```bash
   find /var/www/html/wordpress -type d -exec chmod 755 {} \;
   find /var/www/html/wordpress -type f -exec chmod 644 {} \;
   ```

## 팁

- Ansible playbook을 수정하여 원하는 플러그인/테마 자동 설치 가능
- `vagrant provision`으로 언제든 초기 상태로 재구성 가능
- 개발 중인 테마/플러그인을 호스트에서 편집하고 게스트에 동기화 가능

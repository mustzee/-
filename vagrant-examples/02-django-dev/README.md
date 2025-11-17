# Django 개발 환경

Django 웹 프레임워크 개발을 위한 Vagrant 환경입니다.

## 포함된 내용

- Ubuntu 20.04 LTS
- Python 3.8+
- Django 4.x
- PostgreSQL 12
- Django REST Framework
- Django Debug Toolbar

## 사용 방법

### 1. VM 시작

```bash
vagrant up
```

### 2. SSH 접속

```bash
vagrant ssh
# 자동으로 가상 환경이 활성화되고 /vagrant 디렉토리로 이동합니다
```

### 3. Django 프로젝트 생성 (처음 사용 시)

```bash
# 새 프로젝트 생성
django-admin startproject myproject .

# 앱 생성
python manage.py startapp myapp
```

### 4. 데이터베이스 설정

`myproject/settings.py` 파일 수정:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangodb',
        'USER': 'djangouser',
        'PASSWORD': 'django123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ALLOWED_HOSTS 추가
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.50.20']
```

### 5. 마이그레이션 및 슈퍼유저 생성

```bash
# 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

### 6. 개발 서버 실행

```bash
python manage.py runserver 0.0.0.0:8000
```

브라우저에서 http://localhost:8000 접속

## 데이터베이스 정보

- **Database**: djangodb
- **User**: djangouser
- **Password**: django123
- **Host**: localhost (VM 내부) / 127.0.0.1 (호스트에서 접속)
- **Port**: 5432

## 포트 포워딩

- 8000 → 8000 (Django 개발 서버)
- 5432 → 5432 (PostgreSQL)

## 유용한 명령어

```bash
# Django 쉘
python manage.py shell

# 데이터베이스 쉘
python manage.py dbshell

# 정적 파일 수집
python manage.py collectstatic

# 테스트 실행
python manage.py test

# 새 마이그레이션 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate
```

## PostgreSQL 직접 접속

```bash
# VM 내부에서
psql -U djangouser -d djangodb
# 비밀번호: django123

# 호스트에서 (PostgreSQL 클라이언트 필요)
psql -h localhost -p 5432 -U djangouser -d djangodb
```

## requirements.txt

프로젝트 의존성을 `requirements.txt`에 저장:

```bash
pip freeze > requirements.txt
```

다음 번에 `vagrant up` 하면 자동으로 설치됩니다.

## VM 관리

```bash
# VM 중지
vagrant halt

# VM 재시작
vagrant reload

# VM 삭제
vagrant destroy
```

## 팁

- 가상 환경은 SSH 접속 시 자동으로 활성화됩니다
- 코드 변경 시 Django 개발 서버가 자동으로 재시작됩니다
- PostgreSQL은 외부에서도 접속 가능합니다
- Admin 패널: http://localhost:8000/admin

# http://192.168.88.227:8090/
from datetime import timedelta
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Media files configuration (required for file uploads in CKEditor)
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files configuration for CKEditor
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-miy7u-0r&%m*n7ymj$1276j+l^_oy%^m-p=80-49ks#_k^85)x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
SITE_ID = 1


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3033",           # For local development
    "http://92.168.88.245:8002",        # For frontend running from another PC using your backend IP
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3033",
    "http://92.168.88.245:8002",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'djoser',
    'authentication',
    'quiz',

    'django_ckeditor_5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'authentication.CustomUser'


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',


    ),
}


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/



#settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# URL used to access the media
MEDIA_URL = '/media/'



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJOSER = {

    # 'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'LOGIN_FIELD': 'email',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user_create': 'authentication.serializers.CustomUserSerializer',
        'user': 'authentication.serializers.CustomUserSerializer',
        'current_user': 'authentication.serializers.CustomUserSerializer',
    },
}

# customColorPalette = [
#     {
#         'color': 'hsl(4, 90%, 58%)',
#         'label': 'Red'
#     },
#         {
#             'color': 'hsl(340, 82%, 52%)',
#             'label': 'Pink'
#         },
#         {
#             'color': 'hsl(291, 64%, 42%)',
#             'label': 'Purple'
#         },
#         {
#             'color': 'hsl(262, 52%, 47%)',
#             'label': 'Deep Purple'
#         },
#         {
#             'color': 'hsl(231, 48%, 48%)',
#             'label': 'Indigo'
#         },
#         {
#             'color': 'hsl(207, 90%, 54%)',
#             'label': 'Blue'
#         },
#     ]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
# CKEDITOR_5_CONFIGS = {
#     'default': {
#         'toolbar': {
#             'items': ['heading', '|', 'bold', 'italic', 'link',
#                       'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
#                     }

#     },
#     'extends': {
#         'blockToolbar': [
#             'paragraph', 'heading1', 'heading2', 'heading3',
#             '|',
#             'bulletedList', 'numberedList',
#             '|',
#             'blockQuote',
#         ],
#         'toolbar': {
#             'items': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
#                       'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
#                     'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
#                     'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
#                     'insertTable',
#                     ],
#             'shouldNotGroupWhenFull': 'true'
#         },
#         'image': {
#             'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
#                         'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
#             'styles': [
#                 'full',
#                 'side',
#                 'alignLeft',
#                 'alignRight',
#                 'alignCenter',
#             ]

#         },
#         'table': {
#             'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
#             'tableProperties', 'tableCellProperties' ],
#             'tableProperties': {
#                 'borderColors': customColorPalette,
#                 'backgroundColors': customColorPalette
#             },
#             'tableCellProperties': {
#                 'borderColors': customColorPalette,
#                 'backgroundColors': customColorPalette
#             }
#         },
#         'heading' : {
#             'options': [
#                 { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
#                 { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
#                 { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
#                 { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
#             ]
#         }
#     },
#     'list': {
#         'properties': {
#             'styles': 'true',
#             'startIndex': 'true',
#             'reversed': 'true',
#         }
#     }
# }


# CKEditor 5 configuration
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                   'bulletedList', 'numberedList', 'blockQuote', 'imageUpload'],
    }
}



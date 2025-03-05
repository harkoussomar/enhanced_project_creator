import os
import sys
import subprocess
import json
from pathlib import Path
import shutil

try:
    import questionary
    from questionary import Separator
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'questionary'], check=True)
    import questionary
    from questionary import Separator

# Configuration
DEFAULT_PACKAGES = {
    'server': {
        'express': {
            'required': ['express', 'cors', 'dotenv'],
            'dev': ['nodemon', '@types/express', '@types/cors']
        },
        'fastapi': {
            'required': ['fastapi', 'uvicorn', 'python-dotenv', 'pydantic'],
            'dev': ['pytest', 'black', 'flake8']
        },
        'django': {
            'required': ['django', 'djangorestframework', 'django-cors-headers', 'python-dotenv'],
            'dev': ['pytest', 'pytest-django', 'black', 'flake8']
        },
        'flask': {
            'required': ['flask', 'flask-cors', 'python-dotenv'],
            'dev': ['pytest', 'black', 'flake8']
        },
        'nest': {
            'required': ['@nestjs/core', '@nestjs/common', '@nestjs/platform-express'],
            'dev': ['@nestjs/cli', '@nestjs/schematics', '@nestjs/testing']
        }
    },
    'database': {
        'mongodb': {
            'node': ['mongoose'],
            'python': ['pymongo', 'motor']
        },
        'postgresql': {
            'node': ['pg', 'sequelize'],
            'python': ['psycopg2-binary', 'sqlalchemy']
        },
        'mysql': {
            'node': ['mysql2', 'sequelize'],
            'python': ['mysql-connector-python', 'sqlalchemy']
        },
        'sqlite': {
            'node': ['sqlite3', 'sequelize'],
            'python': ['sqlalchemy']
        }
    },
    'client': {
        'react': {
            'required': ['react-router-dom', 'axios'],
            'dev': [],
            'styling': {
                'tailwind': ['tailwindcss', 'postcss', 'autoprefixer'],
                'bootstrap': ['bootstrap', 'react-bootstrap'],
                'mui': ['@mui/material', '@mui/icons-material', '@emotion/react', '@emotion/styled'],
                'chakra': ['@chakra-ui/react', '@emotion/react', '@emotion/styled', 'framer-motion'],
                'styled-components': ['styled-components']
            },
            'state': {
                'redux': ['redux', 'react-redux', '@reduxjs/toolkit'],
                'zustand': ['zustand'],
                'recoil': ['recoil'],
                'jotai': ['jotai'],
                'context': []
            }
        },
        'vue': {
            'required': ['vue-router', 'axios'],
            'dev': [],
            'styling': {
                'tailwind': ['tailwindcss', 'postcss', 'autoprefixer'],
                'bootstrap': ['bootstrap', 'bootstrap-vue'],
                'vuetify': ['vuetify']
            },
            'state': {
                'pinia': ['pinia'],
                'vuex': ['vuex']
            }
        },
        'svelte': {
            'required': ['svelte-navigator', 'axios'],
            'dev': [],
            'styling': {
                'tailwind': ['tailwindcss', 'postcss', 'autoprefixer']
            },
            'state': {
                'svelte-store': []
            }
        },
        'angular': {
            'required': ['@angular/router', 'axios'],
            'dev': [],
            'styling': {
                'tailwind': ['tailwindcss', 'postcss', 'autoprefixer'],
                'bootstrap': ['bootstrap', 'ngx-bootstrap']
            },
            'state': {
                'ngrx': ['@ngrx/store', '@ngrx/effects', '@ngrx/entity']
            }
        }
    }
}

def create_banner():
    """Display a welcome banner"""
    banner = """
╔══════════════════════════════════════════╗
║                                          ║
║       ENHANCED PROJECT CREATOR           ║
║                                          ║
╚══════════════════════════════════════════╝
    """
    print(banner)

def get_package_manager_command(pm):
    """Handle Windows executable extensions"""
    if os.name == 'nt' and pm in ['npm', 'npx', 'yarn', 'pnpm']:
        return f"{pm}.cmd"
    return pm

def get_python_package_manager():
    """Determine if pip, poetry, or conda should be used"""
    if shutil.which('poetry'):
        if questionary.confirm("Poetry detected. Use it for Python package management?").ask():
            return 'poetry'

    if shutil.which('conda'):
        if questionary.confirm("Conda detected. Use it for Python package management?").ask():
            return 'conda'

    return 'pip'

def get_user_input():
    create_banner()
    project_name = questionary.text("Project name:", default="my-app").ask()

    project_type = questionary.select(
        "Project type:",
        choices=["Full-stack", "Backend only", "Frontend only"]
    ).ask()

    # Backend options
    backend_framework = None
    backend_language = None
    database = None

    if project_type in ["Full-stack", "Backend only"]:
        backend_language = questionary.select(
            "Backend language:",
            choices=["JavaScript", "TypeScript", "Python"]
        ).ask()

        if backend_language in ["JavaScript", "TypeScript"]:
            backend_framework = questionary.select(
                "Backend framework:",
                choices=["Express", "NestJS"]
            ).ask().lower()
        else:  # Python
            backend_framework = questionary.select(
                "Backend framework:",
                choices=["FastAPI", "Django", "Flask"]
            ).ask().lower()

        database = questionary.select(
            "Database:",
            choices=["MongoDB", "PostgreSQL", "MySQL", "SQLite", "None"]
        ).ask().lower()

        if database != "none":
            database = database.lower()

    # Frontend options
    frontend_framework = None
    styling_choice = None
    state_management = None

    if project_type in ["Full-stack", "Frontend only"]:
        frontend_framework = questionary.select(
            "Frontend framework:",
            choices=["React", "Vue", "Svelte", "Angular"]
        ).ask().lower()

        styling_choices = list(DEFAULT_PACKAGES['client'][frontend_framework]['styling'].keys())
        styling_choice = questionary.select(
            "CSS framework/library:",
            choices=styling_choices + ["None"]
        ).ask()
        if styling_choice.lower() == "none":
            styling_choice = None

        state_choices = list(DEFAULT_PACKAGES['client'][frontend_framework]['state'].keys())
        state_management = questionary.select(
            "State management:",
            choices=state_choices + ["None"]
        ).ask()
        if state_management.lower() == "none":
            state_management = None

    # Package managers
    js_package_manager = None
    py_package_manager = None

    if backend_language in ["JavaScript", "TypeScript"] or project_type in ["Full-stack", "Frontend only"]:
        js_package_manager = questionary.select(
            "JavaScript package manager:",
            choices=["npm", "yarn", "pnpm"]
        ).ask()

    if backend_language == "Python":
        py_package_manager = get_python_package_manager()

    # Additional dependencies
    additional_deps = questionary.text(
        "Additional dependencies (space-separated):"
    ).ask().split() if questionary.confirm("Add custom dependencies?").ask() else []

    # Git initialization
    init_git = questionary.confirm("Initialize Git repository?", default=True).ask()

    # Docker support
    add_docker = questionary.confirm("Add Docker support?").ask()

    return {
        'project_name': project_name,
        'project_type': project_type,
        'backend_language': backend_language,
        'backend_framework': backend_framework,
        'frontend_framework': frontend_framework,
        'database': database,
        'styling_choice': styling_choice,
        'state_management': state_management,
        'js_package_manager': js_package_manager,
        'py_package_manager': py_package_manager,
        'additional_deps': additional_deps,
        'init_git': init_git,
        'add_docker': add_docker,
        'use_typescript': backend_language == "TypeScript" or (
            frontend_framework in ['react', 'vue', 'angular'] and
            questionary.confirm("Use TypeScript for frontend?", default=True).ask()
        )
    }

def create_directory_structure(base_path, config):
    """Create project directory structure based on configuration"""
    dirs = []

    if config['project_type'] in ["Full-stack", "Backend only"]:
        server_base = 'server'
        if config['backend_language'] in ["JavaScript", "TypeScript"]:
            if config['backend_framework'] == 'express':
                server_dirs = [
                    f'{server_base}/src/config',
                    f'{server_base}/src/models',
                    f'{server_base}/src/controllers',
                    f'{server_base}/src/routes',
                    f'{server_base}/src/middleware',
                    f'{server_base}/src/utils',
                ]
                if config['use_typescript']:
                    server_dirs.append(f'{server_base}/src/types')
                dirs.extend(server_dirs)
            elif config['backend_framework'] == 'nest':
                server_dirs = [
                    f'{server_base}/src/modules',
                    f'{server_base}/src/common',
                    f'{server_base}/src/config',
                ]
                dirs.extend(server_dirs)
        elif config['backend_language'] == "Python":
            if config['backend_framework'] == 'fastapi':
                server_dirs = [
                    f'{server_base}/app/routers',
                    f'{server_base}/app/models',
                    f'{server_base}/app/schemas',
                    f'{server_base}/app/services',
                    f'{server_base}/app/utils',
                    f'{server_base}/tests',
                ]
                dirs.extend(server_dirs)
            elif config['backend_framework'] == 'django':
                server_dirs = [
                    f'{server_base}/{config["project_name"].replace("-", "_")}',
                    f'{server_base}/api',
                    f'{server_base}/static',
                    f'{server_base}/templates',
                ]
                dirs.extend(server_dirs)
            elif config['backend_framework'] == 'flask':
                server_dirs = [
                    f'{server_base}/app',
                    f'{server_base}/app/routes',
                    f'{server_base}/app/models',
                    f'{server_base}/app/templates',
                    f'{server_base}/app/static',
                    f'{server_base}/tests',
                ]
                dirs.extend(server_dirs)

    for directory in dirs:
        if directory:
            (base_path / directory).mkdir(parents=True, exist_ok=True)

def create_client_additional_dirs(client_path, config):
    """Create additional client directories after Vite setup"""
    dirs = []

    if config['frontend_framework'] == 'react':
        client_dirs = [
            'src/components',
            'src/pages',
            'src/hooks',
            'src/utils',
            'src/assets/styles',
            'src/assets/images',
        ]
        if config['use_typescript']:
            client_dirs.append('src/types')
        if config['state_management'] in ['redux', 'zustand', 'recoil', 'jotai']:
            client_dirs.append('src/store')
        dirs.extend(client_dirs)

    elif config['frontend_framework'] == 'vue':
        client_dirs = [
            'src/components',
            'src/views',
            'src/composables',
            'src/utils',
            'src/assets/styles',
            'src/assets/images',
        ]
        if config['state_management'] in ['pinia', 'vuex']:
            client_dirs.append('src/store')
        dirs.extend(client_dirs)

    elif config['frontend_framework'] == 'svelte':
        client_dirs = [
            'src/components',
            'src/routes',
            'src/lib',
            'src/assets',
        ]
        dirs.extend(client_dirs)

    elif config['frontend_framework'] == 'angular':
        client_dirs = [
            'src/app/components',
            'src/app/pages',
            'src/app/services',
            'src/app/shared',
        ]
        if config['state_management'] == 'ngrx':
            client_dirs.append('src/app/store')
        dirs.extend(client_dirs)

    for directory in dirs:
        if directory:
            (client_path / directory).mkdir(parents=True, exist_ok=True)

def create_server_files(base_path, config):
    """Create server files based on configuration"""
    server_path = base_path / 'server'

    if config['backend_language'] in ["JavaScript", "TypeScript"]:
        ext = 'ts' if config['use_typescript'] else 'js'

        if config['backend_framework'] == 'express':
            create_express_files(server_path, config, ext)
        elif config['backend_framework'] == 'nest':
            create_nest_files(server_path, config)

    elif config['backend_language'] == "Python":
        if config['backend_framework'] == 'fastapi':
            create_fastapi_files(server_path, config)
        elif config['backend_framework'] == 'django':
            create_django_files(server_path, config)
        elif config['backend_framework'] == 'flask':
            create_flask_files(server_path, config)

def create_express_files(server_path, config, ext):
    """Create Express.js server files"""
    db_import = get_db_import_express(config)
    db_connect = get_db_connect_express(config)

    app_content = f"""import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
{db_import}

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

{db_connect}

app.get('/', (req, res) => {{
  res.send('{config["project_name"]} API is running');
}});

app.listen(PORT, () => {{
  console.log(`Server running on port ${{PORT}}`);
}});
"""
    (server_path / 'src' / f'app.{ext}').write_text(app_content)

    env_content = "PORT=5000\n"
    if config['database'] == 'mongodb':
        env_content += f"MONGO_URI=mongodb://localhost:27017/{config['project_name']}\n"
    elif config['database'] in ['postgresql', 'mysql']:
        db_name = config['database'].upper()
        env_content += f"{db_name}_HOST=localhost\n"
        env_content += f"{db_name}_PORT={'5432' if config['database'] == 'postgresql' else '3306'}\n"
        env_content += f"{db_name}_USER=root\n"
        env_content += f"{db_name}_PASSWORD=password\n"
        env_content += f"{db_name}_DATABASE={config['project_name'].replace('-', '_')}\n"

    (server_path / '.env').write_text(env_content)

    if config['use_typescript']:
        (server_path / 'tsconfig.json').write_text("""{
  "compilerOptions": {
    "target": "ES2020",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}""")

def get_db_import_express(config):
    if config['database'] == 'mongodb':
        return "import mongoose from 'mongoose';"
    elif config['database'] == 'postgresql':
        return "import { Pool } from 'pg';"
    elif config['database'] == 'mysql':
        return "import mysql from 'mysql2/promise';"
    elif config['database'] == 'sqlite':
        return "import sqlite3 from 'sqlite3';"
    return ""

def get_db_connect_express(config):
    if config['database'] == 'mongodb':
        return """const mongoUri = process.env.MONGO_URI;
if (!mongoUri) {
  console.error('MONGO_URI is not defined in the environment variables');
  process.exit(1);
}
mongoose.connect(mongoUri)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));"""
    elif config['database'] == 'postgresql':
        return """const pgHost = process.env.POSTGRESQL_HOST;
const pgPort = process.env.POSTGRESQL_PORT;
const pgUser = process.env.POSTGRESQL_USER;
const pgPassword = process.env.POSTGRESQL_PASSWORD;
const pgDatabase = process.env.POSTGRESQL_DATABASE;

if (!pgHost || !pgPort || !pgUser || !pgPassword || !pgDatabase) {
  console.error('PostgreSQL environment variables are not fully set');
  process.exit(1);
}

const pool = new Pool({
  host: pgHost,
  port: Number(pgPort),
  user: pgUser,
  password: pgPassword,
  database: pgDatabase
});

pool.connect()
  .then(() => console.log('Connected to PostgreSQL'))
  .catch(err => console.error('PostgreSQL connection error:', err));"""
    elif config['database'] == 'mysql':
        return """const mysqlHost = process.env.MYSQL_HOST;
const mysqlPort = process.env.MYSQL_PORT;
const mysqlUser = process.env.MYSQL_USER;
const mysqlPassword = process.env.MYSQL_PASSWORD;
const mysqlDatabase = process.env.MYSQL_DATABASE;

if (!mysqlHost || !mysqlPort || !mysqlUser || !mysqlPassword || !mysqlDatabase) {
  console.error('MySQL environment variables are not fully set');
  process.exit(1);
}

const pool = mysql.createPool({
  host: mysqlHost,
  port: Number(mysqlPort),
  user: mysqlUser,
  password: mysqlPassword,
  database: mysqlDatabase
});

pool.getConnection()
  .then(() => console.log('Connected to MySQL'))
  .catch(err => console.error('MySQL connection error:', err));"""
    elif config['database'] == 'sqlite':
        return """const db = new sqlite3.Database('./database.sqlite', (err) => {
  if (err) {
    console.error('SQLite connection error:', err);
  } else {
    console.log('Connected to SQLite database');
  }
});"""
    return ""

def create_nest_files(server_path, config):
    nest_cli = get_package_manager_command('npx')
    subprocess.run([nest_cli, '@nestjs/cli@latest', 'new', server_path.name, '--skip-install'],
                  cwd=server_path.parent, check=True)
    (server_path / '.env').write_text("PORT=3000\n")

def create_fastapi_files(server_path, config):
    app_dir = server_path / 'app'
    main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
"""
    (app_dir / 'main.py').write_text(main_content)

    for dir_path in [app_dir, app_dir / 'routers', app_dir / 'models',
                    app_dir / 'schemas', app_dir / 'services', app_dir / 'utils']:
        (dir_path / '__init__.py').write_text("")

    db_content = get_db_config_python(config)
    (app_dir / 'db.py').write_text(db_content)

    env_content = "PORT=8000\n"
    if config['database'] == 'mongodb':
        env_content += f"MONGO_URI=mongodb://localhost:27017/{config['project_name']}\n"
    elif config['database'] in ['postgresql', 'mysql']:
        db_name = config['database'].upper()
        env_content += f"{db_name}_HOST=localhost\n"
        env_content += f"{db_name}_PORT={'5432' if config['database'] == 'postgresql' else '3306'}\n"
        env_content += f"{db_name}_USER=root\n"
        env_content += f"{db_name}_PASSWORD=password\n"
        env_content += f"{db_name}_DATABASE={config['project_name'].replace('-', '_')}\n"

    (server_path / '.env').write_text(env_content)
    (server_path / 'requirements.txt').write_text("")

def get_db_config_python(config):
    if config['database'] == 'mongodb':
        return """from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/app")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()
"""
    elif config['database'] == 'postgresql':
        return """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("POSTGRESQL_HOST", "localhost")
DB_PORT = os.getenv("POSTGRESQL_PORT", "5432")
DB_USER = os.getenv("POSTGRESQL_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRESQL_DATABASE", "app")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
    elif config['database'] == 'mysql':
        return """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DB_NAME = os.getenv("MYSQL_DATABASE", "app")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
    elif config['database'] == 'sqlite':
        return """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
    return ""

def create_django_files(server_path, config):
    subprocess.run(['django-admin', 'startproject', config['project_name'], '.'],
                  cwd=server_path, check=True)
    subprocess.run(['python', 'manage.py', 'startapp', 'api'],
                  cwd=server_path, check=True)

def create_flask_files(server_path, config):
    app_dir = server_path / 'app'
    init_content = """from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

    from app.routes import main_routes
    app.register_blueprint(main_routes.bp)

    return app
"""
    (app_dir / '__init__.py').write_text(init_content)

    routes_dir = app_dir / 'routes'
    (routes_dir / '__init__.py').write_text("")

    main_routes_content = """from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "API is running"})
"""
    (routes_dir / 'main_routes.py').write_text(main_routes_content)

    wsgi_content = """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')), debug=True)
"""
    (server_path / 'wsgi.py').write_text(wsgi_content)

    env_content = "PORT=5000\nSECRET_KEY=your_secret_key_here\n"
    if config['database'] in ['postgresql', 'mysql']:
        db_name = config['database'].upper()
        env_content += f"{db_name}_HOST=localhost\n"
        env_content += f"{db_name}_PORT={'5432' if config['database'] == 'postgresql' else '3306'}\n"
        env_content += f"{db_name}_USER=root\n"
        env_content += f"{db_name}_PASSWORD=password\n"
        env_content += f"{db_name}_DATABASE={config['project_name'].replace('-', '_')}\n"

    (server_path / '.env').write_text(env_content)
    (server_path / 'requirements.txt').write_text("")

def create_client_files(base_path, config):
    """Update client configuration files if needed"""
    if config['project_type'] == "Full-stack":
        client_path = base_path / 'client'

        if config['frontend_framework'] == 'react':
            ext = 'ts' if config['use_typescript'] else 'js'
            vite_config_path = client_path / f'vite.config.{ext}'
            if vite_config_path.exists():
                content = vite_config_path.read_text()
                if 'server: {' not in content:
                    updated_content = content.replace(
                        'export default defineConfig({',
                        'export default defineConfig({\n  server: {\n    proxy: {\n      "/api": "http://localhost:5000"\n    }\n  },'
                    )
                    vite_config_path.write_text(updated_content)

def setup_server(base_path, config):
    server_path = base_path / 'server'

    if config['backend_language'] in ["JavaScript", "TypeScript"]:
        setup_node_server(server_path, config)
    elif config['backend_language'] == "Python":
        setup_python_server(server_path, config)

def setup_node_server(server_path, config):
    pm = get_package_manager_command(config['js_package_manager'])

    try:
        subprocess.run([pm, '--version'], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"❌ Error: {pm} not found! Install {config['js_package_manager']} and add to PATH")
        sys.exit(1)

    if config['backend_framework'] == 'express':
        subprocess.run([pm, 'init', '-y'], cwd=server_path, check=True)

        framework_deps = DEFAULT_PACKAGES['server']['express']['required']
        framework_dev_deps = DEFAULT_PACKAGES['server']['express']['dev']

        if config['use_typescript']:
            framework_dev_deps.extend(['typescript', '@types/node'])

        if config['database'] != 'none':
            db_deps = DEFAULT_PACKAGES['database'][config['database']]['node']
            framework_deps.extend(db_deps)

        framework_deps.extend(config['additional_deps'])

        subprocess.run([pm, 'install'] + framework_deps, cwd=server_path, check=True)
        subprocess.run([pm, 'install', '-D'] + framework_dev_deps, cwd=server_path, check=True)

        package_json = server_path / 'package.json'
        pkg = json.loads(package_json.read_text())
        pkg['scripts'] = {
            'start': 'node dist/app.js',
            'dev': 'nodemon --watch src --exec ts-node src/app.ts' if config['use_typescript'] else 'nodemon src/app.js',
            'build': 'tsc' if config['use_typescript'] else ''
        }
        package_json.write_text(json.dumps(pkg, indent=2))

        # Removed the block that runs 'npx tsc --init' (or equivalent) here
        # Reason: tsconfig.json is already created in create_express_files,
        # making this step redundant and avoiding the FileNotFoundError on Windows

    elif config['backend_framework'] == 'nest':
        subprocess.run([pm, 'install'], cwd=server_path, check=True)
        subprocess.run([pm, 'install', '-D'] + DEFAULT_PACKAGES['server']['nest']['dev'],
                      cwd=server_path, check=True)

def setup_python_server(server_path, config):
    pm = config['py_package_manager']

    if pm == 'poetry':
        subprocess.run(['poetry', 'init', '--no-interaction'], cwd=server_path, check=True)
    elif pm == 'conda':
        subprocess.run(['conda', 'create', '--name', config['project_name'], 'python=3.9', '-y'],
                      cwd=server_path, check=True)

    framework_deps = DEFAULT_PACKAGES['server'][config['backend_framework']]['required']
    dev_deps = DEFAULT_PACKAGES['server'][config['backend_framework']]['dev']

    if config['database'] != 'none':
        db_deps = DEFAULT_PACKAGES['database'][config['database']]['python']
        framework_deps.extend(db_deps)

    framework_deps.extend(config['additional_deps'])

    if pm == 'poetry':
        subprocess.run(['poetry', 'add'] + framework_deps, cwd=server_path, check=True)
        subprocess.run(['poetry', 'add', '-D'] + dev_deps, cwd=server_path, check=True)
    elif pm == 'conda':
        subprocess.run(['conda', 'install', '-y'] + framework_deps, cwd=server_path, check=True)
        subprocess.run(['pip', 'install'] + dev_deps, cwd=server_path, check=True)
    else:
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + framework_deps + dev_deps,
                      cwd=server_path, check=True)

    if config['backend_framework'] == 'django':
        subprocess.run(['python', 'manage.py', 'migrate'], cwd=server_path, check=True)

def setup_client(base_path, config):
    client_path = base_path / 'client'
    pm = get_package_manager_command(config['js_package_manager'])

    if config['frontend_framework'] == 'react':
        template = '--template react-ts' if config['use_typescript'] else '--template react'
        subprocess.run([pm, 'create', 'vite@latest', client_path.name, template],
                      cwd=client_path.parent, check=True)
        required_deps = DEFAULT_PACKAGES['client']['react']['required']
        subprocess.run([pm, 'install'] + required_deps, cwd=client_path, check=True)

    elif config['frontend_framework'] == 'vue':
        template = '--template vue-ts' if config['use_typescript'] else '--template vue'
        subprocess.run([pm, 'create', 'vite@latest', client_path.name, template],
                      cwd=client_path.parent, check=True)
        required_deps = DEFAULT_PACKAGES['client']['vue']['required']
        subprocess.run([pm, 'install'] + required_deps, cwd=client_path, check=True)

    elif config['frontend_framework'] == 'svelte':
        template = '--template svelte-ts' if config['use_typescript'] else '--template svelte'
        subprocess.run([pm, 'create', 'vite@latest', client_path.name, template],
                      cwd=client_path.parent, check=True)
        required_deps = DEFAULT_PACKAGES['client']['svelte']['required']
        subprocess.run([pm, 'install'] + required_deps, cwd=client_path, check=True)

    elif config['frontend_framework'] == 'angular':
        subprocess.run([pm, 'install', '-g', '@angular/cli'], check=True)
        subprocess.run(['ng', 'new', client_path.name, '--skip-install', '--routing', '--style=scss'],
                      cwd=client_path.parent, check=True)
        required_deps = DEFAULT_PACKAGES['client']['angular']['required']
        subprocess.run([pm, 'install'] + required_deps, cwd=client_path, check=True)

    create_client_additional_dirs(client_path, config)

def add_docker_support(base_path, config):
    dockerfile_content = ""

    if config['project_type'] == "Full-stack":
        dockerfile_content = f"""FROM node:18-alpine AS client
WORKDIR /app/client
COPY client/package*.json .
RUN npm install
COPY client .
RUN npm run build

FROM python:3.11-slim AS server
WORKDIR /app
COPY server/requirements.txt .
RUN pip install -r requirements.txt
COPY server .

FROM nginx:alpine
COPY --from=client /app/client/dist /usr/share/nginx/html
COPY --from=server /app /api
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""
    elif config['project_type'] == "Backend only":
        dockerfile_content = f"""FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]"""

    (base_path / 'Dockerfile').write_text(dockerfile_content)

    if config['database'] != 'none':
        compose_content = """version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
"""
        if config['database'] == 'postgresql':
            compose_content += """
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:"""
        (base_path / 'docker-compose.yml').write_text(compose_content)

def main():
    config = get_user_input()
    base_path = Path.cwd() / config['project_name']

    try:
        base_path.mkdir(exist_ok=False)

        create_directory_structure(base_path, config)

        if config['project_type'] in ["Full-stack", "Backend only"]:
            create_server_files(base_path, config)
            setup_server(base_path, config)

        if config['project_type'] in ["Full-stack", "Frontend only"]:
            setup_client(base_path, config)
            create_client_files(base_path, config)

        if config['add_docker']:
            add_docker_support(base_path, config)

        if config['init_git']:
            subprocess.run(['git', 'init'], cwd=base_path, check=True)
            (base_path / '.gitignore').write_text("node_modules/\nenv/\n.env\n__pycache__/\n*.pyc\n")

        print(f"✅ Project {config['project_name']} created successfully!")
        print(f"📁 Navigate to project directory: cd {config['project_name']}")

    except FileExistsError:
        print(f"❌ Error: Directory {config['project_name']} already exists!")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e.cmd}")
        if e.output:
            print(f"Output: {e.output.decode('utf-8', errors='ignore')}")
        sys.exit(1)

if __name__ == "__main__":
    main()


    
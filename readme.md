# Enhanced Project Creator

A powerful and flexible command-line tool that streamlines the creation of full-stack, backend, and frontend projects with sensible defaults and customizable options.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration Options](#configuration-options)
  - [Project Type](#project-type)
  - [Backend Options](#backend-options)
  - [Frontend Options](#frontend-options)
  - [Package Managers](#package-managers)
  - [Additional Features](#additional-features)
- [Directory Structure](#directory-structure)
- [Supported Technologies](#supported-technologies)
  - [Backend Frameworks](#backend-frameworks)
  - [Frontend Frameworks](#frontend-frameworks)
  - [Databases](#databases)
  - [CSS & Styling](#css--styling)
  - [State Management](#state-management)
- [Examples](#examples)
- [Extending The Tool](#extending-the-tool)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- Create full-stack, backend-only, or frontend-only projects
- Support for multiple backend frameworks:
  - **JavaScript/TypeScript**: Express, NestJS
  - **Python**: FastAPI, Django, Flask
- Support for multiple frontend frameworks:
  - React (with TypeScript option)
  - Vue (with TypeScript option)
  - Svelte (with TypeScript option)
  - Angular
- Integrated database configuration:
  - MongoDB
  - PostgreSQL
  - MySQL
  - SQLite
- Styling and state management options:
  - Tailwind CSS, Bootstrap, Material UI, Chakra UI, and more
  - Redux, Zustand, Pinia, NgRx, and more
- Flexible package management:
  - npm, yarn, pnpm for JavaScript/TypeScript
  - pip, poetry, conda for Python
- Additional features:
  - Git initialization
  - Docker support
  - Customizable directory structure
  - Pre-configured project templates

## 📋 Requirements

- Python 3.6 or higher
- Node.js and npm (for JavaScript/TypeScript projects)
- Git (optional, for repository initialization)
- Docker (optional, for containerization)

## 🚀 Installation

1. Clone this repository or download the script:

   ```bash
   git clone https://github.com/yourusername/enhanced-project-creator.git
   ```

2. Navigate to the directory:

   ```bash
   cd enhanced-project-creator
   ```

3. Install the required Python dependencies:
   ```bash
   pip install questionary
   ```

## 🖥️ Usage

Run the script from the command line:

```bash
python project_creator.py
```

Follow the interactive prompts to configure your project. You'll be asked about project type, languages, frameworks, databases, and more.

## ⚙️ Configuration Options

### Project Type

- **Full-stack**: Creates both frontend and backend
- **Backend only**: Creates only a server application
- **Frontend only**: Creates only a client application

### Backend Options

- **Language**: JavaScript, TypeScript, or Python
- **Framework**:
  - For JavaScript/TypeScript: Express or NestJS
  - For Python: FastAPI, Django, or Flask
- **Database**: MongoDB, PostgreSQL, MySQL, SQLite, or None

### Frontend Options

- **Framework**: React, Vue, Svelte, or Angular
- **TypeScript**: Option to use TypeScript (for React, Vue, and Svelte)
- **CSS Framework/Library**: Options vary by frontend framework
- **State Management**: Options vary by frontend framework

### Package Managers

- **JavaScript/TypeScript**: npm, yarn, or pnpm
- **Python**: pip, poetry, or conda (auto-detected)

### Additional Features

- **Custom Dependencies**: Add additional packages
- **Git Initialization**: Initialize a Git repository
- **Docker Support**: Add Dockerfile and docker-compose.yml

## 📁 Directory Structure

The tool creates a well-organized directory structure tailored to the selected options. Here are some examples:

### Full-stack (Express + React example)

```
my-app/
├── client/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── store/ (if using Redux/Zustand/etc.)
│   │   ├── assets/
│   │   │   ├── styles/
│   │   │   └── images/
│   │   └── types/ (if using TypeScript)
│   ├── package.json
│   └── vite.config.js/ts
├── server/
│   ├── src/
│   │   ├── config/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── types/ (if using TypeScript)
│   ├── .env
│   └── package.json
├── .gitignore
└── docker-compose.yml (if Docker support enabled)
```

### Backend Only (FastAPI example)

```
my-app/
├── server/
│   ├── app/
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── .env
│   └── requirements.txt
└── .gitignore
```

## 🧰 Supported Technologies

### Backend Frameworks

- **Express.js** (JavaScript/TypeScript): Fast, unopinionated, minimalist web framework
- **NestJS** (TypeScript): Progressive Node.js framework for building efficient, reliable applications
- **FastAPI** (Python): Modern, fast web framework for building APIs with Python
- **Django** (Python): High-level Python web framework that encourages rapid development
- **Flask** (Python): Lightweight WSGI web application framework

### Frontend Frameworks

- **React**: A JavaScript library for building user interfaces
- **Vue**: Progressive JavaScript framework for building UIs
- **Svelte**: Cybernetically enhanced web apps
- **Angular**: Platform for building mobile and desktop web applications

### Databases

- **MongoDB**: Document-based NoSQL database
- **PostgreSQL**: Powerful, open-source object-relational database
- **MySQL**: Open-source relational database management system
- **SQLite**: Lightweight, disk-based database

### CSS & Styling

For React:

- Tailwind CSS
- Bootstrap
- Material UI
- Chakra UI
- Styled Components

For Vue:

- Tailwind CSS
- Bootstrap
- Vuetify

For Svelte:

- Tailwind CSS

For Angular:

- Tailwind CSS
- Bootstrap

### State Management

For React:

- Redux
- Zustand
- Recoil
- Jotai
- Context API

For Vue:

- Pinia
- Vuex

For Svelte:

- Svelte Store

For Angular:

- NgRx

## 📝 Examples

### Creating a Full-stack React + Express Application

```bash
python project_creator.py
# Then follow the prompts:
# Project name: my-app
# Project type: Full-stack
# Backend language: JavaScript
# Backend framework: Express
# Database: MongoDB
# Frontend framework: React
# CSS framework/library: Tailwind
# State management: Redux
# JavaScript package manager: npm
# Initialize Git repository: Yes
# Add Docker support: Yes
```

### Creating a Python FastAPI Backend

```bash
python project_creator.py
# Then follow the prompts:
# Project name: api-service
# Project type: Backend only
# Backend language: Python
# Backend framework: FastAPI
# Database: PostgreSQL
# Python package manager: pip
# Initialize Git repository: Yes
# Add Docker support: Yes
```

## 🔧 Extending The Tool

The script is designed to be easily extended for additional frameworks, libraries, and configurations:

1. Update the `DEFAULT_PACKAGES` dictionary to add new technologies
2. Add corresponding setup functions for new technologies
3. Extend the command-line interface to accommodate new options

## ❓ Troubleshooting

### Common Issues

1. **Package Manager Not Found**:

   - Ensure your package managers (npm, yarn, pnpm, pip, etc.) are installed and in your PATH

2. **Permission Errors**:

   - Try running the script with administrator privileges

3. **Framework-specific Dependencies**:
   - Some frameworks may require additional global dependencies, check the error messages for details

## 👥 Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

[MIT License](LICENSE)

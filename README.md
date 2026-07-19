# 🚀 DevVault

> **A community-driven platform for software engineers to share interview questions, algorithm challenges, and technical experiences.**

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-5.1.4-green.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/docker-27+-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 📖 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation with Docker](#installation-with-docker)
  - [Installation without Docker](#installation-without-docker)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📝 About The Project

**DevVault** is a community platform where software engineers can:

- 📝 Share **interview questions** from real companies (Google, Amazon, Snapp, etc.)
- 🧠 Post **algorithm challenges** and technical problems
- 💬 **Answer questions** and get accepted by the post author
- 👍 **Vote** on useful content (upvote/downvote)
- 🔖 **Bookmark** favorite posts for later
- 👥 **Follow** other developers and build your network
- 📚 **Write articles** and share knowledge

Think of it as a **hybrid** between Stack Overflow, GitHub, and Reddit — but specialized for interview preparation and technical learning.

---

## ✨ Key Features

### 🔐 Authentication & Profiles
- User registration and login with validation
- Profile management with avatar, bio, and social links
- Follow/unfollow system

### 📝 Content Management
- Multiple post types: **Social**, **Interview**, **Article**
- Rich content with images and videos
- Tag and company categorization
- Slug-based URLs for SEO

### 💬 Interactions
- **Likes** on any content (posts, answers)
- **Comments** with nested replies (threaded comments)
- **Voting** (upvote/downvote) on posts
- **Bookmarks** for saving content
- **Answers** to interview questions with file upload (`.cpp`, `.py`, etc.)
- **Answer acceptance** by post author

### 🔍 Search & Filters
- Full-text search on titles and content
- Filter by post type, category, difficulty, company, and tags
- Pagination for large result sets

### 🐳 Docker Support
- Fully containerized with Docker and Docker Compose
- PostgreSQL as production database
- Persistent volumes for data safety
- Easy setup with one command

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Programming language |
| **Django** | 5.1.4 | Web framework |
| **PostgreSQL** | 15+ | Production database |
| **Django ORM** | - | Database abstraction |
| **GenericForeignKey** | - | Polymorphic relationships |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Bootstrap** | 5.3 | UI framework |
| **Font Awesome** | 6.4 | Icons |
| **Django Templates** | - | Server-side rendering |

### DevOps
| Technology | Version | Purpose |
|------------|---------|---------|
| **Docker** | 27+ | Containerization |
| **Docker Compose** | 3.8 | Multi-container orchestration |
| **Git** | - | Version control |

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.11 or higher
- **PostgreSQL** 15 or higher
- **Docker** and **Docker Compose** (optional but recommended)
- **Git**

---

### 📦 Installation with Docker (Recommended)

The easiest way to get started:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/DevVault.git
cd DevVault

# 2. Create environment file
cp .env.example .env
# Edit .env with your database credentials

# 3. Build and run with Docker
docker-compose up -d

# 4. Run migrations and create superuser
docker exec -it devvault_web bash
python manage.py migrate
python manage.py createsuperuser
exit

# 5. Access the application
# Open http://localhost:8000
# Admin panel: http://localhost:8000/admin

# Online Exam System

## Project Overview
The Online Exam System is a web-based application designed to facilitate the creation, administration, and evaluation of online examinations. The application offers a user-friendly interface for both administrators and students, ensuring an efficient examination process.

## Features
- User authentication and authorization for students and administrators
- Creation and management of exams with various question types (multiple choice, short answer, etc.)
- Timed exams with automatic submissions
- Interactive dashboard for monitoring exam progress in real-time
- Detailed analytics and reporting features for exam results
- Responsive design for access on various devices

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript, React
- **Backend:** Node.js, Express
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Tokens)

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/adnk000/online-exam-system.git
   cd online-exam-system
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure environment variables (refer to `.env.example` for required variables):
   ```bash
   cp .env.example .env
   ```
4. Start the application:
   ```bash
   npm start
   ```

## Usage Guide
- Access the application at `http://localhost:3000`
- Register as a new user or log in with your credentials
- As an administrator, create new exams, manage users, and view results.
- As a student, take assigned exams during the specified time frames.

## Contributing Guidelines
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeatureName
   ```
5. Open a pull request with a description of the changes.

---

*Documentation Last Updated: 2026-04-24*
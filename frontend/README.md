# Society Node Frontend

React + TypeScript + Tailwind CSS frontend for the Society Node social platform.

## Setup

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Create environment variables
```bash
cp .env.example .env.local
```

### 3. Start development server
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 4. Build for production
```bash
npm run build
```

## Features

- ✅ User authentication (Login/Register)
- ✅ Feed with posts
- ✅ User profiles
- ✅ Follow/Unfollow
- ✅ Create posts
- ✅ Comments and likes
- 🔄 (In progress) Shop/Marketplace
- 🔄 (In progress) Notifications

## Project Structure

```
src/
├── components/     # Reusable React components
├── pages/          # Page components
├── services/       # API service calls
├── store/          # Zustand state management
├── App.tsx         # Main app component
└── index.css       # Tailwind CSS styles
```

## API Integration

The frontend communicates with the Society Node API at `http://localhost:8000`

Make sure the backend is running before starting the frontend.

## Technologies

- React 18
- TypeScript
- Tailwind CSS
- Axios
- React Router
- Zustand (State Management)
- Vite (Build tool)

# Mobile Shopping Chat Agent - Frontend

Modern React frontend for the Mobile Shopping Chat Agent (India Market).

## Features

- 🎨 Modern, responsive UI design
- 💬 Real-time chat interface
- 📱 Product cards with specifications
- 🇮🇳 India-focused (INR currency)
- 📱 Mobile-friendly design

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development
- **Axios** for API calls
- **CSS3** for styling

## Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Development

- Frontend runs on: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Proxy configured in `vite.config.ts` for `/api` routes

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx    # Main chat container
│   │   ├── MessageList.tsx      # Message list component
│   │   ├── MessageBubble.tsx    # Individual message bubble
│   │   ├── ProductCards.tsx     # Product display cards
│   │   └── InputArea.tsx        # Chat input area
│   ├── services/
│   │   └── api.ts               # API service functions
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles
├── package.json
├── vite.config.ts
└── tsconfig.json
```


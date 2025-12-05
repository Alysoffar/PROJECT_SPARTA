# SPARTA Frontend

React + TypeScript frontend for the SPARTA platform.

## Features

- **Chat Interface**: Natural language hardware design specification
- **Design Canvas**: Visual hardware component design
- **Real-time Monitoring**: Live emulation and optimization progress
- **Visualization Dashboard**: Performance metrics and design space exploration
- **Code Editor**: RTL code viewing and editing

## Technology Stack

- React 18
- TypeScript
- TanStack Query (data fetching)
- Zustand (state management)
- TailwindCSS (styling)
- Recharts (visualization)
- Monaco Editor (code editing)

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint
npm run lint
```

## Environment Variables

Create `.env.local`:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/        # React components
│   │   ├── chat/
│   │   ├── canvas/
│   │   ├── editor/
│   │   └── dashboard/
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API clients
│   ├── store/            # State management
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   ├── App.tsx
│   └── index.tsx
├── package.json
└── tsconfig.json
```

## API Integration

The frontend communicates with the backend through the API Gateway at `http://localhost:8000`.

See [API Documentation](../docs/api-reference.md) for endpoint details.

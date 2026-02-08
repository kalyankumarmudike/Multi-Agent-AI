# Multi-Agent Document Intelligence - Frontend

Modern React 18 frontend with TypeScript, Tailwind CSS, and React Query for the Multi-Agent Deep Document Intelligence System.

## 🚀 Tech Stack

- **React 18** - UI framework with latest features
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Lightning-fast build tool
- **Axios** - HTTP client
- **React Query** - Server state management
- **Lucide React** - Beautiful icons
- **React Hot Toast** - Toast notifications

## 📦 Installation

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Setup

1. **Navigate to frontend directory**

```bash
cd frontend
```

2. **Install dependencies**

```bash
npm install
```

3. **Configure environment** (optional)

```bash
cp .env.example .env
```

Edit `.env` if your backend runs on a different URL:

```env
VITE_API_URL=http://localhost:8000
```

4. **Start development server**

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## 🎯 Usage

### Development

```bash
npm run dev        # Start dev server with hot reload
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Run ESLint
```

### Production Build

```bash
npm run build
npm run preview
```

The production-ready files will be in the `dist/` directory.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── client.ts           # Axios client & API endpoints
│   ├── components/
│   │   ├── DocumentUpload.tsx  # Upload & input component
│   │   └── AnalysisResults.tsx # Results display component
│   ├── hooks/
│   │   └── useDocumentAnalysis.ts  # React Query hooks
│   ├── types/
│   │   └── index.ts            # TypeScript type definitions
│   ├── App.tsx                 # Main app component
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── public/                     # Static assets
├── index.html                  # HTML template
├── vite.config.ts             # Vite configuration
├── tailwind.config.js         # Tailwind CSS config
├── tsconfig.json              # TypeScript config
└── package.json               # Dependencies
```

## 🎨 Features

### Document Upload
- Drag & drop file upload
- Direct text input
- Support for .txt and .md files
- Real-time word count
- Input validation

### Analysis Results
- Executive summary display
- Action items with dependencies
- Risk and issue tracking
- Impact level indicators
- Processing time stats
- Beautiful, responsive UI

### User Experience
- Real-time health check status
- Toast notifications
- Loading states
- Error handling
- Responsive design
- Modern gradient backgrounds

## 🔧 Configuration

### API Proxy

The Vite dev server is configured to proxy API requests:

```typescript
// vite.config.ts
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

### Tailwind Theme

Custom colors and animations are configured in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: { /* custom primary colors */ },
    },
    animation: {
      'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    },
  },
}
```

## 🌐 API Integration

The frontend communicates with the FastAPI backend through Axios:

```typescript
// Example API call
POST http://localhost:8000/analyze-document
{
  "document_text": "Your document..."
}
```

React Query handles caching, loading states, and error management automatically.

## 🎯 Architecture Flow

```
User Input (React)
    ↓
Document Upload Component
    ↓
Axios POST → /analyze-document
    ↓
Backend Processing (3 AI Agents)
    ↓
JSON Response
    ↓
React Query Cache
    ↓
Analysis Results Component
    ↓
Beautiful UI Display
```

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

### Deploy Options

1. **Vercel** (Recommended)
   ```bash
   vercel deploy
   ```

2. **Netlify**
   ```bash
   netlify deploy --prod
   ```

3. **Docker**
   ```dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build
   CMD ["npm", "run", "preview"]
   ```

4. **Static Hosting**
   - Upload `dist/` contents to any static host (AWS S3, Cloudflare Pages, etc.)

## 🔒 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

## 🐛 Troubleshooting

### API Connection Issues

1. Ensure backend is running on port 8000
2. Check CORS configuration in backend
3. Verify `.env` file has correct API URL

### Build Issues

```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

### TypeScript Errors

```bash
# Check TypeScript configuration
npx tsc --noEmit
```

## 📝 License

MIT License

## 🤝 Contributing

This frontend is designed to work seamlessly with the Multi-Agent Deep Document Intelligence backend. Ensure both systems are running for full functionality.

---

**Built with ❤️ using React 18, TypeScript, and Tailwind CSS**

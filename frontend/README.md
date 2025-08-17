# Sri Lankan Government Services Portal - Frontend

A modern, responsive Vue.js frontend for the Government Appointment Booking System.

## Features

### 🎨 Modern Design System
- Professional government portal aesthetic
- Responsive design for all devices
- Consistent color scheme and typography
- Smooth animations and transitions

### 🔐 Enhanced Authentication
- Beautiful login and registration forms
- Loading states and error handling
- Form validation and user feedback
- Secure token-based authentication

### 📅 Appointment Booking
- Intuitive service selection interface
- Real-time date and time slot availability
- Booking summary and confirmation
- Progress indicators and status updates

### 🏠 Improved Homepage
- Hero section with call-to-action buttons
- Feature highlights and benefits
- Popular services showcase
- Professional government branding

### 📱 Responsive Layout
- Mobile-first design approach
- Tablet and desktop optimizations
- Touch-friendly interface elements
- Adaptive navigation

## Technology Stack

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe development
- **Vue Router** - Client-side routing
- **Pinia** - State management
- **Axios** - HTTP client for API communication
- **CSS Custom Properties** - Modern styling system

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn package manager

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
# Create .env file with:
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

4. Start development server:
```bash
npm run dev
```

5. Open your browser and visit `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   └── booking/        # Appointment booking components
├── views/              # Page components
│   ├── auth/          # Authentication pages
│   ├── admin/         # Admin dashboard pages
│   ├── officer/       # Officer dashboard pages
│   └── user/          # User dashboard pages
├── stores/            # Pinia state management
├── services/          # API service layer
├── router/            # Vue Router configuration
├── styles.css         # Global styles and design system
└── main.ts           # Application entry point
```

## Design System

### Colors
- **Primary**: Blue (#1e40af) - Government trust and authority
- **Secondary**: Green (#059669) - Success and completion
- **Accent**: Orange (#f59e0b) - Warnings and highlights
- **Neutral**: Gray scale for text and backgrounds

### Typography
- **Font Family**: Inter (system fallbacks)
- **Sizes**: Responsive scale from xs to 4xl
- **Weights**: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

### Components
- **Buttons**: Primary, secondary, outline, and ghost variants
- **Forms**: Consistent input styling with validation states
- **Cards**: Clean containers with shadows and borders
- **Alerts**: Success, warning, error, and info variants
- **Badges**: Status indicators and labels

## API Integration

The frontend communicates with the backend through a RESTful API:

- **Base URL**: Configurable via environment variables
- **Authentication**: JWT token-based
- **Error Handling**: Comprehensive error messages and fallbacks
- **Loading States**: User feedback during API calls

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code style and conventions
2. Use TypeScript for type safety
3. Write meaningful commit messages
4. Test on multiple devices and browsers
5. Ensure accessibility standards are met

## License

This project is part of the Sri Lankan Government Services Portal.

import { lazy, StrictMode, Suspense } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/press-start-2p/latin-400.css';
import '@fontsource/vt323/latin-400.css';
import App from './App';
import { ErrorBoundary } from './components/ErrorBoundary';
import './styles.css';

// The animation review page is its own chunk, so it adds nothing to the first load. It is for development
// (?animations=1) and for checking a build (?preview=1&animations=1).
const AnimationsPage = lazy(() => import('./AnimationsPage'));
const params = new URLSearchParams(window.location.search);
const showAnimations = params.get('animations') === '1' && (import.meta.env.DEV || params.get('preview') === '1');

const root = document.getElementById('root');
if (!root) throw new Error('Missing #root element');
createRoot(root).render(
  <StrictMode>
    <ErrorBoundary>
    {showAnimations ? (
      <Suspense fallback={null}>
        <AnimationsPage />
      </Suspense>
    ) : (
      <App />
    )}
    </ErrorBoundary>
  </StrictMode>,
);

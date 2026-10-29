import { Component, type ReactNode } from 'react';
import { ErrorScreen } from './ErrorScreen';

interface State {
  error: Error | null;
}

/** Catches a crash while rendering and shows the error screen instead of a blank page. Retry reloads the page. */
export class ErrorBoundary extends Component<{ children: ReactNode }, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  render(): ReactNode {
    if (this.state.error) {
      return (
        <main className="app">
          <ErrorScreen message={this.state.error.message || 'something went wrong'} onRetry={() => window.location.reload()} />
        </main>
      );
    }
    return this.props.children;
  }
}

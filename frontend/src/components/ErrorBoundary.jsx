import React from 'react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100svh',
          display: 'grid',
          placeItems: 'center',
          padding: '20px',
          color: '#eef0ff',
          background: '#050511',
          fontFamily: 'Inter, system-ui, sans-serif'
        }}>
          <div style={{
            maxWidth: '520px',
            width: '100%',
            background: 'rgba(255,255,255,.05)',
            border: '1px solid rgba(255,107,107,.4)',
            borderRadius: '20px',
            padding: '32px',
            textAlign: 'center',
            boxShadow: '0 20px 60px rgba(0,0,0,.5)'
          }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>⚠️</div>
            <h2 style={{ fontSize: '1.4rem', margin: '0 0 10px', color: '#ff6b6b' }}>
              Something went wrong
            </h2>
            <p style={{ color: '#9aa0c8', fontSize: '.9rem', margin: '0 0 20px' }}>
              {this.state.error?.message || 'An unexpected rendering error occurred.'}
            </p>
            <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
              <button
                onClick={() => {
                  this.setState({ hasError: false, error: null });
                  window.location.href = '/';
                }}
                style={{
                  background: 'linear-gradient(135deg, #4f7cff, #8b5cf6)',
                  color: '#fff',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '999px',
                  fontWeight: '600',
                  cursor: 'pointer'
                }}
              >
                Return to Home
              </button>
              <button
                onClick={() => window.location.reload()}
                style={{
                  background: 'rgba(255,255,255,.08)',
                  color: '#fff',
                  border: '1px solid rgba(255,255,255,.15)',
                  padding: '12px 24px',
                  borderRadius: '999px',
                  fontWeight: '600',
                  cursor: 'pointer'
                }}
              >
                Reload Page
              </button>
            </div>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

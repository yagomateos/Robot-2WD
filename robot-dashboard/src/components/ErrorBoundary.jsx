import { Component } from 'react';

/**
 * Error Boundary para capturar errores de React y mostrar UI de fallback
 * Evita que toda la aplicación se rompa por errores en componentes
 */
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error) {
    // Actualizar estado para renderizar UI de fallback
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Registrar error en consola (en producción podrías enviarlo a un servicio)
    console.error('Error capturado por ErrorBoundary:', error, errorInfo);

    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-container">
            <h1 className="error-title">⚠️ Algo salió mal</h1>
            <p className="error-message">
              La aplicación encontró un error inesperado.
              Puedes intentar recargar la página o contactar al soporte.
            </p>

            <div className="error-actions">
              <button
                className="btn-primary"
                onClick={() => window.location.reload()}
              >
                Recargar Página
              </button>
              <button
                className="btn-secondary"
                onClick={this.handleReset}
              >
                Intentar de Nuevo
              </button>
            </div>

            {import.meta.env.DEV && this.state.error && (
              <details className="error-details">
                <summary>Detalles del error (solo en desarrollo)</summary>
                <pre className="error-stack">
                  {this.state.error.toString()}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

#!/usr/bin/env python3
"""
ClaroVenta - Servidor de desarrollo simple
------------------------------------------
Ejecuta este archivo para ver el prototipo en el navegador.

Uso:
    python server.py

Luego abre: http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
from functools import partial

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Evitar caché en desarrollo
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, format, *args):
        # Logs más limpios
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 50)
        print("  ClaroVenta - Prototipo UX/UI")
        print("=" * 50)
        print(f"  Servidor corriendo en: {url}")
        print("  Páginas disponibles:")
        print(f"    • Landing     → {url}/")
        print(f"    • Cargar datos→ {url}/upload.html")
        print(f"    • Dashboard   → {url}/dashboard.html")
        print(f"    • Producto    → {url}/product.html")
        print("=" * 50)
        print("  Presiona Ctrl+C para detener")
        print()

        try:
            # Intentar abrir el navegador automáticamente
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")


if __name__ == "__main__":
    main()

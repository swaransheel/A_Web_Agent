#!/usr/bin/env python3
"""
Simple web server to serve the frontend on a single endpoint.
Access at: http://localhost:3000/
"""
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler


class FrontendHandler(SimpleHTTPRequestHandler):
    """Custom handler to serve frontend files."""
    
    def do_GET(self):
        """Handle GET requests."""
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        
        # Allow accessing any file in frontend folder
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def end_headers(self):
        """Add CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        SimpleHTTPRequestHandler.end_headers(self)


def run_server(port=3000):
    """Run the frontend server."""
    # Change to frontend directory
    frontend_dir = Path(__file__).parent / 'frontend'
    os.chdir(frontend_dir)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, FrontendHandler)
    
    print(f"🚀 Frontend Server Running")
    print(f"📱 Open in browser: http://localhost:{port}/")
    print(f"📂 Serving from: {frontend_dir}")
    print(f"⏹️  Press Ctrl+C to stop\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Server stopped")


if __name__ == '__main__':
    run_server(3000)

#!/bin/bash

# AgentTest Documentation Helper Script
# This script provides convenient commands for working with the documentation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if docs dependencies are installed
check_deps() {
    print_status "Checking documentation dependencies..."
    
    if ! python -c "import mkdocs" 2>/dev/null; then
        print_error "MkDocs not found. Installing documentation dependencies..."
        pip install -e ".[docs]"
    else
        print_success "Documentation dependencies are installed"
    fi
}

# Function to serve documentation locally
serve() {
    check_deps
    print_status "Starting documentation server..."
    print_status "Documentation will be available at: http://localhost:8000"
    print_status "Press Ctrl+C to stop the server"
    mkdocs serve
}

# Function to build documentation
build() {
    check_deps
    print_status "Building documentation..."
    
    if mkdocs build --clean; then
        print_success "Documentation built successfully in ./site/"
    else
        print_error "Documentation build failed"
        exit 1
    fi
}

# Function to build with strict mode
build_strict() {
    check_deps
    print_status "Building documentation with strict mode..."
    
    if mkdocs build --clean --strict; then
        print_success "Documentation built successfully with no warnings"
    else
        print_error "Documentation build failed or has warnings"
        exit 1
    fi
}

# Function to deploy to GitHub Pages
deploy() {
    check_deps
    print_status "Deploying documentation to GitHub Pages..."
    
    if mkdocs gh-deploy --clean; then
        print_success "Documentation deployed to GitHub Pages"
    else
        print_error "Documentation deployment failed"
        exit 1
    fi
}

# Function to check for broken links
check_links() {
    check_deps
    print_status "Checking for broken links..."
    
    # Build first to ensure site is up to date
    mkdocs build --clean --quiet
    
    # Simple check for common issues
    print_status "Checking internal links..."
    if find site -name "*.html" -exec grep -l "404.html" {} \; | head -1; then
        print_warning "Found potential broken links. Check the build output for details."
    else
        print_success "No obvious broken links found"
    fi
}

# Function to clean build artifacts
clean() {
    print_status "Cleaning documentation build artifacts..."
    
    if [ -d "site" ]; then
        rm -rf site
        print_success "Removed site/ directory"
    fi
    
    if [ -d ".mkdocs_cache" ]; then
        rm -rf .mkdocs_cache
        print_success "Removed .mkdocs_cache/ directory"
    fi
    
    print_success "Documentation artifacts cleaned"
}

# Function to show help
show_help() {
    echo "AgentTest Documentation Helper"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  serve       Start local development server (default)"
    echo "  build       Build documentation"
    echo "  build-strict Build with strict mode (fail on warnings)"
    echo "  deploy      Deploy to GitHub Pages"
    echo "  check-links Check for broken links"
    echo "  clean       Clean build artifacts"
    echo "  install     Install documentation dependencies"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 serve      # Start development server"
    echo "  $0 build      # Build documentation"
    echo "  $0 deploy     # Deploy to GitHub Pages"
}

# Function to install dependencies
install_deps() {
    print_status "Installing documentation dependencies..."
    pip install -e ".[docs]"
    print_success "Documentation dependencies installed"
}

# Main script logic
case "${1:-serve}" in
    "serve")
        serve
        ;;
    "build")
        build
        ;;
    "build-strict")
        build_strict
        ;;
    "deploy")
        deploy
        ;;
    "check-links")
        check_links
        ;;
    "clean")
        clean
        ;;
    "install")
        install_deps
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac 
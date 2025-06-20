#!/bin/bash
# MCP Server Status and Management Script
# Usage: ./server_manager.sh [start|stop|status|restart]

set -e

PROJECT_DIR="/home/sislam6/Illinois_Tech/PhD/Spring25_iit/CS550/scientific-mcps/slurm-mcp"
SERVER_SCRIPT="src/server.py"
LOG_FILE="server_manager.log"
PID_FILE="server.pid"

cd "$PROJECT_DIR"

print_header() {
    echo ""
    echo "🔍 $1"
    echo "$(printf '=%.0s' {1..40})"
}

check_server_status() {
    print_header "Server Status Check"
    
    # Method 1: Check PID file
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✅ Server is running (PID: $PID)"
            ps aux | grep "$PID" | grep -v grep | head -1
            return 0
        else
            echo "❌ PID file exists but process is dead, cleaning up..."
            rm -f "$PID_FILE"
        fi
    fi
    
    # Method 2: Search for server processes
    SERVER_PID=$(pgrep -f "$SERVER_SCRIPT" | head -1)
    if [ ! -z "$SERVER_PID" ]; then
        echo "✅ Found server process (PID: $SERVER_PID)"
        echo "$SERVER_PID" > "$PID_FILE"
        ps aux | grep "$SERVER_PID" | grep -v grep | head -1
        return 0
    fi
    
    # Method 3: Check ports (for SSE mode)
    if netstat -tuln 2>/dev/null | grep -q ":8000"; then
        echo "⚠️  Port 8000 is in use (possible server)"
        netstat -tuln | grep ":8000"
    else
        echo "❌ No server processes found and port 8000 is free"
    fi
    
    return 1
}

start_server() {
    print_header "Starting MCP Server"
    
    if check_server_status >/dev/null 2>&1; then
        echo "⚠️  Server is already running!"
        return 1
    fi
    
    echo "🚀 Starting server in background..."
    echo "📝 Logs will be written to: $LOG_FILE"
    
    # Start server in background
    nohup python "$SERVER_SCRIPT" > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    
    echo "$SERVER_PID" > "$PID_FILE"
    echo "✅ Server started with PID: $SERVER_PID"
    
    # Give server time to initialize
    sleep 3
    
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "✅ Server is running successfully"
        echo "📋 Recent logs:"
        tail -5 "$LOG_FILE" || echo "No logs yet"
    else
        echo "❌ Server failed to start, check logs:"
        cat "$LOG_FILE"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_server() {
    print_header "Stopping MCP Server"
    
    # Try PID file first
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🛑 Stopping server (PID: $PID)..."
            kill "$PID"
            sleep 2
            
            if kill -0 "$PID" 2>/dev/null; then
                echo "⚠️  Server still running, force killing..."
                kill -9 "$PID"
            fi
            
            rm -f "$PID_FILE"
            echo "✅ Server stopped"
        else
            echo "❌ PID file exists but process is already dead"
            rm -f "$PID_FILE"
        fi
    fi
    
    # Kill any remaining server processes
    SERVER_PIDS=$(pgrep -f "$SERVER_SCRIPT" || true)
    if [ ! -z "$SERVER_PIDS" ]; then
        echo "🛑 Killing remaining server processes: $SERVER_PIDS"
        pkill -f "$SERVER_SCRIPT"
        echo "✅ All server processes stopped"
    else
        echo "✅ No server processes found"
    fi
}

restart_server() {
    print_header "Restarting MCP Server"
    stop_server
    sleep 2
    start_server
}

test_server() {
    print_header "Testing Server Functionality"
    
    echo "🧪 Testing module imports..."
    python -c "
import sys
sys.path.insert(0, 'src')
try:
    import server
    print('✅ Server module: OK')
    import mcp_handlers
    print('✅ MCP handlers: OK')
    from capabilities.slurm_handler import _check_slurm_available
    print(f'✅ Slurm available: {_check_slurm_available()}')
except Exception as e:
    print(f'❌ Import error: {e}')
    exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo "✅ All tests passed!"
    else
        echo "❌ Tests failed!"
        return 1
    fi
}

show_logs() {
    print_header "Server Logs"
    
    if [ -f "$LOG_FILE" ]; then
        echo "📋 Recent server logs (last 20 lines):"
        echo "$(printf '-%.0s' {1..40})"
        tail -20 "$LOG_FILE"
        echo "$(printf '-%.0s' {1..40})"
        echo "💡 To follow live logs: tail -f $LOG_FILE"
    else
        echo "❌ No log file found: $LOG_FILE"
    fi
}

show_help() {
    cat << EOF
🎯 MCP Server Manager

Usage: $0 [COMMAND]

Commands:
    start     Start the MCP server
    stop      Stop the MCP server  
    restart   Restart the MCP server
    status    Check server status
    test      Test server functionality
    logs      Show server logs
    help      Show this help message

Examples:
    $0 start          # Start server
    $0 status         # Check if running
    $0 logs          # View recent logs
    $0 restart       # Restart server

Files:
    $LOG_FILE     # Server logs
    $PID_FILE       # Server PID
    $SERVER_SCRIPT   # Server script
EOF
}

# Main command handling
case "${1:-status}" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        check_server_status
        ;;
    test)
        test_server
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_help
        exit 1
        ;;
esac

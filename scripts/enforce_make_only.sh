#!/bin/bash
# Enforce Make-only execution model
# This script sets up permissions so that tools can only be run through make

set -e

echo "🔐 Setting up Make-only permission model..."

# Create backup of original pytest
if [[ ! -f /home/lou/.local/bin/pytest.original ]]; then
    echo "📦 Creating backup of original pytest..."
    cp /home/lou/.local/bin/pytest /home/lou/.local/bin/pytest.original
fi

# Replace pytest with wrapper
echo "🔄 Replacing pytest with wrapper..."
cp scripts/pytest_wrapper.sh /home/lou/.local/bin/pytest
chmod +x /home/lou/.local/bin/pytest

# Create similar wrappers for other tools
create_tool_wrapper() {
    local tool=$1
    local wrapper_file="scripts/${tool}_wrapper.sh"
    
    if [[ ! -f ""wrapper_fil"e" ]]; then
        echo "📝 Creating wrapper for "tool"..."
        cat > ""wrapper_fil"e" << EOF
#!/bin/bash
# $tool wrapper - only allows execution through make

check_parent_process() {
    local parent_pid=\$(ps -o ppid= -p \$\$)
    local parent_name=\$(ps -o comm= -p \"parent_pid")
    
    # Allow if parent is make
    if [[ "\"parent_nam"e" == "make" ]]; then
        return 0
    fi
    
    # Allow if we're in a make environment
    if [[ -n "\"MAKEFLAG"S" || -n "\"MAKELEVE"L" ]]; then
        return 0
    fi
    
    # Block direct execution
    echo "❌ ERROR: "too"l can only be executed through make"
    echo "✅ Use: make ${tool//_/-}"
    echo "📋 Available targets:"
    echo "   - make ${tool//_/-}"
    echo "   - make ${tool//_/-}-all"
    echo "   - make ${tool//_/-}-python"
    exit 1
}

check_parent_process
exec /home/lou/.local/bin/${tool}.original "\$@"
EOF
        chmod +x ""wrapper_fil"e"
    fi
}

# Create wrappers for common tools
create_tool_wrapper "flake8"
create_tool_wrapper "black"
create_tool_wrapper "mypy"

# Create symbolic links to wrappers
echo "🔗 Creating symbolic links..."
ln -sf /home/lou/Documents/OpenFlow-Playground/scripts/flake8_wrapper.sh
/home/lou/.local/bin/flake8
ln -sf /home/lou/Documents/OpenFlow-Playground/scripts/black_wrapper.sh
/home/lou/.local/bin/black
ln -sf /home/lou/Documents/OpenFlow-Playground/scripts/mypy_wrapper.sh
/home/lou/.local/bin/mypy

# Create a restore script
cat > scripts/restore_tools.sh << 'EOF'
#!/bin/bash
# Restore original tools

echo "🔄 Restoring original tools..."

# Restore pytest
if [[ -f /home/lou/.local/bin/pytest.original ]]; then
    cp /home/lou/.local/bin/pytest.original /home/lou/.local/bin/pytest
    chmod +x /home/lou/.local/bin/pytest
    echo "✅ Restored pytest"
fi

# Remove symbolic links
rm -f /home/lou/.local/bin/flake8
rm -f /home/lou/.local/bin/black
rm -f /home/lou/.local/bin/mypy

echo "✅ Tools restored to original state"
EOF

chmod +x scripts/restore_tools.sh

echo "✅ Make-only permission model set up!"
echo ""
echo "🔒 Tools are now restricted to Make-only execution:"
echo "   - pytest → make test"
echo "   - flake8 → make lint"
echo "   - black → make format"
echo "   - mypy → make type-safety"
echo ""
echo "🔄 To restore original behavior: ./scripts/restore_tools.sh"
echo ""
echo "🧪 Test it:"
echo "   ❌ pytest --version (should fail)"
echo "   ✅ make test (should work)" 

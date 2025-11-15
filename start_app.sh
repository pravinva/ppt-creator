#!/bin/bash

echo "================================================================================"
echo "🎨 PROFESSIONAL AGENTIC AI ARCHITECTURE GENERATOR"
echo "================================================================================"
echo ""
echo "Starting web application..."
echo ""
echo "📍 The app will open at: http://localhost:8050"
echo ""
echo "✨ Features:"
echo "   • GUI-based configuration (NO code editing!)"
echo "   • Professional swim-lane diagrams"
echo "   • Real arrows with arrowheads"
echo "   • PowerPoint generation"
echo "   • Works for ANY company"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================================================"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import dash, dash_bootstrap_components, PIL, pptx" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Installing missing dependencies..."
    pip install dash dash-bootstrap-components pillow python-pptx
    echo ""
fi

echo "Starting app..."
echo ""

# Run the app
python3 agentic_ai_app.py

# SPARTA Chat - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the System

**Option A - Automated (Windows):**
```powershell
.\start.ps1
```

**Option B - Manual:**

Terminal 1 - Backend:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 9000 --reload
```

Terminal 2 - Frontend:
```bash
cd frontend
streamlit run app.py
```

### Step 3: Open Browser
Navigate to: **http://localhost:8501**

---

## 💡 Try These Examples

### Example 1: Simple Adder
```
Generate a 4-bit ripple carry adder
```

### Example 2: ALU
```
Create an 8-bit ALU with ADD, SUB, AND, OR, XOR operations
```

### Example 3: FSM
```
Design a 3-state traffic light controller with RED, YELLOW, GREEN states
```

### Example 4: UART
```
Build a UART transmitter with 8 data bits, 1 stop bit, no parity
```

---

## 🧪 Test Backend
```bash
python test_backend.py
```

Expected output:
```
✅ Health check: healthy
✅ Chat response received
✅ Search returned N results
🎉 All tests passed!
```

---

## 📚 API Documentation

Once running, visit: **http://localhost:9000/docs**

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 9000 (Windows)
netstat -ano | findstr :9000
taskkill /PID <PID> /F

# Kill process on port 8501
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Dependencies Error
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Frontend Won't Connect
- Ensure backend is running: `http://localhost:9000/health`
- Check BACKEND_URL in `frontend/app.py` (should be `http://localhost:9000`)

---

## 📂 Directory Structure
```
sparta-chat/
├── backend/           # FastAPI orchestrator (port 9000)
├── frontend/          # Streamlit UI (port 8501)
├── requirements.txt   # Python dependencies
├── start.ps1          # Windows startup script
└── README.md          # Full documentation
```

---

## 🎯 What to Expect

1. **Chat Interface**: Clean ChatGPT-style UI with message history
2. **Rich Responses**: Emoji-rich outputs with structured sections
3. **Visualizations**: Embedded waveform plots for simulations
4. **Internal Notes**: Expandable reasoning process view
5. **Design Metrics**: Area, power, latency displayed in sidebar
6. **Search**: Find previous designs by keyword

---

## 📖 Next Steps

- Read full documentation: `README.md`
- Explore API: `http://localhost:9000/docs`
- Try complex designs: Multi-bit ALUs, FSMs, UARTs
- Search previous designs in sidebar
- View internal reasoning in expandable sections

---

## 🆘 Support

For issues or questions, check:
- Full README: `README.md`
- API Docs: `http://localhost:9000/docs`
- Test Suite: `python test_backend.py`

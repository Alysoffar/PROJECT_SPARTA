"""
Simple test to validate SPARTA Chat backend
"""
import requests
import uuid
import time

BACKEND_URL = "http://localhost:9000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BACKEND_URL}/health")
    assert response.status_code == 200
    print(f"✅ Health check: {response.json()['status']}")

def test_chat():
    """Test chat endpoint"""
    print("\n💬 Testing chat endpoint...")
    
    session_id = str(uuid.uuid4())
    test_message = "Generate a 4-bit adder"
    
    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={
            "session_id": session_id,
            "message": test_message
        },
        timeout=60
    )
    
    assert response.status_code == 200
    data = response.json()
    
    print(f"✅ Chat response received")
    print(f"   Session: {data['session_id'][:8]}...")
    print(f"   Response length: {len(data['response'])} chars")
    print(f"   Has visualization: {bool(data.get('visualization'))}")
    print(f"\n📝 Response preview:")
    print(data['response'][:200] + "...")

def test_search():
    """Test search endpoint"""
    print("\n🔍 Testing search endpoint...")
    
    response = requests.get(
        f"{BACKEND_URL}/search",
        params={"query": "adder", "limit": 3}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    print(f"✅ Search returned {len(data['results'])} results")

if __name__ == "__main__":
    print("🧪 SPARTA Chat Backend Test Suite\n")
    print("=" * 50)
    
    try:
        test_health()
        test_chat()
        test_search()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Backend not running!")
        print("   Start backend: cd backend && uvicorn main:app --port 9000")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")

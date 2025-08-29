#!/usr/bin/env python3
"""
Test the exact TQDM import pattern used in es.py
"""

print("🧪 Testing TQDM import pattern...")

try:
    from tqdm import tqdm
    print("✅ TQDM import successful!")
    
    # Test if we can use it
    test_list = [1, 2, 3, 4, 5]
    for item in tqdm(test_list, desc="Testing TQDM"):
        pass
    print("✅ TQDM functionality working!")
    
except ImportError as e:
    print(f"❌ TQDM import failed: {e}")
    print("💡 This means the try-except block in es.py will catch this")
except Exception as e:
    print(f"💥 Unexpected error: {e}")

print("🎯 Test completed!")

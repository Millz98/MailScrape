#!/usr/bin/env python3
"""
Test file writing functionality
"""

# Test 1: Basic file writing
print("🧪 Test 1: Basic file writing")
with open('test_emails.txt', 'w') as file:
    file.write("test1@example.com\n")
    file.write("test2@example.com\n")
print("✅ Test 1 completed")

# Test 2: Append mode
print("\n🧪 Test 2: Append mode")
with open('test_emails.txt', 'a') as file:
    file.write("test3@example.com\n")
    file.write("test4@example.com\n")
print("✅ Test 2 completed")

# Test 3: Read and verify
print("\n🧪 Test 3: Read and verify")
with open('test_emails.txt', 'r') as file:
    content = file.read()
    print(f"📄 File content: '{content}'")
    print(f"📊 File size: {len(content)} bytes")
    lines = content.splitlines()
    print(f"📝 Number of lines: {len(lines)}")
    for i, line in enumerate(lines):
        print(f"   Line {i+1}: '{line}'")

# Test 4: Check if emails.txt exists and its content
print("\n🧪 Test 4: Check emails.txt")
try:
    with open('emails.txt', 'r') as file:
        content = file.read()
        print(f"📄 emails.txt content: '{content}'")
        print(f"📊 emails.txt size: {len(content)} bytes")
        if content.strip():
            lines = content.splitlines()
            print(f"📝 emails.txt lines: {len(lines)}")
            for i, line in enumerate(lines):
                print(f"   Line {i+1}: '{line}'")
        else:
            print("❌ emails.txt is empty or contains only whitespace")
except FileNotFoundError:
    print("❌ emails.txt not found")
except Exception as e:
    print(f"💥 Error reading emails.txt: {e}")

print("\n�� Test completed!")

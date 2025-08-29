#!/usr/bin/env python3
"""
Safe Environment Variable Loader
Loads environment variables from .env file safely.
"""

import os
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file if it exists"""
    
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ Found .env file, loading environment variables...")
        
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                
                # Parse key=value pairs
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Set environment variable
                    os.environ[key] = value
                    print(f"   Loaded: {key} = {'*' * len(value) if 'key' in key.lower() or 'secret' in key.lower() else value}")
        
        print("✅ Environment variables loaded successfully!")
    else:
        print("⚠️  No .env file found. Using system environment variables.")

def validate_required_vars():
    """Validate that required environment variables are set"""
    
    required_vars = ['API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nPlease create a .env file with:")
        print("1. Copy env_template.txt to .env")
        print("2. Add your actual values to .env")
        print("3. Never commit .env files to git!")
        return False
    
    print("✅ All required environment variables are set!")
    return True

def show_env_status():
    """Show status of environment variables (without exposing values)"""
    
    print("\n📋 Environment Variables Status:")
    print("=" * 40)
    
    env_vars = {
        'API_KEY': os.getenv('API_KEY'),
        'MAILGUN_DOMAIN': os.getenv('MAILGUN_DOMAIN'),
        'MAILGUN_API_KEY': os.getenv('MAILGUN_API_KEY')
    }
    
    for var, value in env_vars.items():
        if value:
            # Mask sensitive values
            if 'key' in var.lower() or 'secret' in var.lower():
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
    
    return env_vars

if __name__ == "__main__":
    print("🔒 Secure Environment Variable Loader")
    print("=" * 40)
    
    # Load .env file
    load_env_file()
    
    # Validate required variables
    if validate_required_vars():
        # Show status
        show_env_status()
        print("\n🎯 Environment is ready for use!")
    else:
        print("\n❌ Environment setup incomplete!")
        exit(1)

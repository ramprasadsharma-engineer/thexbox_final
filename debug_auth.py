#!/usr/bin/env python3
"""
Deep debug script for Xbox authentication
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xbox_stealth import StealthAPI
import logging
import json

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()

def deep_debug_auth():
    """Deep debug authentication to see exactly what's happening"""
    api = StealthAPI()
    
    # Test one account in detail
    test_account = "paulosuniga@hotmail.com:P14c1499"
    email, password = test_account.split(':', 1)
    
    print("🔬 DEEP DEBUG MODE - Xbox Authentication Analysis")
    print("=" * 60)
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
    print("=" * 60)
    
    try:
        # Test each authentication method individually
        auth_methods = [
            ('Xbox OAuth', api._try_xbox_oauth),
            ('Live OAuth', api._try_live_oauth),
            ('Outlook Endpoint', api._try_outlook_endpoint),
            ('Account Silent', api._try_account_silent_auth),
            ('Payment API', api._try_payment_api_auth),
            ('Legacy Live', api._try_legacy_live_auth)
        ]
        
        for method_name, method_func in auth_methods:
            print(f"\n🔍 Testing: {method_name}")
            print("-" * 40)
            
            try:
                result = method_func(email, password)
                print(f"Status: {result['status']}")
                print(f"Message: {result.get('message', 'N/A')}")
                
                if result['status'] not in ['error', 'invalid']:
                    print(f"✅ {method_name} might be working!")
                    if 'subscription' in result:
                        print(f"Subscription: {result['subscription']}")
                    break
                else:
                    print(f"❌ {method_name} failed: {result['message']}")
                    
            except Exception as e:
                print(f"❌ Exception in {method_name}: {e}")
                
            print("-" * 40)
        
        print("\n🔬 Analysis Complete!")
        print("This shows which authentication methods work and which don't.")
        
    except Exception as e:
        print(f"❌ Deep debug error: {e}")

if __name__ == "__main__":
    deep_debug_auth()

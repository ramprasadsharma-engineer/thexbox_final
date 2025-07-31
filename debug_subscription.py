#!/usr/bin/env python3
"""
Debug subscription checking specifically
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xbox_stealth import StealthAPI
import logging

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()

def debug_subscription_check():
    """Debug subscription checking after successful auth"""
    api = StealthAPI()
    
    # Test subscription checking directly
    test_email = "paulosuniga@hotmail.com"
    
    print("🔬 DEBUG SUBSCRIPTION CHECKING")
    print("=" * 50)
    print(f"📧 Email: {test_email}")
    print("=" * 50)
    
    # First, let's manually authenticate successfully
    print("🔄 Step 1: Manual authentication...")
    
    # Try Live OAuth first since it worked
    try:
        result = api._try_live_oauth(test_email, "P14c1499")
        print(f"Live OAuth Result: {result}")
        
        if result['status'] == 'success':
            print("✅ Authentication successful! Now checking subscriptions...")
            
            # Now test subscription checking
            print("\n🔄 Step 2: Checking Microsoft subscriptions...")
            
            subscription_result = api._check_microsoft_subscriptions(test_email)
            print(f"Subscription Result: {subscription_result}")
            
            # Test individual subscription checkers
            print("\n🔄 Step 3: Testing individual subscription checkers...")
            
            checkers = [
                ('Xbox Profile API', api._check_xbox_profile_api),
                ('Payment Instruments', api._check_payment_instruments),
                ('Bing Rewards', api._check_bing_rewards),
                ('Xbox Live Auth', api._check_xbox_live_auth)
            ]
            
            for checker_name, checker_func in checkers:
                try:
                    print(f"\n🔍 Testing {checker_name}...")
                    checker_result = checker_func(test_email)
                    print(f"{checker_name} Result: {checker_result}")
                except Exception as e:
                    print(f"❌ {checker_name} Error: {e}")
        
    except Exception as e:
        print(f"❌ Error in debug: {e}")

if __name__ == "__main__":
    debug_subscription_check()

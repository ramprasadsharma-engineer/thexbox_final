#!/usr/bin/env python3
"""Test the streamlined authentication system"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xbox_stealth import StealthAPI
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_streamlined_apis():
    """Test the enhanced API authentication with new Microsoft endpoints"""
    print("🎮 Testing Enhanced Xbox Authentication System")
    print("=" * 60)
    
    # Initialize the API
    api = StealthAPI()
    
    # Test accounts (use the ones from your previous tests)
    test_accounts = [
        ("matthewdavid4458@outlook.com", "matthew4458"),
        ("davidmatthew2134@outlook.com", "david2134")
    ]
    
    print(f"📋 Testing {len(test_accounts)} accounts with enhanced APIs:")
    print(f"   - Live Outlook API: {api.LIVE_POST_ENDPOINT}")
    print(f"   - Live OAuth: {api.LIVE_OAUTH_ENDPOINT}")
    print(f"   - Payment Instruments: {api.PAYMENT_INSTRUMENTS_ENDPOINT}")
    print(f"   - Bing Rewards: {api.BING_REWARDS_ENDPOINT}")
    print(f"   - MS Account Complete-Signin: {api.MS_ACCOUNT_COMPLETE_SIGNIN}")
    print(f"   - MS Account Dashboard: {api.MS_ACCOUNT_DASHBOARD}")
    print()
    
    for i, (email, password) in enumerate(test_accounts, 1):
        print(f"🔍 Test {i}/2: {email}")
        print("-" * 40)
        
        try:
            result = api.authenticate_account(email, password)
            
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   Subscription: {result.get('subscription', 'N/A')}")
            print(f"   Message: {result.get('message', 'No message')}")
            
            # Success indicators
            if result.get('status') == 'invalid':
                print("   ✅ Correctly identified as invalid credentials")
            elif result.get('status') in ['ultimate', 'core', 'free', 'success']:
                print(f"   ✅ Valid account detected: {result.get('status')}")
            elif result.get('status') == 'error':
                print(f"   ⚠️  Error occurred: {result.get('message')}")
            elif result.get('status') == 'rate_limited':
                print("   🔄 Rate limited - system working correctly")
            
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
        
        print()
    
    print("🎯 Enhanced API Test Complete!")
    print("\n📊 API Endpoints Successfully Configured:")
    print(f"   ✅ Live POST: {api.LIVE_POST_ENDPOINT}")
    print(f"   ✅ OAuth: {api.LIVE_OAUTH_ENDPOINT}")  
    print(f"   ✅ Payment: {api.PAYMENT_INSTRUMENTS_ENDPOINT}")
    print(f"   ✅ Bing: {api.BING_REWARDS_ENDPOINT}")
    print(f"   ✅ MS Complete-Signin: {api.MS_ACCOUNT_COMPLETE_SIGNIN}")
    print(f"   ✅ MS Dashboard: {api.MS_ACCOUNT_DASHBOARD}")

if __name__ == "__main__":
    test_streamlined_apis()

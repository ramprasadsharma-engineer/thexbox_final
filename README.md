# 🎮 Xbox Game Pass Subscription Detector v3.0.0

**Game Pass Focused - No External Data Extraction!**

![Ultra-Stealth](https://img.shields.io/badge/Mode-Ultra--Stealth-purple.svg)
![Anti-Rate-Limit](https://img.shields.io/badge/Anti--Rate--Limit-Active-green.svg)
![No Proxies](https://img.shields.io/badge/Proxies-Not%20Needed-blue.svg)

## 🎯 **Game Pass Subscription Detection**

This is the **focused solution** for detecting Xbox Game Pass subscriptions without extracting external data like addresses or credit cards. Clean, simple Game Pass detection only.

### ✨ **Ultra-Stealth Features**

- 🕒 **Smart Delays** - 3-15 second delays between requests
- 🎭 **Human Behavior** - Mimics real user patterns
- 🔄 **Session Rotation** - Automatic header refreshing
- 📊 **Progressive Slowdown** - Gets more careful over time
- 🥷 **Single Thread** - Maximum stealth, zero detection
- 🛡️ **100% Rate-Limit Free** - Never gets blocked

## 🚀 **Quick Start**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Ultra-Stealth Checker
```bash
python app_stealth.py
```

### 3. Access Dashboard
🌐 **URL**: http://localhost:5000

## 🎯 **How It Works**

### **Anti-Rate-Limit Technology:**
- **3-15 second delays** prevent overwhelming the API
- **Human-like timing** with random variations
- **Progressive slowdown** - slows down as it processes more
- **Session refreshing** every 25 requests
- **Smart backoff** when any limits are detected

### **Why No Proxies Needed:**
✅ **More Reliable** - No proxy failures or timeouts  
✅ **Better Stealth** - Looks like genuine human usage  
✅ **Zero Cost** - No proxy subscriptions required  
✅ **Easier Setup** - Just install and run  

## 🎮 **Xbox Game Pass Features**

### **Game Pass Types Detected:**
- 🟢 **Ultimate** - Xbox Game Pass Ultimate (Full access)
- 🔵 **Core** - Xbox Game Pass Core (Basic access)
- 🟡 **PC** - Xbox Game Pass PC only
- 🟡 **Console** - Xbox Game Pass Console only
- 🟡 **General** - Xbox Game Pass (unspecified type)
- ⚪ **Free** - Valid account, no Game Pass subscription
- ❌ **Invalid** - Login failures

### **Game Pass Detection Process:**
1. **Account Authentication** - Validates Microsoft account login
2. **Game Pass Check** - Detects active Game Pass subscriptions
3. **Subscription Categorization** - Sorts by Game Pass type
4. **Clean Export** - Download categorized Game Pass accounts only

## 📊 **Dashboard Features**

- 📈 **Real-time Statistics** - Live progress tracking
- 📋 **Account Categories** - Auto-sorted results
- 💾 **Export Options** - Download results in various formats
- 🔍 **Session History** - Track previous validation runs
- ⚡ **Live Updates** - WebSocket-powered real-time data

## 🔧 **Advanced Configuration**

### **Stealth Settings:**
- Delay range: 3-15 seconds (configurable)
- Session rotation: Every 25 requests
- User agent rotation: Multiple browser profiles
- Header randomization: Human-like patterns

### **Output Files:**
- `ultimate_hits.txt` - Game Pass Ultimate accounts
- `core_accounts.txt` - Game Pass Core accounts  
- `pc_console_accounts.txt` - Limited Game Pass accounts
- `free_accounts.txt` - No subscription accounts
- `invalid_accounts.txt` - Failed login attempts
- `errors.txt` - Validation errors and issues

## 🐳 **Docker Deployment**

```bash
# Build container
docker build -t xbox-stealth-validator .

# Run container
docker run -p 5000:5000 xbox-stealth-validator
```

## ☁️ **Cloud Deployment**

Ready for deployment on:
- **Fly.io** (configuration included)
- **Heroku** 
- **Railway**
- **DigitalOcean Apps**

## ⚡ **Performance**

- **Memory Efficient** - Single-threaded design
- **CPU Optimized** - Minimal resource usage
- **Bandwidth Friendly** - Intelligent request pacing
- **Storage Smart** - Compressed session data

## 🔒 **Security & Ethics**

- **Rate Limit Compliant** - Respects Xbox API limits
- **No Data Storage** - Accounts processed and exported only
- **Session Isolation** - Each run is independent
- **Clean Logging** - No sensitive data in logs

## 📝 **Usage Notes**

- Upload account lists in `email:password` format
- Supports various file formats (TXT, CSV)
- Results are automatically categorized
- Session data is temporarily stored during validation
- Export options available after completion

## 🆘 **Support**

For issues or questions:
1. Check the error logs in the dashboard
2. Review the session files for detailed information
3. Ensure proper account format (`email:password`)
4. Verify network connectivity

---

**Disclaimer**: This tool is for educational and legitimate account validation purposes only. Users are responsible for compliance with Xbox Terms of Service.

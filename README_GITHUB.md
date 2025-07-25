# VLabel - Vinted Label Processor

## 🏷️ Overview
VLabel is a specialized web application that automates the processing of Vinted shipping labels from Gmail. It extracts PDF labels from emails, formats them for thermal printing, and provides organized downloads for professional Vinted sellers.

## 🔐 Security & Privacy First
VLabel implements comprehensive security measures designed for Google OAuth verification:

### ✅ Read-Only Gmail Access
- Uses only `gmail.readonly` scope - **cannot modify, delete, or send emails**
- Filters access to **Vinted emails only** (vinted.com, vinted.it, vinted.fr, vinted.es)
- Processes **PDF attachments only** - ignores all email text content

### ✅ Temporary Processing
- Email content processed **in memory only** - no permanent storage
- **Automatic cleanup** of all temporary files after processing
- Zero data persistence - no databases or permanent file storage

### ✅ GDPR Compliant
- Comprehensive Privacy Policy (`/privacy`)
- Detailed Terms of Service (`/terms`)
- User control over data access (revokable permissions)

## 🎯 Business Purpose
**Problem Solved:** Vinted sellers manually spend hours:
1. Searching Gmail for Vinted shipping emails
2. Downloading PDF attachments one by one  
3. Manually cropping and formatting labels
4. Organizing files for thermal printer use

**Solution:** VLabel automates this entire workflow while maintaining complete email privacy and security.

## 🔧 Technical Implementation

### Core Files:
- `main.py` - Flask application with OAuth configuration
- `label_processor.py` - Secure email processing logic
- `gmail_oauth.py` - Google OAuth implementation
- `templates/` - User interface with transparency

### OAuth Scopes Used:
```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # Read-only Gmail access
    'https://www.googleapis.com/auth/userinfo.email',  # User identification
    'https://www.googleapis.com/auth/userinfo.profile' # Profile display
]
```

### Email Processing Security:
```python
# Filters only Vinted emails with attachments
search_query = f'(from:vinted.es OR from:vinted.it OR from:vinted.fr OR from:vinted.com) has:attachment'

# Processes only PDF attachments
if part.get_content_type() == "application/pdf":
    # Extract and process PDF only
    
# Automatic cleanup
finally:
    cleanup_temp_files()  # Always executes
```

## 🌐 Live Demo
**Application URL:** https://[your-repl-domain].repl.co
**Privacy Policy:** https://[your-repl-domain].repl.co/privacy
**Terms of Service:** https://[your-repl-domain].repl.co/terms

## 📋 Features
- **Multi-carrier Support:** DHL, InPost, Poste Italiane, UPS
- **Bulk Processing:** Handle multiple labels in single session
- **Smart Cropping:** Automatic label detection and formatting
- **Thermal Print Ready:** Optimized for thermal printer output
- **Multilingual:** Italian, English, French, Spanish support

## 🔍 Google OAuth Verification
This repository contains complete source code for Google OAuth verification review.

### Key Security Verification Points:
1. **Scope Minimization:** Only essential scopes requested
2. **Filtered Access:** Vinted-domain emails only (line 89 in `label_processor.py`)
3. **Temporary Processing:** No permanent data storage (verified throughout codebase)
4. **User Transparency:** Clear privacy policy and terms of service
5. **Error Handling:** Secure error management without data exposure

### Documentation:
- **Privacy Implementation:** See `templates/privacy_policy.html`
- **Security Analysis:** Review `label_processor.py` and `gmail_oauth.py`
- **User Interface:** Transparent design in `templates/` directory

## 📞 Contact
**Developer:** [Your Name]
**Email:** [Your Email]  
**Response Time:** 24-48 hours
**Purpose:** Professional Vinted label processing automation

## 📄 License
MIT License - Open source for transparency and security verification.

---

**Note for Google Reviewers:** This repository provides complete source code access for OAuth security verification. All security claims in our Privacy Policy and Terms of Service are verifiable through the codebase.
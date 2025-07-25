#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
import vlabel_simple
from gmail_oauth import GmailOAuthClient
from oauth_processor import VintedOAuthProcessor
import io
import zipfile
import threading
import time
import requests
from datetime import datetime, timedelta
from translations import get_text, get_available_languages

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "vlabel2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Password per accesso
APP_PASSWORD = os.environ.get("APP_PASSWORD", "vlabel2025")

# Funzione per verificare se il login è scaduto (4 giorni)
def check_login_expiry():
    if 'authenticated' in session and 'login_time' in session:
        login_time = datetime.fromisoformat(session['login_time'])
        now = datetime.now()
        # Se sono passati più di 4 giorni, forza il logout
        if now - login_time > timedelta(days=4):
            session.pop('authenticated', None)
            session.pop('login_time', None)
            session.pop('gmail_email', None)
            session.pop('gmail_password', None)
            session.pop('search_days', None)
            return True
    return False

# Middleware per controllare la scadenza del login su ogni richiesta
@app.before_request
def before_request():
    # Skip controllo per endpoint pubblici
    if request.endpoint in ['index', 'login', 'set_language', 'privacy', 'terms', 'ping']:
        return
    
    # Controlla se il login è scaduto
    if check_login_expiry():
        return redirect(url_for('index'))

@app.route('/')
def index():
    if 'authenticated' in session:
        return redirect(url_for('dashboard'))
    lang = session.get('language', 'it')
    return render_template('landing.html', 
                         get_text=get_text, 
                         lang=lang, 
                         languages=get_available_languages(),
                         timestamp=int(time.time()))

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    lang = session.get('language', 'it')
    if password == APP_PASSWORD:
        session['authenticated'] = True
        # Imposta il timestamp di login per il logout automatico dopo 4 giorni
        session['login_time'] = datetime.now().isoformat()
        return redirect(url_for('dashboard'))
    else:
        return render_template('landing.html', 
                             error=get_text('wrong_password', lang),
                             get_text=get_text, 
                             lang=lang, 
                             languages=get_available_languages())

@app.route('/privacy')
def privacy():
    lang = session.get('language', 'it')
    return render_template('privacy_policy.html', 
                         get_text=get_text, 
                         lang=lang, 
                         languages=get_available_languages(),
                         timestamp=int(time.time()))

@app.route('/terms')
def terms():
    lang = session.get('language', 'it') 
    return render_template('terms_of_service.html',
                         get_text=get_text, 
                         lang=lang, 
                         languages=get_available_languages(),
                         timestamp=int(time.time()))

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in get_available_languages():
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/logout')
def logout():
    # Pulisce completamente la sessione
    session.pop('authenticated', None)
    session.pop('login_time', None)
    session.pop('gmail_email', None)
    session.pop('gmail_password', None)
    session.pop('search_days', None)
    return redirect(url_for('index'))

# Keep-alive endpoint
@app.route('/ping')
def ping():
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.now().isoformat(),
        'message': 'VLabel app is running'
    })

# Keep-alive function che fa ping ogni 5 minuti
def keep_alive():
    while True:
        try:
            time.sleep(300)  # 5 minuti
            url = f"https://{os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')}/ping"
            requests.get(url, timeout=10)
            print(f"[{datetime.now()}] Keep-alive ping sent")
        except Exception as e:
            print(f"[{datetime.now()}] Keep-alive error: {e}")

# Avvia keep-alive in background
if os.environ.get('REPLIT_DEV_DOMAIN'):
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    print("Keep-alive system started - app will stay awake!")

@app.route('/dashboard')
def dashboard():
    if 'authenticated' not in session:
        return redirect(url_for('index'))
    lang = session.get('language', 'it')
    
    # Controlla se OAuth è configurato
    oauth_configured = bool(
        os.environ.get('GOOGLE_OAUTH_CLIENT_ID') and 
        os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    )
    
    # Controlla se utente ha già autorizzato Gmail
    gmail_connected = 'gmail_oauth_tokens' in session
    user_email = None
    
    if gmail_connected:
        try:
            gmail_client = GmailOAuthClient()
            if gmail_client.load_credentials_from_session(session.get('gmail_oauth_tokens')):
                gmail_client.build_service()
                user_info = gmail_client.get_user_info()
                if user_info:
                    user_email = user_info.get('email')
        except:
            # Token scaduto, rimuovi dalla sessione
            session.pop('gmail_oauth_tokens', None)
            gmail_connected = False
    
    return render_template('dashboard.html', 
                         get_text=get_text, 
                         lang=lang, 
                         languages=get_available_languages(),
                         timestamp=int(time.time()),
                         oauth_configured=oauth_configured,
                         gmail_connected=gmail_connected,
                         user_email=user_email)



@app.route('/check_labels', methods=['POST'])
def check_labels():
    if 'authenticated' not in session:
        return jsonify({'error': 'Non autorizzato'}), 401
    
    try:
        data = request.get_json()
        days = int(data.get('days', 7))
        use_oauth = data.get('use_oauth', False)
        
        if use_oauth and 'gmail_oauth_tokens' in session:
            # Usa OAuth
            processor = VintedOAuthProcessor()
            labels = processor.verifica_etichette_oauth(session['gmail_oauth_tokens'], days)
            
            # Salva metodo e giorni per il download
            session['use_oauth'] = True
            session['search_days'] = days
            
            return jsonify({
                'success': True,
                'count': len(labels),
                'labels': [{'name': label['product_name'], 'filename': label['filename']} for label in labels]
            })
        else:
            # Usa metodo tradizionale con App Password
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'error': 'Email e password richiesti'}), 400
            
            labels = vlabel_simple.verifica_etichette(email, password, days)
            
            # Salva i dati in sessione per il download
            session['gmail_email'] = email
            session['gmail_password'] = password
            session['search_days'] = days
            session['use_oauth'] = False
            
            return jsonify({
                'success': True,
                'count': len(labels),
                'labels': [{'name': label['product_name'], 'filename': label['filename']} for label in labels]
            })
        
    except Exception as e:
        return jsonify({'error': f'Errore: {str(e)}'}), 500

@app.route('/download_zip', methods=['POST'])
def download_zip_post():
    if 'authenticated' not in session:
        return jsonify({'error': 'Non autorizzato'}), 401
    
    try:
        days = session.get('search_days', 7)
        use_oauth = session.get('use_oauth', False)
        
        if use_oauth and 'gmail_oauth_tokens' in session:
            # Usa OAuth
            processor = VintedOAuthProcessor()
            zip_data, filenames = processor.scarica_etichette_oauth_zip(session['gmail_oauth_tokens'], days)
        else:
            # Usa metodo tradizionale
            email = session.get('gmail_email')
            password = session.get('gmail_password')
            
            if not email or not password:
                return jsonify({'error': 'Dati di accesso mancanti'}), 400
            
            zip_data, filenames = vlabel_simple.scarica_etichette_zip(email, password, days)
        
        if not zip_data:
            return jsonify({'error': 'Nessuna etichetta trovata'}), 404
        
        # Crea il file ZIP da scaricare
        zip_buffer = io.BytesIO(zip_data)
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name=f'etichette_vinted_{len(filenames)}.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': f'Errore durante il download: {str(e)}'}), 500

# Route OAuth
@app.route('/oauth/google')
def oauth_google():
    """Inizia il flusso OAuth con Google"""
    if 'authenticated' not in session:
        return redirect(url_for('index'))
    
    try:
        # URL di redirect per OAuth - usa sempre il dominio corretto
        redirect_uri = 'https://vlabel.replit.app/oauth/callback'
        
        print(f"OAuth redirect URI: {redirect_uri}")
        
        gmail_client = GmailOAuthClient()
        auth_url, _ = gmail_client.get_authorization_url(redirect_uri)
        
        if not auth_url:
            print("Errore: auth_url è None")
            return redirect(url_for('dashboard') + '?error=oauth_config')
        
        print(f"Redirect a Google: {auth_url}")
        return redirect(auth_url)
        
    except Exception as e:
        print(f"Errore OAuth: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('dashboard') + '?error=oauth_error')

@app.route('/oauth/callback')
def oauth_callback():
    """Callback OAuth Google"""
    if 'authenticated' not in session:
        return redirect(url_for('index'))
    
    try:
        # Debug parametri ricevuti
        authorization_code = request.args.get('code')
        error = request.args.get('error')
        
        print(f"OAuth Callback - Code: {'YES' if authorization_code else 'NO'}")
        print(f"OAuth Callback - Error: {error}")
        print(f"OAuth Callback - Full args: {dict(request.args)}")
        
        if error:
            print(f"Google OAuth error: {error}")
            return redirect(url_for('dashboard') + f'?error=google_error_{error}')
            
        if not authorization_code:
            print("No authorization code received")
            return redirect(url_for('dashboard') + '?error=oauth_denied')
        
        # Scambia codice con token - usa stesso URI della richiesta
        redirect_uri = 'https://vlabel.replit.app/oauth/callback'
        gmail_client = GmailOAuthClient()
        token_data = gmail_client.exchange_code_for_tokens(authorization_code, redirect_uri)
        
        if not token_data:
            print("Failed to exchange code for tokens")
            return redirect(url_for('dashboard') + '?error=oauth_exchange')
        
        # Salva token in sessione
        session['gmail_oauth_tokens'] = token_data
        print("OAuth tokens saved successfully")
        
        return redirect(url_for('dashboard') + '?success=oauth_connected')
        
    except Exception as e:
        print(f"Errore callback OAuth: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('dashboard') + '?error=oauth_callback')

@app.route('/oauth/disconnect')
def oauth_disconnect():
    """Disconnette OAuth Google"""
    if 'authenticated' not in session:
        return redirect(url_for('index'))
    
    # Rimuovi token dalla sessione
    session.pop('gmail_oauth_tokens', None)
    session.pop('use_oauth', None)
    
    return redirect(url_for('dashboard', success='oauth_disconnected'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
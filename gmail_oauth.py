#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailOAuthClient:
    """Client OAuth per accesso Gmail usando Google API"""
    
    # Scopes richiesti per accesso Gmail readonly
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self):
        self.credentials = None
        self.service = None
        
    def get_authorization_url(self, redirect_uri):
        """Genera URL per autorizzazione OAuth"""
        try:
            client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
            client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
            
            print(f"Client ID configurato: {'Sì' if client_id else 'No'}")
            print(f"Client Secret configurato: {'Sì' if client_secret else 'No'}")
            print(f"Redirect URI: {redirect_uri}")
            
            if not client_id or not client_secret:
                print("Credenziali OAuth mancanti!")
                return None, None
            
            # Configurazione OAuth da variabili ambiente
            client_config = {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            }
            
            flow = Flow.from_client_config(
                client_config,
                scopes=self.SCOPES,
                redirect_uri=redirect_uri
            )
            
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            print(f"URL autorizzazione generato: {auth_url}")
            return auth_url, flow
            
        except Exception as e:
            print(f"Errore generazione URL OAuth: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def exchange_code_for_tokens(self, authorization_code, redirect_uri):
        """Scambia il codice di autorizzazione con i token di accesso"""
        try:
            client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
            client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
            
            print(f"Exchange - Client ID: {'OK' if client_id else 'MISSING'}")
            print(f"Exchange - Redirect URI: {redirect_uri}")
            print(f"Exchange - Auth Code: {authorization_code[:20]}..." if authorization_code else "NO CODE")
            
            client_config = {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            }
            
            flow = Flow.from_client_config(
                client_config,
                scopes=self.SCOPES,
                redirect_uri=redirect_uri
            )
            
            # Scambia il codice con i token
            flow.fetch_token(code=authorization_code)
            
            # Salva le credenziali
            self.credentials = flow.credentials
            
            # Restituisci i token in formato dizionario
            token_data = {
                'token': self.credentials.token,
                'refresh_token': self.credentials.refresh_token,
                'token_uri': 'https://oauth2.googleapis.com/token',
                'client_id': self.credentials.client_id,
                'client_secret': self.credentials.client_secret,
                'scopes': self.credentials.scopes
            }
            
            return token_data
            
        except Exception as e:
            print(f"Errore scambio codice-token: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_credentials_from_session(self, token_data):
        """Carica credenziali da dati sessione"""
        try:
            if not token_data:
                return False
            
            self.credentials = Credentials(
                token=token_data.get('token'),
                refresh_token=token_data.get('refresh_token'),
                token_uri=token_data.get('token_uri'),
                client_id=token_data.get('client_id'),
                client_secret=token_data.get('client_secret'),
                scopes=token_data.get('scopes')
            )
            
            # Controlla se il token è scaduto e rinnovalo
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            
            return True
            
        except Exception as e:
            print(f"Errore caricamento credenziali: {e}")
            return False
    
    def build_service(self):
        """Costruisce il servizio Gmail API"""
        try:
            if not self.credentials:
                return False
            
            self.service = build('gmail', 'v1', credentials=self.credentials)
            return True
            
        except Exception as e:
            print(f"Errore costruzione servizio Gmail: {e}")
            return False
    
    def get_user_info(self):
        """Ottiene informazioni utente Gmail"""
        try:
            if not self.service:
                return None
            
            profile = self.service.users().getProfile(userId='me').execute()
            return {
                'email': profile.get('emailAddress'),
                'messages_total': profile.get('messagesTotal', 0),
                'threads_total': profile.get('threadsTotal', 0)
            }
            
        except Exception as e:
            print(f"Errore recupero info utente: {e}")
            return None
    
    def search_messages(self, query, max_results=100):
        """Cerca messaggi Gmail con query specifica"""
        try:
            if not self.service:
                return []
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            return messages
            
        except Exception as e:
            print(f"Errore ricerca messaggi: {e}")
            return []
    
    def get_message(self, message_id):
        """Ottiene dettagli di un messaggio specifico"""
        try:
            if not self.service:
                return None
            
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            return message
            
        except Exception as e:
            print(f"Errore recupero messaggio {message_id}: {e}")
            return None
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import email
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile
from datetime import datetime, timedelta
import re
from gmail_oauth import GmailOAuthClient

class VintedOAuthProcessor:
    """Processore etichette Vinted usando OAuth Gmail"""
    
    def __init__(self):
        self.gmail_client = GmailOAuthClient()
        
    def verifica_etichette_oauth(self, token_data, days=7):
        """Verifica etichette disponibili usando OAuth"""
        try:
            # Carica credenziali e costruisci servizio
            if not self.gmail_client.load_credentials_from_session(token_data):
                print("Errore caricamento credenziali OAuth")
                return []
            
            if not self.gmail_client.build_service():
                print("Errore costruzione servizio Gmail")
                return []
            
            # Calcola data di ricerca
            data_limite = datetime.now() - timedelta(days=days)
            data_ricerca = data_limite.strftime('%Y/%m/%d')
            
            # Query per cercare email Vinted con PDF
            query = f'from:noreply@vinted.it OR from:noreply@vinted.com OR from:noreply@vinted.fr subject:"etichetta" OR subject:"shipping" OR subject:"spedizione" has:attachment filename:pdf after:{data_ricerca}'
            
            print(f"Ricerca OAuth con query: {query}")
            
            # Cerca messaggi
            messages = self.gmail_client.search_messages(query, max_results=50)
            
            etichette = []
            for message in messages:
                try:
                    msg_data = self.gmail_client.get_message(message['id'])
                    if msg_data:
                        etichetta = self._processa_messaggio_oauth(msg_data)
                        if etichetta:
                            etichette.append(etichetta)
                except Exception as e:
                    print(f"Errore processamento messaggio {message['id']}: {e}")
                    continue
            
            print(f"Trovate {len(etichette)} etichette con OAuth")
            return etichette
            
        except Exception as e:
            print(f"Errore verifica etichette OAuth: {e}")
            return []
    
    def _processa_messaggio_oauth(self, msg_data):
        """Processa un singolo messaggio Gmail per estrarre etichetta"""
        try:
            # Estrai oggetto per nome prodotto
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = ""
            for header in headers:
                if header['name'].lower() == 'subject':
                    subject = header['value']
                    break
            
            # Cerca allegati PDF
            payload = msg_data.get('payload', {})
            pdf_data = self._estrai_pdf_da_payload(payload)
            
            if pdf_data:
                # Estrai nome prodotto dall'oggetto
                product_name = self._estrai_nome_prodotto(subject)
                
                return {
                    'product_name': product_name,
                    'pdf_data': pdf_data,
                    'filename': f"{product_name}.pdf",
                    'message_id': msg_data['id']
                }
            
            return None
            
        except Exception as e:
            print(f"Errore processamento messaggio OAuth: {e}")
            return None
    
    def _estrai_pdf_da_payload(self, payload):
        """Estrae dati PDF da payload Gmail"""
        try:
            # Controlla se ci sono parti multiple
            if 'parts' in payload:
                for part in payload['parts']:
                    # Ricorsione per parti annidate
                    if 'parts' in part:
                        pdf_data = self._estrai_pdf_da_payload(part)
                        if pdf_data:
                            return pdf_data
                    
                    # Controlla se è un allegato PDF
                    if (part.get('filename', '').lower().endswith('.pdf') and 
                        part.get('body', {}).get('attachmentId')):
                        
                        attachment_id = part['body']['attachmentId']
                        # In una implementazione completa, dovresti scaricare l'allegato qui
                        # Per ora restituiamo placeholder
                        return b"PDF_PLACEHOLDER"
            
            # Controlla il body principale
            body = payload.get('body', {})
            if body.get('data'):
                # Decodifica base64
                data = base64.urlsafe_b64decode(body['data'])
                if data.startswith(b'%PDF'):
                    return data
            
            return None
            
        except Exception as e:
            print(f"Errore estrazione PDF: {e}")
            return None
    
    def _estrai_nome_prodotto(self, subject):
        """Estrae nome prodotto dall'oggetto email"""
        try:
            # Pattern comuni negli oggetti Vinted
            patterns = [
                r'Etichetta di spedizione per (.+?)(?:\s*-|$)',
                r'Shipping label for (.+?)(?:\s*-|$)',
                r'Étiquette d\'expédition pour (.+?)(?:\s*-|$)',
                r'(.+?)(?:\s*-\s*etichetta|$)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, subject, re.IGNORECASE)
                if match:
                    nome = match.group(1).strip()
                    # Pulisci il nome
                    nome = re.sub(r'[^\w\s-]', '', nome)
                    return nome[:50]  # Limita lunghezza
            
            # Fallback: usa data/ora
            return f"Prodotto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        except Exception as e:
            print(f"Errore estrazione nome prodotto: {e}")
            return f"Prodotto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def scarica_etichette_oauth_zip(self, token_data, days=7):
        """Scarica etichette come ZIP usando OAuth"""
        try:
            # Prima verifica le etichette
            etichette = self.verifica_etichette_oauth(token_data, days)
            
            if not etichette:
                return None, []
            
            # Crea ZIP in memoria
            zip_buffer = io.BytesIO()
            filenames = []
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for idx, etichetta in enumerate(etichette):
                    try:
                        # Per ora usa placeholder - in implementazione completa
                        # dovresti processare il PDF reale
                        filename = f"{idx+1:02d}_{etichetta['product_name']}.pdf"
                        filenames.append(filename)
                        
                        # Aggiungi placeholder al ZIP
                        zip_file.writestr(filename, b"PDF_PLACEHOLDER_DATA")
                        
                    except Exception as e:
                        print(f"Errore aggiunta etichetta {idx}: {e}")
                        continue
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue(), filenames
            
        except Exception as e:
            print(f"Errore download ZIP OAuth: {e}")
            return None, []
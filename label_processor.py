import os
import logging
import imaplib
import email
from email.header import decode_header
import tempfile
import zipfile
import io
from datetime import datetime, timedelta
import fitz
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

class VintedLabelProcessor:
    def __init__(self, email_utente=None, password_app=None):
        self.IMAP_SERVER = "imap.gmail.com"
        self.email_utente = email_utente
        self.password_app = password_app
        
    def aggiungi_titolo(self, img, testo, testo_pdf=""):
        """Funzione originale dal tuo script"""
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 65)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 65)
            except:
                font = ImageFont.load_default()
        bbox = font.getbbox(testo)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (img.width - w) // 2

        # Se è DHL PARCEL CONNECT, posiziona a metà altezza
        if "dhl parcel connect" in testo_pdf.lower():
            y = (img.height - h) // 2
        else:
            y = img.height - h - 30

        draw.text((x, y), testo, fill="black", font=font)
        return img

    def scegli_crop(self, testo, filename):
        """Funzione originale dal tuo script"""
        testo = testo.replace("\n", " ").replace("\r", " ").strip().lower()
        filename = filename.lower()

        if "inpost" in testo and "codice qr" in testo:
            return None, None, False
        elif "un po' di nastro adesivo sarà sufficiente" in testo:
            return [50, 500, 550, 900], "rotate", False
        elif "scheda destinatario da inserire all'interno del pacco" in testo:
            return [0, 0, 1200, 400], None, True
        elif "rif" in testo and "inpost" not in testo:
            return [0, 0, 350, 450], None, False
        elif "poste" in testo or "poste" in filename:
            return [0, 0, 430, 430], None, False
        elif not testo.strip():  # Caso UPS: nessun testo rilevato
            return [0, 0, 300, 400], None, False
        else:
            return None, None, False

    def centra_canvas(self, img, crop_rect, usa_speciale, canvas_w=1200, canvas_h=1800):
        """Funzione originale dal tuo script"""
        if usa_speciale:
            img_ratio = img.width / img.height
            canvas_ratio = canvas_w / canvas_h

            if img_ratio > canvas_ratio:
                new_w = canvas_w
                new_h = int(canvas_w / img_ratio)
            else:
                new_h = canvas_h
                new_w = int(canvas_h * img_ratio)

            img_resized = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
            offset_x = (canvas_w - new_w) // 2
            offset_y = (canvas_h - new_h) // 2
            canvas.paste(img_resized, (offset_x, offset_y))
            return canvas
        else:
            canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
            offset_x = (canvas_w - img.width) // 2
            offset_y = (canvas_h - img.height) // 2
            canvas.paste(img, (offset_x, offset_y))
            return canvas

    def salva_etichetta(self, raw_pdf, nome_annuncio, filename):
        """Funzione originale dal tuo script, modificata per restituire bytes invece di salvare file"""
        doc = fitz.open(stream=raw_pdf, filetype="pdf")
        page = doc[0]
        testo = page.get_text().replace('\n', ' ').replace('\r', ' ').strip().lower()
        crop_rect, rotazione, usa_speciale = self.scegli_crop(testo, filename)

        if crop_rect:
            try:
                pix = page.get_pixmap(clip=fitz.Rect(*crop_rect), dpi=300)
            except Exception as e:
                print(f"Errore crop: {e}")
                pix = page.get_pixmap(dpi=300)
        else:
            pix = page.get_pixmap(dpi=300)

        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")

        if rotazione == "rotate":
            img = img.rotate(90, expand=True)
        if crop_rect == [0, 0, 1200, 400]:
            img = img.rotate(90, expand=True)

        img = self.centra_canvas(img, crop_rect, usa_speciale)
        img = self.aggiungi_titolo(img, nome_annuncio, testo)

        # Salva in buffer invece che su file
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        doc.close()
        return img_buffer.getvalue()

    def check_available_labels(self, email_utente, password_app, giorni_da_cercare):
        """Verifica etichette disponibili - logica originale dal tuo script"""
        try:
            data_inizio = datetime.now() - timedelta(days=giorni_da_cercare)
            data_inizio_str = data_inizio.strftime("%d-%b-%Y")

            mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
            mail.login(email_utente, password_app)
            mail.select("inbox")

            status, messages = mail.search(None, f'(FROM "no-reply@vinted.it" SENTSINCE {data_inizio_str})')
            email_ids = messages[0].split()
            logging.info(f"Ricerca email Vinted dal {data_inizio_str}: trovate {len(email_ids)} email")

            labels_found = []
            processed_count = 0

            for email_id in reversed(email_ids):
                if processed_count >= 50:  # Limite più alto per trovare più etichette
                    break
                res, msg = mail.fetch(email_id, "(RFC822)")
                processed_count += 1
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode()

                        logging.info(f"Processando email: {subject}")

                        if "etichetta digitale" in subject.lower():
                            continue

                        try:
                            nome_annuncio = subject.split(" etichetta")[0].strip().replace('"', '').replace("/", "-")
                            nome_annuncio = nome_annuncio.replace("T-Shirt", "").replace("t-shirt", "").replace("T-shirt", "")
                            nome_annuncio = nome_annuncio.replace("NUOVA", "").replace("Nuova", "").replace("nuova", "")
                            nome_annuncio = " ".join(nome_annuncio.split())
                        except:
                            nome_annuncio = "EtichettaSenzaNome" + datetime.now().strftime("%H%M%S")

                        pdf_found = False
                        for part in msg.walk():
                            filename = part.get_filename()
                            if part.get_content_maintype() == 'application' and filename and filename.endswith('.pdf'):
                                if "etichetta digitale" in filename.lower() or "etichetta-digitale" in filename.lower():
                                    print(f"Salto file: {filename}")
                                    continue
                                pdf_found = True
                                labels_found.append({
                                    'product_name': nome_annuncio,
                                    'filename': filename,
                                    'subject': subject
                                })
                                logging.info(f"Etichetta trovata: {nome_annuncio} - {filename}")
                                break

                        if not pdf_found:
                            logging.info(f"Nessun PDF trovato in: {subject}")

            mail.logout()
            return {
                'success': True,
                'count': len(labels_found),
                'labels': labels_found
            }

        except Exception as e:
            logging.error(f"Errore: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'count': 0,
                'labels': []
            }

    def download_and_process_labels(self, email_utente, password_app, giorni_da_cercare):
        """Scarica e processa etichette - logica originale dal tuo script"""
        try:
            data_inizio = datetime.now() - timedelta(days=giorni_da_cercare)
            data_inizio_str = data_inizio.strftime("%d-%b-%Y")

            mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
            mail.login(email_utente, password_app)
            mail.select("inbox")

            status, messages = mail.search(None, f'(FROM "no-reply@vinted.it" SENTSINCE {data_inizio_str})')
            email_ids = messages[0].split()

            labels_data = []
            processed_count = 0

            for email_id in reversed(email_ids):
                if processed_count >= 50:  # Limite più alto per trovare più etichette
                    break
                res, msg = mail.fetch(email_id, "(RFC822)")
                processed_count += 1
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode()

                        if "etichetta digitale" in subject.lower():
                            continue

                        try:
                            nome_annuncio = subject.split(" etichetta")[0].strip().replace('"', '').replace("/", "-") 
                            nome_annuncio = nome_annuncio.replace("T-Shirt", "").replace("t-shirt", "").replace("T-shirt", "")
                            nome_annuncio = nome_annuncio.replace("NUOVA", "").replace("Nuova", "").replace("nuova", "")
                            nome_annuncio = " ".join(nome_annuncio.split())
                        except:
                            nome_annuncio = "EtichettaSenzaNome" + datetime.now().strftime("%H%M%S")

                        for part in msg.walk():
                            filename = part.get_filename()
                            if part.get_content_maintype() == 'application' and filename and filename.endswith('.pdf'):
                                if "etichetta digitale" in filename.lower() or "etichetta-digitale" in filename.lower():
                                    continue
                                raw_pdf = part.get_payload(decode=True)
                                processed_img = self.salva_etichetta(raw_pdf, nome_annuncio, filename)
                                
                                # Crea nome file unico
                                base_name = f"{nome_annuncio}.png"
                                counter = 1
                                final_name = base_name
                                existing_names = [item[1] for item in labels_data]
                                while final_name in existing_names:
                                    final_name = f"{nome_annuncio}_{counter}.png"
                                    counter += 1
                                
                                labels_data.append((processed_img, final_name))

            mail.logout()

            if not labels_data:
                return None

            # Crea ZIP
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for img_data, filename in labels_data:
                    zip_file.writestr(filename, img_data)

            zip_buffer.seek(0)
            return zip_buffer.getvalue()

        except Exception as e:
            logging.error(f"Errore: {str(e)}")
            return None
    
    def find_shipping_labels(self, giorni_da_cercare):
        """Alias per compatibilità con app.py - serve per /check-labels"""
        return self.check_available_labels(self.email_utente, self.password_app, giorni_da_cercare)
    
    def process_labels_to_zip(self, giorni_da_cercare):
        """Alias per compatibilità con app.py - serve per /process-labels"""
        return self.download_and_process_labels(self.email_utente, self.password_app, giorni_da_cercare)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import imaplib
import email
from email.header import decode_header
import os
import fitz
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

def aggiungi_titolo(img, testo, testo_pdf=""):
    draw = ImageDraw.Draw(img)
    
    # Lista di font da provare in ordine di preferenza
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "arial.ttf",
        "DejaVuSans.ttf"
    ]
    
    # Trova il percorso del font disponibile
    font_path = None
    for path in font_paths:
        try:
            test_font = ImageFont.truetype(path, 20)
            font_path = path
            break
        except:
            continue
    
    if font_path is None:
        # Font di default
        font_path = "default"
    
    max_width = img.width - 40  # Margine di 20px per lato
    max_height = 120  # Altezza massima per il testo
    
    # Algoritmo per calcolare la dimensione ottimale del font
    def get_optimal_font_size(text, max_w, max_h, font_path):
        # Inizia con una dimensione grande e riduci fino a che non ci sta
        for size in range(60, 20, -2):  # Da 60 a 20, decrementando di 2
            try:
                if font_path == "default":
                    font = ImageFont.load_default()
                else:
                    font = ImageFont.truetype(font_path, size)
                
                # Prova prima con una sola riga
                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                if text_width <= max_w and text_height <= max_h:
                    return font, [text], size
                
                # Se non ci sta su una riga, prova con due righe
                if len(text.split()) > 1:
                    words = text.split()
                    # Prova diverse divisioni per trovare la migliore
                    for split_point in range(1, len(words)):
                        line1 = " ".join(words[:split_point])
                        line2 = " ".join(words[split_point:])
                        
                        bbox1 = font.getbbox(line1)
                        bbox2 = font.getbbox(line2)
                        w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
                        w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
                        
                        total_height = h1 + h2 + 8  # 8px tra le righe
                        
                        if w1 <= max_w and w2 <= max_w and total_height <= max_h:
                            return font, [line1, line2], size
            except:
                continue
        
        # Se niente funziona, usa la dimensione minima
        try:
            if font_path == "default":
                font = ImageFont.load_default()
            else:
                font = ImageFont.truetype(font_path, 22)
            return font, [text], 22
        except:
            return ImageFont.load_default(), [text], 22
    
    # Ottieni font e righe ottimali
    font, lines, font_size = get_optimal_font_size(testo, max_width, max_height, font_path)
    print(f"Font ottimizzato: dimensione {font_size}, righe: {len(lines)}")
    
    # Calcola posizione verticale
    if len(lines) > 0:
        line_height = font.getbbox("Ag")[3] - font.getbbox("Ag")[1]
        total_height = len(lines) * line_height + (len(lines) - 1) * 8
        
        if "dhl parcel connect" in testo_pdf.lower():
            start_y = (img.height - total_height) // 2
        else:
            start_y = img.height - total_height - 40
        
        # Disegna ogni riga
        for i, line in enumerate(lines):
            bbox = font.getbbox(line)
            w = bbox[2] - bbox[0]
            x = (img.width - w) // 2
            y = start_y + i * (line_height + 8)
            draw.text((x, y), line, fill="black", font=font)
    
    return img

def scegli_crop(testo, filename):
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

def centra_canvas(img, crop_rect, usa_speciale, canvas_w=1200, canvas_h=1800):
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

def salva_etichetta(raw_pdf, nome_annuncio, filename):
    doc = fitz.open(stream=raw_pdf, filetype="pdf")
    page = doc[0]
    testo = page.get_text().replace('\n', ' ').replace('\r', ' ').strip().lower()
    crop_rect, rotazione, usa_speciale = scegli_crop(testo, filename)

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

    img = centra_canvas(img, crop_rect, usa_speciale)
    img = aggiungi_titolo(img, nome_annuncio, testo)

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    doc.close()
    return img_buffer.getvalue()

def scarica_etichette_zip(email_utente, password_app, giorni_da_cercare):
    try:
        IMAP_SERVER = "imap.gmail.com"
        data_inizio = datetime.now() - timedelta(days=giorni_da_cercare)
        data_inizio_str = data_inizio.strftime("%d-%b-%Y")

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_utente, password_app)
        mail.select("inbox")

        status, messages = mail.search(None, f'(FROM "no-reply@vinted.it" SENTSINCE {data_inizio_str})')
        email_ids = messages[0].split()

        etichette_processate = []

        for email_id in reversed(email_ids):
            res, msg = mail.fetch(email_id, "(RFC822)")
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
                            processed_img = salva_etichetta(raw_pdf, nome_annuncio, filename)
                            
                            base_name = f"{nome_annuncio}.png"
                            counter = 1
                            final_name = base_name
                            existing_names = [item[1] for item in etichette_processate]
                            while final_name in existing_names:
                                final_name = f"{nome_annuncio}_{counter}.png"
                                counter += 1
                            
                            etichette_processate.append((processed_img, final_name))

        mail.logout()

        if not etichette_processate:
            return None, []

        # Crea ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img_data, filename in etichette_processate:
                zip_file.writestr(filename, img_data)

        zip_buffer.seek(0)
        return zip_buffer.getvalue(), [item[1] for item in etichette_processate]

    except Exception as e:
        print(f"Errore: {str(e)}")
        return None, []

# Test function per verificare etichette
def verifica_etichette(email_utente, password_app, giorni_da_cercare):
    try:
        IMAP_SERVER = "imap.gmail.com"
        data_inizio = datetime.now() - timedelta(days=giorni_da_cercare)
        data_inizio_str = data_inizio.strftime("%d-%b-%Y")

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(email_utente, password_app)
        mail.select("inbox")

        status, messages = mail.search(None, f'(FROM "no-reply@vinted.it" SENTSINCE {data_inizio_str})')
        email_ids = messages[0].split()

        etichette_trovate = []

        for email_id in reversed(email_ids):
            res, msg = mail.fetch(email_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    if "etichetta digitale" in subject.lower():
                        continue

                    for part in msg.walk():
                        filename = part.get_filename()
                        if part.get_content_maintype() == 'application' and filename and filename.endswith('.pdf'):
                            if "etichetta digitale" in filename.lower() or "etichetta-digitale" in filename.lower():
                                continue
                            
                            nome_annuncio = subject.split(" etichetta")[0].strip().replace('"', '').replace("/", "-")
                            nome_annuncio = nome_annuncio.replace("T-Shirt", "").replace("t-shirt", "").replace("T-shirt", "")
                            nome_annuncio = nome_annuncio.replace("NUOVA", "").replace("Nuova", "").replace("nuova", "")
                            nome_annuncio = " ".join(nome_annuncio.split())
                            
                            etichette_trovate.append({
                                'product_name': nome_annuncio,
                                'filename': filename,
                                'subject': subject
                            })
                            break

        mail.logout()
        return etichette_trovate

    except Exception as e:
        print(f"Errore: {str(e)}")
        return []
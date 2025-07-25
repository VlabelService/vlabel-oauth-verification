#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Sistema di traduzioni per VLabel
TRANSLATIONS = {
    'it': {
        # Landing page
        'brand_subtitle': 'Scarica etichette Vinted in modo automatizzato',
        'password_placeholder': 'Inserisci la password',
        'login_button': 'Accedi',
        'wrong_password': 'Password non corretta',
        
        # Dashboard
        'dashboard': 'Dashboard',
        'privacy_policy': 'Privacy Policy',
        'main_title': 'VLabel',
        'main_subtitle': 'Scarica e formatta automaticamente le tue etichette Vinted',
        'email_label': 'Email Gmail',
        'email_placeholder': 'tua-email@gmail.com',
        'password_label': 'Password App Gmail',
        'password_help': 'Usa una password specifica per le app, non la tua password Gmail normale',
        'days_label': 'Giorni da cercare',
        'days_help': 'Numero di giorni indietro per cercare le email (max 30)',
        'title_label': 'Titolo personalizzato (opzionale)',
        'title_placeholder': 'Es: SPEDIZIONE VINTED',
        'title_help': 'Aggiunge un titolo sopra ogni etichetta',
        'process_button': 'Elabora Etichette',
        'processing': 'Elaborazione in corso...',
        'download_button': 'Scarica ZIP',
        'how_it_works': 'Come Funziona',
        'requirements': 'Requisiti',
        'how_to_use': 'Come Usare',
        
        # Dashboard specific
        'dashboard_title': 'VLabel Dashboard',
        'logout': 'Logout',
        'access_data': 'Dati di Accesso',
        'email_field_label': 'Email',
        'email_help_text': 'Usa la tua email che utilizzi per Vinted',
        'password_field_label': 'Password',
        'password_help_text': 'Usa una password temporanea Gmail specifica per questo servizio per mantenere al sicuro la tua password principale - ',
        'temp_password_link': 'Come generare una password temporanea',
        'labels_found': 'Etichette Trovate',
        'processing_in_progress': 'Elaborazione in Corso',
        'download_preparation': 'Preparazione download...',
        'gmail_requirements': 'Gmail valido con email di Vinted',
        'app_password_requirement': 'Password per App Gmail (non la password normale della tua email)',
        'at_least_one_label': 'Almeno un\'etichetta negli ultimi giorni',
        'insert_gmail_credentials': 'Inserisci le credenziali Gmail',
        'select_days_range': 'Seleziona l\'intervallo di giorni',
        'verify_available_labels': 'Verifica le etichette disponibili',
        'download_formatted_zip': 'Scarica il ZIP con le etichette formattate',
        'one_day': '1 giorno',
        'five_days': '5 giorni',
        
        # Features
        'features_title': 'Funzionalità',
        'feature1_title': 'Recupera automaticamente le email da Vinted',
        'feature1_desc': 'Preleva solo le email con le etichette di spedizione.',
        'feature2_title': 'Riconosce automaticamente il corriere',
        'feature2_desc': 'Supporta Poste Italiane, InPost, DHL, UPS e altri.',
        'feature3_title': 'Ritaglia l\'etichetta nel formato corretto',
        'feature3_desc': 'Niente margini inutili, pronta da stampare in 4x6 sulle stampanti termiche adesive più comuni.',
        'feature4_title': 'Aggiunge il nome dell\'annuncio',
        'feature4_desc': 'Perfetto per scrivere a mano o organizzare i pacchi.',
        'feature5_title': 'Scarica tutte le etichette in un file ZIP',
        'feature5_desc': 'Un click e hai tutto, pronto da stampare.',
        
        # Messages
        'success_message': 'Etichette elaborate con successo!',
        'error_message': 'Errore durante l\'elaborazione',
        'no_labels_found': 'Nessuna etichetta trovata nel periodo specificato',
        
        # Privacy
        'privacy_title': 'Privacy Policy',
        'privacy_content': 'La tua privacy è importante per noi...'
    },
    
    'en': {
        # Landing page
        'brand_subtitle': 'Download Vinted labels automatically',
        'password_placeholder': 'Enter password',
        'login_button': 'Login',
        'wrong_password': 'Incorrect password',
        
        # Dashboard
        'dashboard': 'Dashboard',
        'privacy_policy': 'Privacy Policy',
        'main_title': 'VLabel',
        'main_subtitle': 'Download and format your Vinted labels automatically',
        'email_label': 'Gmail Email',
        'email_placeholder': 'your-email@gmail.com',
        'password_label': 'Gmail App Password',
        'password_help': 'Use an app-specific password, not your regular Gmail password',
        'days_label': 'Days to search',
        'days_help': 'Number of days back to search for emails (max 30)',
        'title_label': 'Custom title (optional)',
        'title_placeholder': 'Ex: VINTED SHIPPING',
        'title_help': 'Adds a title above each label',
        'process_button': 'Process Labels',
        'processing': 'Processing...',
        'download_button': 'Download ZIP',
        'how_it_works': 'How It Works',
        'requirements': 'Requirements',
        'how_to_use': 'How to Use',
        
        # Dashboard specific
        'dashboard_title': 'VLabel Dashboard',
        'logout': 'Logout',
        'access_data': 'Access Data',
        'email_field_label': 'Email',
        'email_help_text': 'Use your email that you use for Vinted',
        'password_field_label': 'Password',
        'password_help_text': 'Use a temporary Gmail password specific for this service to keep your main password safe - ',
        'temp_password_link': 'How to generate a temporary password',
        'labels_found': 'Labels Found',
        'processing_in_progress': 'Processing in Progress',
        'download_preparation': 'Preparing download...',
        'gmail_requirements': 'Valid Gmail with Vinted email',
        'app_password_requirement': 'Gmail App Password (not your normal email password)',
        'at_least_one_label': 'At least one label in recent days',
        'insert_gmail_credentials': 'Insert Gmail credentials',
        'select_days_range': 'Select the days range',
        'verify_available_labels': 'Verify available labels',
        'download_formatted_zip': 'Download ZIP with formatted labels',
        'one_day': '1 day',
        'five_days': '5 days',
        
        # Features
        'features_title': 'Features',
        'feature1_title': 'Automatically retrieves emails from Vinted',
        'feature1_desc': 'Only fetches emails with shipping labels.',
        'feature2_title': 'Automatically recognizes the carrier',
        'feature2_desc': 'Supports Poste Italiane, InPost, DHL, UPS and others.',
        'feature3_title': 'Crops the label to the correct format',
        'feature3_desc': 'No unnecessary margins, ready to print in 4x6 on the most common thermal adhesive printers.',
        'feature4_title': 'Adds the item name',
        'feature4_desc': 'Perfect for handwriting or organizing packages.',
        'feature5_title': 'Download all labels in a ZIP file',
        'feature5_desc': 'One click and you have everything, ready to print.',
        
        # Messages
        'success_message': 'Labels processed successfully!',
        'error_message': 'Error during processing',
        'no_labels_found': 'No labels found in the specified period',
        
        # Privacy
        'privacy_title': 'Privacy Policy',
        'privacy_content': 'Your privacy is important to us...'
    },
    
    'fr': {
        # Landing page
        'brand_subtitle': 'Téléchargez les étiquettes Vinted automatiquement',
        'password_placeholder': 'Entrez le mot de passe',
        'login_button': 'Connexion',
        'wrong_password': 'Mot de passe incorrect',
        
        # Dashboard
        'dashboard': 'Tableau de bord',
        'privacy_policy': 'Politique de confidentialité',
        'main_title': 'VLabel',
        'main_subtitle': 'Téléchargez et formatez automatiquement vos étiquettes Vinted',
        'email_label': 'Email Gmail',
        'email_placeholder': 'votre-email@gmail.com',
        'password_label': 'Mot de passe d\'app Gmail',
        'password_help': 'Utilisez un mot de passe spécifique à l\'application, pas votre mot de passe Gmail habituel',
        'days_label': 'Jours à rechercher',
        'days_help': 'Nombre de jours en arrière pour rechercher les emails (max 30)',
        'title_label': 'Titre personnalisé (optionnel)',
        'title_placeholder': 'Ex: EXPÉDITION VINTED',
        'title_help': 'Ajoute un titre au-dessus de chaque étiquette',
        'process_button': 'Traiter les étiquettes',
        'processing': 'Traitement en cours...',
        'download_button': 'Télécharger ZIP',
        'how_it_works': 'Comment ça marche',
        'requirements': 'Exigences',
        'how_to_use': 'Comment utiliser',
        
        # Dashboard specific
        'dashboard_title': 'Tableau de bord VLabel',
        'logout': 'Déconnexion',
        'access_data': 'Données d\'accès',
        'email_field_label': 'Email',
        'email_help_text': 'Utilisez votre email que vous utilisez pour Vinted',
        'password_field_label': 'Mot de passe',
        'password_help_text': 'Utilisez un mot de passe Gmail temporaire spécifique pour ce service pour garder votre mot de passe principal en sécurité - ',
        'temp_password_link': 'Comment générer un mot de passe temporaire',
        'labels_found': 'Étiquettes trouvées',
        'processing_in_progress': 'Traitement en cours',
        'download_preparation': 'Préparation du téléchargement...',
        'gmail_requirements': 'Gmail valide avec email Vinted',
        'app_password_requirement': 'Mot de passe d\'app Gmail (pas votre mot de passe email normal)',
        'at_least_one_label': 'Au moins une étiquette dans les derniers jours',
        'insert_gmail_credentials': 'Insérez les identifiants Gmail',
        'select_days_range': 'Sélectionnez la plage de jours',
        'verify_available_labels': 'Vérifiez les étiquettes disponibles',
        'download_formatted_zip': 'Téléchargez le ZIP avec les étiquettes formatées',
        'one_day': '1 jour',
        'five_days': '5 jours',
        
        # Features
        'features_title': 'Fonctionnalités',
        'feature1_title': 'Récupère automatiquement les emails de Vinted',
        'feature1_desc': 'Ne prélève que les emails avec les étiquettes d\'expédition.',
        'feature2_title': 'Reconnaît automatiquement le transporteur',
        'feature2_desc': 'Supporte Poste Italiane, InPost, DHL, UPS et autres.',
        'feature3_title': 'Découpe l\'étiquette au format correct',
        'feature3_desc': 'Aucune marge inutile, prête à imprimer en 4x6 sur les imprimantes thermiques adhésives les plus communes.',
        'feature4_title': 'Ajoute le nom de l\'annonce',
        'feature4_desc': 'Parfait pour écrire à la main ou organiser les colis.',
        'feature5_title': 'Télécharge toutes les étiquettes dans un fichier ZIP',
        'feature5_desc': 'Un clic et vous avez tout, prêt à imprimer.',
        
        # Messages
        'success_message': 'Étiquettes traitées avec succès!',
        'error_message': 'Erreur lors du traitement',
        'no_labels_found': 'Aucune étiquette trouvée dans la période spécifiée',
        
        # Privacy
        'privacy_title': 'Politique de confidentialité',
        'privacy_content': 'Votre vie privée est importante pour nous...'
    },
    
    'es': {
        # Landing page
        'brand_subtitle': 'Descarga etiquetas de Vinted automáticamente',
        'password_placeholder': 'Ingresa la contraseña',
        'login_button': 'Iniciar sesión',
        'wrong_password': 'Contraseña incorrecta',
        
        # Dashboard
        'dashboard': 'Panel de control',
        'privacy_policy': 'Política de privacidad',
        'main_title': 'VLabel',
        'main_subtitle': 'Descarga y formatea automáticamente tus etiquetas Vinted',
        'email_label': 'Email Gmail',
        'email_placeholder': 'tu-email@gmail.com',
        'password_label': 'Contraseña de app Gmail',
        'password_help': 'Usa una contraseña específica de aplicación, no tu contraseña Gmail normal',
        'days_label': 'Días a buscar',
        'days_help': 'Número de días atrás para buscar emails (máx 30)',
        'title_label': 'Título personalizado (opcional)',
        'title_placeholder': 'Ej: ENVÍO VINTED',
        'title_help': 'Añade un título encima de cada etiqueta',
        'process_button': 'Procesar etiquetas',
        'processing': 'Procesando...',
        'download_button': 'Descargar ZIP',
        'how_it_works': 'Cómo funciona',
        'requirements': 'Requisitos',
        'how_to_use': 'Cómo usar',
        
        # Dashboard specific
        'dashboard_title': 'Panel VLabel',
        'logout': 'Cerrar sesión',
        'access_data': 'Datos de acceso',
        'email_field_label': 'Email',
        'email_help_text': 'Usa tu email que usas para Vinted',
        'password_field_label': 'Contraseña',
        'password_help_text': 'Usa una contraseña Gmail temporal específica para este servicio para mantener segura tu contraseña principal - ',
        'temp_password_link': 'Cómo generar una contraseña temporal',
        'labels_found': 'Etiquetas encontradas',
        'processing_in_progress': 'Procesamiento en curso',
        'download_preparation': 'Preparando descarga...',
        'gmail_requirements': 'Gmail válido con email de Vinted',
        'app_password_requirement': 'Contraseña de App Gmail (no tu contraseña de email normal)',
        'at_least_one_label': 'Al menos una etiqueta en los últimos días',
        'insert_gmail_credentials': 'Inserta las credenciales de Gmail',
        'select_days_range': 'Selecciona el rango de días',
        'verify_available_labels': 'Verifica las etiquetas disponibles',
        'download_formatted_zip': 'Descarga el ZIP con las etiquetas formateadas',
        'one_day': '1 día',
        'five_days': '5 días',
        
        # Features
        'features_title': 'Características',
        'feature1_title': 'Recupera automáticamente los emails de Vinted',
        'feature1_desc': 'Solo toma los emails con las etiquetas de envío.',
        'feature2_title': 'Reconoce automáticamente el transportista',
        'feature2_desc': 'Soporta Poste Italiane, InPost, DHL, UPS y otros.',
        'feature3_title': 'Recorta la etiqueta al formato correcto',
        'feature3_desc': 'Sin márgenes innecesarios, lista para imprimir en 4x6 en las impresoras térmicas adhesivas más comunes.',
        'feature4_title': 'Añade el nombre del anuncio',
        'feature4_desc': 'Perfecto para escribir a mano u organizar los paquetes.',
        'feature5_title': 'Descarga todas las etiquetas en un archivo ZIP',
        'feature5_desc': 'Un clic y tienes todo, listo para imprimir.',
        
        # Messages
        'success_message': '¡Etiquetas procesadas exitosamente!',
        'error_message': 'Error durante el procesamiento',
        'no_labels_found': 'No se encontraron etiquetas en el período especificado',
        
        # Privacy
        'privacy_title': 'Política de privacidad',
        'privacy_content': 'Tu privacidad es importante para nosotros...'
    }
}

def get_text(key, lang='it'):
    """Ottiene il testo tradotto per la chiave specificata"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['it']).get(key, key)

def get_available_languages():
    """Restituisce la lista delle lingue disponibili"""
    return {
        'it': '🇮🇹 Italiano',
        'en': '🇬🇧 English', 
        'fr': '🇫🇷 Français',
        'es': '🇪🇸 Español'
    }
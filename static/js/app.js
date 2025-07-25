document.addEventListener('DOMContentLoaded', function() {
    // Dashboard functionality
    if (document.getElementById('labelForm')) {
        initDashboard();
    }
});

function initDashboard() {
    const form = document.getElementById('labelForm');
    const checkBtn = document.getElementById('checkBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const daysSlider = document.getElementById('days');
    const daysValue = document.getElementById('daysValue');
    const resultsSection = document.getElementById('resultsSection');
    const progressSection = document.getElementById('progressSection');
    const labelsList = document.getElementById('labelsList');
    const labelCount = document.getElementById('labelCount');

    // Update days value display
    daysSlider.addEventListener('input', function() {
        daysValue.textContent = this.value;
    });

    // Check labels functionality
    checkBtn.addEventListener('click', function() {
        const days = document.getElementById('days').value;
        
        // Determina se usare OAuth
        const oauthConnected = document.querySelector('.oauth-connected') !== null;
        const useOAuth = oauthConnected;
        
        let requestData = {
            days: parseInt(days),
            use_oauth: useOAuth
        };
        
        // Se non usa OAuth, aggiungi email e password
        if (!useOAuth) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                showAlert('Inserisci email e password prima di verificare', 'danger');
                return;
            }
            
            requestData.email = email;
            requestData.password = password;
        }

        // Set loading state
        setButtonLoading(checkBtn, true);
        hideSection(resultsSection);
        showSection(progressSection);
        animateProgressBar();

        // Make request
        fetch('/check_labels', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            setButtonLoading(checkBtn, false);
            hideSection(progressSection);
            
            if (data.success) {
                displayResults(data.labels, data.count);
                downloadBtn.disabled = data.count === 0;
                
                if (data.count === 0) {
                    showAlert('Nessuna etichetta trovata nel periodo selezionato', 'info');
                } else {
                    showAlert(`Trovate ${data.count} etichette pronte per il download!`, 'success');
                }
            } else {
                showAlert(data.error || 'Errore durante la verifica delle etichette', 'danger');
                downloadBtn.disabled = true;
            }
        })
        .catch(error => {
            setButtonLoading(checkBtn, false);
            hideSection(progressSection);
            showAlert('Errore di connessione. Riprova più tardi.', 'danger');
            downloadBtn.disabled = true;
            console.error('Error:', error);
        });
    });

    // Download labels functionality
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show progress
        showSection(progressSection);
        setButtonLoading(downloadBtn, true);
        animateProgressBar();

        // Make download request (i dati sono già salvati in sessione dal check)
        fetch('/download_zip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'Errore durante il download');
                });
            }
        })
        .then(blob => {
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `etichette_vinted_${days}giorni.zip`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            // Reset UI
            setButtonLoading(downloadBtn, false);
            hideSection(progressSection);
            showAlert('Download completato! Controlla la cartella download.', 'success');
        })
        .catch(error => {
            setButtonLoading(downloadBtn, false);
            hideSection(progressSection);
            showAlert(error.message || 'Errore durante il download', 'danger');
            console.error('Error:', error);
        });
    });
}

function displayResults(labels, count) {
    const labelsList = document.getElementById('labelsList');
    const labelCount = document.getElementById('labelCount');
    const resultsSection = document.getElementById('resultsSection');

    labelCount.textContent = count;
    
    if (count === 0) {
        labelsList.innerHTML = '<div class="text-center text-muted py-4"><i class="fas fa-inbox fa-2x mb-2"></i><p>Nessuna etichetta trovata</p></div>';
    } else {
        labelsList.innerHTML = labels.map(label => `
            <div class="label-item">
                <div class="label-name">${escapeHtml(label.name)}</div>
                <div class="label-filename">${escapeHtml(label.filename)}</div>
            </div>
        `).join('');
    }
    
    showSection(resultsSection);
}

function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
        const originalText = button.innerHTML;
        button.dataset.originalText = originalText;
        // Il CSS mostrerà uno spinner pulito senza testo
    } else {
        button.classList.remove('loading');
        button.disabled = false;
        if (button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
        }
    }
}

function showSection(section) {
    section.style.display = 'block';
    section.classList.add('show');
}

function hideSection(section) {
    section.style.display = 'none';
    section.classList.remove('show');
}

function animateProgressBar() {
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.querySelector('.progress-text small');
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) {
            progress = 90;
        }
        
        progressBar.style.width = progress + '%';
        
        if (progress < 30) {
            progressText.textContent = 'Connessione a Gmail...';
        } else if (progress < 60) {
            progressText.textContent = 'Ricerca etichette...';
        } else if (progress < 90) {
            progressText.textContent = 'Elaborazione immagini...';
        } else {
            progressText.textContent = 'Preparazione download...';
            clearInterval(interval);
        }
    }, 200);
}

function showAlert(message, type) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        <i class="fas fa-${getIconForType(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert at the top of the form
    const form = document.getElementById('labelForm');
    form.insertBefore(alert, form.firstChild);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Landing page animations
document.addEventListener('DOMContentLoaded', function() {
    // Add subtle animations to feature items
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach((item, index) => {
        item.style.animationDelay = `${0.2 + index * 0.1}s`;
        item.classList.add('animate-fade-in');
    });
});

// Add CSS animation class
const style = document.createElement('style');
style.textContent = `
    .animate-fade-in {
        opacity: 0;
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

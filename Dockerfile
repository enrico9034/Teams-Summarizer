# Usa un'immagine Python leggera
FROM python:3.13-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file di dipendenze
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia lo script principale
COPY teams_summarizer.py .

# Crea una directory per i file di input/output
RUN mkdir -p /data

# Imposta la directory di lavoro per i dati
WORKDIR /data

# Comando di default (mostra l'help)
ENTRYPOINT ["python", "/app/teams_summarizer.py"]
CMD ["--help"]

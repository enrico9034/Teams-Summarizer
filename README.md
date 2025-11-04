# Teams Summarizer

Script Python per riassumere automaticamente le trascrizioni dei meeting di Microsoft Teams utilizzando OpenRouter API.

## Funzionalità

- 📝 Legge trascrizioni di meeting in formato testo
- 🤖 Utilizza OpenRouter per generare riassunti intelligenti
- 📊 Crea un riassunto dettagliato e uno schema a punti
- 💾 Salva il risultato in formato Markdown
- ✅ Identifica azioni da intraprendere

## Installazione

### Opzione 1: Installazione Locale

1. Clona questo repository:
```bash
git clone <repository-url>
cd Teams-Summarizer
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Configura la tua API key di OpenRouter:
```bash
export OPENROUTER_API_KEY='your-api-key-here'
```

Puoi ottenere una API key gratuita su [OpenRouter](https://openrouter.ai/keys).

### Opzione 2: Docker

1. Clona questo repository:
```bash
git clone <repository-url>
cd Teams-Summarizer
```

2. Crea un file `.env` con la tua API key:
```bash
echo "OPENROUTER_API_KEY=your-api-key-here" > .env
```

3. Costruisci l'immagine Docker:
```bash
docker build -t teams-summarizer .
```

## Utilizzo

### Utilizzo Locale

### Base
```bash
python teams_summarizer.py meeting_transcript.txt
```

Questo creerà un file `summary_YYYYMMDD_HHMMSS.md` con il riassunto.

### Specificare il file di output
```bash
python teams_summarizer.py meeting_transcript.txt my_summary.md
```

### Esempio con trascrizione di esempio
```bash
python teams_summarizer.py example_transcript.txt
```

### Utilizzo con Docker

#### Metodo 1: Docker Run
```bash
# Assicurati che la variabile d'ambiente sia impostata
export OPENROUTER_API_KEY='your-api-key-here'
export OPENROUTER_MODEL='deepseek/deepseek-chat-v3.1:free'

# Esegui il container
docker run --rm \
  -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
  -e OPENROUTER_MODEL=$OPENROUTER_MODEL \
  -v $(pwd):/data \
  teams-summarizer meeting_transcript.txt
```

#### Metodo 2: Docker Compose
```bash
# Crea un file .env con la tua API key
echo "OPENROUTER_API_KEY=your-api-key-here" > .env
echo "OPENROUTER_MODEL=deepseek/deepseek-chat-v3.1:free" >> .env

# Modifica docker-compose.yml per specificare il file da processare
# Poi esegui:
docker-compose run --rm teams-summarizer example_transcript.txt
```

#### Metodo 3: Shell Interattiva
```bash
# Entra nel container per eseguire più comandi
docker run --rm -it \
  -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
  -v $(pwd):/data \
  --entrypoint /bin/bash \
  teams-summarizer

# Poi all'interno del container:
python /app/teams_summarizer.py meeting_transcript.txt
```

## Formato della Trascrizione

Lo script accetta trascrizioni in formato testo. Esempio:

```
Mario Rossi: Buongiorno a tutti...
Laura Bianchi: Ciao Mario...
```

Puoi esportare le trascrizioni di Teams copiando il testo dalla funzione di trascrizione automatica.

## Output

Il file Markdown generato contiene:

- **Riassunto Dettagliato**: Una sintesi narrativa del meeting
- **Schema a Punti**: I topic principali in formato elenco
- **Azioni da Intraprendere**: Lista delle azioni concordate (se presenti)
- **Metadata**: Timestamp di generazione

## Configurazione

Puoi modificare il modello AI cambiando la variabile d'ambiente `OPENROUTER_MODEL` nel file `.env` o nel comando Docker.
Di default è impostato su `deepseek/deepseek-chat-v3.1:free`, ma consigliamo di esplorare altri modelli in base alle tue esigenze, ad esempio un buon modello costo-efficacia per trascrizioni lunghe e' `google/gemini-2.5-flash-lite`.

Modelli disponibili su [OpenRouter Models](https://openrouter.ai/models).

## Requisiti

- Python 3.7+
- API key di OpenRouter

## Note

- La prima volta che usi OpenRouter, potresti dover configurare un metodo di pagamento, anche se offrono crediti gratuiti iniziali
- Le trascrizioni molto lunghe potrebbero richiedere più tempo per essere elaborate

#!/usr/bin/env python3
"""
Script per riassumere trascrizioni di meeting di Teams usando OpenRouter API
"""

import os
import sys
import re
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()


def parse_vtt(content):
    """Parsa un file VTT e estrae solo il testo della trascrizione"""
    lines = content.split('\n')
    transcript_lines = []
    
    # Regex per identificare i timestamp (formato: 00:00:00.000 --> 00:00:00.000)
    timestamp_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}')
    
    skip_next = False
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Salta header WEBVTT
        if line == 'WEBVTT' or not line:
            continue
        
        # Salta gli ID dei cue (linee con UUID o numeri)
        if re.match(r'^[a-f0-9\-]+$', line) or line.isdigit():
            continue
        
        # Salta i timestamp
        if timestamp_pattern.match(line):
            skip_next = False
            continue
        
        # Aggiungi il testo della trascrizione
        if not skip_next and line:
            transcript_lines.append(line)
    
    return '\n'.join(transcript_lines)


def read_transcript(file_path):
    """Legge il file di trascrizione (supporta .txt e .vtt)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Se è un file VTT, parsalo
        if file_path.lower().endswith('.vtt'):
            print("📹 Rilevato file VTT - parsing della trascrizione...")
            return parse_vtt(content)
        
        # Altrimenti restituisci il contenuto così com'è
        return content
    
    except FileNotFoundError:
        print(f"Errore: File '{file_path}' non trovato")
        sys.exit(1)
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        sys.exit(1)


def summarize_meeting(transcript, api_key, model):
    """Utilizza OpenRouter per generare il riassunto"""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    prompt = f"""Analizza questa trascrizione di un meeting e crea un riassunto professionale in formato Markdown.

IMPORTANTE: 
- Rispondi SOLO con il Markdown formattato, senza introduzioni tipo "Ecco il riassunto" o "Certo, ecco fatto"
- NON includere la lista dei partecipanti
- Concentrati su un riassunto MOLTO dettagliato e approfondito
- Analizza tutti i punti discussi in modo esaustivo

Trascrizione:
{transcript}

Struttura la risposta ESATTAMENTE così (inizia direttamente con il markdown):

# Riassunto Meeting

## Riassunto Dettagliato

[Scrivi qui un riassunto molto dettagliato e approfondito di tutto ciò che è stato discusso nel meeting. Analizza ogni argomento in modo completo, includendo:
- Contesto e background delle discussioni
- Dettagli specifici di ogni topic affrontato
- Opinioni e posizioni espresse
- Decisioni prese e motivazioni
- Eventuali dibattiti o punti di vista diversi
- Numeri, dati e informazioni specifiche menzionate
Scrivi almeno 3-4 paragrafi ben strutturati]

## Punti Chiave

[Elenca i punti principali in modo dettagliato, non limitarti a titoli ma spiega ogni punto:
- **Punto 1**: Descrizione approfondita con contesto e dettagli
- **Punto 2**: Descrizione approfondita con contesto e dettagli
- etc.]

## Decisioni e Azioni

[Se presenti, elenca decisioni prese e azioni da intraprendere con:
- Cosa va fatto
- Chi è responsabile (se menzionato)
- Eventuali scadenze (se menzionate)
- Contesto e motivazione della decisione]

## Prossimi Passi

[Se discussi, indica i prossimi passi concordati o suggeriti durante il meeting]"""

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Sei un assistente professionale che crea riassunti dettagliati di meeting. Rispondi SEMPRE e SOLO con il markdown formattato, senza introduzioni o convenevoli. Non dire mai frasi come 'Ecco il riassunto' o 'Certo, ecco fatto'. Inizia direttamente con il markdown."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return completion.choices[0].message.content
    
    except Exception as e:
        print(f"Errore durante la chiamata API: {e}")
        sys.exit(1)


def save_summary(summary, output_file):
    """Salva il riassunto in un file Markdown"""
    try:
        # Aggiungi metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_content = f"---\nGenerato il: {timestamp}\n---\n\n{summary}"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"✅ Riassunto salvato in: {output_file}")
    
    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")
        sys.exit(1)


def main():
    # Verifica argomenti
    if len(sys.argv) < 2:
        print("Uso: python teams_summarizer.py <file_trascrizione> [file_output]")
        print("\nEsempio:")
        print("  python teams_summarizer.py meeting_transcript.txt")
        print("  python teams_summarizer.py meeting_transcript.txt summary.md")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    
    # Nome file output (default: summary_TIMESTAMP.md)
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"summary_{timestamp}.md"
    
    # Verifica API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL")
    if not api_key:
        print("Errore: Imposta la variabile d'ambiente OPENROUTER_API_KEY")
        print("\nEsempio:")
        print("  export OPENROUTER_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    print(f"📖 Lettura trascrizione da: {transcript_file}")
    transcript = read_transcript(transcript_file)
    
    print(f"🤖 Generazione riassunto con OpenRouter...")
    summary = summarize_meeting(transcript, api_key, model)
    
    print(f"💾 Salvataggio in: {output_file}")
    save_summary(summary, output_file)
    
    print("\n✨ Completato!")


if __name__ == "__main__":
    main()

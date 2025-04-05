#!/bin/bash

# Dossier de stockage
DATA_DIR="$HOME/crypto_dashboard/data"
CSV_FILE="$DATA_DIR/prices.csv"
LOG_FILE="$HOME/crypto_dashboard/scrape_debug.log"

# Créer le dossier s’il n’existe pas
mkdir -p "$DATA_DIR"

# Timestamp actuel
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Récupérer le prix du BTC en USD
PRICE=$(curl -s "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD" | grep -o '"USD":[0-9.]*' | cut -d ':' -f2)

# Si on récupère bien un prix
if [[ -n "$PRICE" ]]; then
    echo "$TIMESTAMP,$PRICE" >> "$CSV_FILE"
    echo "[$TIMESTAMP] Prix récupéré : $PRICE USD" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ❌ Erreur : prix vide" >> "$LOG_FILE"
fi



#!/bin/sh
# extinction.sh : ferme Claude desktop puis éteint le Mac. Généré par la
# compétence extinction du kit go pour le projet {{PROJET}}, le {{DATE}}.
# Tourne HORS de Claude (agent launchd), sinon il meurt avec lui.
# Mode essai : généré avec ESSAI=1, il journalise tout et ne touche à rien.

DELAI={{DELAI}}
ESSAI={{ESSAI}}
LOG="$HOME/Library/Logs/{{PROJET}}-extinction.log"
MARQUEUR="/private/tmp/{{PROJET}}-extinction.done"
CLAUDE_BIN="/Applications/Claude.app/Contents/MacOS/Claude"

log(){ echo "$(date '+%H:%M:%S') $1" >> "$LOG"; }

claude_present(){
  ps -axo pid=,comm= | grep -F "$CLAUDE_BIN" | grep -v grep | awk '{print $1}' | head -1
}

# Une seule exécution (le marqueur disparaît au redémarrage, comme ce script).
if [ -e "$MARQUEUR" ]; then log "marqueur présent : seconde exécution refusée"; exit 0; fi
touch "$MARQUEUR"

[ "$ESSAI" = "1" ] && log "MODE ESSAI : rien ne sera fermé ni éteint"
log "départ (délai ${DELAI} s)"
sleep "$DELAI"

PID=$(claude_present)
if [ -n "$PID" ]; then
  if [ "$ESSAI" = "1" ]; then
    log "ESSAI : Claude détecté (pid $PID), quit puis TERM puis KILL seraient tentés"
  else
    osascript -e 'tell application "Claude" to quit' 2>> "$LOG"
    ATTENTE=0
    while [ $ATTENTE -lt 40 ] && [ -n "$(claude_present)" ]; do sleep 2; ATTENTE=$((ATTENTE+2)); done
    PID=$(claude_present)
    if [ -n "$PID" ]; then
      log "Claude ne s'est pas fermé : TERM"
      kill -TERM "$PID" 2>> "$LOG"
      sleep 8
      PID=$(claude_present)
      if [ -n "$PID" ]; then
        log "Claude toujours là : KILL"
        kill -KILL "$PID" 2>> "$LOG"
        sleep 2
      fi
    fi
  fi
else
  log "Claude n'était pas ouvert"
fi

# On n'éteint QUE si Claude est confirmé fermé (sinon macOS bloque l'extinction
# et l'ordinateur reste allumé toute la nuit).
if [ "$ESSAI" = "1" ]; then
  log "ESSAI : vérification finale, Claude $( [ -n "$(claude_present)" ] && echo 'encore présent' || echo 'absent' ) ; extinction qui aurait été demandée. Fin de l'essai"
  exit 0
fi
if [ -n "$(claude_present)" ]; then
  log "ABANDON : Claude est toujours ouvert après KILL, le Mac reste allumé"
  exit 1
fi
log "Claude fermé (confirmé)"
log "arrêt demandé à macOS"
osascript -e 'tell application "System Events" to shut down' 2>> "$LOG"
sleep 120
# Secours : si on lit encore ceci, le Mac ne s'est pas éteint.
log "le Mac est encore allumé : extinction de secours (loginwindow)"
osascript -e 'tell application "loginwindow" to «event aevtrsdn»' 2>> "$LOG"

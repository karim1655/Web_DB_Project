# Web Database

## Requisiti
- Python 3.12
- Git

## Installazione (Windows e MacOS)
### Clona il repository ed entra nella cartella top-level di progetto
```
git clone https://github.com/karim1655/Web_DB_Project.git
```
```
cd Web_DB_Project
```
### Installa pipenv
```
pip install pipenv
```
### Crea ambiente virtuale
```
pipenv install -r requirements.txt
```
Questo comando creerà un nuovo ambiente virtuale e installerà tutte le dipendenze elencate nel file requirements.txt (se presente). Altrimenti pipenv creerà un ambiente vuoto.
### Attiva ambiente virtuale
```
pipenv shell
```
### Esegui le migrazioni per il database
```
python manage.py migrate
```
### Avvia il server di sviluppo
```
python manage.py runserver
```


## Utilizzo
### Accesso web
Se hai seguito gli step precedenti, ti basta inserire http://localhost:8000 in un qualunque browser per accedere all'applicazione.

Per spegnere il server web locale usa la combinazione `Ctrl+C`.

### Riutilizzo
Assicurati di essere posizionato con il terminale nella cartella top level di progetto.

Esegui i comandi:
```
pipenv shell
```
```
python manage.py runserver
```
e inserisci nuovamente http://localhost:8000 in un qualunque browser.

## Testing
Per eseguire i test, posizionati con il terminale nella cartella top lever di progetto ed esegui:
```
python manage.py test
```



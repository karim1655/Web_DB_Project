# Web Database

## Requisiti
- Python 3.12
- Django 5.1.2
- virtual environment

## Installazione
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
pipenv install
```
Questo comando creerà un nuovo ambiente virtuale e installerà tutte le dipendenze elencate nel file Pipfile (se presente). Altrimenti pipenv creerà un ambiente vuoto.
### Attiva ambiente virtuale
```
pipenv shell
```
### Installa le dipendenze
```
pipenv install -r requirements.txt
```
### Esegui le migrazioni per il database
```
python manage.py migrate
```
### Crea il superutente per accedere alla console admin (facoltativo)
```
python manage.py createsuperuser
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
Per eseguire i test posizionati con il terminale nella cartella top lever di progetto ed esegui:
```
python manage.py test
```



from django.core.management.base import BaseCommand
import pyodbc
from web_app.models import Relazione, TrainingPlan, CustomUser

"""
Transfers entries from sql server table Participants to sqlite3 table (model) Relazione. 
"""


name_id_map = {
    'Alberto': 3,
    'Alessandro': 4,
    'Davide': 5,
    'Domenico': 6,
    'Emma': 7,
    'Enrica': 8,
    'Enrico': 9,
    'Laura': 10,
    'Livaldi': 11,
    'Luca': 12,
    'Marco_M': 13,
    'Marco_P': 14,
    'Mirko': 15,
    'Riccardo': 16,
    'Silvio Cavuto': 17,
    'Sonia': 18
}


class Command(BaseCommand):
    help = "Migra i dati dalla tabella SQL Server a SQLite3"

    def handle(self, *args, **kwargs):
        # Configura la connessione a SQL Server
        sql_server_connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=DESKTOP-KARIM\SQLEXPRESS;'
            'DATABASE=TraineeData;'
            f"Trusted_Connection=yes;"
        )

        cursor = sql_server_connection.cursor()

        # Query per ottenere i dati da SQL Server
        query = """
        SELECT
            TrainingPlan_id, Participant
        FROM Participants
        """

        cursor.execute(query)
        data = cursor.fetchall()

        # Migrazione dei dati
        for row in data:
            try:
                training_plan_instance = TrainingPlan.objects.get(id=row.TrainingPlan_id - 206)
                custom_user_instance = CustomUser.objects.get(id=name_id_map[row.Participant])

                relazione = Relazione(
                    training_plan = training_plan_instance,
                    user = custom_user_instance,
                    stato = 'completato'
                )
                relazione.save()
                self.stdout.write(self.style.SUCCESS(f"Migrated: {relazione}"))
            except Exception as e:
                self.stderr.write(f"Error migrating row {row}: {e}")

        # Chiudi la connessione
        cursor.close()
        sql_server_connection.close()
        self.stdout.write(self.style.SUCCESS("Migrazione completata!"))
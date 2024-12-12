from django.core.management.base import BaseCommand
import pyodbc
from web_app.models import TrainingPlan

"""
Transfers entries from sql server table TrainingPlans to sqlite3 table (model) TrainingPlan. 
"""


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
            FILE_YEAR, COURSE_N, COURSE,
            PLANNEDDATE_DT, EFFECTIVEDATE_DT, EFFECTIVE_YEAR,
            [TYPE], [Start], CheckReview, [End],
            DURATION, [I/E], TRAINER, COST, Requirement
        FROM TrainingPlans
        """

        cursor.execute(query)
        data = cursor.fetchall()

        # Migrazione dei dati
        for row in data:
            try:
                training_plan = TrainingPlan(
                    file_year=row.FILE_YEAR,
                    course_n=row.COURSE_N,
                    course=row.COURSE,
                    planned_date=row.PLANNEDDATE_DT,
                    effective_date=row.EFFECTIVEDATE_DT,
                    effective_year=row.EFFECTIVE_YEAR,
                    type=row.TYPE,
                    start=row.Start,
                    check_review=row.CheckReview,
                    end=row.End,
                    duration=row.DURATION,
                    i_e=row[11],
                    trainer=row.TRAINER,
                    cost=row.COST,
                    requirement=row.Requirement
                )
                training_plan.save()
                self.stdout.write(self.style.SUCCESS(f"Migrated: {training_plan}"))
            except Exception as e:
                self.stderr.write(f"Error migrating row {row}: {e}")

        # Chiudi la connessione
        cursor.close()
        sql_server_connection.close()
        self.stdout.write(self.style.SUCCESS("Migrazione completata!"))

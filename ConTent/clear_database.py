import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ConTent.settings")
    os.remove(os.path.join(".","db.sqlite3"))
    os.remove(os.path.join(".","testApp","migrations","0001_initial.py"))
    from django.core.management import execute_from_command_line

    execute_from_command_line(["","makemigrations"])
    execute_from_command_line(["","migrate"])


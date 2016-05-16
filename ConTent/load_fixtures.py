import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ConTent.settings")

    from django.core.management import execute_from_command_line

    comand_line = ["","loaddata","fixture"]

    fixtures_in_order_of_execution = ["MyUser.json","FieldOwner.json","Customer.json","Campsite.json","PlaceType.json","Convenience.json","Rating.json","Reservation.json"]
    for fixture in fixtures_in_order_of_execution:
        comand_line[2]= os.path.join(".","fixtures",fixture)
        print(fixture)
        execute_from_command_line(comand_line)

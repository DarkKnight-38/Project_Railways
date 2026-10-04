import csv
import random
import pandas
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def bookticket():
    name = input("Enter your Name: ")
    address = input("Enter your Address: ")
    phonenumber = int(input("Enter your Phone Number: "))
    boarding = input("Enter Boarding Station: ").lower()
    destination = input("Enter your Destination: ").lower()
    date_of_boarding = input("Enter the Date of Boarding: ")
    ticketclass = input("Enter your Ticket Class: ")
    number_of_seats = int(input("Enter the Number of Seats: "))
    pnr_number = random.randint(10000000, 99999999)

    with open("TrainTable.csv", "r") as g:
        x = csv.reader(g)
        next(x)

        trains = []

        for i in x:
            stoppages = i[2].split("|")

            if boarding in stoppages and destination in stoppages:
                print(i)
                trains.append(i)

    train_number = int(input("Enter the Train Number: "))

    fare = 0

    for j in trains:
        if train_number == int(j[0]):
            classes = j[3].split('|')

            for c in classes:
                class_name, price = c.split(':')
                class_name = class_name.strip()
                price = int(price)

                if ticketclass == class_name:
                    fare = price

    if fare == 0:
        print("Invalid train number or ticket class.")
        return

    total_fare = fare * number_of_seats

    L = [
        name,
        address,
        phonenumber,
        boarding,
        destination,
        date_of_boarding,
        ticketclass,
        number_of_seats,
        train_number,
        total_fare,
        pnr_number
    ]

    with open("customertable.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(L)

    print("Ticket booked successfully!")
    print("PNR:", pnr_number)
    print("Total Fare:", total_fare)

def cancelticket():
    pnr = int(input("Enter the PNR Number: "))

    df = pandas.read_csv("customertable.csv")

    if pnr in df['pnr'].values:
        df = df[df['pnr'] != pnr]
        df.to_csv("customertable.csv", index=False)
        print("Ticket cancelled successfully.")
    else:
        print("PNR not found.")

def viewticket():
    console = Console()
    pnr = int(input("Enter the PNR Number: "))
    f = open("customertable.csv", "r")
    reader = csv.DictReader(f)
    found = False
    for row in reader:
        if row['pnr']==str(pnr):
            found = True
            ticket_table=Table(show_header=False,box=None)

            ticket_table.add_column("Field", style="light_sea_green")
            ticket_table.add_column("Details", style="medium_purple1")

            ticket_table.add_row("Name:", row['name'])
            ticket_table.add_row("Address:", row['address'])
            ticket_table.add_row("Phone Number:", row['phonenumber'])
            ticket_table.add_row("Boarding Station:", row['boarding'])
            ticket_table.add_row("Destination:", row['destination'])
            ticket_table.add_row("Date of Boarding:", row['date_of_boarding'])
            ticket_table.add_row("Ticket Class:", row['ticketclass'])
            ticket_table.add_row("Number of Seats:", row['number_of_seats'])
            ticket_table.add_row("Train Number:", row['train_number'])
            ticket_table.add_row("Total Fare:", row['total_fare'])
            ticket_table.add_row("PNR:", row['pnr'])
            console.print(Panel(ticket_table,title="Ticket Details",title_align="center",border_style="pink1"))
    if found==False:
        console.print("[red]PNR not found.[/red]")
            
def viewtraintable():
    console=Console()
    f = open("TrainTable.csv", "r")
    reader = csv.DictReader(f)

    for row in reader:
        train_table=Table(show_header=False,box=None)
        train_table.add_column("Train Field", style="light_sea_green")
        train_table.add_column("Train Details", style="medium_purple1")

        train_table.add_row(f"Train Number:", row['train_no'])
        train_table.add_row(f"Train Name:", row['train_name'])
        train_table.add_row(f"Arrival Time:", row['stoppages'])
        train_table.add_row(f"Classes Available:", row['class'])
        console.print(Panel(train_table,title="Train Details",title_align="center",border_style="pink1"))
        print()
    f.close()

def menu():
    while True:
        print("1. Book Ticket")
        print("2. Cancel Ticket")
        print("3. View Ticket")
        print("4. View Train Table")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            bookticket()
        elif choice == "2":
            cancelticket()
        elif choice == "3":
            viewticket()
        elif choice == "4":
            viewtraintable()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

menu()
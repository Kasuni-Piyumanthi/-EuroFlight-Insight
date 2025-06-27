"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 20240454
 4. Date: 2024.06.26
****************************************************************************

"""

from graphics import *
import csv
from datetime import datetime

# Task A: Input Validation
def get_valid_filename():

    # Example list
    valid_city_codes = ['CDG', 'BCN', 'LHR', 'FRA', 'AMS']
    airport_names = {
        'CDG': 'Paris Charles de Gaulle airport',
        'BCN': 'Barcelona airport',
        'LHR': 'London Heathrow airport',
        'FRA': 'Frankfurt airport',
        'AMS': 'Amsterdam airport'
    }

    # --- CITY CODE INPUT ---
    while True:
        city_code = input("Please enter the three-letter code for the departure city required: ").upper()
        if len(city_code) != 3:
            print("Wrong code length - please enter a three-letter city code")
        elif city_code not in valid_city_codes:
            print("Unavailable city code - please enter a valid city code")
        else:
            break

    # --- YEAR INPUT ---
    while True:
        year_input = input("Please enter the year required in the format YYYY: ")
        if not year_input.isdigit() or len(year_input) != 4:
            print("Wrong data type - please enter a four-digit year value")
        else:
            year = int(year_input)
            if year < 2000 or year > 2025:
                print("Out of range - please enter a value from 2000 to 2025")
            else:
                break

    # --- BUILD FILENAME ---
    selected_data_file = f"{city_code}{year}.csv"
    airport_full_name = airport_names.get(city_code, "Unknown Airport")

    print(f"\nFile {selected_data_file} selected - Planes departing {airport_full_name} {year}.\n")

    return selected_data_file, city_code, year, airport_full_name

# Task B:Outcomes

def load_csv(CSV_chosen):
    outcomes = []
    try:
        with open(CSV_chosen, 'r') as file:
            data = csv.reader(file)
            # Skip the header row
            header = next(data)
            content = list(data)

            # Initialize counters
            total_departure_flight = 0
            total_flights_runway1 = 0
            total_depflights_over_500miles = 0
            total_depflights_by_BA = 0
            total_flights_in_rain = 0
            avg_no_depatures_perhour = 0
            percentage_total_departures_AF = 0
            percentage_delayed_depflights = 0
            total_rain_hours = 0
            longnames_most_common_des = 0

            
            # Get the total number of flights from this airport
            total_departure_flight = len(content)

            # Get the total number of flights departing Runway one
            total_flights_runway1 = sum(1 for row in content if row[8] == "1")

            # Get the total number of departures of flights over 500 miles
            total_depflights_over_500miles = sum(1 for row in content if int(row[5]) > 500)
                    
            # Get the number of departure flights by British Airways aircraft
            total_depflights_by_BA = sum(1 for row in content if row[1].startswith("BA"))
                    
            # Get the total number of flights departing in rain
            total_flights_in_rain = sum(1 for row in content if "rain" in row[9].lower())
                    
            # Get the average number of departures per hour
            hours = [row[2][:2] for row in content]
            unique_hours = set(hours)
            avg_no_depatures_perhour = round(total_departure_flight / len(unique_hours))
                    
            # Get the percentage of total departures that are Air France aircraft
            total_departures_AF = sum(1 for row in content if row[1].startswith("AF"))
            percentage_total_departures_AF = f"{round((total_departures_AF / total_departure_flight)*100)}%"
                    
            # Get the percentage of flights with delayed departures
            delayed_depflights = sum(1 for row in content if row[3] > row[2])
            percentage_delayed_depflights = f"{round((delayed_depflights / total_departure_flight)*100)}%"
                    
            # Get the total number of rain hours
            rain_hours = set(row[2][:2] for row in content if "rain" in row[9].lower())
            total_rain_hours = len(rain_hours)
                    
            # Get the long name of the most common destination
            destinations = [row[4]for row in content]
            dest_counts = {dest: destinations.count(dest) for dest in set(destinations)}
            max_freq = max(dest_counts.values())
            longnames_most_common_des = [dest for dest, count in dest_counts.items() if count == max_freq]                
                                   

            # Print the outcomes
            outcomes.append(f"The total number of flights from this airport was {total_departure_flight}")
            outcomes.append(f"The total number of flights departing Runway one was {total_flights_runway1}")
            outcomes.append(f"The total number of departures of flights over 500 miles was {total_depflights_over_500miles}")
            outcomes.append(f"There were {total_depflights_by_BA} British Airways flights from this airport")
            outcomes.append(f"There were {total_flights_in_rain} flights from this airport departing in rain")
            outcomes.append(f"There was an average of {avg_no_depatures_perhour} flights per hour from this airport")
            outcomes.append(f"Air France planes made up {percentage_total_departures_AF} of all departures")
            outcomes.append(f"{percentage_delayed_depflights} of all departures were delayed")
            outcomes.append(f"There were {total_rain_hours} hours in which rain fell")
            outcomes.append(f"The most common destinations are {', '.join(longnames_most_common_des)}")

            
            # Prepare outcomes to return
            return outcomes, content

    except FileNotFoundError:
        print("File does not exist.")
        return[], []

# Display Results
def display_outcomes(file_path, outcomes):
    print(f"\nResults for {file_path}")
    print("*************************************")
    for outcome in outcomes:
          print(outcome)
    print("************************************\n")



# Task C: Save Results to Text File
def save_results_to_file(outcomes, city_code, year, airport_name, file_name="results.txt"):
    try:
        with open(file_name, "a") as file:
            file.write("************************************************************\n")
            file.write(f"File: {city_code}{year}.csv\n")
            file.write(f"Airport: {airport_name}\n")
            file.write(f"Year: {year}\n\n")
            for line in outcomes:
                file.write(line + "\n")
            file.write("************************************************************\n\n")
        print(f"Results saved to {file_name}\n")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Task D: Histogram Display

def plot_histogram(data, airline_code, airline_name, airport_name, year):
    win = GraphWin(f"{airline_name} Departures Histogram", 800, 600)
    win.setBackground("white")

    #Draw axis
    x_axis = Line(Point(50 ,550), Point(750, 550))
    x_axis.draw(win)
    '''
    y_axis = Line(Point(50 ,50), Point(50, 550))
    y_axis.draw(win)
    '''

    
    #Draw Grid Lines and Y-axis Labels
    max_count = max(data.values()) if data else 1
    '''
    for i in range(0, max_count+ 1,max(1, max_count // 5)):
        y = 550 - (i/max_count)*400
        grid_line = Line(Point(50,y), Point(750,y))
        grid_line.setOutline("lightgray")
        grid_line.draw(win)
        y_label = Text(Point(30,y), str(i))
        y_label.setSize(8)
        y_label.draw(win)
    '''

    #Draw x-axis label
    x_label =Text(Point(390,590), "Hours 00:00 to 12:00")
    x_label.setSize(12)
    x_label.draw(win)

    #Draw title
    title = Text(Point(400, 20), f"{airline_name} Departures from {airport_name}, {year}")
    title.setSize(14)
    title.setStyle("bold")
    title.draw(win)

    #Scale bars to fit the window
    bar_width = 40
    spacing = 10
    colors = ["lightgreen"]
    
    for i, hour in enumerate(sorted(data.keys())):
        count = data[hour]
        height = int((count / max_count) * 400)
        x1 = 60 + i * (bar_width + spacing)
        x2 = x1 + bar_width
        y1 = 550 - height
        y2 = 550

        # Draw bar
        bar = Rectangle(Point(x1, y1), Point(x2, y2))
        bar.setFill(colors[i % len(colors)])
        bar.setOutline("black")
        bar.draw(win)

        # Draw count above bar
        label = Text(Point((x1 + x2) / 2, y1 - 10), str(count))
        label.setSize(10)
        label.draw(win)

        # Draw hour below bar
        hour_label = Text(Point((x1 + x2) / 2, 560), f"{hour}:00")
        hour_label.setSize(10)
        hour_label.draw(win)

    # Wait for user to close window
    try:
        win.getMouse()
    except GraphicsError:
        pass
    win.close()

def handle_histogram_request(content, airport_name, year):
    valid_airlines = {
        'BA': 'British Airways',
        'AF': 'Air France',
        'LH': 'Lufthansa',
        'KL': 'KLM',
        'IB': 'Iberia',
        'AY': 'Finnair',
        'SK': 'Scandinavian Airlines',
        'TP': 'TAP Air Portugal',
        'TK': 'Turkish Airlines',
        'W6': 'Wizz Air',
        'U2': 'easyJet',
        'FR': 'Ryanair',
        'A3': 'Aegean Airlines',
        'SN': 'Brussels Airlines',
        'EK': 'Emirates',
        'QR': 'Qatar Airways',
    }

    while True:
        airline_code = input("Enter a two-character Airline code to plot a histogram: ").upper()
        if airline_code in valid_airlines:
            break
        else:
            print("Unavailable Airline code please try again.")

    # Count flights per hour for selected airline
    hourly_counts = {f"{str(h).zfill(2)}": 0 for h in range(12)}
    for row in content:
        if row[1].startswith(airline_code):
            hour = row[2][:2]
            if hour in hourly_counts:
                hourly_counts[hour] += 1

    plot_histogram(hourly_counts, airline_code, valid_airlines[airline_code], airport_name, year)

#Task E - Loop
def validate_continue_input():
    while True:
        again = input("Do you want to select another data file for a different date? Y/N: ").lower()
        if again in ['y', 'n']:
            return again
        else:
            print("Please enter 'Y' or 'N'.")


while True:
    selected_data_file, city_code, year, airport_name = get_valid_filename()
    outcomes, content = load_csv(selected_data_file)

    if outcomes:
        display_outcomes(selected_data_file, outcomes)
        save_results_to_file(outcomes, city_code, year, airport_name)
        handle_histogram_request(content, airport_name, year)

    if validate_continue_input() == 'n':
        print("Program Ended.")
        break




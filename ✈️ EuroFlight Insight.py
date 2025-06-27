
from graphics import *
import csv
from datetime import datetime

# Task A: Input Validation
def get_valid_filename():
    valid_city_codes = ['CDG', 'BCN', 'LHR', 'FRA', 'AMS']
    airport_names = {
        'CDG': 'Paris Charles de Gaulle airport',
        'BCN': 'Barcelona airport',
        'LHR': 'London Heathrow airport',
        'FRA': 'Frankfurt airport',
        'AMS': 'Amsterdam airport'
    }

    while True:
        city_code = input("Please enter the three-letter code for the departure city required: ").upper()
        if len(city_code) != 3:
            print("Wrong code length - please enter a three-letter city code")
        elif city_code not in valid_city_codes:
            print("Unavailable city code - please enter a valid city code")
        else:
            break

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

    selected_data_file = f"{city_code}{year}.csv"
    airport_full_name = airport_names.get(city_code, "Unknown Airport")
    print(f"\nFile {selected_data_file} selected - Planes departing {airport_full_name} {year}.\n")
    return selected_data_file, city_code, year, airport_full_name

# Task B: Load CSV and Outcomes
def load_csv(CSV_chosen):
    outcomes = []
    try:
        with open(CSV_chosen, 'r') as file:
            data = csv.reader(file)
            header = next(data)
            content = list(data)

            total_departure_flight = len(content)
            total_flights_runway1 = sum(1 for row in content if row[8] == "1")
            total_depflights_over_500miles = sum(1 for row in content if int(row[5]) > 500)
            total_depflights_by_BA = sum(1 for row in content if row[1].startswith("BA"))
            total_flights_in_rain = sum(1 for row in content if "rain" in row[9].lower())
            hours = [row[2][:2] for row in content]
            unique_hours = set(hours)
            avg_no_depatures_perhour = round(total_departure_flight / len(unique_hours))
            total_departures_AF = sum(1 for row in content if row[1].startswith("AF"))
            percentage_total_departures_AF = f"{round((total_departures_AF / total_departure_flight)*100)}%"
            delayed_depflights = sum(1 for row in content if row[3] > row[2])
            percentage_delayed_depflights = f"{round((delayed_depflights / total_departure_flight)*100)}%"
            rain_hours = set(row[2][:2] for row in content if "rain" in row[9].lower())
            total_rain_hours = len(rain_hours)
            destinations = [row[4] for row in content]
            dest_counts = {dest: destinations.count(dest) for dest in set(destinations)}
            max_freq = max(dest_counts.values())
            longnames_most_common_des = [dest for dest, count in dest_counts.items() if count == max_freq]

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

            return outcomes, content
    except FileNotFoundError:
        print("File does not exist.")
        return [], []

# Display Results
def display_outcomes(file_path, outcomes):
    print(f"\nResults for {file_path}")
    print("*************************************")
    for outcome in outcomes:
        print(outcome)
    print("*************************************\n")

# Task C: Save Results
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

# Task D: Histogram
def plot_histogram(data, airline_code, airline_name, airport_name, year):
    win = GraphWin(f"{airline_name} Departures Histogram", 800, 600)
    win.setBackground("white")

    
    x_axis = Line(Point(50, 550), Point(750, 550))
    x_axis.draw(win)
    y_axis = Line(Point(50, 50), Point(50, 550))
    y_axis.draw(win)

    title = Text(Point(400, 20), f"{airline_name} Departures from {airport_name}, {year}")
    title.setSize(14)
    title.setStyle("bold")
    title.draw(win)

    max_count = max(data.values()) if data else 1
    bar_width = 50
    spacing = 15

    for i, hour in enumerate(sorted(data.keys())):
        count = data[hour]
        height = int((count / max_count) * 400)
        x1 = 70 + i * (bar_width + spacing)
        x2 = x1 + bar_width
        y1 = 550 - height
        y2 = 550

        bar = Rectangle(Point(x1, y1), Point(x2, y2))
        bar.setFill("skyblue")
        bar.setOutline("black")
        bar.draw(win)

        label = Text(Point((x1 + x2) / 2, y1 - 10), str(count))
        label.setSize(10)
        label.draw(win)

        hour_label = Text(Point((x1 + x2) / 2, 560), hour)
        hour_label.setSize(10)
        hour_label.draw(win)

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
        'IB': 'Iberia'
    }

    while True:
        airline_code = input("Enter a two-character Airline code to plot a histogram: ").upper()
        if airline_code in valid_airlines:
            break
        else:
            print("Unavailable Airline code please try again.")

    hourly_counts = {f"{str(h).zfill(2)}": 0 for h in range(12)}
    for row in content:
        if row[1].startswith(airline_code):
            hour = row[2][:2]
            if hour in hourly_counts:
                hourly_counts[hour] += 1

    print("Hourly counts:", hourly_counts)  # Debug print
    plot_histogram(hourly_counts, airline_code, valid_airlines[airline_code], airport_name, year)

# Loop (Task E)
def validate_continue_input():
    while True:
        again = input("Do you want to select another data file for a different date? Y/N: ").strip().lower()
        if again in ['y', 'n']:
            return again
        else:
            print("Please enter 'Y' or 'N'.")

# Main loop
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

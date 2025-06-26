# Task A: Input Validation

from graphics import *
import csv
import math
from datetime import datetime

def get_valid_filename():

    # Example list from Table 2 (you can replace it with actual list)
    valid_city_codes = ['CDG', 'BCN', 'LHR', 'FRA', 'AMS']
        # --- DISPLAY CONFIRMATION ---
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
                        # Prepare outcomes to return
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
            return outcomes

    except FileNotFoundError:
        print("File does not exist.")
        return[]

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

def validate_continue_input():
    while True:
        again = input("Do you want to select another data file for a different date? Y/N: ").strip().lower()
        if again in ['y', 'n']:
            return again
        else:
            print("Please enter 'Y' or 'N'.")


while True:
    selected_data_file, city_code, year, airport_name = get_valid_filename()
    outcomes = load_csv(selected_data_file)

    if outcomes:
        display_outcomes(selected_data_file, outcomes)
        save_results_to_file(outcomes, city_code, year, airport_name)

    if validate_continue_input() == 'n':
        print("Program Ended.")
        break

'''
# Task D: Histogram Display
valid_airlines = {
    'BA': 'British Airways',
    'AF': 'Air France',
    'LH': 'Lufthansa',
    'KL': 'KLM',
    'IB': 'Iberia',
    }

def plot_histogram(data, airline_code, airline_name, airport_name, year):
    win = GraphWin(f"{airline_name} Departures Histogram", 800, 600)
    win.setBaackground("white")

#Draw axis
x_axis = Line(Point(50 ,550), point(750, 550))
x.axis.draw(win)
y_axis = Line(Point(50 ,50), point(50, 550))
y.axis.draw(win)

#Draw title
title = Text(Point(400, 20), f"{airline_name} Departures from {airport_name}, {year}")
title.setSize(14)
title.setStyle("bold")
title.draw(win)

#Scale bars to fit the window
max_count = max(data.values()) if data else 1
bar_width = 50
spacing = 15
for i, hour in enumerate(sorted(data.keys())):
    count = data[hour]
    height = int((count / max_count) * 400)
    x1 = 70 + i * (bar_width + spacing)
    x2 = x1 + bar_width
    y1 = 550 - heigh
    y2 = 550

    # Draw bar
    bar = Rectangle(Point(x1, y1), Point(x2, y2))
    bar.setFill("skyblue")
    bar.setOutline("black")
    bar.draw(win)

    # Draw count above bar
    label = Text(Point((x1 + x2) / 2, y1 - 10), str(count))
    label.setSize(10)
    label.draw(win)

    # Draw hour below bar
    hour_label = Text(Point((x1 + x2) / 2, 560), hour)
    hour_label.setSize(10)
    hour_label.draw(win)

# Wait for user to close window
win.getMouse()
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

    # Count flights per hour for selected airline
    hourly_counts = {f"{str(h).zfill(2)}": 0 for h in range(12)}  # 00 to 11

    for row in content:
        if row[1].startswith(airline_code):
            hour = row[2][:2]
            if hour in hourly_counts:
                hourly_counts[hour] += 1

    plot_histogram(hourly_counts, airline_code, valid_airlines[airline_code], airport_name, year)


'''
'''
import tkinter as tk
from collections import defaultdict

class HistogramApp:
    def __init__(self, traffic_data, date):
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.root.title(f"Traffic Data Histogram - {self.date}")
        self.canvas = tk.Canvas(self.root, width=1300, height=600, bg="white")
        self.canvas.pack()

    def draw_histogram(self):
        hourly_data = defaultdict(lambda: [0, 0])  # [Elm Ave Count, Hanley Hwy Count]

        for row in self.traffic_data:
            junction, time_of_day = row[0], row[2]
            hour = int(time_of_day.split(":")[0])
            if junction == "Elm Avenue/Rabbit Road":
                hourly_data[hour][0] += 1
            elif junction == "Hanley Highway/Westway":
                hourly_data[hour][1] += 1

        bar_width = 20
        max_count = max(
            max(counts[0], counts[1]) for counts in hourly_data.values()
        )
        scale_factor = 400 / max_count if max_count > 0 else 1

        # Draw the x-axis and y-axis
        self.canvas.create_line(40, 450, 1300, 450, width=2)  # x-axis
        self.canvas.create_line(40, 450, 40, 50, width=2)     # y-axis
        
        # Add labels to the y-axis (vehicle counts)
        for i in range(0, max_count + 1, max(1, max_count // 10)):
            y_position = 450 - i * scale_factor
            self.canvas.create_line(35, y_position, 45, y_position, width=1)
            self.canvas.create_text(25, y_position, text=str(i), anchor="e", font=("Arial", 10))
        
        # Draw bars and labels for each hour
        for hour in range(24):
            counts = hourly_data[hour]
            x_start = 50 + hour * (2 * bar_width + 10)
            x_mid = x_start + bar_width
            x_end = x_mid + bar_width

            # Draw bars for Elm Avenue/Rabbit Road
            self.canvas.create_rectangle(
                x_start, 450 - counts[0] * scale_factor, x_mid, 450, fill="#AFE1AF"
            )
            self.canvas.create_text(
                (x_start + x_mid) / 2, 450 - counts[0] * scale_factor - 10,
                text=str(counts[0]), fill="#000000", font=("Arial", 8)
            )

            # Draw bars for Hanley Highway/Westway
            self.canvas.create_rectangle(
                x_mid, 450 - counts[1] * scale_factor, x_end, 450, fill="#FFFFC5"
            )
            self.canvas.create_text(
                (x_mid + x_end) / 2, 450 - counts[1] * scale_factor - 10,
                text=str(counts[1]), fill="#000000", font=("Arial", 8)
            )

            # Draw hour labels on the x-axis
            self.canvas.create_text(
                (x_start + x_end) / 2, 460, text=f"{hour}:00", anchor="n", font=("Arial", 8)
            )

        # Add axis labels and histogram title
        self.canvas.create_text(
            400, 15, text=f"Histogram of Vehical Frequency per Hour ({self.date})", font=("Arial", 15, "bold"), anchor="w"
        )
        self.canvas.create_text(
            700, 500, text="Time (hours)", font=("Arial", 12), anchor="w"
        )
        self.canvas.create_text(
            20, 250, text="Vehicle Count", font=("Arial", 12), anchor="center", angle=90
        )
        self.canvas.create_rectangle(
            50, 45, 75, 70, fill="#AFE1AF", outline="#000000", width=2
        )
        self.canvas.create_text(
            80, 57.5, text="Elm Avenue/Rabbit Road", font=("Arial", 10), fill="#000000", anchor="w"
        )
        self.canvas.create_rectangle(
            50, 75, 75, 100, fill="#FFFFC5", outline="#000000", width=2
        )
        self.canvas.create_text(
            80, 87.5, text="Hanley Highway/Westway", font=("Arial", 10), fill="#000000", anchor="w"
        )

    def run(self):
        self.draw_histogram()
        self.root.mainloop()

# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.current_data = None

    def load_csv_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()[1:]  # Skip header
                self.current_data = [line.strip().split(",") for line in lines]
            return True
        except FileNotFoundError:
            print("Error: File not found.")
            return False

    def process_data_and_display_histogram(self, date):
        if self.current_data:
            app = HistogramApp(self.current_data, date)
            app.run()

    def handle_user_interaction(self):
        while True:
            # Step 1: Ask if the user wants to load another histogram
            user_choice = input("Do you want to load the histogram? (Y/N): ").strip().upper()
        
            if user_choice == "Y":
                # Step 2: Collect the date, month, and year as separate inputs
                while True:
                    try:
                        DD = int(input("Enter the day (DD): "))
                        if DD < 1 or DD > 31:
                            print("Out of range - values must be in the range 1 and 31")
                            continue

                        MM = int(input("Enter the month (MM): "))
                        if MM < 1 or MM > 12:
                            print("Out of range - values must be in the range 1 and 12")
                            continue

                        YYYY = int(input("Enter the year (YYYY): "))
                        if YYYY < 2000 or YYYY > 2024:
                            print("Out of range - values must be in the range 2000 and 2024")
                            continue

                        # Combine inputs into the desired filename format
                        file_path = f"traffic_data{DD:02d}{MM:02d}{YYYY}.csv"
                        
                        # Check leap years
                        def is_leap_year(YYYY):
                            return(YYYY % 4 == 0)

                        # Check the validation logic 
                        if 1 <= DD <= 31 and 1 <= MM <= 12 and 2000 <= YYYY <= 2024:
                            # Chech maximum days for each month
                            if MM in [1,3,5,7,8,10,12]:    # Months with 31 days
                                max_days = 31
                            elif MM in [4,6,9,11]:    # Months with 30 days
                                max_days = 30    
                            elif MM == 2:    # February
                                max_days = 29 if is_leap_year(YYYY) else 28
                            else:
                                max_days = 0    # Invalid month
                                
                            # Check if the day is valid:
                            if 1 <= DD <= max_days:
                                date = f"{DD}/{MM}/{YYYY}"
                            
                            else:
                                print("Invalid data check day, month and year")
                        else:
                            pass
                    
                        if self.load_csv_file(file_path):
                            self.process_data_and_display_histogram(f"{DD:02d}/{MM:02d}/{YYYY}")
                            break
                        
                        else:
                            print("File not found or failed to process. Please try again.")

                    except ValueError:
                        print("Integer required")
                        
            # Exit from the programme           
            elif user_choice == "N":
                        print("Exiting program.")
                        break
                    
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.handle_user_interaction()
'''    
    
# Task D: Draw Histogram using graphics.py
def get_valid_airline_code():
    valid_airline_codes = ['BA', 'AF', 'FR', 'LH', 'IB', 'EK', 'SN', 'TP', 'U2', 'AY', 'KL', 'QR', 'SK', 'W6']
    while True:
        code = input("Enter a two-character Airline code to plot a histogram: ").upper()
        if code in valid_airline_codes:
            return code
        else:
            print("Unavailable Airline code please try again.")

def draw_histogram(datafile, airline_code, airport_name, year):
    try:
        with open(datafile, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            hourly_counts = [0] * 12  # 12-hour survey period

            for row in reader:
                if row[1].startswith(airline_code):
                    hour = int(row[2].split(":")[0])
                    if 0 <= hour < 12:
                        hourly_counts[hour] += 1

        max_count = max(hourly_counts)
        win = GraphWin(f"{airline_code} Departures from {airport_name} ({year})", 800, 400)
        win.setCoords(0, 0, 12, max_count + 5)

        # Draw bars and labels
        for i in range(12):
            bar = Rectangle(Point(i + 0.2, 0), Point(i + 0.8, hourly_counts[i]))
            bar.setFill("blue")
            bar.draw(win)
            Text(Point(i + 0.5, -0.5), str(i)).draw(win)  # Hour label
            Text(Point(i + 0.5, hourly_counts[i] + 0.5), str(hourly_counts[i])).draw(win)  # Count

        # Draw title
        title = Text(Point(6, max_count + 3), f"{airline_code} Departures from {airport_name} ({year})")
        title.setSize(14)
        title.setStyle("bold")
        title.draw(win)

        win.getMouse()
        win.close()

    except Exception as e:
        print("Error drawing histogram:", e)










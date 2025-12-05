import csv
import matplotlib.pyplot as plt
from collections import namedtuple
from typing import List, Dict, Any, TypeVar

T = TypeVar("T")

"""
GCDS CS: Titanic Dataset Analysis
Dataset: titanic.csv

SETUP:
------


The titanic.csv dataset contains the following columns:
- PassengerId: Unique ID for each passenger
- Survived: 0 = No, 1 = Yes
- Pclass: Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)
- Name: Passenger name
- Sex: male or female
- Age: Age in years
- SibSp: Number of siblings/spouses aboard
- Parch: Number of parents/children aboard
- Ticket: Ticket number
- Fare: Passenger fare
- Cabin: Cabin number
- Embarked: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)

ASSIGNMENT GOALS:
-----------------

GOAL 1 (Beginner): Load and Display Data
-----------------------------------------
Load the titanic.csv file and display the first 10 rows.
Print the column names and the total number of passengers.

GOAL 2 (Beginner): Calculate Survival Rate
-------------------------------------------
Calculate and print the overall survival rate (percentage of passengers who survived).

GOAL 3 (Intermediate): Survival by Gender
------------------------------------------
Calculate the survival rate for males and females separately.
Display which gender had a higher survival rate.

GOAL 4 (Intermediate): Age Analysis
------------------------------------
Find and print:
- The average age of all passengers
- The average age of survivors vs non-survivors
- The youngest and oldest passengers

GOAL 5 (Intermediate): Class-Based Analysis
--------------------------------------------
For each passenger class (1st, 2nd, 3rd):
- Calculate the survival rate
- Calculate the average fare paid
Create a summary showing which class had the best survival chances.

GOAL 6 (Advanced): Family Survival Patterns
--------------------------------------------
Create a new column called 'FamilySize' (SibSp + Parch + 1).
Analyze survival rates based on family size.
Determine if traveling alone or with family improved survival chances.

GOAL 7 (Advanced): Data Visualization
--------------------------------------
Create at least 3 different charts:
1. Bar chart comparing survival rates by gender
2. Histogram showing age distribution
3. Bar chart showing survival rates by passenger class
(You'll need matplotlib: pip install matplotlib)

GOAL 8 (Challenge): Comprehensive Report
-----------------------------------------
Write a function that generates a complete survival analysis report including:
- Overall statistics (total passengers, survivors, survival rate)
- Breakdown by gender, class, and age group (child <18, adult 18-60, senior >60)
- Identify the profile of passengers most likely to survive (combination of features)
- Handle missing data appropriately
- Save the report to a text file

STARTER CODE TEMPLATE:
"""

TitanicData = namedtuple("TitanicData", ["passenger_id", "survived", "p_class", "name", "sex", "age", "sib_sp", "parch", "ticket", "fare", "cabin", "embarked", "family_size"])

def read_data(file_name : str) -> List[TitanicData]:
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        lines = [line for line in reader][1:]
        return [TitanicData(*line, family_size=str(int(line[6]) + int(line[7]) + 1)) for line in lines]
    
def display_data(data : List[TitanicData]):
    data_len_map = {i : 0 for i, _ in enumerate(data[0])}
    header = ["PassengerId", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked", "FamilySize"]
    for line in data:
        for i, value in enumerate(line):
            data_len_map[i] = max(max(data_len_map[i], len(value)), len(header[i]) + 1 + i)
    print("Titanic Data".center(sum(data_len_map.values()) + len(data_len_map.values()))) # Title centered on datals
    for i, title in enumerate(header):
        print(f"{title:^{data_len_map[i] + 1}}", end="")
    print()
    for line in data:
        for i, value in enumerate(line):
            print(f"{value:^{data_len_map[i]}}", end="|")
        print()

def survival_rate(data : List[TitanicData]) -> float:
    return sum([int(value.survived) for value in data]) / len(data)

def survival_rate_gender(data : List[TitanicData]):
    male_data = [person for person in data if person.sex == "male"]
    female_data = [person for person in data if person.sex == "female"]
    male_survival = survival_rate(male_data)
    female_survival = survival_rate(female_data)
    return male_survival, female_survival

def valid_property(data : List[TitanicData], property : str):
    return [person for person in data if getattr(person, property) != ""]

def average_age(data : List[TitanicData]):
    return sum([float(person.age) for person in valid_property(data, "age")]) / len(data)

def average_age_survived(data : List[TitanicData]):
    survivors = [person for person in data if person.survived == "1"]
    non_survivors = [person for person in data if person.survived == "0"]
    survivor_age = average_age(survivors)
    non_survivor_age = average_age(non_survivors)
    return survivor_age, non_survivor_age

def oldest_passenger(data : List[TitanicData]):
    age = -1
    for person in valid_property(data, "age"):
        if float(person.age) > age:
            age = float(person.age)
    return age

def youngest_passenger(data : List[TitanicData]):
    age = float("inf")
    for person in valid_property(data, "age"):
        if float(person.age) < age:
            age = float(person.age)
    return age

def class_data(data : List[TitanicData], passenger_class : int):
    class_recorded = valid_property(data, "p_class")
    return [person for person in class_recorded if person.p_class == str(passenger_class)]

def class_survival(data : List[TitanicData], passenger_class : int):
    return survival_rate(class_data(data, passenger_class))

def average_fare(data : List[TitanicData]):
    return sum([float(person.fare) for person in data]) / len(data)

def class_fare(data : List[TitanicData], passenger_class : int):
    return average_fare(class_data(data, passenger_class))

def family_size_data(data : List[TitanicData], family_size : int):
    return [person for person in data if int(person.family_size) == family_size]

def family_size_survival(data : List[TitanicData], family_size : int):
    return survival_rate(family_size_data(data, family_size))

def min_family_size(data : List[TitanicData]):
    family_size = float("inf")
    for person in data:
        if int(person.family_size) < family_size:
            family_size = int(person.family_size)
    return int(family_size)

def max_family_size(data : List[TitanicData]):
    family_size = -1
    for person in data:
        if int(person.family_size) > family_size:
            family_size = int(person.family_size)
    return family_size

def group_analysis(data : List[TitanicData], tabs = 1) -> str:
    analysis = f"{"\t" * tabs}Population: {len(data)}\n"
    analysis += f"{"\t" * (tabs + 1)}Survivors: {len([person for person in data if person.survived == "1"])}\n"
    analysis += f"{"\t" * (tabs + 1)}Deceased: {len([person for person in data if person.survived == "0"])}\n"
    analysis += f"{"\t" * tabs}Survival Rate: {survival_rate(data) * 100:.1f}%"
    return analysis

def write_analysis(data : List[TitanicData], filepath : str):
    def name_max_map(map : Dict[T, Any]) -> T:
        return list(map.keys())[list(map.values()).index(max(map.values()))]
    
    with open(filepath, 'w') as file:
        file.write("Titanic Data Analysis\n\n")
        
        file.write(f"All Passengers:\n")
        file.write(group_analysis(data))
        
        males = [person for person in data if person.sex == "male"]
        females = [person for person in data if person.sex == "female"]
        
        file.write(f"\nGenders:")
        file.write(f"\n\tMale:\n")
        file.write(group_analysis(males, tabs=2))
        file.write(f"\n\tFemale:\n")
        file.write(group_analysis(females, tabs=2))
        
        first_class = class_data(data, 1)
        second_class = class_data(data, 2)
        third_class = class_data(data, 3)
        
        file.write("\nClasses:")
        file.write("\n\tFirst Class:\n")
        file.write(group_analysis(first_class, tabs=2))
        file.write("\n\tSecond Class:\n")
        file.write(group_analysis(second_class, tabs=2))
        file.write("\n\tThird Class:\n")
        file.write(group_analysis(third_class, tabs=2))
        
        children = [person for person in valid_property(data, "age") if float(person.age) < 18]
        adults = [person for person in valid_property(data, "age") if float(person.age) >= 18 and float(person.age) < 60]
        seniors = [person for person in valid_property(data, "age") if float(person.age) >= 18 and float(person.age) < 60]
        
        file.write("\nAge Groups:")
        file.write("\n\tChild (<18):\n")
        file.write(group_analysis(children, tabs=2))
        file.write("\n\tAdult (18-60):\n")
        file.write(group_analysis(adults, tabs=2))
        file.write("\n\tSeniors (>60):\n")
        file.write(group_analysis(seniors, tabs=2))
        
        family_sizes = [int(person.family_size) for person in data]
        family_size_map = dict()
        
        file.write("\nFamily Sizes:")
        for i in range(min(family_sizes), max(family_sizes) + 1):
            family_size_group = [person for person in data if int(person.family_size) == i]
            if len(family_size_group) > 0:
                rate = survival_rate(family_size_group)
                file.write(f"\n\t{i}. {rate*100:.1f}%")
                family_size_map[i] = rate
            else:
                file.write(f"\n\t{i}. None Applicable")
        
        gender_map = {"Male" : survival_rate(males), "Female" : survival_rate(females)}
        best_gender = name_max_map(gender_map)
        
        class_map = {"First" : survival_rate(first_class), "Second" : survival_rate(second_class), "Third" : survival_rate(third_class)}
        best_class = name_max_map(class_map)
        
        age_group_map = {"Child" : survival_rate(children), "Adult" : survival_rate(adults), "Senior" : survival_rate(seniors)}
        best_age_group = name_max_map(age_group_map)
        
        best_family_size = name_max_map(family_size_map)
        
        file.write("\n\nHighest Survival Rate Group:")
        file.write(f"\n\tGender: {best_gender}")
        file.write(f"\n\tClass: {best_class}")
        file.write(f"\n\tAge Group: {best_age_group}")
        file.write(f"\n\tFamily Size: {best_family_size}")

def plot_data(data : List[TitanicData]):
    male, female = survival_rate_gender(data)
    valid_int_ages = [int(float(person.age)) for person in valid_property(data, "age")]
    mens_ages = [int(float(person.age)) for person in valid_property(data, "age") if person.sex == "male"]
    first_survival_rate = class_survival(data, 1)
    second_survival_rate = class_survival(data, 2)
    third_survival_rate = class_survival(data, 3)
    
    _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14.5, 4.5), num="Titanic Graphs")
    
    ax1.bar(["Male", "Female"], [male * 100, female * 100], color=["skyblue", "pink"])
    ax1.set_xlabel("Gender")
    ax1.set_ylabel("Survival Rate %")
    ax1.set_ylim(0, 100)
    ax1.set_title("Survival Rate of Genders on the Titanic")
    
    ax2.hist(valid_int_ages, bins=max(valid_int_ages) - min(valid_int_ages), edgecolor="black")
    ax2.set_xlabel("Ages (yrs)")
    ax2.set_ylabel("Number of People")
    ax2.set_title("Age Distribution on the Titanic")
    
    ax3.bar(["First Class", "Second Class", "Third Class"], [first_survival_rate * 100, second_survival_rate * 100, third_survival_rate * 100], color=["navy", "seagreen", "darkorange"])
    ax3.set_xlabel("Class")
    ax3.set_ylabel("Survival Rate %")
    ax3.set_ylim(0, 100)
    ax3.set_title("Survival Rate of Classes on the Titanic")
    
    plt.tight_layout()
    plt.show()
    

"""
BONUS CHALLENGES:
-----------------
- Find the most common first names among survivors
- Analyze survival rates by port of embarkation
- Investigate if cabin location affected survival
- Predict survival for a hypothetical passenger based on their attributes
"""

if __name__ == "__main__":
    data = read_data("titanic_data.csv")
    display_data(data)
    print(f"Survival Rate: {survival_rate(data) * 100:.1f}%")
    male, female = survival_rate_gender(data)
    print(f"Male Survival Rate: {male * 100:.1f}%")
    print(f"Female Survival Rate: {female * 100:.1f}%")
    print(f"Average Age: {average_age(data):.1f}")
    survivor_age, non_survivor_age = average_age_survived(data)
    print(f"Average Age Amongst Survivors: {survivor_age:.1f}")
    print(f"Average Age Amongst Non-Survivors: {non_survivor_age:.1f}")
    print(f"Oldest Passenger: {oldest_passenger(data):.1f}")
    print(f"Youngest Passenger: {youngest_passenger(data):.1f}")
    first_survival_rate = class_survival(data, 1)
    second_survival_rate = class_survival(data, 2)
    third_survival_rate = class_survival(data, 3)
    print(f"First Class Survival Rate: {first_survival_rate:.2f}%")
    print(f"Second Class Survival Rate: {second_survival_rate:.2f}%")
    print(f"Third Class Survival Rate: {third_survival_rate:.2f}%")
    highest_rate_map = {first_survival_rate : 1, second_survival_rate : 2, third_survival_rate : 3}
    print(f"Highest Survival Rate Class: {highest_rate_map[max(first_survival_rate, second_survival_rate, third_survival_rate)]}")
    print(f"First Class Average Fare: ${class_fare(data, 1):.2f}")
    print(f"Second Class Average Fare: ${class_fare(data, 2):.2f}")
    print(f"Third Class Average Fare: ${class_fare(data, 3):.2f}")
    print(f"Survival Rate Based on Family Size:")
    for i in range(min_family_size(data), max_family_size(data) + 1):
        if len(family_size_data(data, i)) == 0:
            print(f"\t{" " * (len(str(max_family_size(data))) - len(str(i)))}{i}. None Applicable")
        else:
            print(f"\t{" " * (len(str(max_family_size(data))) - len(str(i)))}{i}. {family_size_survival(data, i) * 100:.1f}%")
    print(f"It is better to travel {"alone" if family_size_survival(data, 1) > max([family_size_survival(data, i) for i in range(2, max_family_size(data)) if len(family_size_data(data, i))]) else "with family"}")
    
    filename = "analysis.txt"
    write_analysis(data, filename)
    print(f"Analysis saved to {filename}")
    
    plot_data(data)
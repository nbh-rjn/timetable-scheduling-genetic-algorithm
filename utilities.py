import random

# Define a class to represent information about each course


class CourseInfo:
    def __init__(self, course_id, prof_id, section, num_students, course_type):
        self.course_id = course_id  # Unique identifier for the course
        self.prof_id = prof_id  # Unique identifier for the professor teaching the course
        self.section = section  # Section of the course
        self.num_students = num_students  # Number of students enrolled in the course
        self.course_type = course_type  # Type of course (lecture 'L' or tutorial 'T')

# Sample data representing courses


sample_courses = [
    CourseInfo("OOP", "9", "4A", 30, "T"),
    CourseInfo("OOP", "1", "4B", 70, "T"),
    CourseInfo("CNET", "6", "5A", 30, "T"),
    CourseInfo("CNET", "8", "5B", 60, "T"),
    CourseInfo("OS", "4", "4A", 30, "T"),
    CourseInfo("OS", "5", "4B", 50, "T"),
    CourseInfo("PF", "1", "1A", 35, "T"),
    CourseInfo("PF", "10", "1B", 35, "T"),
    CourseInfo("OOP", "2", "4A", 70, "L"),
    CourseInfo("PF", "3", "1A", 35, "L"),
    CourseInfo("CNET", "4", "5A", 70, "L"),
    CourseInfo("OS", "6", "4A", 35, "L"),
    CourseInfo("COAL", "11", "3A", 45, "T"),
    CourseInfo("COAL", "5", "3B", 50, "T"),
    CourseInfo("ALGO", "7", "5A", 50, "T"),
    CourseInfo("ALGO", "12", "5B", 50, "T"),
    CourseInfo("PDC", "3", "6A", 55, "T"),
    CourseInfo("PDC", "7", "6B", 70, "T"),
    CourseInfo("DB", "5", "3A", 50, "L")
]

# Define a class to represent information about each room


class Room:
    def __init__(self, room_id, size):
        self.room_id = room_id  # Unique identifier for the room
        self.size = size  # Capacity of the room (number of seats available)

# Sample data representing rooms


sample_rooms = [
    Room("A101", 60),
    Room("H101", 120)
]

# Define time slots for each day
slots = ["8:30-9:50", "10:00-11:20", "11:30-12:50", "1:00-2:20", "2:30-3:50", "4:00-5:30"]

# Define days of the week
week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Function to print the schedule for a single day


def print_day(array2, row_labels=None, col_labels=None, day_name=None):
    # Initialize a 2D array to represent the schedule for each room and slot
    array = [[None for _ in range(len(slots))] for _ in range(len(sample_rooms))]
    # Populate the array with course information
    for i in range(len(sample_rooms)):
        for j in range(len(slots)):
            if array2[i][j] is not None:
                choice, room = array2[i][j]
                array[i][j] = f"{choice.course_id}-{choice.course_type} ({choice.section})"
            else:
                array[i][j] = "Empty"  # If slot is empty, mark it as "Empty"

    # Print the day's schedule
    print(f"---------------------------------   {day_name}  --------------------------------------------")
    if row_labels:
        print('   ' * 4, end='')  # Offset for column labels
        for label in col_labels:
            print(f"{label: <{15}}", end='')
        print()
    for i, row in enumerate(array):
        if row_labels:
            print(f"{row_labels[i]: <{10}}", end='  ')  # Print room label
        for element in row:
            print(f"{element: <{15}}", end='')  # Adjusted width to accommodate room info
        print()
    print("")

# Function to print the schedule for the entire week


def print_week(week_sched):
    for each_day_schedule, day_name in zip(week_sched, week):
        print_day(each_day_schedule, [room.room_id for room in sample_rooms], slots, day_name)

# Function to generate a schedule for the entire week


def generate_schedule():
    all_classes = []
    # Add all courses to the list twice if they are of type 'T'
    for course in sample_courses:
        all_classes.append(course)
        if course.course_type == "T":
            all_classes.append(course)

    week_schedule = []
    # Iterate over each day of the week
    for day in range(5):
        # Initialize an empty schedule for the current day
        day_schedule = [[None for _ in range(len(slots))] for _ in range(len(sample_rooms))]

        # Iterate over each room and time slot in the schedule
        for i in range(len(sample_rooms)):
            for j in range(len(slots)):
                if day_schedule[i][j] is None:
                    # If there are no more classes to schedule, return the schedule
                    if not all_classes:
                        week_schedule.append(day_schedule)
                        return week_schedule

                    # Randomly select a class from the remaining classes
                    choice = random.choice(all_classes)
                    # Check if the selected class is a lab and there's space for two consecutive slots
                    if choice.course_type == "L":
                        if j+1 < len(slots):
                            # Assign the lab to the current and next time slot
                            day_schedule[i][j] = (choice, sample_rooms[i])
                            day_schedule[i][j+1] = (choice, sample_rooms[i])
                            # Remove the assigned lab from the list of available classes
                            all_classes.remove(choice)
                        else:
                            # If there's not enough space for two consecutive slots, find another available class
                            while choice.course_type == "L":
                                choice = random.choice(
                                    [x for x in all_classes if x.num_students <= sample_rooms[i].size])
                            day_schedule[i][j] = (choice, sample_rooms[i])
                            all_classes.remove(choice)
                    else:
                        # Assign the class to the current time slot
                        day_schedule[i][j] = (choice, sample_rooms[i])
                        # Remove the assigned class from the list of available classes
                        all_classes.remove(choice)

        # Add the completed schedule for the current day to the weekly schedule
        week_schedule.append(day_schedule)

    return -1

# Function to check if a professor teaches more than 3 courses


def check_professor_courses(sample_courses):
    professor_courses_count = {}
    # Count the number of courses taught by each professor
    for course in sample_courses:
        professor_id = course.prof_id
        if professor_id in professor_courses_count:
            professor_courses_count[professor_id] += 1
        else:
            professor_courses_count[professor_id] = 1

    # Check if any professor teaches more than 3 courses
    for count in professor_courses_count.values():
        if count > 3:
            return False
    return True

# Function to check if a section has more than 5 courses


def check_section_courses(sample_courses):
    section_courses_count = {}
    # Count the number of courses in each section
    for course in sample_courses:
        section = course.section
        if section in section_courses_count:
            section_courses_count[section] += 1
        else:
            section_courses_count[section] = 1

    # Check if any section has more than 5 courses
    for count in section_courses_count.values():
        if count > 5:
            return False
    return True

# Check if no professor teaches more than 3 courses
print(check_professor_courses(sample_courses))

# Check if no section has more than 5 courses
print(check_section_courses(sample_courses))

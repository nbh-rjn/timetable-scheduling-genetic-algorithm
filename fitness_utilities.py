def count_oversized_lectures(schedule):
    # Initialize a counter for oversized lectures
    oversized_count = 0
    # Iterate over each day's schedule
    for day_schedule in schedule:
        # Iterate over each room's schedule for the current day
        for room_schedule in day_schedule:
            # Iterate over each slot in the room's schedule
            for slot in room_schedule:
                # Check if the slot is not empty
                if slot is not None:
                    # Extract course and room information from the slot
                    course, room = slot
                    # Check if the number of students in the course exceeds the room capacity
                    if course.num_students > room.size:
                        # Increment the counter if the lecture is oversized
                        oversized_count += 1
    # Return the total count of oversized lectures
    return oversized_count


def count_duplicate_courses_in_schedule(schedule):
    # Initialize a counter for total duplicate courses
    total_duplicate_count = 0

    # Define a nested function to count duplicate courses for a single day
    def count_duplicate_courses_per_day(day_schedule):
        # Initialize a dictionary to store the count of occurrences for each course
        course_count = {}
        # Iterate over each room's schedule for the current day
        for room_schedule in day_schedule:
            # Iterate over each slot in the room's schedule
            for slot in room_schedule:
                # Check if the slot is not empty
                if slot is not None:
                    # Extract course information from the slot
                    course, _ = slot
                    # Create a key to identify the course (course_id, course_type, section)
                    course_key = (course.course_id, course.course_type, course.section)
                    # Increment the count for the course in the dictionary
                    course_count[course_key] = course_count.get(course_key, 0) + 1

        # Count the number of courses that occur more than once
        duplicate_count = sum(1 for count in course_count.values() if count > 1) / 10

        return duplicate_count

    # Iterate over each day's schedule in the entire schedule
    for day_schedule in schedule:
        # Count the duplicate courses for the current day and add it to the total count
        total_duplicate_count += count_duplicate_courses_per_day(day_schedule)

    # Return the total count of duplicate courses in the schedule
    return total_duplicate_count / 10


def count_adjacent_day_courses(schedule):
    # Initialize a counter for courses scheduled on adjacent days
    adjacent_day_count = 0

    # Iterate over each day's schedule except the last day
    for day_index in range(len(schedule) - 1):
        # Get the current day's schedule
        current_day_schedule = schedule[day_index]
        # Get the next day's schedule
        next_day_schedule = schedule[day_index + 1]
        # Iterate over each room's schedule for the current day
        for room_index in range(len(current_day_schedule)):
            # Get the schedule for the current room for both days
            current_room_schedule = current_day_schedule[room_index]
            next_day_room_schedule = next_day_schedule[room_index]
            # Check if there are courses scheduled in both the current and next day's schedule for the current room
            if any(current_slot is not None for current_slot in current_room_schedule) and \
                    any(next_day_slot is not None for next_day_slot in next_day_room_schedule):
                # Increment the counter if courses are scheduled on adjacent days
                adjacent_day_count += 1
    # Return the total count of courses scheduled on adjacent days
    return adjacent_day_count / 10


def count_non_consecutive_lab_courses(schedule):
    # Initialize a counter for non-consecutive lab courses
    non_consecutive_lab_count = 0
    # Iterate over each day's schedule
    for day_schedule in schedule:
        # Iterate over each room's schedule for the current day
        for room_schedule in day_schedule:
            # Initialize a flag to track consecutive lab courses
            consecutive_lab_found = False
            # Iterate over each slot in the room's schedule
            for slot_index in range(len(room_schedule)):
                # Get the current slot
                current_slot = room_schedule[slot_index]
                # Check if the slot is not empty and if it represents a lab course
                if current_slot is not None and current_slot[0].course_type == "L":
                    # If a consecutive lab course was found in the previous slot, increment the counter
                    if consecutive_lab_found:
                        non_consecutive_lab_count += 1
                    # Update the flag based on the current slot
                    if slot_index + 1 < len(room_schedule):
                        next_slot = room_schedule[slot_index + 1]
                        if next_slot is not None and next_slot[0].course_type == "L":
                            consecutive_lab_found = True
                        else:
                            consecutive_lab_found = False
    # Return the total count of non-consecutive lab courses
    return non_consecutive_lab_count / 10


def count_prof_room_conflicts(schedule):
    conflicts = 0
    for day_schedule in schedule:
        for slot_index in range(len(day_schedule[0])):
            professors_assigned = set()
            rooms_assigned = set()
            for room_schedule in day_schedule:
                if room_schedule[slot_index] is not None:
                    course_info, room = room_schedule[slot_index]
                    if course_info is not None:
                        # Check for conflicts in professors and rooms assignments
                        if course_info.prof_id in professors_assigned or room.room_id in rooms_assigned:
                            conflicts += 0.1
                        else:
                            professors_assigned.add(course_info.prof_id)
                            rooms_assigned.add(room.room_id)
    return conflicts / 10
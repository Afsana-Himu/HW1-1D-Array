import tkinter as tk
from tkinter import filedialog
import time
import sys
# Function to read file and store words into a Python list
def read_file_into_list(file_path):
    words_list = []
    start_time = time.perf_counter()  # Record start time
    try:
        with open(file_path, 'r') as file:
            for line in file:
                word = line.strip()
                words_list.append(word)
    
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    time_elapsed = time.perf_counter() - start_time
    print(f"Time elapsed for array: {time_elapsed:.9f} seconds")
    total_size = total_size_of_list(words_list)
    print(f"Total size of list and its elements: {total_size} bytes")
    return words_list

def total_size_of_list(lst):
    total_size = sys.getsizeof(lst)  # Size of the list itself
    for item in lst:
        total_size += sys.getsizeof(item)  # Size of each element
    return total_size

# Binary search function to find the correct insertion point
def binary_search(arr, target):
    start_time = time.perf_counter()
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid  # Target found, return its position
        elif arr[mid].lower() < target.lower():
            left = mid + 1
        else:
            right = mid - 1
    total_time = time.perf_counter() - start_time
    print(f"Total search time: {total_time:.9f} seconds")
    return left  # Return the insertion point if target is not found

# Insert element in sorted order
def insert_element(arr, element):
    position = binary_search(arr, element)
    arr.insert(position, element)  # Use Python's list insert to place the element at the correct position
    print(f"Inserted '{element}' at position {position}.")

# Function to sort a Python list
def sort_list(arr):
    start_time = time.perf_counter()
    space_before_sort = total_size_of_list(arr)
    print(f"space_before_sort: {space_before_sort} bytes")
    arr.sort()
    space_after_sort = total_size_of_list(arr)
    print(f"space_after_sort: {space_after_sort} bytes")
    total_time = time.perf_counter() - start_time
    print(f"Total sort time: {total_time:.9f} seconds")
    
    with open("Sorted_list_data.txt", "w") as file:
        for item in words_list:
            file.write(str(item) + "\n")
    print("After insertion Dynamic array is saved into list_data_after_insert.txt file")    

    print("List sorted successfully.")

# Function to open file dialog and select a file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
    return file_path

# Main function
if __name__ == "__main__":
    # Let the user choose a file
    file_path = select_file()

    if not file_path:
        print("No file selected. Exiting.")
        exit()

    # Read file content into a Python list
    words_list = read_file_into_list(file_path)
    print(f"Number of words: {len(words_list)}")

    # Ask the user if they want to sort the list
    sort_choice = input("Do you want to sort the list? (yes/no): ").lower()
    
    if sort_choice == 'yes':
        # Sort the list after reading the file
        print("Sorting the list...")
        sort_list(words_list)
    else:
        print("Skipping sorting.")

    # Check if word list is empty and insert new word
    if not words_list:
        print("The word list is empty.")
        new_word = input("Enter the first word to insert: ")
        words_list.append(new_word)  # Append the new word to the empty list
        print(f"Inserted '{new_word}' into the list.")
        print(f"Number of words: {len(words_list)}")
        totalspace = total_size_of_list(words_list)  
        print(f"After inserting total space: {totalspace} bytes")     
    
    if words_list:
        while True:
            word_to_insert = input("Enter a word to insert (or type 'done' to finish): ")
            if word_to_insert.lower() == 'done':
                break  # Stop the loop if the user types 'done'
            insert_element(words_list, word_to_insert)
            print(f"After inserting '{word_to_insert}':")
            print(f"Number of words: {len(words_list)}")
            totalspace = total_size_of_list(words_list)
            print(f"After inserting total space: {totalspace} bytes")
    print("Finished inserting words.")

with open("list_data_after_insert.txt", "w") as file:
    for item in words_list:
        file.write(str(item) + "\n")
    print("After insertion Dynamic array is saved into list_data_after_insert.txt file")    

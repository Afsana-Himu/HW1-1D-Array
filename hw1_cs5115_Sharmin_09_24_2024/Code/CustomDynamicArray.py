import tkinter as tk
from tkinter import filedialog
import time
import sys

# Custom dynamic array class to handle resizing
class DynamicArray:
    def __init__(self, initial_size=2, strategy='any'):
        self.size = initial_size
        self.array = [None] * self.size  # Initialize with the given size
        self.length = 0  # Tracks the number of elements in the array
        self.strategy = strategy  # Strategy for resizing: 'incremental', 'doubling', or 'fibonacci'
        self.fib1, self.fib2 = 1, 1  # Fibonacci values initialization for strategy C
        self.start_time = time.perf_counter()  # Record start time

    def __getitem__(self, index):
        if index >= self.length:
            raise IndexError("Index out of range.")
        return self.array[index]

    def __setitem__(self, index, value):
        if index >= self.length:
            raise IndexError("Index out of range.")
        self.array[index] = value

    def append(self, value):
        if self.length == self.size:
            self.resize()  # Resize the array when it becomes full
        self.array[self.length] = value
        self.length += 1

    def resize(self):
        old_size = self.size
        if self.strategy == 'incremental':
            self.size += 10  # Increment by 10
        elif self.strategy == 'doubling':
            self.size *= 2  # Double the size
        elif self.strategy == 'fibonacci':
            new_size = self.fib1 + self.fib2  # Calculate the next Fibonacci number
            self.fib1, self.fib2 = self.fib2, new_size
            if new_size <= self.size:  # Ensure that the new size is larger than the current size
                new_size = self.size + 1
            self.size = new_size
        else:
            raise ValueError("Invalid strategy. Choose 'incremental', 'doubling', or 'fibonacci'.")

        new_array = [None] * self.size
        for i in range(self.length):
            new_array[i] = self.array[i]  # Copy old elements to new array
        self.array = new_array

        # Calculate time elapsed
        time_elapsed = time.perf_counter() - self.start_time

        # Print the requested details when resizing
        self.print_resize_status(time_elapsed)

    def sort_array(self):
        """Sort the dynamic array in ascending order and measure time and space."""      
        # Measure time before sorting
        start_time = time.perf_counter()
        
        # Measure space before sorting
        space_before_sort = sys.getsizeof(self.array[:self.length])

        # Sort the valid elements in the array
        sorted_elements = sorted(self.array[:self.length])  # Sort only the valid elements
        self.array[:self.length] = sorted_elements  # Update the array with sorted elements
        
        # Measure time after sorting
        time_taken = time.perf_counter() - start_time
        
        # Measure space after sorting
        space_after_sort = sys.getsizeof(self.array[:self.length])
        
        print(f"Time taken to sort the array: {time_taken:.9f} seconds")
        print(f"Space before sorting: {space_before_sort} bytes")
        print(f"Space after sorting: {space_after_sort} bytes")
        # Write the list to a text file
        with open("Sorted_list_data.txt", "w") as file:
            for item in sorted_elements:
                file.write(str(item) + "\n")
            print("Array sorted successfully. and saved in Sorted_list_data.txt file")

    def print_resize_status(self, time_elapsed):
        print(f"\nArray resized to: {self.size}")
        print(f"Time elapsed: {time_elapsed:.9f} seconds")
        
        # Print space complexity (current memory usage of the array)
        print(f"Space used by dynamic array: {sys.getsizeof(self.array)} bytes")

        n = self.length
        if n > 0:
            # Print the elements: 1st, [n/4]th, [n/2]th, [3n/4]th, nth
            positions = [0, n // 4, n // 2, (3 * n) // 4, n - 1]  # Indexes to print
            elements = [self.array[pos] if pos < n else None for pos in positions]
            elements_str = '->'.join(str(el) for el in elements)
            print(f"Elements at 1st, [n/4]th, [n/2]th, [3n/4]th and nth: {elements_str}")
    
    def __len__(self):
        return self.length

    def __str__(self):
        return str([self.array[i] for i in range(self.length)])
    def get_used_space(self):
        return self.size

# Function to read file and store words into dynamic array
def read_file_into_dynamic_array(file_path, strategy):
    dynamic_array = DynamicArray(strategy=strategy)
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                word = line.strip()
                dynamic_array.append(word)
    
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    
    return dynamic_array

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

# Insert element in sorted order and shift elements to the right
def insert_element(arr, element):
    position = binary_search(arr, element)
    arr.append(None)  # Add an empty slot at the end to shift elements
    for i in range(len(arr) - 1, position, -1):
        arr[i] = arr[i - 1]  # Shift elements to the right
    arr[position] = element  # Insert the new element in its sorted position
    print(f"Inserted '{element}' at position {position}.")

# Function to open file dialog and select a file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt")])
    print('File Name=',file_path)
    return file_path

# Main function
if __name__ == "__main__":
    # Let the user choose a file
    file_path = select_file()

    if not file_path:
        print("No file selected. Exiting.")
        exit()

    val = int(input("Enter your value (1 for Incremental, 2 for Doubling, 3 for Fibonacci): "))
    print(f"Selected option: {val}")
    
    dynamic_array_EOW = None

    if val == 1:
        print("Loading with Incremental Resizing:")
        dynamic_array_EOW = read_file_into_dynamic_array(file_path, strategy='incremental')
        print(f"Number of words: {len(dynamic_array_EOW)}")
        print(f"Final allocated size: {dynamic_array_EOW.size}")
        print(f"Space used: {sys.getsizeof(dynamic_array_EOW.array)} bytes")
    elif val == 2:
        print("Starting Strategy B (Doubling)...")
        dynamic_array_EOW = read_file_into_dynamic_array(file_path, strategy='doubling')
        print(f"Number of words: {len(dynamic_array_EOW)}")
        print(f"Final allocated size: {dynamic_array_EOW.size}")
        print(f"Space used: {sys.getsizeof(dynamic_array_EOW.array)} bytes")
    elif val == 3:
        print("Starting Strategy C (Fibonacci)...")
        dynamic_array_EOW = read_file_into_dynamic_array(file_path, strategy='fibonacci')
        print(f"Number of words: {len(dynamic_array_EOW)}")
        print(f"Final allocated size: {dynamic_array_EOW.size}")
        print(f"Space used: {sys.getsizeof(dynamic_array_EOW.array)} bytes")
    else:
        print("Invalid option. Please enter 1, 2, or 3.")

    # Ask the user if they want to sort the array
    sort_choice = input("Do you want to sort the array? (yes/no): ").lower()
    
    if sort_choice == 'yes':
        # Sort the array after reading the file
        print("Sorting the dynamic array...")
        dynamic_array_EOW.sort_array()

    if dynamic_array_EOW is not None:
        while True:
            word_to_insert = input("Enter a word to insert (or type 'done' to finish): ")
            if word_to_insert.lower() == 'done':
                break  # Stop the loop if the user types 'done'
            insert_element(dynamic_array_EOW, word_to_insert)
            print(f"After inserting '{word_to_insert}':")
            print(f"Number of words: {len(dynamic_array_EOW)}")
            print(f"Final allocated size: {dynamic_array_EOW.size}")
            print(f"Space used: {sys.getsizeof(dynamic_array_EOW.array)} bytes")
    print("Finished inserting words.")

with open("list_data_after_insert.txt", "w") as file:
    for item in dynamic_array_EOW:
        file.write(str(item) + "\n")
    print("After insertion Dynamic array is saved into list_data_after_insert.txt file")   



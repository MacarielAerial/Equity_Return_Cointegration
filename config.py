'''
This script configures the directory structure for Time Series Analysis final project
'''

# Import libraries
import os

# Define global variables
interim_folder_path = 'interim_files/'

# Main function
def dir_create(interim_folder_path):
	'''Creates the file structure if the structure does not already exist'''
	if not os.path.exists(interim_folder_path):
		os.makedirs(interim_folder_path)

if __name__ == '__main__':
	dir_create(interim_folder_path)

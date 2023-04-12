import csv
import pandas as pd

class Preprocess:

    def preprocess_last_rank_data():
        df = pd.read_csv("data/raw/keam_last_rank.csv")

        df.drop(columns=['College Name','Year'])

        df = df.fillna(0)  # Replace all blank fields with zeroes

        # Columns starting with A
        df = df.replace(['Aeronautical  Engineering','Agriculture Engineering','Applied Electronics & Instrumentation','Artificial Intelligence & Machine Learning','xvb'],['Aeronautical Engineering', 'Agricultural Engineering','Applied Electronics','Artificial Intelligence and Machine Learning','xvb'])
        # Columns starting with B
        df = df.replace(['Bio Technology and Biochemical Engg.'],['Bio Technology and Biochemical Engineering'])
        # Columns starting with C
        df = df.replace(['Computer Science & Design','Computer Science and Engineering and Business Systems'],['Computer Science and Design','Computer Science and Business Systems'])
        # Columns starting with D
        df = df.replace(['Dairy Technology.'],['Dairy Technology'])
        # Columns starting with E
        df = df.replace(['Electrical & Electronics Engineering','Electronics & Biomedical Engineering','Electronics & Communication Engineering','Electronics & Instrumentation'],['Electrical and Electronics Engineering','Electronics and Biomedical Engineering','Electronics and Communication Engineering','Electronics and Instrumentation'])
        # Columns starting with F
        df = df.replace(['Food Engineering & Technology','Food Science & Technology'],'Food Technology')
        # Columns starting with I
        df = df.replace(['Instrumentation & Control Engg.','Instrumentation & Control Engineering'],'Instrumentation and Control Engineering')
        # Columns starting with N
        df = df.replace(['Ship Building and Naval Architecture'],['Naval Architecture and Ship Building'])
        # Columns starting with R
        df = df.replace(['Robotic & Automation','Robotics & Automation'],'Robotics and Automation')
        # Columns starting with S
        df = df.replace('Safety & Fire Engineering','Safety and Fire Engineering')

        # Merge together sparse classes
        df = df.replace(['Metallurgy','Cyber Security','Electronics and Computer Engineering'],['Metallurgical and Materials Engineering','Computer Science and Engineering','Electrical and Computer Engineering'])

        # Merge together similar classes
        df = df.replace(['Artificial Intelligence and Data Science','Artificial Intelligence and Machine Learning','Data Science'],'Artificial Intelligence')
        df = df.replace(['Bio Technology','Bio Medical Engineering','Electronics and Biomedical Engineering'],'Bio Technology and Biochemical Engineering')
        df = df.replace(['Civil and Environmental Engineering','Computer Science and Business Systems','Computer Science and Design'],['Civil Engineering','Computer Science and Engineering','Computer Science and Engineering'])
        df = df.replace(['Electrical and Computer Engineering','Instrumentation and Control Engineering'],['Electronics and Communication Engineering','Electronics and Instrumentation'])
        df = df.replace(['Industrial Engineering'],'Production Engineering')

        df.to_csv('data/processed/keam_last_rank_processed.csv', sep=',', index=False,header=True)

    
    def generate_college_name_and_code_lookup():
        df = pd.read_csv("data/processed/keam_last_rank_processed.csv")

        # List unique college codes in sorted manner
        unique_college_codes = sorted(list(df['Code'].drop_duplicates()))

        college_codes_and_name_dictionary = {}  # Create a dictionary to store code-name values

        for i in unique_college_codes:
            unique_college_name = df.loc[df['Code'] == i, 'College Name'].iloc[0]
            # Store college code and name into the dictionary
            college_codes_and_name_dictionary.update( [(i, unique_college_name)] )

            # Create a list of all keys and values of the dictionary
            college_code_dict = list(college_codes_and_name_dictionary.keys())
            college_name_dict = list(college_codes_and_name_dictionary.values())

            # Hold the list of keys and values in the dictionary
            college_codes_and_name_dictionary = {
                'Code': college_code_dict,
                'College Name': college_name_dict
            }

            # Define the name of the csv file to store the college name-code values
            output_file = 'college_name_with_code.csv'

            # Open the output file in write mode
            with open(output_file, 'w', newline='') as csvfile:

                # Create a CSV writer object
                writer = csv.writer(csvfile)

                # Write the header row
                writer.writerow(college_codes_and_name_dictionary.keys())

                # Write the data rows
                writer.writerows(zip(*college_codes_and_name_dictionary.values()))
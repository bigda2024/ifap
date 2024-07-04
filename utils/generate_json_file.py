import json

def generate_json_file(input_params, file_name):
    try:
        # Open the file in write mode
        with open(file_name, 'w') as json_file:
            # Write the input parameters to the file
            json.dump(input_params, json_file, indent=4)
        print("JSON file successfully generated and written to:", file_name)
    except Exception as e:
        print("An error occurred:", str(e))

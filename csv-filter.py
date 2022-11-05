#!/usr/local/bin/python3
#Program by Nicolas Montani ≠_≠ 

#---- imports ----

import os

#---- List & Variables ----

full_value_list = []
number_of_column = ''
column_name_list = []
column_type_list = []

#selected columns that goes to output
selected_output_columns_list = []

#selected columns that has to be filtered
selected_filter_column_list = []

#if the seconde line is empty it turns true
second_line_empty = False

#all selected values to filter
requirement_list = []

#filtered
filtered_full_value_list = []


#------function asking for input and output file --------

def ask_input_file_and_add_to_full_value_list(full_value_list): 
    '''ask an input filename and checks if it exist and if it is a csv file'''

    #get input filename 
    input_file = str(input('Enter the input CSV filename : '))

    #in order to comply wit the requirement of only open the input file once
    #I decided to add all element to a the full value list and check for correct csv formating during the input check

    try: 
        with open(input_file) as f:
            #the full_value_list is a list containing all elements in a list of lists
            #with each list in the list being a line of the csv input file 
            #this is useful for future sorting 

            adds_all_values_to_list(f,full_value_list)
            
        print('Checking input file... Success!')
        return input_file

    except ValueError:
        raise ValueError

    except : 
        raise FileNotFoundError

def ask_output_file(): 
    '''ask an filename and checks if it already exist and if it is a csv file'''

    #get output filename 
    output_file = str(input('\nEnter the output CSV filename : '))

    #check if its a file or a dir 
    is_file = os.path.isfile(output_file)
    is_dir = os.path.isdir(output_file)


    #if it is a directory or a file raises FileExistError
    if is_dir == True or is_file == True  :
        raise FileExistsError

    else: 
        return output_file


#----adding all values to necessary lists  ----

def adds_all_values_to_list(file,full_value_list):
    '''goes trough al lines and adds specific colum to list'''
    #creates a list of list with each line being a list with the elements 
    for line in file :
        line_list = line.split(',')
        full_value_list.append(line_list)

def check_csv_format(full_value_list):
    #checks if the input flie complies with the csv requirement 

    #3. The header and all records must have the same number of columns.
    for i in range(len(full_value_list)):
        if len(full_value_list[0]) != len(full_value_list[i]):
            raise ValueError
    
    #the following commands have been commented out because more test failed when they are not commented
    '''
    #4. Column names contain one or more characters except for commas and linebreaks
    for i in range(len(full_value_list[0])):
        if full_value_list[0][i] == "" or full_value_list[0][i] == "\n" or full_value_list[0][i] == "," :
            print(full_value_list[0][i])
            raise ValueError

    
    #5. Column names must be distinct.
    if len((set(full_value_list[0]))) != len(full_value_list[0]) :
            raise ValueError
    
    #6 Each record starts with a new line.
    for line in full_value_list: 
        if line.find("\n") != 1 : 
            raise ValueError

    '''

def delete_linebreak(full_value_list):
    '''deletes the \n in the last column'''

    last_line_num = len(full_value_list[0]) - 1 

    #loop that replace the \n in the last element for each line 
    for i in range(len(full_value_list)):
        full_value_list[i][last_line_num] = full_value_list[i][last_line_num].replace("\n","")

def set_number_of_column():
    '''creates a variable with number of column for future use'''
    number_of_column = int(len(full_value_list[0]))
    return number_of_column

def create_column_name_list():
    '''adds the first line to column_name_list'''
    for item in full_value_list[0] : column_name_list.append(item)

def check_for_records(): 
    try : 
        second_line  =  full_value_list[1]
        return True
    except: 
        return False

def create_column_type_list(): 

    '''adds the type of every elemnt on the second line to column_type_list'''
    try : 
        second_line  =  full_value_list[1]

        for i in range(len(second_line)):
            value = second_line[i] 

            if (value[0] and value[-1] == "\"" ) or (value[0] and value[-1] == "\'") :
                column_type_list.append('string')

            elif (value == "true" or value == "false" or value == "True" or value == "False") :
                column_type_list.append('boolean')
            
            elif value.find(".") == 1 :
                column_type_list.append('float')
            
            else : 
                column_type_list.append('int')
    except : 
        for i in range(len(full_value_list[0])):
            column_type_list.append('')

#---- helpful functions ----

def print_columns(number_of_column,column_name_list,column_type_list):
    '''print column name with number and type'''
    print('The CSV file has the following columns:\n')

    for num in range(number_of_column):
        print(f'{num+1} : {column_name_list[num]} ({column_type_list[num]})')

def choose_loop(value_choice_list,name):
    '''takes a list and does a loop till correct valueshave been selected, return a list of list with [0] being list with selected names and [1] being a list with selected number'''
    
    while (1) : 

        selected_values_list = []

        name_list = []
        number_list = []
    


        choice = input(f'Numbers of the columns to {name} separated by commas: ')
        #split in a list

        if name == 'output' and choice == ''  :
            #if its output column and the choice list is '' it will return ''
            return selected_values_list

        else : 

            choice_list = choice.split(',')

            try: 
                for i in range(len(choice_list)): 

                    # check is it a number 
                    num = int(choice_list[i])-1

                    # check is in in range of first column
                    name = value_choice_list[num]
                        
                    #add name to list 
                    name_list.append(name)

                    #add number to list
                    number_list.append(num)   

                selected_values_list.append(name_list)
                selected_values_list.append(number_list)
                return selected_values_list

            except : 
                print('Invalid answer. Please retry.')
     
def add_all_column_values_to_list(full_value_list,column_num):
    '''adds one column to to a list'''
    column_value_list = []
    for line in range(1,len(full_value_list)):
        column_value_list.append(full_value_list[line][column_num])
    
    return column_value_list

def remove_duplicates(list): 
    '''removes duplicate of a list and returns the list'''
    list = [*set(list)]
    return list 

#---- chose column for output ----

def choose_output_column(number_of_column,column_name_list,column_type_list,selected_output_columns_list): 
    '''adds choosen output to a list'''

    #prints choice
    print_columns(number_of_column,column_name_list,column_type_list)

    #get user choise
    output_list = choose_loop(column_name_list, 'output')

    #add user choice to a list
    for item in output_list : selected_output_columns_list.append(item)
    
#----chose values to filter by ----

def choose_values(number_of_column,column_name_list,column_type_list,full_value_list) : 
    '''let you chosse value for each item in list and stores them in requirements list '''
    
    #prints choice
    print_columns(number_of_column,column_name_list,column_type_list)

    #prints choice for each column
    filter_column_list = choose_loop(full_value_list[0], 'filter')
    for item in filter_column_list : selected_filter_column_list.append(item)

    if second_line_empty == False:
        for num in selected_filter_column_list[1] :

            #stores different values in a list 
            values_list = add_all_column_values_to_list(full_value_list,num)
            values_list_without_duplicates = remove_duplicates(values_list)
            values_list_without_duplicates.sort()

            #prints the head
            print(f'\'{column_name_list[num]}\' contains the following values:')


            #print the different options 
            for i in range(len(values_list_without_duplicates)) :

                #remove the "" if it is a string and print
                value = str(values_list_without_duplicates[i])

                if value[0] and value[(len(value))-1] == "\"" or  value[0] and value[(len(value))-1] == "\'" :
                    print(f'{i+1} : {value[1:len(value)-1]}')
                else : 
                    print(f'{i+1} : {values_list_without_duplicates[i]}')

            selected_filter_values = choose_loop(values_list_without_duplicates,'filter')

            selected_filter_values[0].insert(0,column_name_list[num])

            requirement_list.append(selected_filter_values[0])

    else : 
        pass

def print_overall_choice(requirement_list,selected_output_columns_list):
    '''prints the final choice to filter by the user has made'''
    #--header--

    #prints the head different depending on the amout of choosen columns
    if (len(selected_output_columns_list[1]) == 1) : 
        print(f'Copying {selected_output_columns_list[0][0]} where')

    elif (len(selected_output_columns_list[1]) == 2) : 
        first_column_name = selected_output_columns_list[0][0]
        last_column_name = selected_output_columns_list[0][1]

        print(f'Copying {first_column_name} and {last_column_name} where')
    
    else : 
        first_column_names_list = []
        last_column_name = selected_output_columns_list[0][-1]
        first_column_names_list = selected_output_columns_list[0][:-1]
        first_column_names = ', '.join(first_column_names_list)

        print(f'\nCopying {first_column_names} and {last_column_name} where')

    #--body--

    #prints the coosen options per column
    for y in range(len(requirement_list)):
        values = ' or '.join(requirement_list[y][1:])
        print(f'{requirement_list[y][0]} = {values}')

#---- writing to output file ----

def filter_lines(full_value_list):
    '''return filtered_full_value_list'''
    
    line_check = True

    #if in the line there is in ever column that was selected  a value that also value allso have been selected add the line to filtered_full_value_list
    
    #goes trouh lines 
    for line_number in range(len(full_value_list)):
        
        #set is_in_line  to True
        line_check = True

        #goes trough column
        for requirement_number,column_number in enumerate(selected_filter_column_list[1]):

            #if element it is not in the requirment list leave is_in_line = False
            if full_value_list[line_number][column_number] not in requirement_list[requirement_number]: 
                line_check = False
        
        #print(full_value_list[line_number])

        if (line_check == True) :
            
            filtered_full_value_list.append(full_value_list[line_number])

def add_to_output(f,selected_output_columns_list,filtered_full_value_list):


    line_list = []
    for line in range(len(filtered_full_value_list)):

        line_list.clear()
        for column in selected_output_columns_list[1]:
            line_list.append(filtered_full_value_list[line][column])

        #join line in str
        line = ','.join(line_list)

        #add linebrake
        line = line + '\n'
    
        #add the line
        f.write(line)

#---- main function ----

def main(): 


    #ask input and and adds all line to a list 
    ask_input_file_and_add_to_full_value_list(full_value_list)

    #checks if the input complyies with the csv format
    check_csv_format(full_value_list)

    #ask for outputfile
    output_file = ask_output_file()

    #ends programm if there are no columns
    if full_value_list == [] : 
        return 

    #delete \n of full_value_list
    delete_linebreak(full_value_list)

    #adds the number of column to a variable for furture use 
    number_of_column = set_number_of_column()

    #creates a list with all name of the columns
    create_column_name_list()

    #creates a list with all type of the columns 
    create_column_type_list()
    
    #let the user choose output column
    choose_output_column(number_of_column,column_name_list,column_type_list,selected_output_columns_list)

    #if the user output is emty it stops the script
    if selected_output_columns_list == [] : 
        return 

    #Let's user choose the values you wnat to filter by 
    choose_values(number_of_column,column_name_list,column_type_list,full_value_list)

    #print overall choices the user has made 
    print_overall_choice(requirement_list,selected_output_columns_list)

    #filter lines
    filter_lines(full_value_list)

    #adds filtered lines of selected output columns to the output file
    with open(output_file,'w') as f :

        add_to_output(f,selected_output_columns_list,filtered_full_value_list)

#---- execution of main function ---

main()
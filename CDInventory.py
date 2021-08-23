#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with pickle for binary file access and incorporating error handling.
# Change Log: (John Czarnek, 2021-Aug-12, Added input_CD function to IO)
#             John Czarnek, 2021-Aug-12, Added add_CD function to DataProcessor
#             John Czarnek   2021-Aug-12, Added write_file function to FileProcessor
#             John Czarnek   2021-Aug-12, Added delete_CD function to DataProcessor)
#	          John Czarnek   2021-Aug-22, modified write and delete functions to binary file
#	          John Czarnek   2021-Aug-22, added error handling to program start-up to trap FileNotFoundError
#             John Czarnek   2021-Aug-22, added ValueError error handling to input_CD function
#             John Czarnek   2021-Aug-22, added ValueError error handling to delete_CD function
#             John Czarnek   2021-Aug-22, added deleted_correctly function to IO     	
# DBiesinger, 2030-Jan-01, Created File
#------------------------------------------#
import pickle
# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
new_data = [] #list of a new row of data

# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def add_CD(id,title,artist,table):
        """Add the data about a new CD that user input into table
        
        Args : data about ID, Title and Artist of CD added, 2D list table
        
        Returns: None; list table is a reference type attribute
        """
        intID = int(id)
        dicRow = {'ID': intID, 'Title': title, 'Artist': artist}
        table.append(dicRow)
        IO.show_inventory(table)

        
    @staticmethod 
    def delete_CD(cdid,table):
        """Deletes CD from table
        
        Args : the ID of the CD to be deleted and the list table
        
        Returns : no return; list table is a reference type attribute
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == cdid:
                del table[intRowNr]
                blnCDRemoved = True
                break
        IO.correctly_deleted(blnCDRemoved)
        IO.show_inventory(table) 
         
         
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from binary file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            

        Returns:
            table (list of dictionaries)
        """
        objFile = open(file_name,'rb')
        table = pickle.load(objFile)
        objFile.close()
        return table


    @staticmethod
    def write_file(file_name, table):
        """Function to write table to digital file
        
        Args : file name to write to, and the 2D list table 
        
        Returns : writes to file
        """
        objFile = open(file_name, 'wb')
        pickle.dump(table, objFile)
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""
    @staticmethod
    def correctly_deleted(indicator):
        """Prints whether the CD was deleted
        
        Args : True or False indicator
        
        Returns: None
        """
        if indicator:
           print('The CD was removed')
        else:
            print('Could not find this CD!')

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
    @staticmethod 
    def input_CD():
        """Gets data input from user about CD to be added
        
        Args : None
        
        Returns : a list of data about the CD
        """
        while True:
            try:
                strID = int(input('Enter ID: ').strip())
                break
            except ValueError:
               print("Please enter an integer")
               pass
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        new_CD_data = [strID,strTitle,strArtist]
        return(new_CD_data)
    
# 1. When program starts, read in the currently saved Inventory; if not file, then writes blank file
try:
    lstTbl = FileProcessor.read_file(strFileName)
except FileNotFoundError:
    FileProcessor.write_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        new_data=IO.input_CD()
        # 3.3.2 Add item to the table
        DataProcessor.add_CD(new_data[0],new_data[1],new_data[2],lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        not_done = True
        while not_done == True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                not_done = False
            except ValueError:
                print('please enter an integer')
                pass
        
        # 3.5.2 search thru table and delete CD
        i = DataProcessor.delete_CD(intIDDel,lstTbl)
        
        
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName,lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')





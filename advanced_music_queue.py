# =================================================================
# CMPUT 175 - Introduction to the Foundations of Computation II
# Lab 6 - Advanced Music Queue
#
# ~ Created by CMPUT 175 Team ~
# ============================================================

# Install ytmusicapi using pip
from ytmusicapi import YTMusic
from structures import DLinkedListNode, DLinkedList, Song, time_to_seconds
import os

NO_OF_RESULTS = 5

def clear():
    '''
    Clears the screen based on the operating system.
    '''
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')

def extract_artists(song):
    """
    Input: A dictionary containing song information
    Returns: A string of artist names separated by commas
    Working:
    This function extracts and returns a comma-separated string of artist names from the song dictionary.
    """
    try:
        if 'artists' in song and song['artists']:
            artist_names = []
            for i in song['artists']: # takes each artist from the song and appends them into a list
                artist_names.append(i['name'])
            return ','.join(artist_names)
        else:
            return 'NA'
    except Exception:
        return 'NA'
    

def song_search(query):
    """
    Input: Search query
    Returns: Top "NO_OF_RESULTS" i.e. 5 results from the retrieved data
    Working:
    This function invokes the search method on YTMusic object with required arguments
    """
    try:

        ytmusic = YTMusic() # Initializes the object
        result = ytmusic.search(query, filter='songs') # searches for all the songs that have similar titles
        return result[:NO_OF_RESULTS]
    
    except Exception:
        raise Exception("Couldn't fetch songs")

def filter_info(results):
    """
    Input: Search results in a JSON like format
    Returns: List of Song Objects
    Working:
    This function is supposed to extract the required information from the JSON,
    create Song objects and append them to a list. If an error occurs, raise an
    exception.
    """
    try:
        songs = []
        for song in results: # Takes each song and organizes them into a list, and returns that list

            title = song.get('title', 'Unknown Title')
            artist = extract_artists(song)
            duration_str = song.get('duration', '0.00')
            duration = time_to_seconds(duration_str)

            songs.append(Song(title,artist,duration))
        
        return songs

    except Exception:
        raise Exception("Error filtering information")
    

def print_song_results(results):
    """
    Input: A list of Song objects
    Returns: None
    Working:
    This function prints the list of Song objects in a formatted manner.
    """
    assert type(results[0]) == Song, "The list to be printed doesn't have the items of type 'Song'"

    print("RESULTS:")
    for i in range(len(results)):
        print(f"{i+1}. {results[i]}")

def search():
    """
    Input: None
    Return: A Song object representing the song the user wants to add into the Queue, or None if the user wants to go back
    Working:
    1. This function takes search query from the user
    2. Searches for the song using song_search function
    3. Filters the information using filter_info function
    4. Prints the song results using print_song_results function
    5. Asks for user choice
    6. Returns the chosen song information
    7. If the user wants to go back, it returns None
    """

    try:

        clear()

        searching = True

        while searching:

            query = input("Search: ").strip()
            while not query:
                query = input("Invalid input, please enter a valid input: ").strip()
            
            results = song_search(query)
            if not results:
                print("No song found")
                return None 
            
            songs = filter_info(results)
            print_song_results(songs)
            
            print('\nChoose one of the following options: ')
            print('\tEnter a number (1-5) to add a song to the playlist')
            print("\tEnter '0' to search again")
            print("\tEnter 'q' to go back")

            choose = True
            
            while choose:

                choice = input('>> ').strip()

                if choice == 'q':
                    searching = False
                    choosing = False
                    return None
                elif choice == '0':
                    clear()
                    searching = True
                    choose = False
                    
                elif choice.isdigit() and int(choice) <= 5 and int(choice) >= 0:
                
                    searching = False
                    choose = False
                    return songs[int(choice) - 1]
                
                else: 
                    print("Invalid choice")
                
    
    except Exception:
        print("Error while searching for song")
        return None

def main():
    """
    Initializes the music queue and provides an interactive menu to manage songs.
    Users can add songs, navigate to next or previous songs, remove the current song,
    display or clear the queue, and quit the program.

    NOTE: You need to modify the main function to use the DLinkedList class to manage the music queue. 
          Add the new features that are needed for this Lab assignment as per the description.

          ** MAKE SURE YOU READ THE DESCRIPTION CAREFULLY AND UNDERSTAND THE REQUIREMENTS. **
    """
    queue = DLinkedList()
    clear()
    print("WELCOME\n")
    choice_str = """Choose one of the following options:
                \t1. Add Song
                \t2. Next Song
                \t3. Previous Song
                \t4. Remove Current Song
                \t5. Show Queue
                \t6. Clear Queue
                \t7. Quit
                Enter the choice (eg: 2)
                """
    contBuild = True
    try:
        while contBuild:

            print('Currently playing:')
            if queue.is_empty() == False: 
                print('  ',queue.get_current(),'\n')
            else: 
                print('  ',"None",'\n')

            print(choice_str)
            choice = input('>> ')
            while choice not in ['1','2','3','4','5','6','7']:
                print('Invalid Input.')
                choice = input('>> ')
            
            if choice == '1':
                song = search()
                if song != None:
                    if queue.is_empty():
                        queue.add_last(song) # adds the song to the last part of the queue if empty
                    else:
                        place = input("Where would you like to add the song:\n\t1. Add Next\n\t2. Add to the End\n>> ")
                        while place not in ['1','2']:
                            print('Invalid Input.')
                            place = input('>> ')
                        
                        if place == '1':
                            queue.add_next(song)

                        elif place == '2':
                            queue.add_last(song)
                    print("Song added successfully!")
                    input("\nPress enter key to continue...")

            elif choice == '2':
                clear()
                temp = queue.get_current()    # Looks at the temporary current song
                queue.play_next()
                if queue.get_current() != temp and queue.get_current() != None:    # Checks if the temporary current song is the same as the current song and if it is empty
                    print(f"Now playing: '{queue.get_current().get_name()}'")
                else:
                    print("No Songs ahead in queue.")
                input("\nPress enter key to continue...")

            elif choice == '3':
                clear()
                temp = queue.get_current()     # Checks if the temporary current song is the same as the current song and if it is empty
                queue.play_previous()
                if queue.get_current() != temp and queue.get_current() != None:
                    print(f"Now playing: '{queue.get_current().get_name()}'")
                else:
                    print("No Songs behind in queue")
                input("\nPress enter key to continue...")

            elif choice == '4':
                clear()
                if not queue.is_empty():
                    removed_node = queue.remove_current()    # Gets the returned object from DLinkedListNode
                    removed_song = removed_node.get_data()   # Gets the returned object from Song 
                    print(f"'{removed_song.get_name()}' removed successfully!")
                
                else:
                    print("Queue is empty.")

                input('\nPress enter key to continue...')

            elif choice == '5':
                clear()
                try:
                    print(queue)     # Prints the queue
                    input("\nPress enter key to continue...")
                except Exception as e:
                    print(e)
            
            elif choice == '6':
                queue.clear()   # Clears the queue
                print('The queue has been cleared!')
                input("\nPress enter key to continue...")

            elif choice == '7':
                contBuild = False
            
            clear()

    except Exception as e:
        print(e)

    print("Thanks for listening!")

if __name__ == "__main__":
    main()
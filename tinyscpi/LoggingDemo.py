from tinyscpi.tinySCPI import execute_from_file, user_input

if __name__ == "__main__":
    start_freq = 50000000
    # stop_freq = 65000000
    # execute_from_file('/Users/ivinbiju/Desktop/tinySCPI_Ultra/SCPI_Command_Demo_List.txt')

    # Send frequency commands
    # user_input(f'FREQ:START {start_freq}')
    # # print(f"Response: {response_start}")
    #
    user_input('DISP:CAPT')
    # # print(f"Response: {response_stop}")
    #
    # # Send an invalid command for testing
    # response_invalid = user_input("INVALID:COMMAND")

    # print("Commands executed. Check 'tinySA_commands.log' for details.")

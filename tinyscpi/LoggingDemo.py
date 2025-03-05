from tinyscpi.tinySCPI import user_input

if __name__ == "__main__":
    start_freq = 50000000
    stop_freq = 65000000

    # Send frequency commands
    response_start = user_input(f'FREQ:START {start_freq}')
    # print(f"Response: {response_start}")

    response_stop = user_input(f'FREQ:STOP {stop_freq}')
    # print(f"Response: {response_stop}")

    # Send an invalid command for testing
    response_invalid = user_input("INVALID:COMMAND")

    # print("Commands executed. Check 'tinySA_commands.log' for details.")

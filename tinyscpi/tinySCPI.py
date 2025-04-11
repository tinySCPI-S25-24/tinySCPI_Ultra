import argparse
import os

import numpy as np
import scpi_functional
import scpi_parser
import logging

# Configure logging once here in tinySCPI.py
logging.basicConfig(
    filename="tinySA_commands.log",
    level=logging.DEBUG,  # Change to DEBUG for more verbosity
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def process_command(command: str):
    """ Process SCPI command """
    logging.info(f"Command executed: {command}")  # Log the command

def user_input(input_cmd: str) -> str:
    try:
        parser = scpi_parser.SCPI_Parser()
        functional = scpi_functional.SCPI_functional()
        cmd, args = parser.parse_command(input_cmd)
        usb_str = functional.convert_scpi_to_usb(cmd, args)
        process_command(input_cmd)
        if cmd == 'CONF:CAPT':
            print("Screen captured")
        functional.send(usb_str)
        return functional.send(usb_str)
    except Exception as e:
        # Log the error if something goes wrong
        logging.error(f"Error processing command '{input_cmd}': {e}")
        return f"Error: {e}"

def debug_input(input_cmd: str) -> str:
    functional = scpi_functional.SCPI_functional()
    return functional.send(input_cmd)

def execute_from_file(filepath: str) -> None:
    with open(filepath, "r") as file:
        list_of_cmds = []
        for line in file:
            list_of_cmds.append(line)
        for cmd in list_of_cmds:
            result = user_input(cmd.strip())
            if result:
                print(result)

    file.close()


def capture(filename: str) -> str:
    functional = scpi_functional.SCPI_functional()
    functional.take_screenshot(filename)
    return f"Success, saved as {filename} in current directory"

def scan_raw_points(savedata: bool, start_freq: int = None, stop_freq: int = None, num_points: int = 101, filename: str = "data_dump.csv", save_dir: str = ".") -> str:
    # Automatically fetch start and stop frequencies if not provided
    if start_freq is None or stop_freq is None:
        freq_dump_raw = user_input("FREQ:DUMP")
        try:
            # Parse newline-separated frequency values
            freq_list = list(map(int, freq_dump_raw.strip().splitlines()))
            if len(freq_list) < 2:
                raise ValueError("FREQ:DUMP returned too few frequency values.")
            start_freq = freq_list[0]
            stop_freq = freq_list[-1]
        except Exception as e:
            return f"Error parsing frequency dump: {e}"

    # Scan the raw points
    functional = scpi_functional.SCPI_functional()
    result = functional.scan_raw(start_freq, stop_freq, num_points)

    # Save the data if requested
    if savedata:
        frequencies = np.linspace(start_freq, stop_freq, num_points)
        combined_data = np.column_stack((frequencies, result))
        file_path = os.path.join(save_dir, filename)
        np.savetxt(file_path, combined_data, delimiter=',', header='x,y', comments='', fmt='%.0f,%.8f')
        print(f"Successfully saved data to: {file_path}")

    return result

def main():
    parser = argparse.ArgumentParser(description="Run SCPI functions from the command line.")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Add a subparser for `user_input`
    user_input_parser = subparsers.add_parser("user_input", help="Send a SCPI command and process input.")
    user_input_parser.add_argument("input_cmd", type=str, help="The SCPI command string.")

    # Add a subparser for `debug_input`
    debug_input_parser = subparsers.add_parser("debug_input", help="Send a raw SCPI input.")
    debug_input_parser.add_argument("input_cmd", type=str, help="The raw SCPI command string.")

    # Add a subparser for `execute_from_file`
    execute_parser = subparsers.add_parser("execute_from_file", help="Execute SCPI commands from a file.")
    execute_parser.add_argument("filepath", type=str, help="Path to the file with SCPI commands.")

    # Add a subparser for `capture`
    capture_parser = subparsers.add_parser("capture", help="Take a screenshot and save to a file.")
    capture_parser.add_argument("filename", type=str, help="Filename to save the screenshot.")

    # Add a subparser for `scan_raw_points`
    scan_parser = subparsers.add_parser("scan_raw_points", help="Scan raw points and optionally save data.")
    scan_parser.add_argument("savedata", type=bool, help="Whether to save the data (True/False).")
    scan_parser.add_argument("start_freq", type=int, help="Start frequency in Hz.")
    scan_parser.add_argument("stop_freq", type=int, help="Stop frequency in Hz.")
    scan_parser.add_argument("num_points", type=int, help="Number of points.")
    scan_parser.add_argument("filename", type=str, help="Filename to save the data.")

    args = parser.parse_args()

    # Dispatch to the correct function
    if args.command == "user_input":
        print(user_input(args.input_cmd))
    elif args.command == "debug_input":
        print(debug_input(args.input_cmd))
    elif args.command == "execute_from_file":
        execute_from_file(args.filepath)
    elif args.command == "capture":
        print(capture(args.filename))
    elif args.command == "scan_raw_points":
        print(scan_raw_points(args.savedata, args.start_freq, args.stop_freq, args.num_points, args.filename))
    else:
        user_input("MEAS:OFF")

if __name__ == "__main__":
    main()

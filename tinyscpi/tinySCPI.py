import argparse
import numpy as np
import scpi_functional
import scpi_parser

def user_input(input_cmd: str) -> str:
    parser = scpi_parser.SCPI_Parser()
    functional = scpi_functional.SCPI_functional()
    cmd, args = parser.parse_command(input_cmd)
    usb_str = functional.convert_scpi_to_usb(cmd, args)
    return functional.send(usb_str)

def debug_input(input_cmd: str) -> str:
    functional = scpi_functional.SCPI_functional()
    return functional.send(input_cmd)

def execute_from_file(filepath: str) -> None:
    with open(filepath, "r") as file:
        list_of_cmds = []
        for line in file:
            list_of_cmds.append(line)
        for cmd in list_of_cmds:
            print(user_input(cmd.strip()))
    file.close()

def capture(filename: str) -> str:
    functional = scpi_functional.SCPI_functional()
    functional.take_screenshot(filename)
    return f"Success, saved as {filename} in current directory"

def scan_raw_points(savedata: bool, start_freq: int, stop_freq: int, num_points: int, filename: str) -> str:
    functional = scpi_functional.SCPI_functional()
    result = functional.scan_raw(start_freq, stop_freq, num_points)
    if savedata:
        np.savetxt(filename, result, delimiter=',', fmt='%.8f')
        print(f"Successfully saved data in current working directory as {filename}")
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

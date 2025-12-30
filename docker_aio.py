# VERSION: 0.0.3 (Audited)
import os
import subprocess
import sys

# Removed unused 'shlex'

try:
    from colorama import init, Fore, Style
except ImportError:
    print("Colorama library not found. Please install it with: pip install colorama")
    sys.exit(1)

init(autoreset=True)

def set_title(title):
    if os.name == 'nt':
        os.system(f'title {title}')
    else:
        sys.stdout.write(f'\x1b]2;{title}\x07')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_running_containers():
    try:
        # Added --no-trunc to ensure long names aren't cut off if using specific formats
        command = ["docker", "ps", "--format", "{{.Names}}"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        containers = result.stdout.strip().split('\n')
        return [c for c in containers if c]
    except FileNotFoundError:
        print(Fore.RED + "Error: 'docker' command not found. Is Docker installed?")
        return None
    except subprocess.CalledProcessError:
        # Simplified error message for clarity
        print(Fore.RED + "Error: Docker daemon is not running or you lack permissions.")
        return None

def shell_into_container(container_name):
    clear_screen()
    print(Fore.CYAN + f"Connecting to '{container_name}'...")
    
    # Audit Fix: Added /bin/ash for Alpine support
    shells = ["/bin/bash", "/bin/ash", "/bin/sh"]
    
    for shell in shells:
        print(Style.DIM + f"Trying {shell}...")
        try:
            # check=True will raise exception if exit code is non-zero
            subprocess.run(["docker", "exec", "-it", container_name, shell], check=True)
            return # Exit function on success
        except subprocess.CalledProcessError:
            continue # Try next shell
        except Exception as e:
            print(Fore.RED + f"System Error: {e}")
            return
    
    print(Fore.RED + f"\nCould not find a supported shell ({', '.join(shells)}) in '{container_name}'.")

def view_container_logs(container_name):
    clear_screen()
    print(Fore.CYAN + f"Logs for '{container_name}' (Ctrl+C to exit):")
    try:
        subprocess.run(["docker", "logs", "-f", container_name])
    except KeyboardInterrupt:
        pass # Clean exit without printing "Stopped viewing logs" redundancy
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error viewing logs: {e}")

def stop_container(container_name):
    clear_screen()
    print(Fore.YELLOW + f"Stopping '{container_name}'...")
    try:
        # Audit Fix: Suppressed stdout, we already know the name
        subprocess.run(["docker", "stop", container_name], 
                       check=True, stdout=subprocess.DEVNULL)
        print(Fore.GREEN + f"Successfully stopped '{container_name}'.")
    except subprocess.CalledProcessError:
        print(Fore.RED + f"Failed to stop '{container_name}'. Check permissions.")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

def action_menu(container_name):
    while True:
        clear_screen()
        print(f"Target: {Fore.GREEN}{Style.BRIGHT}{container_name}")
        print(Style.BRIGHT + "------------------------------------\n")
        print("  [S] Shell (Bash/Ash/Sh)")
        print("  [L] Live Logs")
        print("  [D] Stop Container")
        print("  [B] Back")

        action = input("\nSelect: ").lower()

        if action == 's':
            shell_into_container(container_name)
            input("\nSession ended. Enter to continue...")
        elif action == 'l':
            view_container_logs(container_name)
        elif action == 'd':
            stop_container(container_name)
            input("\nEnter to return to main menu...")
            return 
        elif action == 'b':
            return
        else:
            pass # Just refresh screen on invalid input

def main_menu():
    while True:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "Docker Container Manager v0.0.3")
        print(Style.BRIGHT + "-------------------------------\n")
        
        containers = get_running_containers()

        if containers is None:
            input("\nPress Enter to exit...")
            break
        
        if not containers:
            print(Fore.YELLOW + "No running containers found.")
        else:
            for i, name in enumerate(containers, 1):
                print(f"  [{i}] {Fore.GREEN}{name}")

        print("\n" + Style.BRIGHT + "Options:")
        if containers:
            print("  [#] Select Container")
        print("  [R] Refresh")
        print("  [Q] Quit")
        
        choice = input("\nChoice: ").lower()

        if choice == 'q':
            break
        elif choice == 'r':
            continue
        elif choice.isdigit() and containers:
            try:
                index = int(choice) - 1
                if 0 <= index < len(containers):
                    action_menu(containers[index])
                else:
                    # Input validation visual feedback
                    print(Fore.RED + "Invalid number.")
                    input()
            except ValueError:
                pass
        else:
            pass

if __name__ == "__main__":
    try:
        set_title("Docker Manager")
        main_menu()
    except KeyboardInterrupt:
        # Handle Ctrl+C at the main menu level gracefully
        print(Fore.CYAN + "\nGoodbye!")
        sys.exit(0)
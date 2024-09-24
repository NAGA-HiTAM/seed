#!/bin/bash

# Global variables
REPO_URL="https://github.com/arun993/seed-bot.git"
REPO_DIR="seed-bot/seed-query"
QUERY_FILE="query.txt"

# Function to remove old files
cleanup_old_files() {
    rm -rf seed-bot seed.sh
}

# Function to clone the repository
clone_repo() {
    git clone "$REPO_URL"
    if [[ $? -ne 0 ]]; then
        printf "Error cloning repository\n" >&2
        return 1
    fi
}

# Function to change directory to the seed-query folder
change_directory() {
    cd "$REPO_DIR" || { printf "Failed to change directory to %s\n" "$REPO_DIR" >&2; return 1; }
}

# Function to check if Python 3.10+ is installed
check_python_version() {
    local python_version
    python_version=$(python3 --version 2>&1)
    
    if ! echo "$python_version" | grep -q "3.1[0-9]"; then
        printf "Python 3.10+ is required but not found. Please install it.\n" >&2
        return 1
    fi
}


# Function to prompt user input and save to query.txt
get_user_input() {
    printf "Enter query ids and press Ctrl+D:\n"
    cat > "$QUERY_FILE"
    if [[ ! -s "$QUERY_FILE" ]]; then
        printf "Input was empty or file was not created successfully\n" >&2
        return 1
    fi
}
# Function to install Python modules
install_requirements() {
    pip3 install requests colorama pytz
    if [[ $? -ne 0 ]]; then
        printf "Failed to install required Python modules\n" >&2
        return 1
    fi
}

# Function to run the Python script
run_python_script() {
    python3 seed.py
    if [[ $? -ne 0 ]]; then
        printf "Error running the Python script\n" >&2
        return 1
    fi
}

# Main function to manage script execution flow
main() {
    cleanup_old_files || return 1
    clone_repo || return 1
    change_directory || return 1
    check_python_version || return 1
    install_requirements || return 1
    get_user_input || return 1
    run_python_script || return 1
}

# Execute main
main

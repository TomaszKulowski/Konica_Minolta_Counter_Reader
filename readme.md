# Konica Minolta Counter Reader

This Python project is designed for retrieving printer statistics from networked devices, scheduling reports, and sending them via email. It includes several utility classes and functions for these tasks.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)


## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/TomaszKulowski/Konica_Minolta_Counter_Reader.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Konica_Minolta_Counter_Reader
    ```

3. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```


## Usage

To run the Konica Minolta Counter Reader, follow these simple steps:

1. Open a command prompt or terminal window.

2. Navigate to the project directory containing the `main.py` file:

    ```bash
    cd path/to/Konica_Minolta_Counter_Reader
    ```

3. Execute the following command to start the application:

    ```bash
    python main.py
    ```

4. The application will run, retrieve printer statistics, schedule reports, and send them via email according to your configuration.

**Note**: Ensure that you have set up your configuration, including SMTP server details, email credentials, and device IP addresses, in the `.env` file before running the application.


### Contributing
Contributions are welcome! If you find issues or want to enhance the project, please create a GitHub issue or submit a pull request.
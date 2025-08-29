Error Detection and Correction Toolkit
A Python command-line tool that demonstrates various error detection and correction techniques used in computer networks, including Parity, Checksum, CRC, and Hamming codes.
Features
Interactive Menu: Choose which method to demonstrate.
Simple Demos: See each technique in action with pre-defined examples.
Custom Inputs: Try your own binary data and see the results.
Bit-Flipping Simulation: Simulate a data transmission error to test the methods.

Installation
This script uses only standard Python libraries and does not require any additional packages to be installed.
1. Clone the repository (or download the Python file directly):
2. Run the script:

Usage
When you run the script, a simple menu will appear.

Error Detection & Correction Toolkit
------------------------------------------------------------
1) Parity (even/odd)
2) Checksum (16-bit words)
3) CRC
4) Hamming (7,4)
5) Demo all (quick showcase)
0) Exit
------------------------------------------------------------
Choose an option:

Option 1: Parity
The parity check adds a single bit to the data to make the total number of '1's either even or odd. This method can detect a single bit error.

Option 2: Checksum (16-bit)
This method calculates a checksum for a block of data and sends it with the data. The receiver recomputes the checksum and compares it to the received one to detect if an error occurred.

Option 3: CRC
Cyclic Redundancy Check (CRC) is a more robust technique that uses polynomial division to generate a redundant "remainder" to append to the data. It can detect a wider range of errors than a simple parity check.

Option 4: Hamming (7,4)
Hamming code is an error-correcting technique, not just for detection. The (7,4) code can correct any single-bit error in a 7-bit word.

Option 5: Demo all
This option runs a quick, non-interactive showcase of all the methods, demonstrating the encoding, a simulated error, and the result of the detection/correction.

Code structure
The script is organized into separate functions for each method, making it easy to understand and modify.
. parity_encode, parity_check: Functions for parity.
. checksum_16, checksum_verify: Functions for 16-bit checksum.
. xor, crc_remainder, crc_transmit, crc_verify: Functions for CRC.
. hamming_74_encode, hamming_74_decode: Functions for Hamming (7,4).
. demo_all: A function to run a showcase of all features.
. main: The main function that drives the interactive menu.


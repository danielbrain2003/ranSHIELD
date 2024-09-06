# ranSHIELD: Anti-Ransomware Tool


Overview: 
          ranSHIELD is a powerful Python-based application designed to protect your system from ransomware attacks. By combining multiple monitoring tools and preventative measures, ranSHIELD offers a comprehensive defense against ransomware, ensuring the safety of your files, processes, and network. The tool is built using Python's CustomTkinter framework for a user-friendly interface.

Key Features:

File Monitor:

Allows users to specify directories to monitor.
The tool regularly watches the files within the specified path.
If any files are encrypted, ranSHIELD immediately commands the system to shut down, preventing further damage.

Process Monitor:

Continuously monitors system processes.
If more than 10 files are encrypted within 2 seconds, the tool automatically identifies and kills the process responsible for the encryption, then shuts down the system.

Network Shield:

When enabled, this feature monitors network activities for signs of rapid encryption.
Upon detecting a potential ransomware attack, it disables the system's network connection and alerts the user, minimizing data loss or theft.

Authorized Installation:

Prevents unauthorized software installation by requiring a password when new applications are being installed.
Protects against malicious software being installed without the user’s consent.

Extortion Prevention:

Encryption:

ranSHIELD provides the ability to encrypt your own data, ensuring that sensitive information is protected.
This method prevents hackers from accessing and leaking your private data during an extortion attempt.

Decryption:

Users can decrypt their data using a password-protected decryption tool.
This feature is useful when you are in a secure environment and want to access your encrypted data.

Additional Features:

Status Menu: Displays system information, including monitoring status and other relevant details.

About Menu: Provides a link to the ranSHIELD GitHub page for updates and more information.

Important Note: Never open ransomware files on your local system, as doing so may lead to encryption of your files. ranSHIELD offers proactive defense, but user vigilance is critical.

Technology Stack:

Developed using Python
UI created with CustomTkinter to provide a modern and responsive interface.

How to Use:

First, run the "app" file to launch the user interface.
Configure monitoring settings, enable protection, and rest assured that ranSHIELD will monitor your system in real time.
ranSHIELD offers a blend of real-time protection, proactive data encryption, and user-friendly controls, making it an essential tool for anyone looking to secure their system against ransomware threats.

# HAR to Image Downloader

![License](https://img.shields.io/badge/license-MIT-blue.svg)

HAR to Image Downloader is a Python-based tool that extracts images from `.har` (HTTP Archive) files. This tool provides a command-line interface (CLI) with a rich progress bar, error handling, and support for parallel downloads.

## Features

- **Extract Images from HAR Files:** Automatically extracts all image URLs from selected `.har` files.
- **Parallel Downloads:** Download images using multiple threads to speed up the process.
- **Error Handling:** Robust handling of network errors with retry mechanisms.
- **Progress Monitoring:** Detailed progress bars showing download status, speed, and estimated time remaining.
- **GUI Integration:** Uses Tkinter for file and folder selection.
- **Summary Report:** Provides a summary report after downloads, including the number of successful and failed downloads.

## Installation

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Clone the Repository

```bash
git clone https://github.com/hglmz/HAR2JPG.git
cd HAR2JPG
```

### Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains the following dependencies:

- `requests`: For making HTTP requests.
- `rich`: For creating rich CLI interfaces with progress bars.
- `urllib3`: For managing HTTP connections and retries.

## Usage

Run the script using Python:

```bash
python hars2jpg.py
```

### Command-Line Interface

Upon running the script, you'll be presented with the following menu:

```text
██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗███╗   ███╗ ██████╗ 
██║  ██║██╔══██╗██╔══██╗╚════██╗██║████╗ ████║██╔════╝ 
███████║███████║██████╔╝ █████╔╝██║██╔████╔██║██║  ███╗
██╔══██║██╔══██║██╔══██╗██╔═══╝ ██║██║╚██╔╝██║██║   ██║
██║  ██║██║  ██║██║  ██║███████╗██║██║ ╚═╝ ██║╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝ ╚═════╝ 

[1] Select HAR Files
[2] Select Download Folder
[3] Start Download
[q] Quit
```

### Options

1. **Select HAR Files:** Opens a file dialog to select one or more `.har` files.
2. **Select Download Folder:** Opens a directory dialog to select the folder where images will be saved.
3. **Start Download:** Starts downloading images based on the selected `.har` files and the download folder.
   - You'll be prompted to enter the number of parallel downloads (default is 10).

### Progress Bar and Download Summary

During the download process, a progress bar shows the current status:

- **Images Downloaded/Total:** Shows how many images have been downloaded out of the total.
- **Speed:** Indicates the download speed in MB/s.
- **Time Elapsed:** Shows how long the process has been running.
- **Time Remaining:** Estimates the remaining time for completion.

At the end of the process, a summary report will be displayed, indicating:

- **Total Images:** Number of images found in the `.har` files.
- **Downloaded:** Number of successfully downloaded images.
- **Failed:** Number of images that failed to download.
- **Total Size:** Total size of the downloaded images in MB.
- **Elapsed Time:** Total time taken for the download process.
- **Download Speed:** Average download speed in MB/s.

## Error Handling

This tool has robust error handling, including:

- **Retry Mechanism:** Automatically retries downloading an image up to 5 times if a network error occurs.
- **Timeouts:** Each download attempt has a 10-second timeout to prevent hanging.
- **Detailed Error Logs:** Errors encountered during the download are logged to the console.

## Example Output

```text
Downloading images from example.har...
█████████████████████████████████████████ 100% • 100/100 images • 00:01:23 • 00:00:00 • Speed: 3.45 MB/s

Download Summary
┌───────────┬────────────┬────────────┬───────────┬─────────────────┬───────────────┬─────────────┐
│ HAR File  │ Total Images │ Downloaded │ Failed   │ Total Size (MB) │ Elapsed Time  │ Speed (MB/s)│
├───────────┼────────────┼────────────┼───────────┼─────────────────┼───────────────┼─────────────┤
│ example   │ 100        │ 95         │ 5         │ 345.23          │ 83.12         │ 4.15        │
└───────────┴────────────┴────────────┴───────────┴─────────────────┴───────────────┴─────────────┘
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

## Contact

If you have any questions or suggestions, feel free to reach out to the project maintainer.

```

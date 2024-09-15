import json
import requests
import os
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from rich.progress import Progress, TimeElapsedColumn, TimeRemainingColumn, BarColumn, TextColumn
from rich.console import Console
from rich.table import Table
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

console = Console()

har_files = []
download_folder = ""
max_workers = 10

# İndirme sırasında hata almamak için bir retry stratejisi belirleyelim.
retry_strategy = Retry(
    total=5,  # Toplam 5 deneme
    backoff_factor=1,  # Her denemede bekleme süresi
    status_forcelist=[429, 500, 502, 503, 504],  # Bu hata kodları ile karşılaşılırsa tekrar dene
    allowed_methods=["HEAD", "GET", "OPTIONS"]  # Yalnızca GET, HEAD ve OPTIONS isteklerinde tekrar dene
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def download_image(url, target_folder):
    try:
        response = http.get(url, timeout=10)
        if response.status_code == 200:
            file_name = url.split('/')[-1]
            with open(os.path.join(target_folder, file_name), 'wb') as img_file:
                img_file.write(response.content)
            return len(response.content), True  # İndirilen dosya boyutu ve başarı durumu
        else:
            console.print(f"[bold red]Failed to download {url} with status code {response.status_code}[/bold red]")
            return 0, False
    except requests.RequestException as e:
        console.print(f"[bold red]Error downloading {url}: {str(e)}[/bold red]")
        return 0, False

def extract_images_from_har(har_file_path, download_folder, max_workers=10):
    har_name = os.path.splitext(os.path.basename(har_file_path))[0]
    target_folder = os.path.join(download_folder, har_name)
    os.makedirs(target_folder, exist_ok=True)

    with open(har_file_path, 'r', encoding='utf-8') as file:
        har_data = json.load(file)

    image_urls = []
    entries = har_data['log']['entries']
    for entry in entries:
        try:
            if 'image' in entry['response']['content']['mimeType']:
                url = entry['request']['url']
                image_urls.append(url)
        except KeyError:
            continue

    total_images = len(image_urls)
    downloaded_images = 0
    failed_images = 0
    total_size = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            TextColumn("[progress.completed]{task.completed}/{task.total} images"),
            "•",
            TimeElapsedColumn(),
            "•",
            TimeRemainingColumn(),
            "•",
            TextColumn("Speed: {task.fields[download_speed]:.2f} MB/s"),
            console=console,
        ) as progress:

            download_task = progress.add_task(f"[cyan]Downloading images from {har_name}...", total=total_images, download_speed=0.0)

            futures = {executor.submit(download_image, url, target_folder): url for url in image_urls}
            for future in as_completed(futures):
                file_size, success = future.result()
                if success:
                    downloaded_images += 1
                    total_size += file_size / (1024 * 1024)  # Dosya boyutunu MB cinsine çevir
                else:
                    failed_images += 1
                
                elapsed_time = time.time() - start_time
                speed = total_size / elapsed_time if elapsed_time > 0 else 0
                progress.update(download_task, advance=1, download_speed=speed)

    elapsed_time = time.time() - start_time
    speed = total_size / elapsed_time if elapsed_time > 0 else 0

    table = Table(title="Download Summary")
    table.add_column("HAR File", justify="left")
    table.add_column("Total Images", justify="right")
    table.add_column("Downloaded", justify="right")
    table.add_column("Failed", justify="right")
    table.add_column("Total Size (MB)", justify="right")
    table.add_column("Elapsed Time (s)", justify="right")
    table.add_column("Speed (MB/s)", justify="right")

    table.add_row(har_name, str(total_images), str(downloaded_images), str(failed_images), f"{total_size:.2f}", f"{elapsed_time:.2f}", f"{speed:.2f}")
    console.print(table)

def browse_files():
    global har_files
    root = tk.Tk()
    root.withdraw()
    har_files = filedialog.askopenfilenames(
        title='Open files',
        initialdir='/',
        filetypes=[("HAR files", "*.har")]
    )
    root.destroy()

    if har_files:
        console.print("\n[green]Selected HAR files:[/green]")
        for idx, file in enumerate(har_files, 1):
            console.print(f"{idx}- {file}")
    else:
        console.print("[bold red]No HAR files selected.[/bold red]")

def select_folder():
    global download_folder
    root = tk.Tk()
    root.withdraw()
    download_folder = filedialog.askdirectory()
    root.destroy()

    if download_folder:
        console.print(f"[green]Selected download folder:[/green] {download_folder}")
    else:
        console.print("[bold red]No download folder selected.[/bold red]")

def start_download():
    if not har_files:
        console.print("[bold red]No HAR files selected. Please select HAR files first.[/bold red]")
        return
    if not download_folder:
        console.print("[bold red]No download folder selected. Please select a download folder first.[/bold red]")
        return
    
    max_workers = console.input("[cyan]Enter the number of parallel downloads (recommended: 10): [/cyan]").strip()
    max_workers = int(max_workers) if max_workers.isdigit() else 10

    for file in har_files:
        extract_images_from_har(file, download_folder, max_workers)
    console.print("[bold green]All downloads completed successfully![/bold green]")

def main_menu():
    ascii_art = r"""
██╗  ██╗ █████╗ ██████╗ ██████╗ ██╗███╗   ███╗ ██████╗ 
██║  ██║██╔══██╗██╔══██╗╚════██╗██║████╗ ████║██╔════╝ 
███████║███████║██████╔╝ █████╔╝██║██╔████╔██║██║  ███╗
██╔══██║██╔══██║██╔══██╗██╔═══╝ ██║██║╚██╔╝██║██║   ██║
██║  ██║██║  ██║██║  ██║███████╗██║██║ ╚═╝ ██║╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚═╝ ╚═════╝ 

    """
    console.print(ascii_art, style="bold cyan")
    console.print("[1] Select HAR Files", style="bold green")
    console.print("[2] Select Download Folder", style="bold green")
    console.print("[3] Start Download", style="bold green")
    console.print("[q] Quit", style="bold red")

    while True:
        choice = console.input("\n[bold cyan]Select an option: [/bold cyan]").strip().lower()

        if choice == '1':
            browse_files()
        elif choice == '2':
            select_folder()
        elif choice == '3':
            start_download()
        elif choice == 'q':
            console.print("[bold red]Exiting program...[/bold red]")
            break
        else:
            console.print("[bold red]Invalid option. Please choose 1, 2, 3 or q.[/bold red]")

if __name__ == "__main__":
    main_menu()

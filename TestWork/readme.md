
# DeFiLlama Chains Data Scraper

## Overview

The **DeFiLlama Chains Data Scraper** is a Python-based tool designed to automate the extraction of blockchain statistics from the [DeFiLlama](https://defillama.com/chains) website. This script gathers essential data such as **Name**, **Protocols**, and **TVL (Total Value Locked)** for various blockchain protocols. The collected data is saved in either **JSON** or **CSV** format and is updated at configurable intervals. Additionally, the scraper supports proxy configurations to enhance anonymity and reliability.

## Features

- **Automated Scraping**: Extracts Name, Protocols, and TVL data from DeFiLlama's chains page.
- **Configurable Intervals**: Schedule scraping tasks at customizable intervals (default every 5 minutes).
- **Proxy Support**: Configure multiple proxies to avoid IP blocking and enhance scraping reliability.
- **Flexible Output Formats**: Save scraped data in **JSON** or **CSV** formats.
- **Robust Logging**: Detailed logs for monitoring scraping activities, successes, and failures.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
  - [config.json](#configjson)
- [Usage](#usage)
- [Output](#output)
- [Logging](#logging)
- [Proxy Configuration](#proxy-configuration)
- [Scheduling](#scheduling)
- [Troubleshooting](#troubleshooting)

## Requirements

- **Python**: Version 3.6 or higher
- **Google Chrome**: Latest version recommended
- **ChromeDriver**: Compatible with your installed Chrome version

## Installation

### 1. Open the file 


### 2. Set Up a Virtual Environment (Recommended)

Using a virtual environment ensures that dependencies are isolated from your global Python installation.

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

### 3. Install Dependencies

Ensure you have `pip` updated:

```bash
pip install --upgrade pip
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Install ChromeDriver

1. **Check Your Chrome Version:**

   Open Chrome and navigate to `chrome://settings/help` to find your Chrome version.

2. **Download Corresponding ChromeDriver:**

   Visit the ChromeDriver Downloads page and download the version that matches your Chrome browser.

3. **Add ChromeDriver to PATH:**

   - **On macOS/Linux:**

     ```bash
     sudo mv chromedriver /usr/local/bin/
     sudo chmod +x /usr/local/bin/chromedriver
     ```

   - **On Windows:**

     Move `chromedriver.exe` to a directory that's in your system's `PATH`, or add its location to the `PATH` environment variable.

## Configuration

All configurable settings are managed via the `config.json` file. This allows you to adjust scraping intervals, proxy settings, output formats, and more without modifying the script.

### config.json
#### Приклад Файлу `config.json`

```json
{
    "scrape_interval_minutes": 5,
    "proxy": {
        "enabled": false,
        "proxy_list": [
            "http://username:password@proxy1.example.com:8080",
            "http://username:password@proxy2.example.com:8080"
        ]
    },
    "output_format": "json",
    "output_file": "chains_data.json",
    "log_file": "scraping.log",
    "scroll_pause_time": 1.5,
    "scroll_increment": 1000,
    "max_attempts": 5
}
```

Create a `config.json` file in the root directory of the project with the following structure:

```json
{
    "scrape_interval_minutes": 5,
    "proxy": {
        "enabled": false,
        "proxy_list": [
            "http://username:password@proxy1:port",
            "http://username:password@proxy2:port"
        ]
    },
    "output_format": "json",
    "output_file": "chains_data.json",
    "log_file": "scraping.log",
    "scroll_pause_time": 1.5,
    "scroll_increment": 1000,
    "max_attempts": 5
}

```

#### Parameters:

- **scrape_interval_minutes**:  
  *Type*: Integer  
  *Description*: Interval in minutes between consecutive scraping tasks.  
  *Default*: `5`

- **proxy**:  
  *Type*: Object  
  *Description*: Proxy configuration settings.  
  - **enabled**:  
    *Type*: Boolean  
    *Description*: Toggle to enable or disable proxy usage.  
    *Default*: `false`
  
  - **proxy_list**:  
    *Type*: Array of Strings  
    *Description*: List of proxy server URLs in the format `http://username:password@proxy:port`.  
    *Example*:  
    ```json
    [
        "http://user:pass@proxy1.example.com:8080",
        "http://user:pass@proxy2.example.com:8080"
    ]
    ```

- **output_format**:  
  *Type*: String  
  *Description*: Desired output format for the scraped data.  
  *Options*: `"json"`, `"csv"`  
  *Default*: `"json"`

- **output_file**:  
  *Type*: String  
  *Description*: Name of the output file where data will be saved.  
  *Default*: `"chains_data.json"`

- **log_file**:  
  *Type*: String  
  *Description*: Name of the log file for recording scraping activities.  
  *Default*: `"scraping.log"`

- **scroll_pause_time**:  
  *Type*: Float  
  *Description*: Time in seconds to pause between each scroll action to allow data to load.  
  *Default*: `1.5`

- **scroll_increment**:  
  *Type*: Integer  
  *Description*: Number of pixels to scroll down the page in each scroll action.  
  *Default*: `1000`

- **max_attempts**:  
  *Type*: Integer  
  *Description*: Maximum number of consecutive attempts to scroll without finding new content before stopping the scraper.  
  *Default*: `5`

## Usage

### Running the Scraper

Activate your virtual environment (if not already active):

- **On macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

Run the scraper script:

```bash
python scraper.py
```

The script will perform an immediate scraping upon launch and then continue to scrape at intervals defined in `config.json`.

### Stopping the Scraper

To stop the scraper, press `Ctrl + C` in the terminal where the script is running.

## Output

The scraped data is saved in the format specified in `config.json` (`json` or `csv`) within the specified `output_file`.

### Example: JSON Output (`chains_data.json`)

```json
[
    {
        "Name": "Ethereum",
        "Protocols": "1212",
        "TVL": "56.95b"
    },
    {
        "Name": "Solana",
        "Protocols": "174",
        "TVL": "7.154b"
    },
    {
        "Name": "Tron",
        "Protocols": "34",
        "TVL": "6.734b"
    }
    // ... additional records
]
```

### Example: CSV Output (`chains_data.csv`)

```csv
Name,Protocols,TVL
Ethereum,1212,56.95b
Solana,174,7.154b
Tron,34,6.734b
```

## Logging

The scraper maintains a detailed log of its activities, including:

- **Startup and Shutdown Messages**
- **Proxy Usage Information**
- **Scraping Progress**
- **Errors and Exceptions**
- **Data Collection Status**

Logs are saved to the file specified in `config.json` (`log_file`), e.g., `scraping.log`, and are also output to the console for real-time monitoring.

### Example Log Entries (`scraping.log`)

```
2024-04-27 12:00:00 - INFO - Проксі не використовується.
2024-04-27 12:00:01 - INFO - Початок скрапінгу даних.
2024-04-27 12:00:15 - INFO - Заголовки таблиці: ['Name', 'Protocols', 'TVL']
2024-04-27 12:00:20 - INFO - Зібрано дані: {'Name': 'Ethereum', 'Protocols': '1212', 'TVL': '56.95b'}
2024-04-27 12:00:20 - INFO - Зібрано дані: {'Name': 'Solana', 'Protocols': '174', 'TVL': '7.154b'}
2024-04-27 12:00:20 - INFO - Знайдено 2 рядків.
2024-04-27 12:00:20 - INFO - Дані скраплені та збережені у chains_data.json.
2024-04-27 12:00:20 - INFO - Завершення скрапінгу даних.
2024-04-27 12:05:00 - INFO - Початок скрапінгу даних.
...
```

## Proxy Configuration

Proxy support allows the scraper to route its requests through different IP addresses, enhancing anonymity and helping to avoid IP bans.

### Enabling Proxy

1. **Edit `config.json`:**

   Set `"enabled": true` within the `proxy` section and provide a list of proxies.

   ```json
   "proxy": {
       "enabled": true,
       "proxy_list": [
           "http://username:password@proxy1.example.com:8080",
           "http://username:password@proxy2.example.com:8080"
       ]
   }
   ```

2. **Proxy Selection:**

   The scraper randomly selects a proxy from the provided `proxy_list` for each scraping session.

### Proxy Format

Ensure proxies are in the correct format:

```
http://username:password@proxyserver:port
```

- **username**: Proxy username (if required)
- **password**: Proxy password (if required)
- **proxyserver**: Proxy server address
- **port**: Proxy server port

*Example:*

```
http://user123:pass456@proxy1.example.com:8000
```

### Notes

- **Authentication**: If your proxy requires authentication, include the `username` and `password` in the proxy URL as shown above.
- **Rotation**: Consider adding multiple proxies to `proxy_list` to rotate IP addresses and reduce the risk of being blocked.

## Scheduling

The scraper is configured to run at intervals defined by `scrape_interval_minutes` in `config.json`. The default interval is **5 minutes**, but you can adjust this to suit your needs.

### Adjusting the Interval

1. **Open `config.json`.**
2. **Modify the `scrape_interval_minutes` value.**

   ```json
   {
       "scrape_interval_minutes": 10,  // Scrape every 10 minutes
       ...
   }
   ```

3. **Save the file and restart the scraper.**

### Immediate Scraping

Upon starting, the scraper performs an immediate scraping before entering the scheduled intervals.

## Troubleshooting

### Common Issues

1. **ChromeDriver Version Mismatch**

   - **Issue**: "SessionNotCreatedException: This version of ChromeDriver only supports Chrome version XX"
   - **Solution**: Ensure that your ChromeDriver version matches your installed Chrome browser version. Download the correct version from [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads).

2. **Element Not Found**

   - **Issue**: The scraper fails to locate the `'table-header'` element.
   - **Solution**: The website structure may have changed. Inspect the DeFiLlama chains page and update the CSS selectors in the script accordingly.

3. **Proxy Connection Errors**

   - **Issue**: Unable to connect through the specified proxy.
   - **Solution**: Verify proxy credentials and server availability. Test proxies independently to ensure they are operational.

4. **Missing Output File**

   - **Issue**: Output file not generated.
   - **Solution**: Check for errors in the log file (`scraping.log`). Ensure that the script has write permissions to the directory.

### Debugging Steps

1. **Check Logs**

   Review the `scraping.log` file for any error messages or warnings that can provide insights into the issue.

2. **Enable Debug Logging**

   Modify the `setup_logging` function to set the logging level to `DEBUG` for more detailed logs.

   ```python
   logging.basicConfig(
       filename=log_file,
       level=logging.DEBUG,  # Change to DEBUG
       ...
   )
   ```

3. **Inspect Page Source**

   If elements are not found, log or print parts of the page source to verify if the content is loaded correctly.

   ```python
   logging.debug(driver.page_source)
   ```

4. **Update Selectors**

   Use browser developer tools (F12) to inspect the current structure of the DeFiLlama chains page and update CSS selectors in the script if necessary.







```


---


# Multiple URLs to screenshot

This Python script automates the process of taking screenshots of websites in
both desktop and mobile views. It was created to help a coworker who was tasked
with entering 2600 websites and capturing screenshots of each.

A coworker was tasked with entering over 2600 websites and capturing screenshots
(desktop and mobile views) of each and that's when this Python script was born.

Pass in a list of URLs, get back a list of screenshots in Desktop and Mobile
views.

I also added a few methods to check for cases in which the website crashed, the
screenshot couldn't be created (just generate a black screenshot) and also add
successful screenshots to a json file so, if something goes wrong (script
breaks, laptop crashes...) I can just run the script and ignore URLs that have
been already used.

## Installation

If for some reason, you need to generate a bunch of screenshots from URLs,
here's the installation guide (feel free to change the code to match your case,
and even send a PR if you'd like to contribute!).

1. Clone this repository to your local machine:

```
git clone https://github.com/darioaladuz/screenshots_py.git
```

2. Navigate to the directory:

```
cd screenshots_py
```

3. Install the required dependencies:

```
pip install selenium webdriver-manager Pillow
```

## Usage

1. Prepare a file named `urls.json` containing the list of URLs to capture
   screenshots of. The format should be:

```json
{
    "urls": [
        "https://example1.com",
        "https://example2.com",
        ...
    ]
}
```

2. Run the script using the following command:

```
python index.py
```

3. The script will iterate over each URL in urls.json, capture both desktop and
   mobile screenshots, and save them in the /screenshots/Desktop and
   /screenshots/Mobile directories respectively.

4. If any screenshots fail to be captured, they will be logged in failed.json.
   Successful screenshots will be logged in all_used.json

### Note

- You may need to install a headless browser driver such as ChromeDriver or
  GeckoDriver. Please ensure you have the appropriate driver installed and added
  to your system's PATH.

- Make sure to review the failed.json file after running the script to address
  any failed captures.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

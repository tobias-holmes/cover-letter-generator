[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Cover Letter Generator

A Python-based cover letter generator that creates professional cover letters using LaTeX templates. Supports both English and German languages.

## Features

- Generates customized cover letters from YAML configuration files
- Supports mulitple (language) layouts.
- Uses LaTeX for professional PDF output
- Templating with Jinja2
- Configurable sender and recipient information
- Dynamic file naming based on company and sender details

## Prerequisites

- Python 3.x
- LaTeX distribution with `lualatex`
- Required Python packages (see [Installation](#installation))

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd cover-letter-generator
   ```
2. Set up the Python virtual environment:
   ```bash
   source setup.sh
   ```
   This will create a virtual environment, install all required dependencies and activate the venv in the current terminal.

## Configuration

1. Copy the example context files:
   ```bash
   cp context/sender_context.yml.example context/sender_context.yml
   cp context/position_context.yml.example context/position_context.yml
   cp context/text_context_en.yml.example context/text_context_en.yml
   cp context/text_context_de.yml.example context/text_context_de.yml
   ```
2. Edit the context files
   - sender_context.yml: Your personal information
   - position_context.yml: Job and company details
   - text_context_en.yml: English letter content
   - text_context_de.yml: German letter content

## Useage

Run the generator script:

```bash
python main.py
```

When prompted, enter the desired language (`en` for English, `de` for German).

The script will:

1. Generate a $\TeX$ file in the [renders](/renders) directory
2. Compile it into a PDF using lualatex
3. Dynamically create the file names in the following format: `cover_letter-<company>-<sender>-<language>.pdf`

## Project Structure

```
├── context/                  # Configuration files
│   ├── position_context.yml  # Job and company details
│   ├── sender_context.yml    # Personal information
│   ├── text_context_de.yml   # German letter content
│   └── text_context_en.yml   # English letter content
├── renders/                  # Output directory for generated files
├── templates/                # LaTeX template
│   └── cover_letter_template.tex.j2
├── create_cover_letter.py    # Main Python script
├── requirements.txt          # Python dependencies
└── setup.sh                  # Setup script
```

## Dependencies

- Jinja2
- PyYAML
- $\LaTeX$ with `lualatex`
- DejaVu Sans font

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author

Tobias Holmes

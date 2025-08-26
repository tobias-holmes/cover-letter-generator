#######################################################################
# Creates a cover letter using LaTeX/Jinja templates as well as yaml
# context files.
# Copyright (C) 2025  Tobias Holmes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#  any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#######################################################################

import yaml
import subprocess
from jinja2 import Environment, FileSystemLoader
from io import StringIO
from datetime import date


# Function to load YAML files with Jinja2 templating
def load_yaml_with_jinja(filename: str, context: str) -> dict:
    """
    Load a YAML file and render it with Jinja2 templating.
    :param filename: Path to the YAML file.
    :param context: Context for Jinja2 rendering.
    :return: Rendered YAML as a Python dictionary.
    """
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(filename)
    rendered_yaml = template.render(context)
    return yaml.safe_load(StringIO(rendered_yaml))


# Render the LaTeX file from Jinja2 template
def render_tex_file(language: str = "en") -> str:
    """
    Render a LaTeX file from a Jinja2 template using data from YAML files. Places the output in 'renders/' directory.
    :param language: Language for the cover letter content, either 'en' or 'de'.
    :return: Name of the generated .tex file.
    """
    # Import the YAML files
    with open("context/sender_context.yml", "r") as file:
        sender_context = yaml.safe_load(file)
    with open("context/position_context.yml", "r") as file:
        position_context = yaml.safe_load(file)

    # Combine personal data and add today's date and start date in DD.MM.YYYY format
    sender_position_context = {
        **sender_context,
        **position_context,
        "today": date.today().isoformat(),
        "start_date": sender_context.get("start_date_iso").strftime("%d.%m.%Y"),
    }

    # Cover letter content
    if language == "de":
        text_context = load_yaml_with_jinja(
            "context/text_context_de.yml", sender_position_context
        )
    elif language == "en":
        text_context = load_yaml_with_jinja(
            "context/text_context_en.yml", sender_position_context
        )
    else:
        raise ValueError(f"Unsupported language '{language}'. Please use 'en' or 'de'.")

    # Combine data from both YAML files
    context = {**sender_position_context, **text_context}

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("cover_letter_template.tex.j2")

    # Render LaTeX
    rendered = template.render(**context)

    ## Extract relevant information for the filename
    # Combine the first initial with the last name
    sender_first_name = context["sender"]["first_name"]
    sender_last_name = context["sender"]["last_name"]
    sender_identifier = f"{sender_first_name[0]}{sender_last_name}".lower()
    
    # Language and replacements for filename
    language = context["language"].lower()
    replacements = [("-", "_"),(",", "_"),(".", "_"), (":","_"),(" ", "_"),("/", "_"),("&","_"),("*","_"),("(",""),(")","")]
    
    # Set company short name, replacing spaces and special characters with underscores
    company_short_filename = context["recipient"]["company_short"].lower()
    for old, new in replacements:
        company_short_filename = company_short_filename.replace(old, new)
    
    # Set position, replacing spaces and special characters with underscores
    if context.get("initiative") == True:
        position = "init" 
    else:
        position = context["position"].lower()
        print(position)
        for old, new in replacements:
            position = position.replace(old, new)

    # Create dynamic filename
    output_filename = f"cover_letter-{company_short_filename}-{position}-{sender_identifier}-{language}.tex"

    # Save .tex file
    tex_file = "renders/" + output_filename
    with open(tex_file, "w") as f:
        f.write(rendered)

    return output_filename


# Compile TeX to PDF
def compile_tex_to_pdf(tex_filename: str) -> None:
    """
    Compile a LaTeX file to PDF using lualatex. Working directory is set to 'renders'.
    :param tex_filename: Name of the .tex file to compile.
    """
    subprocess.run(["lualatex", tex_filename], cwd="renders")


if __name__ == "__main__":
    # Print license notice
    print(
        """
        Cover Letter Generator - Copyright (C) 2025  Tobias Holmes
        This program comes with ABSOLUTELY NO WARRANTY;
        This is free software, and you are welcome to redistribute it
        under certain conditions; see GPL v3 for details.
        """
    )

    # Get language input from user, default to 'de'
    language = input("Enter language (en/DE): ").strip().lower() or "de"

    filename = render_tex_file(language=language)
    compile_tex_to_pdf(filename)

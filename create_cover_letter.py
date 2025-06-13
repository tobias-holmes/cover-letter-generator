import yaml
import subprocess
from jinja2 import Environment, FileSystemLoader
from io import StringIO


# Function to load YAML files with Jinja2 templating
def load_yaml_with_jinja(filename, context):
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
def render_tex_file(language="en"):
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

    # Combine personal data
    sender_position_context = {**sender_context, **position_context}

    # Cover letter content
    if language == "de":
        text_context = load_yaml_with_jinja(
            "context/text_context_de.yml", sender_position_context
        )
    else:
        text_context = load_yaml_with_jinja(
            "context/text_context_en.yml", sender_position_context
        )

    # Combine data from both YAML files
    context = {**sender_position_context, **text_context}

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("cover_letter_template.tex.j2")

    # Render LaTeX
    rendered = template.render(**context)

    # Extract relevant information for the filename
    sender_first_name = context["sender"]["first_name"]
    sender_last_name = context["sender"]["last_name"]
    # Combine the first initial with the last name
    sender_identifier = f"{sender_first_name[0]}{sender_last_name}".lower()
    company_short = context["recipient"]["company_short"].replace(" ", "_").lower()
    language = context["language"].lower()

    # Create dynamic filename
    output_filename = f"cover_letter-{company_short}-{sender_identifier}-{language}.tex"

    # Save .tex file
    tex_file = "renders/" + output_filename
    with open(tex_file, "w") as f:
        f.write(rendered)

    return output_filename


# Compile TeX to PDF
def compile_tex_to_pdf(tex_filename):
    """
    Compile a LaTeX file to PDF using lualatex. Working directory is set to 'renders'.
    :param tex_filename: Name of the .tex file to compile.
    """
    subprocess.run(["lualatex", tex_filename], cwd="renders")


if __name__ == "__main__":
    # Get language input from user, default to 'de'
    language = input("Enter language (en/DE): ").strip().lower() or "de"

    filename = render_tex_file(language=language)
    compile_tex_to_pdf(filename)

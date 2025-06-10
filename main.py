import yaml
import subprocess
from jinja2 import Environment, FileSystemLoader

# Import the YAML file
with open("data_en.yml", "r") as file:
    data = yaml.safe_load(file)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("cover_letter_template.tex.j2")

# Render LaTeX
rendered = template.render(**data)

# Save .tex file
tex_file = "renders/cover_letter_en.tex"
with open(tex_file, "w") as f:
    f.write(rendered)

# Compile to PDF
subprocess.run(["lualatex", tex_file])

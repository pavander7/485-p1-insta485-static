"""Build static HTML site from directory of HTML templates and plain files."""
from pathlib import Path
from json import JSONDecodeError, load
import sys
from shutil import copytree
import click
import jinja2


# DRIVER FUNCTION
@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('-o', '--output', nargs=1, type=click.Path(exists=False),
              help="Output directory.")
@click.option('-v', '--verbose', is_flag=True, help="Print more output.")
def main(input_dir, output, verbose):
    """Templated static website generator."""
    # ----STEP 01: PROCESS COMMAND LINE W/ CLICK----

    # locate input directory
    input_dir = Path(input_dir)

    # initialize & locate output directory
    output_dir = None
    if output is None:
        output_dir = Path(input_dir / 'html')
    else:
        output_dir = Path(output)

    # INVARIANT: output_dir cannot already exist
    if output_dir.exists():
        print(f"insta485generator error: '{output_dir}' already exists")

    # locate config.json
    config_filename = input_dir / 'config.json'
    config_filename = Path(config_filename)

    # INVARIANT: input_dir must have a config.json
    if not config_filename.exists():
        print(f"insta485generator error: '{config_filename}' not found")
        sys.exit(2)

    # ----STEP 02: PROCESS CONFIG W/ JSON----

    # extract dictionaries from cofig.json
    try:
        dictionaries = dictionaries_get(config_filename=config_filename)

    # INVARIANT: config.json must be valid
    except (JSONDecodeError) as err:
        print(f"insta485generator error: '{config_filename}'")
        print(err)
        sys.exit(3)

    # ----STEP 03: PROCESS TEMPLATES W/ JINJA2

    # loop through templates
    for book in dictionaries:

        # --STEP 03A: EXTRACT INFORMATION--

        # extract url from dictionaries & strip leading '/'
        url = book.get('url')
        url = url.lstrip("/")

        # extract template from dictionaries
        template_file = book.get('template')

        # extract context from dictionaries
        context = book.get('context')

        # --STEP 03B: RENDER TEMPLATE W/ JINJA2--

        # render template using values extracted from dictionaries
        try:
            render = render_template(template_dir=input_dir / 'templates',
                                     template_file=template_file, data=context)

        # INVARIANT: template must be valid
        except (jinja2.exceptions.TemplateError) as err:
            print(f"insta485generator error: '{template_file}'")
            print(err)
            sys.exit(4)

        # ---STEP 03C: WRITE TO OUTPUT--

        # write to output
        output_path = scribe(render=render, output_dir=output_dir, url=url)

        # CHATTY CATHY
        if verbose:
            print(f"Rendered index.html -> {output_path}")

    # ----STEP 04: COPY STATIC DIR (OPTIONAL)----
    static_copy(input_dir=input_dir, output_dir=output_dir, verbose=verbose)


# CONTEXT MANAGER
def dictionaries_get(config_filename):
    """Context manager for dictionaries retrieval from config.json."""
    with config_filename.open() as config_file:
        #  config_filename is open within this code block
        return load(config_file)
    #  config_filename is automatically closed


# JINJA2 TEMPLATE RENDERER
def render_template(template_dir, template_file, data):
    """Jinja2 Template Renderer."""
    # intialize environment from template_dir
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )

    # generate template in template_env from template_file
    template = template_env.get_template(template_file)

    # render template by injecting data
    render = template.render(data)

    # return final render
    return render


# OUTPUT WRITER
def scribe(render, output_dir, url):
    """HTML file writer."""
    # locate uninitialized output file
    output_path = output_dir / url / 'index.html'
    output_path = Path(output_path)

    # ensure output directory is ready for scribing
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # write to output file
    output_path.write_text(render, encoding='utf-8')

    # return file location
    return output_path


def static_copy(input_dir, output_dir, verbose):
    """Check for static directory and copy any contents."""
    # generate static directory path
    static_dir = input_dir / 'static'
    static_dir = Path(static_dir)

    # check for static directory
    if static_dir.exists() and static_dir.is_dir():

        # execute copy
        copytree(src=static_dir, dst=output_dir, dirs_exist_ok=True)

        # CHATTY CATHY
        if verbose:
            print(f"Copied {static_dir} -> {output_dir}")


if __name__ == "__main__":
    main()

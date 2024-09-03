"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib
import json

def main():
    """Top level command line interface."""
    print("Hello World!")

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('-o', '--output', nargs=1, type=click.Path(exists=True), help = "Output directory.")
@click.option('-v', '--verbose', is_flag=True, help = "Print more output.")
def main(input_dir, output, verbose):
    input_dir = pathlib.Path(input_dir)
    print(f"DEBUG input_dir={input_dir}")
    print(f"DEBUG output={output}")
    if verbose :
        print("DEBUG verbose selected")

    config_filename = input_dir / 'config.json'
    config_filename = pathlib.Path(config_filename)
    with config_filename.open() as config_file:
        # config_filename is open within this code block
        print(f"DEBUG config_file(name)={config_file}")
        library = json.load(config_file)[0]
        print(f"DEBUG Library={library}")
        url = library.get('url')
        print(f"DEBUG url={url}")
        template = library.get('template')
        print(f"DEBUG template={template}")
        context = library.get('context')
        print(f"DEBUG context={context}")
        return
    # config_filename is automatically closed

    

if __name__ == "__main__":
    main()


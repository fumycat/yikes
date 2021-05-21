import os
import click

@click.command()
@click.option('--dim', type=click.INT, help='Number of greetings.')
@click.option('--name', help='The person to greet.')
@click.argument('filename', type=click.Path())
def gen(dim, name, filename):
    """Program that creates test cases."""

    click.echo(filename)
    click.echo(dim)
    with open(filename, 'x') as file:
        file.write('test\nhi ')

    
    for x in range(dim):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    gen()
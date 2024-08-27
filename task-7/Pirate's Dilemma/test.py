import click

@click.command()
@click.argument('number', type=click.INT)
def my_script(number):
    click.echo(f"You entered the number: {number}")

if __name__ == '__main__':
    my_script()

import sys
import os.path
import click
import six

home = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(home, "pdf2mp3"))

import mp3_converter

try:
	import colorama

	colorama.init()
except ImportError:
	colorama = None

try:
	from termcolor import colored
except ImportError:
	colored = None



@click.group()
@click.version_option(colored("1.0.0", "magenta"))
def main():
	"""Pdf2audio"""
	pass


@main.command()
@click.argument('path', required=True, type=click.Path(exists=True))
@click.option('-n', '--name',default='test')
def convert(name,**kwargs):
	"""Convert a pdf into audio file (mp3)"""
	six.print_(colored(mp3_converter.extract_text(kwargs.get('path'),name), "green"))


if __name__ == '__main__':
	args = sys.argv
	if "--help" in args or len(args) == 1:
		six.print_(colored("pdf2mp3", "magenta"))
	main()

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from PyPDF2 import PdfFileReader
from tqdm import tqdm
import pyttsx3
import six
from time import sleep

try:
	import colorama

	colorama.init()
except ImportError:
	colorama = None

try:
	from termcolor import colored
except ImportError:
	colored = None

engine = pyttsx3.init()


def on_start(name,length):
	with tqdm(total=length, desc=colored(name,"cyan")) as pbar:
		for i in range(length):
			sleep(0.2)
			pbar.update(1)


def on_error(name, exception):
	six.print_(colored(f"{name} caused error: ","red"))
	raise Exception(exception)


def get_info(pdf_path,in_file):
	pdf = PdfFileReader(in_file)
	information = pdf.getDocumentInfo()
	number_of_pages = pdf.getNumPages()

	txt = f"""
		  Information about {pdf_path}: 
		  Author: {information.author}
		  Creator: {information.creator}
		  Producer: {information.producer}
		  Subject: {information.subject}
		  Title: {information.title}
		  Number of pages: {number_of_pages}
		  """
	return txt,number_of_pages


def get_text(in_file,output_string,number_of_pages):
	parser = PDFParser(in_file)
	doc = PDFDocument(parser)
	rsrcmgr = PDFResourceManager()
	device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	for page in tqdm(PDFPage.create_pages(doc), total=(number_of_pages - 1), desc=colored('Converting pdf to text',"cyan")):
		interpreter.process_page(page)


def convert_to_audio(number_of_pages,output,file_name):
	engine.connect('started-utterance', on_start('Converting text to audio', number_of_pages - 1))
	engine.connect('error', on_error)
	engine.save_to_file(output, f'{file_name}.mp3')
	engine.runAndWait()


def extract_text(pdf_path, file_name):
	output_string = StringIO()

	with open(pdf_path, 'rb') as in_file:
		info,number_of_pages = get_info(pdf_path, in_file)
		get_text(in_file,output_string,number_of_pages)

	output = output_string.getvalue()
	output = output.replace('\n','')
	output = output.replace('\t','')
	output = info + output

	convert_to_audio(number_of_pages,output,file_name)

	return f"Finished converting pdf at {pdf_path} to {file_name}.mp3"


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
from time import sleep
engine = pyttsx3.init()


def on_word(name, location, length):
	with tqdm(total=length, desc=name) as pbar:
		for i in range(10):
			sleep(0.1)
			pbar.update(length/10)


def on_error(name, exception):
	print(f"{name} caused error: ")
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
	for page in tqdm(PDFPage.create_pages(doc), total=(number_of_pages - 1), desc='Converting pdf to text'):
		interpreter.process_page(page)


def convert_to_audio(number_of_pages,output):
	engine.connect('started-word', on_word('Converting text to audio', 0, number_of_pages - 1))
	engine.connect('error', on_error)
	engine.save_to_file(output, 'test_01.mp3')
	engine.runAndWait()


def extract_text(pdf_path):
	output_string = StringIO()

	with open(pdf_path, 'rb') as in_file:
		info,number_of_pages = get_info(pdf_path, in_file)
		get_text(in_file,output_string,number_of_pages)

	output = output_string.getvalue()
	output = output.replace('\n','')
	output = output.replace('\t','')
	output = info + output

	convert_to_audio(number_of_pages,output)

	return 'Finished converting pdf to mp3'


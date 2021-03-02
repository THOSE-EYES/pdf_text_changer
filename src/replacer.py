import os
import argparse
import json
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DecodedStreamObject, NameObject, NullObject

class Replacer :
	def __init__(self, input, replacements):
		# Open PDF streams
		self._input = input
		self._inputPDF = PdfFileReader(input)
		self._outputPDF = PdfFileWriter()
		self._replacements = replacements

	def __replaceText(self, content):
		lines = content.splitlines()
		result = str()

		for line in lines:
			for key, value in self._replacements.items():
				line = line.replace(key, value)
			result += (line + '\n')

		return result

	def __processContent(self, content):
		data = content.getData()

		# Replace data inside of the encoded file
		decodedData = data.decode('utf-8')
		replacedData = self.__replaceText(decodedData)
		encodedData = replacedData.encode('utf-8')

		# Save data as PDF page's content object
		decodedContent = DecodedStreamObject()
		decodedContent.setData(encodedData)

		return decodedContent

	def __processFile(self):
		# Iterate over the pages
		for number in range(0, self._inputPDF.getNumPages()):
			page = self._inputPDF.getPage(number)
			contents = page.getContents()

			# Try to iterate over the content
			try :
				for instance in contents:
					stream = instance.getObject()
					contents = self.__processContent(contents)
			except AttributeError:
				# If the content is not iterable (not a container)
				contents = self.__processContent(contents)

			# Update the content
			page[NameObject('/Contents')] = contents

			# Save the page
			self._outputPDF.addPage(page)

	def process(self):
		self.__processFile()

		if self._outputPDF.getNumPages() != 0 :
			with open(self._input + ".result.pdf", 'wb') as out_file:
				print ("Saving...")
				self._outputPDF.write(out_file)
		else :
			print("Nothing to write. Exiting...")


def get_arguments():
	# Get data from the user
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--replacements', required=True, type=json.loads)
	parser.add_argument("-i", "--input", required=True, help="path to PDF document")
	args = vars(parser.parse_args())

	# Parse arguments
	replacements = args["replacements"]
	input_file = args["input"]

	return input_file, replacements

def main():
	input_file, replacements = get_arguments()

	# Replace the text
	replacer = Replacer(input_file, replacements)
	out = replacer.process()

if __name__ == "__main__":
	main()
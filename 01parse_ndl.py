import glob, os
import xml.etree.ElementTree as et
import re

# define namespaces
ns = {'oai':     'http://www.openarchives.org/OAI/2.0/',
      'dcterms': 'http://purl.org/dc/terms/',
      'dcndl':   'http://ndl.go.jp/dcndl/terms/',
      'rdf':     'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
      'foaf':    'http://xmlns.com/foaf/0.1/' }

# function for isbn 10->13 with exception handling
def isbn10to13(isbn):
	# remove "-"
	isbn = re.sub('-', '', isbn)

	# isbn 10 -> 13
	if (len(isbn) == 10):
		sum = 0
		isbn = "978"+isbn

		# calc check digit
		for i in range(len(isbn)-1):

			# check for X (even if it is not at the last digit)
			if (isbn[i] == "X"):
				c = 10
			else:
				c = int(isbn[i])

			# calc weight
			if (i % 2):
				w = 3
			else:
				w = 1

			sum += w * c
			res = 10 - (sum % 10)
			if (res == 10):
				res = 0
		return isbn[0:12]+str(res)
	else:
		return isbn	

# begin main
# for all files
for file in glob.glob('../data/opac_2020-01-29/*.xml'):

	# read file
	tree = et.parse(file)
	root = tree.getroot()

	# for each record
	for r in root.iterfind('.//oai:record', ns):

		# get NDL id
		ndl_id = r.find('.//oai:header/oai:identifier',ns).text

		# get isbn
		e = r.find('.//oai:metadata//dcterms:identifier[@rdf:datatype="http://ndl.go.jp/dcndl/terms/ISBN"]', ns)

		# only proceed if ISBN exists
		if e is not None:
			isbn = e.text

			# get language
			tmp = r.find('.//dcndl:BibResource/dcterms:language[@rdf:datatype="http://purl.org/dc/terms/ISO639-2"]', ns)
			if tmp is not None:
				lang = tmp.text
			else:
				lang = "nan"

			# get publisher (could be empty)
			tmp = r.find('.//dcndl:BibResource/dcterms:publisher/foaf:Agent/foaf:name',ns)
			if tmp is not None:
				publisher = tmp.text
			else:
				publisher = "nan"

			# get year
			tmp = r.find('.//dcndl:BibResource/dcterms:issued[@rdf:datatype="http://purl.org/dc/terms/W3CDTF"]',ns)
			if tmp is not None:
				year = tmp.text
			else:
				year = "nan"


			print(file, isbn, isbn10to13(isbn), year, lang, publisher, sep='\t')

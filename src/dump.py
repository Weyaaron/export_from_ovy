def teste():
    pass

    import PyPDF2
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords

    filename = "Data.pdf"
    pdfFileObj = open(filename, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    num_pages = pdfReader.numPages
    count = 0
    text = ""  # The while loop will read each page.
    while count < 5:
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText()

    print(text)


def testd():
    import pdftotext

    # Load your PDF
    with open("Data.pdf", "rb") as f:
        pdf = pdftotext.PDF(f)

    # How many pages?
    print(len(pdf))

    # Iterate over all the pages
    for page in pdf:
        print(page)

    # Read some individual pages
    print(pdf[0])
    print(pdf[1])

    # Read all the text into one string
    print("\n\n".join(pdf))


def testc():
    for i in range(0, 100):
        table = tabula.read_pdf("Data.pdf", pages=i)
        table[0].to_csv("./data/test" + str(i) + ".csv")
        print("Done " + str(i))


#  print(table[0].to_csv())


def testb():

    table_list = []
    for i in range(0, 2):

        tables2 = camelot.read_pdf("Data.pdf", flavor="stream", pages=str(i))
        table_list.append(tables2[0])

    print(table_list[0])
    pass


from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

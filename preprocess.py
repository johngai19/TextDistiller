from imports import *

def splitChapters(filename):
    checkFlag = 0
    skipCount = 0
    flag = 0
    chapterNumber = 0
    filename = filename[:7]
    file = filename + '.txt'
    with open(file, 'r', encoding='utf-8') as f1:
        lines = f1.readlines()
        print('Total Number of Lines:', len(lines))
        for line in lines:
            words = ['CONTENTS', 'Contents']
            ignoreWords = ['ACKNOWLEDGEMENT', 'INDEX', 'Subject Index']
            tokens = line.split()
            check = any(item in words for item in tokens)

            if check is True:
                print('Contents page found!!\n')
                checkFlag = 1
                skipCount = 40
                continue

            elif checkFlag == 1 and skipCount > 0:
                skipCount -= 1
                continue

            pattern = re.compile(r'CHAPTER')
            foundChapter = re.search(pattern, line)

            if foundChapter:
                flag = 1
                chapterNumber += 1
                counter = 0
                continue

            elif flag == 1:
                if counter == 0:
                    counter += 1
                    print('Chapter',chapterNumber,'found! Writing to a txt file')
                    file = filename + 'Chapter' + str(chapterNumber) + '.txt'
                    with open(file, 'w', encoding='utf-8') as f2:
                        f2.write(line)
                    f2.close()
                else:
                    print('Writing chapter', chapterNumber, '!\n')
                    file = filename + 'Chapter' + str(chapterNumber) + '.txt'
                    with open(file, 'a', encoding='utf-8') as f2:
                        f2.write(line)
                    f2.close()
                continue

            ignoreCheck = any(item in ignoreWords for item in tokens)
            if ignoreCheck is True:
                print('All Chapters written!\n')
                break
    f1.close()

def pdfParser(filename):

    fp = open(filename, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp, check_extractable=False):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    print('Converting PDF to txt file')
    filename = filename[:7]
    file = filename + '.txt'
    with open(file, 'w', encoding='utf-8') as f:
        f.write(data)
    f.close()
    print('Successfully converted PDF to txt.')
    splitChapters(filename)



from imports import *
from mail import *

model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def cleanText(text):
    text = re.sub(r"@[A-Za-z0-9]+", ' ', text)
    text = re.sub(r"https?://[A-Za-z0-9./]+", ' ', text)
    text = re.sub(r"[^a-zA-z.!?'0-9]", ' ', text)
    text = re.sub('\t', ' ', text)
    text = re.sub(r" +", ' ', text)
    return text


def getSummary(text, tokenizer):
    preprocess_text = text.strip().replace("\n", "")
    t5_prepared_Text = "summarize: " + preprocess_text
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)

    summary_ids = model.generate(tokenized_text,
                                 num_beams=5,
                                 no_repeat_ngram_size=2,
                                 min_length=30,
                                 max_length=96,
                                 early_stopping=True)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output


def sentenceCorrection(text):
    correctedText = ""
    parser = GingerIt()
    sentences = sent_tokenize(text, language='english')
    for sentence in sentences:
        sentenceDict = parser.parse(sentence)
        sentence = str(sentenceDict['result'])
        correctedText += sentence

    return correctedText


def summaryGeneration(mailid=None):
    try:
        txtFiles = []
        for filename in os.listdir(app.config["PDF_UPLOADS"]):
            if fnmatch.fnmatch(filename, 'pdf_fileChapter*.txt'):
                print(filename)
                txtFiles.append(filename)

        for fname in txtFiles:
            summary = ""
            print("Summarising: ", fname)
            text = ""
            with open(os.path.join(app.config['PDF_UPLOADS'] + '/' + fname), 'r', encoding="utf-8") as f:
                textLines = f.readlines()
                for line in textLines:
                    line = cleanText(line)
                    line = line.replace("\n", " ")
                    text += line

                textTokens = word_tokenize(text)
                totalTokens = len(textTokens)
                chunkCounter = 0
                maxTokenLen = 400
                chunkList = []
                start = 0
                end = maxTokenLen

                if (totalTokens % maxTokenLen) == 0:
                    totalChunks = int(totalTokens / maxTokenLen)

                    for i in range(0, totalChunks):
                        tempTokens = textTokens[start:end]
                        chunkText = ' '.join([str(elem) for elem in tempTokens])
                        chunkList.append(chunkText)
                        start = end
                        end += maxTokenLen
                        chunkText = ""

                else:
                    totalChunks = int(totalTokens / maxTokenLen) + 1

                    for i in range(0, (totalChunks - 1)):
                        tempTokens = textTokens[start:end]
                        chunkText = ' '.join([str(elem) for elem in tempTokens])
                        chunkList.append(chunkText)
                        start = end
                        end += maxTokenLen
                        chunkText = ""

                    tempTokens = textTokens[start:totalTokens]
                    chunkText = ' '.join([str(elem) for elem in tempTokens])
                    chunkList.append(chunkText)

                for chunk in chunkList:
                    tempSummary = getSummary(chunk, tokenizer)
                    summary += tempSummary

                summary = sentenceCorrection(summary)

                print("Summarisation complete!")
                fileName = fname[:-4] + "_summary.txt"
                with open(os.path.join(app.config['PDF_UPLOADS'] + '/' + fileName), 'w', encoding="utf-8") as f1:
                    f1.write(summary)
                print("Summary written to file!")
                f1.close()
            f.close()
            os.remove(os.path.join(app.config['PDF_UPLOADS'] + '/' + fname))
        makezipAndCleanUp(mailid)
    except Exception as e:
        print(e)
        send_fail(mailid)


def makezipAndCleanUp(mailid=None):
    # function to compress all summary text files into single zip file
    # call mail function and send zip file
    shutil.make_archive('summarized_chapters', 'zip', app.config['PDF_UPLOADS'])
    for file in os.listdir(app.config['PDF_UPLOADS']):
        os.remove(os.path.join(app.config['PDF_UPLOADS'] + '/' + file))
    if mailid is not None:
        send_mail('summarized_chapters.zip', mailid)
    else:
        print('\nChapter-wise Summaries stored in summarized_chapters.zip')

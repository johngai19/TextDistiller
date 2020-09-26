from imports import *
from mail import *

model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')


def cleanText(text):
    text = re.sub(r"@[A-Za-z0-9]+", ' ', text)
    text = re.sub(r"https?://[A-Za-z0-9./]+", ' ', text)
    text = re.sub(r"[^a-zA-z.!?'0-9]", ' ', text)
    text = re.sub('\t', ' ',  text)
    text = re.sub(r" +", ' ', text)
    return text

def getSummary(text,tokenizer):
    preprocess_text = text.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+preprocess_text
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)


    # summmarize
    summary_ids = model.generate(tokenized_text,
                                        num_beams=4,
                                        no_repeat_ngram_size=2,
                                        min_length=30,
                                        max_length=512,
                                        early_stopping=True)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output

def summaryGeneration(mailid):
    txtFiles = []
    for filename in os.listdir(app.config["PDF_UPLOADS"]):
        if fnmatch.fnmatch(filename, 'pdf_fileChapter*.txt'):
            print(filename)
            txtFiles.append(filename)

    for fname in txtFiles:
        print("Summarising :", fname)
        text = ""
        with open(os.path.join(app.config['PDF_UPLOADS'] + '/' + fname), 'r', encoding="utf-8") as f:
            textLines = f.readlines()
            for line in textLines:
                line = cleanText(line)
                line = line.replace("\n", " ")
                text += line

            summary = getSummary(text, tokenizer)
            print("Summarisation done!!!")
            fileName = fname[:-4] + "_summary.txt"
            with open(os.path.join(app.config['PDF_UPLOADS'] + '/' + fileName), 'w', encoding="utf-8") as f1:
                f1.write(summary)
            print("Summary written into file!")
            f1.close()
        f.close()
        os.remove(os.path.join(app.config['PDF_UPLOADS'] + '/' + fname))

    #makezip(mailid)

#def makezip(mailid):
    # function to compress all summary text files into single zip file
    # call mail function and send zip file


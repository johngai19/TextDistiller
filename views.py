from imports import *
from preprocess import *
from mail import *


def allowed_pdf(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    return False




@app.route('/upload-pdf', methods=["GET", "POST"])
def upload_pdf():
    if request.method == "POST":
        if request.files:
            pdf = request.files["pdf"]
            mail = request.form['email']

            if pdf.filename == "":
                # msg = "PDF must have a filename."
                return render_template('public/upload_pdf.html')
            if not allowed_pdf(pdf.filename):
                # msg = "Incorrect extension. Please upload a PDF."
                return render_template('public/upload_pdf.html')
            else:
                #filename = secure_filename(pdf.filename)
                filename = 'pdf_file.pdf'
                pdf.save(os.path.join(app.config["PDF_UPLOADS"], filename))
                pdfParser(os.path.join(app.config["PDF_UPLOADS"], 'pdf_file.pdf'), 'deshpandesaarth@gmail.com')
                return render_template('public/upload_pdf.html')
        return redirect(request.url)
    return render_template('public/upload_pdf.html')


if __name__ == '__main__':
    app.run()

#    pdfParser(os.path.join(app.config["PDF_UPLOADS"], filename))

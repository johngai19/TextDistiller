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

@app.route("/", methods=["GET"])
def redirect_to_site():
    return redirect(request.url + 'upload-pdf')

@app.route('/upload-pdf', methods=["GET", "POST"])
def upload_pdf():
    if request.method == "POST":
        if request.files:
            pdf = request.files["pdf"]
            mail = request.form['email']

            if pdf.filename == "":
                return render_template('public/upload_pdf.html')
            if not allowed_pdf(pdf.filename):
                return render_template('public/upload_pdf.html')
            else:
                filename = 'pdf_file.pdf'
                pdf.save(os.path.join(app.config["PDF_UPLOADS"], filename))
                thread = Thread(target = pdfParser, kwargs={'filename': os.path.join(app.config["PDF_UPLOADS"], 'pdf_file.pdf'), 'mailid': f'{mail}'})
                thread.start()
                return render_template('public/upload_pdf.html')
        return redirect(request.url)
    return render_template('public/upload_pdf.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 9876))
    app.run(host="0.0.0.0", port=port)

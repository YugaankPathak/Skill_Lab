import os
import fitz  # PyMuPDF
from flask import Flask, send_from_directory, render_template, url_for, flash, request
import toPDF
import table
import API
import to_csv

#Initializing the app variable
app= Flask(__name__)

with open('static/appkey.txt','r') as f:
    key=f.read()
    
app.config['SECRET_KEY'] = key

#Defining the directories
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'Uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DOWNLOAD_FOLDER = os.path.join(os.getcwd(),'Download/')
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

Table_Folder = os.path.join(os.getcwd(),'Tables/')
app.config['TABLE_FOLDER'] = Table_Folder

#Path to the uploaded PDF
pdf_path = 'I:/Skill_Lab/Uploads/_p_d_f.pdf'

#home page
@app.route('/', methods=['POST','GET'])
def home():
    return render_template('Home.html',title='Summarizer-Home')

#summarizer part
@app.route('/submit', methods=['POST'])
def submit_file1():
    if 'pdfFile' not in request.files:
        return "No file part"
    
    file = request.files['pdfFile']
    
    if file.filename == '':
        flash('Upload a File to Continue','danger')
        return home()
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], '_p_d_f.pdf')
        file.save(file_path)
        return gen_sum()
    else:
        return "Please upload a PDF file"
    
#table extractor part
@app.route('/TablesExt', methods=['POST'])
def submit_file2():
    if 'pdfFile' not in request.files:
        return "No file part"
    
    file = request.files['pdfFile']
    
    if file.filename == '':
        flash('Upload a File to Continue','danger')
        return home()
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], '_p_d_f.pdf')
        file.save(file_path)
        return ext_Tab()
    else:
        return "Please upload a PDF file"
   
#Download page for summary
@app.route('/download', methods=['POST','GET'])
def download(summy):
    flash('Summarization Complete','success')
    with open('I:/Skill_Lab/Download/summary.txt','w',encoding='utf-8',errors='replace') as f:
       f.write(summy)
    toPDF.toPDF()
    files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    return render_template('Download.html',title='Summarizer-Download',text="Summary", summary=to_csv.process(summy),files=files)

#Download page for summary
@app.route('/downloadTable', methods=['POST','Get'])
def downloadTable(summary):
    flash('Extraction Complete','success')
    files = os.listdir(app.config['TABLE_FOLDER'])
    if not files:
        summary="Sorry, No Tables Found!"
    return render_template('DownTable.html',title='Table-Download',text="Table(s)", summary=summary, files=files)

#helper to the summarizer function, extracts text
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

#main summarizer caller fucntion  
def gen_sum():
   extracted_text= extract_text_from_pdf(pdf_path)
   summary= API.summarize(extracted_text)
   partwise_summary= API.summ(extracted_text)
   with open('I:/Skill_Lab/Download/summary.txt','w',encoding='utf-8',errors='replace') as f:
       f.write(summary)
   to_csv.CSV()
   return download(partwise_summary)

#extractor module caller function
def ext_Tab():
    table.getTables(pdf_path)
    return downloadTable("Here are the extracted tables.")

#uploader for pdf
@app.route('/download/<filename>')
def uploaded_file(filename):
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

#uploader for pdf
@app.route('/downloadTable/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['TABLE_FOLDER'], filename)
   
if __name__ == '__main__':
    app.run(debug=True)
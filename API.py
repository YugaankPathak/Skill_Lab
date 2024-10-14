import google.generativeai as genai

key=""
with open('static/key.txt','r') as f:
    key=f.read()

genai.configure(api_key=key)

def summarize(text):

    model = genai.GenerativeModel('gemini-1.5-flash')
    TEXT= text
    response = model.generate_content("Give me a summary of this union budget having columns as Category, Allocation/Change, Details in tabluar form seperated by '|', Categories should be unique, mention numbers/figures in the Allocation/Change column and its short description in the Details column, dont give any opening line or notes, just give the table, keep the headings and subheadings as plain text and not bold text, cover all important points : "+TEXT)
    return response.text

def summ(text):

    model = genai.GenerativeModel('gemini-1.5-flash')
    TEXT= text
    response = model.generate_content("Give me a properly structured summary of this budget, Split paragraphs in titles of 'Agriculture','Service Sector','Manufacturing Sector'and 'Taxes' each of maximum 50 words:"+TEXT)
    return response.text
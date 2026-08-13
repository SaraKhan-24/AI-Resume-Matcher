import pdfplumber

def extract_text(file_path:str)->str:
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text=page.extract_text()
            print(text)
    return text

if __name__=="__main__":
    print(extract_text("testfiles/Resume.pdf"))
    print("--------------------------------")
    print(extract_text("testfiles/testpdf.pdf"))
import pdfplumber
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def pdf_to_text(path):
    with pdfplumber.open(path) as pdf:
        content = ''
        for page in pdf.pages:
            content += ''.join(page.extract_text().split('\n')[:-1])
    return content

def clean_data(x, additional_chars):
    x = re.sub('{IMG:.?.?.?}', ' ', x)
    x = re.sub('<!--IMG_\d+-->', ' ', x)
    x = re.sub('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', ' ', x)  # 过滤网址
    x = re.sub('<a[^>]*>', '', x).replace("</a>", " ")  # 过滤a标签
    x = re.sub('<P[^>]*>', '', x).replace("</P>", " ")  # 过滤P标签
    x = re.sub('<strong[^>]*>', ',', x).replace("</strong>", " ")  # 过滤strong标签
    x = re.sub('<br>', ',', x)  # 过滤br标签
    x = re.sub('www.[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', '', x).replace("()", " ")  # 过滤www开头的网址
    x = re.sub('\s', ' ', x)   # 过滤不可见字符
    x = re.sub('Ⅴ', 'V', x)

    for wbad in additional_chars:
        x = x.replace(wbad, ' ')
    return x

    return x

def extract_tokenize_from_pdf(path):
    content = pdf_to_text(path)
    additional_chars = set()
    additional_chars.update(re.findall(u'[^\u4e00-\u9fa5a-zA-Z0-9\*]', str(content)))
    # 一些需要保留的符号
    extra_chars = set("!#+._#‘’")
    additional_chars = additional_chars.difference(extra_chars)
    content = content.lower()
    content = clean_data(content, additional_chars)
    tokenizes = word_tokenize(content)
    # remove stop words
    tokenizes = [w for w in tokenizes if w not in stopwords.words('english')]

    return tokenizes




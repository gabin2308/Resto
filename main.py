from app import app
import unicodedata
from dotenv import load_dotenv  

load_dotenv()  

def slugify(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower().replace(" ", "_")

app.jinja_env.filters['slugify'] = slugify

if __name__ == '__main__':
    app.run(debug=True)

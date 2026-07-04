# ============================================================
# CONTRACTION_MAPPING — English contractions -> expanded form
# (based on the user's original list, kept as-is; this list is already
# comprehensive for standard English contractions)
# ============================================================
CONTRACTION_MAPPING = {
    "ain't": 'is not', "aren't": 'are not', "c'est": "c'est", "c'mon": "c'mon",
    "can't": 'cannot', 'cause': 'because', "con't": 'continued', "cont'd": 'continued',
    "could've": 'could have', "couldn't": 'could not', "didn't": 'did not',
    "doesn't": 'does not', "don't": 'do not', "else's": 'else', "gov's": 'government',
    "gov't": 'government', "gov'ts": 'governments', "govt's": 'government',
    "had'nt": 'had not', "hadn't": 'had not', "hasn't": 'has not', "haven't": 'have not',
    "he'd": 'he would', "he'll": 'he will', "he's": 'he is', "here's": 'here is',
    "how'd": 'how did', "how'd'y": 'how do you', "how'll": 'how will', "how's": 'how is',
    "i'd": 'i would', "i'd've": 'i would have', "i'll": 'i will', "i'll've": 'i will have',
    "i'm": 'i am', "i's": 'it is', "i've": 'i have', "isn't": 'is not', "it'd": 'it would',
    "it'd've": 'it would have', "it'll": 'it will', "it'll've": 'it will have',
    "it's": 'it is', "let's": 'let us', "ma'am": 'madam', "mayn't": 'may not',
    "might've": 'might have', "mightn't": 'might not', "mightn't've": 'might not have',
    "must've": 'must have', "mustn't": 'must not', "mustn't've": 'must not have',
    "needn't": 'need not', "needn't've": 'need not have', "o'clock": 'of the clock',
    "oughtn't": 'ought not', "oughtn't've": 'ought not have', "sha'n't": 'shall not',
    "shan't": 'shall not', "shan't've": 'shall not have', "she'd": 'she would',
    "she'd've": 'she would have', "she'll": 'she will', "she'll've": 'she will have',
    "she's": 'she is', "should've": 'should have', "shouldn't": 'should not',
    "shouldn't've": 'should not have', "so's": 'so as', "so've": 'so have',
    "that'd": 'that would', "that'd've": 'that would have', "that'll": 'that will',
    "that's": 'that is', "there'd": 'there would', "there'd've": 'there would have',
    "there'll": 'there will', "there's": 'there is', "they'd": 'they would',
    "they'd've": 'they would have', "they'll": 'they will', "they'll've": 'they will have',
    "they're": 'they are', "they've": 'they have', "this's": 'this is', "to've": 'to have',
    "wasn't": 'was not', "we'd": 'we would', "we'd've": 'we would have', "we'll": 'we will',
    "we'll've": 'we will have', "we're": 'we are', "we've": 'we have', "weren't": 'were not',
    "what'll": 'what will', "what'll've": 'what will have', "what're": 'what are',
    "what's": 'what is', "what've": 'what have', "when's": 'when is', "when've": 'when have',
    "where'd": 'where did', "where's": 'where is', "where've": 'where have',
    "who'd": 'who would', "who'll": 'who will', "who'll've": 'who will have',
    "who're": 'who are', "who's": 'who is', "who've": 'who have', "why's": 'why is',
    "why've": 'why have', "will've": 'will have', "won't": 'will not',
    "won't've": 'will not have', "would't": 'would not', "would've": 'would have',
    "wouldn't": 'would not', "wouldn't've": 'would not have', "y'all": 'you all',
    "y'all'd": 'you all would', "y'all'd've": 'you all would have',
    "y'all're": 'you all are', "y'all've": 'you all have', "y'got": 'you got',
    "y'know": 'you know', "ya'll": 'you will', "you'd": 'you would',
    "you'd've": 'you would have', "you'll": 'you will', "you'll've": 'you will have',
    "you're": 'you are', "you've": 'you have',
}

# ============================================================
# SLANG_MAPPING — Malay SMS-speak / Manglish / English internet slang
#
# NOTE on sentiment safety: a handful of common short forms ("x", "tak",
# "tk", "bkn"...) are themselves negation tokens already recognized
# directly by lexicon.NEGATION_TOKENS — they are intentionally NOT
# remapped here to avoid double handling. Likewise "sgt", "gila" etc are
# already lexicon.INTENSIFIER_TOKENS and left as-is. This mapping mainly
# normalizes pronouns, connectors, and common shorthand so the lexicon
# doesn't need to separately enumerate every spelling variant of a word
# that ISN'T itself a sentiment-bearing term.
# ============================================================
SLANG_MAPPING = {
    # --- Malay: pronouns ---
    "sy": "saya", "sya": "saya", "aq": "aku", "ak": "aku", "ko": "kau",
    "koq": "kau", "kt": "kita", "kte": "kita", "kite": "kita",
    "korang": "kamu semua", "ko0rang": "kamu semua", "dia2": "dia orang",
    "dorang": "dia orang", "diorang": "dia orang", "kami2": "kami",
    # --- Malay: common shorthand (non-sentiment connectors) ---
    "yg": "yang", "tu": "itu", "dgn": "dengan", "dlm": "dalam",
    "sdh": "sudah", "ni": "ini", "nih": "ini", "mne": "mana", "mana2": "mana-mana",
    "dah": "sudah", "dh": "sudah", "udh": "sudah", "da": "sudah",
    "jgn": "jangan", "jangan2": "jangan-jangan", "mcm": "macam",
    "mcm2": "macam-macam", "camni": "macam ini", "camtu": "macam itu",
    "camne": "macam mana", "utk": "untuk", "org": "orang", "orng": "orang",
    "ape": "apa", "ap": "apa", "ape2": "apa-apa", "knp": "kenapa",
    "knapa": "kenapa", "sbb": "sebab", "skrg": "sekarang", "skrng": "sekarang",
    "skg": "sekarang", "smlm": "semalam", "mlm": "malam", "pg": "pagi",
    "ptg": "petang", "byk": "banyak", "bnyk": "banyak", "sket": "sedikit",
    "skit": "sedikit", "sikit2": "sedikit-sedikit", "blh": "boleh",
    "bley": "boleh", "bole": "boleh", "jd": "jadi", "jgk": "juga",
    "jugak": "juga", "tgk": "tengok", "tgh": "tengah", "bgtau": "beritahu",
    "btau": "beritahu", "ckp": "cakap", "citer": "cerita", "cite": "cerita",
    "kalo": "kalau", "klu": "kalau", "klau": "kalau", "klo": "kalau",
    "kalo2": "kalau-kalau", "igt": "ingat", "igtkan": "ingatkan",
    "almaklum": "dimaklumkan", "pasni": "lepas ini", "kowtim": "selesai",
    "sng": "senang", "mest": "mesti", "mst": "mesti", "esk": "esok",
    "ke2": "entah", "smua": "semua", "sumer": "semua", "trus": "terus",
    "trs": "terus", "lps": "lepas", "spe": "siapa", "sape": "siapa",
    "sesapa": "sesiapa", "bru": "baru", "bbrp": "beberapa", "byr": "bayar",
    "dpt": "dapat", "nti": "nanti", "nnt": "nanti", "tlg": "tolong",
    "tlng": "tolong", "ssh": "susah", "senanglah": "senang", "wat": "buat",
    "buatpe": "buat apa", "npe": "kenapa", "npa": "kenapa", "kne": "kena",
    "kena2": "kena", "tggl": "tinggal", "tggu": "tunggu", "tggu2": "tunggu-tunggu",
    "smpai": "sampai", "smpi": "sampai", "tpi": "tapi", "tp": "tapi",
    "ttp": "tetap", "stiap": "setiap", "stuju": "setuju", "stju": "setuju",
    "slh": "salah", "gi": "pergi", "aje": "sahaja", "nape": "kenapa",
    "mau": "mahu", "td": "tadi", "skjp": "sekejap", "lme": "lama",
    "skali": "sekali", "ye": "ya", "yer": "ya", "memang2": "memang",
    "sgt2": "sangat",
    # --- Malay: negation shorthand -> canonicalized to "tidak" ---
    # (x, tak, tk and all their compound forms below all resolve to a
    # "tidak ..." phrase so the rest of the pipeline only has to deal
    # with one consistent negation word)
    "x": "tidak", "tak": "tidak", "tk": "tidak", "bkn": "bukan",
    "tdk": "tidak", "xpe": "tidak apa", "xpe2": "tidak apa",
    "xtau": "tidak tahu", "xtahu": "tidak tahu", "xnak": "tidak nak",
    "xnk": "tidak nak", "tknak": "tidak nak", "xde": "tidak ada",
    "xada": "tidak ada", "xleh": "tidak boleh", "xboleh": "tidak boleh",
    "xblh": "tidak boleh", "xfaham": "tidak faham", "xphm": "tidak faham",
    "xpyh": "tidak payah", "xbest": "tidak best", "xsuka": "tidak suka",
    "xcaya": "tidak percaya", "xkan": "tidak akan", "takkan": "tidak akan",
    "xpernah": "tidak pernah", "xmungkin": "tidak mungkin",
    "xnampak": "tidak nampak", "xberapa": "tidak berapa",
    "xtahan": "tidak tahan", "xsangka": "tidak sangka",
    "xpasal": "tidak pasal", "xkesah": "tidak kisah", "xkisah": "tidak kisah",
    "xcukup": "tidak cukup", "xreti": "tidak reti", "xlarat": "tidak larat",
    "xterer": "tidak terer", "xpasti": "tidak pasti", "xsempat": "tidak sempat",
    "xsabar": "tidak sabar", "xmau": "tidak mahu", "xpun": "tidak pun",
    "taw": "tahu", "tau": "tahu",
    # --- Malay: vowel-dropped slang base forms (NOT sentiment words,
    #     map to standard spelling so sentiment lexicon entries still hit) ---
    "femes": "famous", "skola": "sekolah", "blaja": "belajar",
    # --- English: pronoun/shorthand ---
    "u": "you", "ur": "your", "yr": "your", "urs": "yours", "im": "i am",
    "ive": "i have", "ill": "i will", "id": "i would", "youre": "you are",
    "theyre": "they are", "thats": "that is", "whats": "what is",
    "hes": "he is", "shes": "she is",
    # --- English: negation contractions without apostrophes -> full form ---
    "isnt": "is not", "wasnt": "was not", "arent": "are not",
    "havent": "have not", "hasnt": "has not", "hadnt": "had not",
    "wouldnt": "would not", "couldnt": "could not", "shouldnt": "should not",
    "didnt": "did not", "doesnt": "does not", "dont": "do not",
    "cant": "cannot", "wont": "will not", "werent": "were not",
    "aint": "is not", "mustnt": "must not", "neednt": "need not",
    "darent": "dare not", "shant": "shall not", "neva": "never",
    # --- English: common abbreviations ---
    "pls": "please", "plz": "please", "btw": "by the way",
    "idk": "i do not know", "imo": "in my opinion", "imho": "in my opinion",
    "omg": "oh my god", "omw": "on my way", "brb": "be right back",
    "tbh": "to be honest", "smh": "shaking my head", "fyi": "for your information",
    "asap": "as soon as possible", "rn": "right now", "ngl": "not gonna lie",
    "tbf": "to be fair", "wbu": "what about you", "hbu": "how about you",
    "gg": "good game", "dm": "direct message", "irl": "in real life",
    "ftw": "for the win", "afaik": "as far as i know", "tho": "though",
    "bcoz": "because", "bcuz": "because", "cuz": "because", "coz": "because",
    "gonna": "going to", "wanna": "want to", "gotta": "got to",
    "kinda": "kind of", "sorta": "sort of", "lemme": "let me", "gimme": "give me",
    "dunno": "do not know", "gotcha": "got you", "yea": "yes", "yeah": "yes",
    "yep": "yes", "yup": "yes", "nope": "no", "nah": "no", "thx": "thanks",
    "thanx": "thanks", "np": "no problem", "jk": "just kidding",
    "afk": "away from keyboard", "n": "and", "tmrw": "tomorrow",
    "tmr": "tomorrow", "2day": "today", "2nite": "tonight", "b4": "before",
    "gr8": "great", "str8": "straight", "luv": "love", "msg": "message",
    "ppl": "people", "pic": "picture", "pics": "pictures", "vid": "video",
    "vids": "videos", "info": "information", "abt": "about", "w/": "with",
    "w/o": "without", "cld": "could", "shld": "should", "wld": "would",
    "rly": "really", "prob": "probably", "probs": "probably",
    "def": "definitely", "obv": "obviously", "obvi": "obviously",
    "appreciate it": "appreciate it", "congrats": "congratulations",
    "kk": "okay", "alrite": "alright", "aight": "alright",
    "evry": "every", "evryone": "everyone", "evrything": "everything",
    "dis": "this", "dat": "that", "diz": "this", "ders": "there is",
}

# ============================================================
# MALAY_STOPWORDS — common Malay function words.
# Negation words (tak, tidak, x, bukan...) and intensifiers (sangat,
# gila, memang...) are deliberately NOT included here even though many
# generic Malay stopword lists include them — removing them breaks the
# sentiment lexicon's negation/intensifier handling.
# ============================================================
MALAY_STOPWORDS = {
    "yang", "dan", "di", "dari", "daripada", "ke", "kepada", "ini", "itu",
    "untuk", "pada", "dengan", "juga", "adalah", "ialah", "atau", "akan",
    "telah", "sudah", "sedang", "boleh", "harus", "perlu", "mesti",
    "kita", "kami", "mereka", "anda", "kamu", "saya", "aku", "kau", "dia",
    "ia", "nya", "lah", "kah", "pun", "ada", "oleh", "seperti", "kerana",
    "supaya", "sebab", "bagi", "antara", "semua", "setiap", "satu", "dua",
    "para", "yakni", "iaitu", "tetapi", "namun", "walaupun", "sekiranya",
    "jika", "kalau", "apabila", "ketika", "semasa", "sementara", "hingga",
    "sehingga", "sampai", "selain", "selepas", "sebelum", "semasa",
    "ataupun", "mahupun", "lagi", "lain", "sahaja", "saja", "hanya",
    "sentiasa", "kadangkala", "biasanya", "sekarang", "tadi", "nanti",
    "esok", "semalam", "hari", "tahun", "bulan", "minggu", "masa",
    "waktu", "tempat", "orang", "yang mana", "begini", "begitu",
    "demikian", "tersebut", "berkenaan", "mengenai", "terhadap",
}

# ============================================================
# ENGLISH_STOPWORDS — derived from nltk's default English stopword list,
# with negation words and intensifiers removed (see module docstring).
# Embedded as a static set so this module has no nltk runtime dependency.
# ============================================================
ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "ain", "all", "am", "an",
    "and", "any", "are", "aren", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "couldn", "d", "did",
    "didn", "do", "does", "doesn", "doing", "don", "down", "during", "each", "few",
    "for", "from", "further", "had", "hadn", "has", "hasn", "have", "haven", "having",
    "he", "he'd", "he'll", "he's", "her", "here", "hers", "herself", "him", "himself",
    "his", "how", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn",
    "it", "it'd", "it'll", "it's", "its", "itself", "just", "ll", "m", "ma", "me",
    "mightn", "more", "most", "mustn", "my", "myself", "needn", "now", "o", "of",
    "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out",
    "over", "own", "re", "s", "same", "shan", "she", "she'd", "she'll", "she's",
    "should", "should've", "shouldn", "some", "such", "t", "than", "that", "that'll",
    "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they",
    "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "ve", "was", "wasn", "we", "we'd", "we'll", "we're",
    "we've", "were", "weren", "what", "when", "where", "which", "while", "who", "whom",
    "why", "will", "with", "won", "wouldn", "y", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves",
}

# For keyword frequency
MALAY_STOPWORDS_FULL = {
    # --- articles / determiners ---
    "yang", "ini", "itu", "satu", "dua", "tiga", "beberapa", "semua",
    "setiap", "tiap", "tiap-tiap", "mana-mana", "mana", "segala",
    "pelbagai", "berbagai", "sesuatu", "sebarang", "para", "se",
    # --- prepositions / postpositions ---
    "di", "ke", "dari", "daripada", "kepada", "pada", "untuk", "bagi",
    "oleh", "dengan", "antara", "antara", "tentang", "mengenai",
    "berkenaan", "terhadap", "terhadap", "melalui", "sepanjang", "sekitar",
    "seluruh", "merentasi", "hingga", "sehingga", "sampai", "sebelum",
    "selepas", "semasa", "sewaktu", "setelah", "sejak", "selain",
    "kecuali", "tanpa", "beserta", "bersama", "demi",
    # --- conjunctions ---
    "dan", "atau", "tetapi", "namun", "walau", "walaupun", "meskipun",
    "biarpun", "sungguhpun", "sekalipun", "kendatipun", "ataupun",
    "mahupun", "bahkan", "malah", "malahan", "juga", "serta", "lalu",
    "kemudian", "selepas itu", "lagi pun", "lagipun", "apatah lagi",
    "tambahan pula", "tambahan", "selain itu", "selain daripada itu",
    "justeru", "justeru itu", "oleh itu", "oleh sebab itu", "maka",
    "sehingga", "hingga", "supaya", "agar", "kerana", "sebab", "lantaran",
    "disebabkan", "memandangkan", "jika", "kalau", "sekiranya", "andai",
    "andainya", "andaikan", "apabila", "ketika", "tatkala", "manakala",
    "sementara", "selagi", "asalkan", "walaupun", "sungguh",
    # --- copulas / auxiliaries ---
    "adalah", "ialah", "merupakan", "menjadi", "jadikan", "akan", "telah",
    "sudah", "sedang", "masih", "pernah", "belum", "mahu", "nak", "boleh",
    "dapat", "mampu", "harus", "perlu", "mesti", "patut", "wajar", "suka",
    "ingin", "hendak",
    # --- pronouns ---
    "saya", "aku", "ku", "kita", "kami", "kamu", "anda", "awak",
    "kau", "engkau", "dia", "beliau", "ia", "mereka", "diri",
    "sendiri", "nya", "mu",
    # --- particles / discourse markers ---
    "lah", "lha", "kah", "tah", "pun", "jua", "sahaja", "saja", "hanya",
    "cuma", "je", "aje", "pula", "juga", "lagi", "lagi-lagi", "memang",
    "sebenarnya", "sebentar", "sebentar tadi", "sebenar", "rupanya",
    "rupa-rupanya", "agaknya", "barangkali", "mungkin", "kiranya",
    "tentunya", "sudah tentu", "pastinya", "pasti",
    # --- demonstratives / adverbs of place and time ---
    "sini", "sana", "situ", "sana sini", "di sini", "di sana", "di situ",
    "begini", "begitu", "demikian", "tersebut", "berkenaan",
    "sekarang", "kini", "tadi", "nanti", "kemudian", "esok", "semalam",
    "dahulu", "dulu", "terdahulu", "akhirnya", "akhir", "pertama",
    "pertamanya", "kedua", "ketiganya", "hari", "tahun", "bulan",
    "minggu", "masa", "waktu", "tempoh",
    # --- question words ---
    "apa", "siapa", "bila", "bagaimana", "kenapa", "mengapa", "berapa",
    "di mana", "ke mana", "dari mana",
    # --- negation (included for general-purpose NLP) ---
    "tidak", "tak", "bukan", "tiada", "tanpa", "jangan", "x",
    "bukanlah", "tidaklah", "takkan", "tidak akan", "bukan sahaja",
    "bukannya", "belum", "belum pun",
    # --- common filler / generic nouns used as discourse words ---
    "orang", "tempat", "perkara", "hal", "benda", "cara", "macam",
    "seperti", "contoh", "misalnya", "iaitu", "yakni", "sama ada",
    "sama", "lain", "berbeza", "tertentu", "berterusan", "sentiasa",
    "kadangkala", "kadang-kadang", "biasanya", "lazimnya", "selalu",
    "acap kali", "kerap", "jarang",
}
 
# ============================================================
# ENGLISH_STOPWORDS — comprehensive general-purpose English stopword list.
# Includes negation words (not, no, never, can't, won't, etc.) and common
# intensifiers since this list is for general NLP use (e.g. TF-IDF,
# topic modelling), NOT for the sentiment scorer pipeline.
# ============================================================
ENGLISH_STOPWORDS_FULL = {
    # --- articles / determiners ---
    "a", "an", "the", "this", "that", "these", "those", "some", "any",
    "all", "both", "each", "every", "few", "more", "most", "other",
    "such", "same", "own", "another", "either", "neither", "several",
    "enough", "much", "many", "more", "most", "least", "less",
    # --- prepositions ---
    "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below",
    "to", "from", "up", "down", "out", "off", "over", "under", "again",
    "further", "then", "once", "of", "along", "among", "around",
    "behind", "beside", "besides", "beyond", "despite", "except",
    "inside", "near", "outside", "since", "towards", "toward", "upon",
    "within", "without", "across", "per", "via", "versus",
    # --- conjunctions ---
    "and", "but", "or", "nor", "so", "yet", "for", "although", "because",
    "since", "unless", "until", "while", "whereas", "whether", "though",
    "even", "if", "when", "where", "how", "as", "than",
    # --- pronouns ---
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves", "he", "him",
    "his", "himself", "she", "her", "hers", "herself", "it", "its",
    "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "whose",
    # --- auxiliary / modal verbs ---
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "will", "would", "could", "should", "may", "might", "shall",
    "can", "ought", "must", "dare", "need",
    # --- negation (included for general-purpose NLP) ---
    "not", "no", "nor", "never", "neither", "nobody", "nothing",
    "nowhere", "none", "cannot", "cant", "cant't",
    "isn't", "isn", "wasn't", "wasn", "aren't", "aren",
    "weren't", "weren", "haven't", "haven", "hasn't", "hasn",
    "hadn't", "hadn", "don't", "don", "doesn't", "doesn",
    "didn't", "didn", "won't", "won", "wouldn't", "wouldn",
    "couldn't", "couldn", "shouldn't", "shouldn", "mustn't", "mustn",
    "mightn't", "mightn", "needn't", "needn", "shan't", "shan",
    "ain't", "ain", "daren't", "daresn't", "hardly", "scarcely",
    "barely", "without",
    # --- adverbs / discourse markers ---
    "very", "too", "just", "also", "only", "even", "still", "already",
    "almost", "quite", "rather", "really", "simply", "just", "already",
    "often", "usually", "sometimes", "always", "ever", "never",
    "here", "there", "now", "then", "soon", "just", "once", "twice",
    "again", "however", "therefore", "thus", "hence", "moreover",
    "furthermore", "meanwhile", "nevertheless", "nonetheless",
    "otherwise", "instead", "indeed", "certainly", "probably",
    "perhaps", "maybe", "actually", "basically", "generally",
    "typically", "especially", "particularly", "specifically",
    "literally", "obviously", "clearly", "apparently",
    # --- contractions (bare stems after apostrophe stripping) ---
    "i'd", "i'll", "i'm", "i've", "he'd", "he'll", "he's",
    "she'd", "she'll", "she's", "it'd", "it'll", "it's",
    "we'd", "we'll", "we're", "we've", "they'd", "they'll",
    "they're", "they've", "you'd", "you'll", "you're", "you've",
    "that's", "that'll", "that'd", "there's", "there'll", "there'd",
    "here's", "who's", "who'd", "who'll", "what's", "what'll",
    "when's", "where's", "why's", "how's", "should've", "could've",
    "would've", "might've", "must've", "let's",
    # --- bare stems left by apostrophe removal (nltk-style tokens) ---
    "d", "ll", "m", "re", "s", "t", "ve", "y",
    # --- misc high-frequency filler ---
    "etc", "eg", "ie", "vs", "via", "per", "re", "ok", "okay",
    "yes", "no", "well", "like", "go", "get", "got", "getting",
    "make", "made", "making", "know", "think", "say", "said",
    "see", "look", "come", "came", "take", "put", "give", "way",
    "thing", "things", "time", "year", "day", "week", "month",
    "people", "man", "men", "woman", "women", "place", "point",
    "part", "number", "use", "used", "using",'ada', 'la', 'lah',
    'buat', 'dalam', 'jadi', 'kena', 'tapi', '&', ',' '.', '!', 
    '-', '@', '?', 'nk', 'tu', 'ni', 'baru', 'kan', "s", 'kat',
    'banyak', 'tahu', 'lebih', 'baik', 'lepas', 'betul', 'sangat', 
    'terus', 'punya', 'pulak', 'ramai', 'us', 'why', 'good', 'one', 
    'cakap', 'ya', '2', '1', 'semoga', 'tengok', 'terbaik', 'besar', 'balik', 
    'kata', 'makan', 'guna', 'want', 'atas', 'pihak', 'masuk', 'naik', 'lama',
    'pakai', 'please', 'jalan', 'pon', 'mmg', 'lg', 'ambil', 'cari', 'kali', 'sekali', 
    'ikut', 'pergi', 'sebagai', 'berlaku', 'tolong', 'rasa', 
    'paling', 'turun', 'ingat', 'harap', 'benar', 'habis', 
    'keluar', 'biar', '3', 'back', 'free', 'years', 'luar', 'berani', 'biasa', 'bagus', 'nampak', 'tetap', 
    'bawa', 'kuat', 'terima', 'stop', 'going', 'nama', 'right', 'sgt', 'makin', 'kpd', 'tunggu', 'sikit', 'let',
    'nie', 'jer', 'ja', 'ka', 'takde', 'si', 'secara', 'dekat', 'pasal', 
    'kasi', 'susah', 'buang', 'berat', 'kurang', 'datang', 'jaga', 
     'senang',  'first', 'new', 'next', 'life', 'ade', 'dn', 'swt', 'salam', 'cukup', 'tinggi', 'cerita', 
    'hantar', 'menang', 'hilang', 'kepala', 'done', 'long' ,'bg',
    'dan', 'atau', 'tetapi', 'yang', 'untuk', 'dengan', 'pada', 'dari', 'daripada',
    'ke', 'di', 'ini', 'itu', 'sini', 'situ', 'sana', 'akan', 'telah',
    'sudah', 'sedang', 'belum', 'bukan', 'tidak', 'tiada', 'adalah', 'ialah', 'saya',
    'aku', 'kami', 'kita', 'kamu', 'anda', 'dia', 'mereka', 'ia', 'bila',
    'bila-bila', 'mengapa', 'kenapa', 'bagaimana', 'apa', 'siapa', 'mana', 'secara', 'bagi',
    'oleh', 'serta', 'seperti', 'bagaikan', 'umpama', 'maka', 'namun', 'malah', 'sambil',
    'kerana', 'sebab', 'agar', 'supaya', 'walaupun', 'sungguhpun', 'meskipun', 'sehingga', 'hingga',
    'sementara', 'banyak', 'tahu', 'lebih', 'baik', 'lepas', 'betul', 'sangat', 'terus',
    'punya', 'ramai', 'cakap', 'ya', 'semoga', 'tengok', 'terbaik', 'besar', 'balik',
    'kata', 'makan', 'guna', 'atas', 'pihak', 'masuk', 'naik', 'lama', 'ambil',
    'cari', 'kali', 'sekali', 'ikut', 'pergi', 'sebagai', 'berlaku', 'tolong', 'rasa',
    'paling', 'turun', 'ingat', 'harap', 'benar', 'habis', 'keluar', 'biar', 'bayar',
    'luar', 'berani', 'biasa', 'bagus', 'nampak', 'tetap', 'bawa', 'kuat', 'terima',
    'kasih', 'si', 'dekat', 'pasal', 'kasi', 'susah', 'buang', 'berat', 'kurang',
    'datang', 'jaga', 'gila', 'senang', 'ade', 'cukup', 'tinggi', 'cerita', 'hantar',
    'menang', 'hilang', 'kepala', 'buat', 'dengar', 'fikir', 'tanya', 'minta', 'bg',
    'bgii', 'yg', 'tk', 'tak', 'x', 'xdak', 'tu', 'ni', 'kt',
    'kat', 'dkt', 'dr', 'k', 'je', 'jer', 'ja', 'jrr', 'saja',
    'saje', 'pon', 'pun', 'pn', 'mmg', 'memg', 'lg', 'lgi', 'dh',
    'dah', 'blm', 'blum', 'knp', 'npa', 'cmne', 'cmna', 'mcmne', 'mcm',
    'mcm2', 'bkn', 'syg', 'utk', 'dgn', 'pd', 'drpd', 'sbb', 'krn',
    'korg', 'korang', 'dorg', 'diaorang', 'gtau', 'bgtau', 'tau', 'thw', 'klu',
    'kalu', 'jk', 'jika', 'tp', 'tpi', 'skrg', 'skg', 'msh', 'masih',
    'pax', 'pas', 'bleh', 'bkh', 'blh', 'xleh', 'xtakboleh', 'tgh', 'tengah',
    'nk', 'nak', 'xnak', 'xnk', 'g', 'gi', 'mai', 'kot', 'ko',
    'ka', 'wey', 'wei', 'weyh', 'lah', 'la', 'lar', 'loh', 'leh',
    'oh', 'ooh', 'uh', 'takde', 'xde', 'tkde', 'dn', 'swt', 'saw',
    'salam', 'al', '5', '6', '7', '8', '9', '10'
}
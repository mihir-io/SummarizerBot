from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words

LANG = 'english'
SENTENCE_COUNT = 7


def summarize_text(textbody):
    parser = PlaintextParser.from_string(textbody, Tokenizer(LANG))
    stemmer = Stemmer(LANG)

    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANG)

    summary = summarizer(parser.document, SENTENCE_COUNT)

    summarized_text = ''
    for sentence in summary:
        summarized_text += str(sentence) + ' '

    return summarized_text


def main():
    # Random comment from reddit.com/r/tifu to test with.
    print(summarize_text(
        "Ok. So. I am a bartender at a pretty popular place where I live. Last night I worked and after work around"
        " midnight I'm rolling silverware and having an after work beer. The barback walks up to me and says"
        " \"Hey, customers keep telling me there has been someone in the women's restroom for almost an hour."
        " I am worried someone is passed out in there, can you check it for me?\" Just so you know it is a one "
        "stall bathroom and that exact scenario has happened before. So I go over and I'm pounding on the door and no"
        " one answers. I start to panic. So I start pounding harder and eventually slam my shoulder into the door and"
        " bash the door open. Wood splinters from the door frame go flying. There is a girl on the toilet TAKING A"
        " DUMP. She turns to me and in the most classic valley girl voice says, \"Seriously?\" So I'm babbling and"
        " apologizing profusely saying oh man I work here blah blah blah. Super embarrassing. Then I come out of the"
        " bathroom area to tell my co workers carrying shard of wood with me and they tell me \"You know there\'s a"
        " KEY TO THE BATHROOM RIGHT?\" I. Am. So. Embarrassed. I'll never live it down. "
    )
    )


if __name__ == '__main__':
    main()

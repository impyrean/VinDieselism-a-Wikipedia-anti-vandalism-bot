# Chirag Medhora
# Under GPL

from datetime import date
import os
import sys

from sonet.mediawiki import EditsPageanalyzer, get_translations, get_tags
from sonet import lib
from sonet.timr import Timr

class EditsAnalyzer(EditsPageanalyzer):
    words_counter = 0
    counter_acceptable_words = None
    _check_creation = True
    _creation = None

    def __init__(self, **kwargs):
        super(EditsAnalyzer, self).__init__(**kwargs)
        self.tokenizer = ValdalWordsTokenizer()
        self.counter_acceptable_words = FreqDist()

    def process_text(self, elem):
        if self._skip:
            return

        try:
            text = elem.text.encode('utf-8')
        except AttributeError:
            return
        tokens = self.tokenizer.tokenize(clean_html(text.lower()))

        text = [t for t in tokens if len(t) > 2 and
                         t not in self.stopwords]
        self.words_counter += len(text)
        self.counter_acceptable_words.update(text)

        self.count += 1
        if not self.count % 100000:
            print 'PAGES:', self.counter_pages, 'REVS:', self.count
            sys.exit(0)

    def process_timestamp(self, elem):
        if self._skip or not self._check_creation: return

        timestamp = elem.text
        year = int(timestamp[:4])
        month = int(timestamp[5:7])
        day = int(timestamp[8:10])
        revision_time = date(year, month, day)
        if self._creation is None:
            self._creation = revision_time
        elif (revision_time - self._creation).days > 14:
            self.counter_first = self.counter_acceptable_words.copy()
            self._check_creation = False

    def save(self):
        data = dict((k, v) for k, v in
                    ((word, self.counter_acceptable_words.freq(word))
                    for word in self.words) if v > 0)
        del self.counter_acceptable_words
        ww = WikiWord(
            title=self._title,
            lang=self.lang,
            desired=self._desired,
            talk=(self._type == 'talk')
        )
        if data:
            ww.data = data
        if self.counter_first:
            data_first = dict((k, v) for k, v in
                              ((word, self.counter_first.freq(word))
                               for word in self.words) if v > 0)
            if data_first:
                ww.data_first = data_first
        elif data:
            ww.data_first = data
        self.counter_pages += 1
  	self.counter_acceptable_words = FreqDist()
        self._check_creation = True
        self._creation = None


def get_lines_in_list(fn, encoding='latin-1'):
    with open(fn) as f:
        lines = f.readlines()

    return [l.decode(encoding) for l in [l.strip() for l in lines]
            if l and not l[0] == '#']

def main():
    import optparse

    p = optparse.OptionParser(
        usage="usage: %prog [options] file desired_list acceptance_ratio")
    p.add_option('-v', action="store_true", dest="verbose", default=False,
                 help="Verbose output (like timings)")
    opts, files = p.parse_args()
    if opts.verbose:
        import logging
        logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)

    if not files:
        p.error("Error: No file received.")

    xml, desired_pages_fn, desired_words_fn = files[0:3]
    threshold = float(files[3])

    desired_words = [w.lower() for w in get_lines_in_list(desired_words_fn)]

    lang, _, _ = explode_dump_filename(xml)

    deflate, _lineno = lib.find_open_for_this_file(xml)

    if _lineno:
        src = deflate(xml, 51)
    else:
        src = deflate(xml)

    translation = get_translations(src)
    tag = get_tags(src, tags='page,title,revision,minor,timestamp,redirect,text')

    src.close()
    src = deflate(xml)

    analyzer = EditsAnalyzer(tag=tag, lang=lang)
    analyzer.set_desired_from_csv(desired_pages_fn)
    analyzer.words = desired_words

    with Timr('Analyzing...'):
        analyzer.start(src)

if __name__ == "__main__":
    import cProfile as profile
    profile.run('main()', 'mainprof')
    #main()

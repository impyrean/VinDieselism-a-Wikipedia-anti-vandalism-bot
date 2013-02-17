import time
import getopt

from collections import defaultdict

import requests
import feedparser

def main(argv):
    try:
        opts, args = getopt.gnu_getopt(argv[1:], '', [
            'publisher=',
            'update_frequency=',
            'name='
        ])
    except getopt.GetoptError as e:
        print(str(e))
        return 1

    update_frequency = 60
    name = 'wiki'
    for o, a in opts:
        if o == '--publisher':
            publisher = a.strip()
        elif o == '--update_frequency':
            update_frequency = int(a.strip())
        elif o == '--name':
            name = a.strip()

    last_checked = defaultdict(int)
    first_run = True

    while True:
        for wiki in args:
            d = feedparser.parse(wiki)

            for entry in d.entries:
                # We can ignore about certain namespaces.
                if entry.title.strip().startswith(_ignored_namespaces):
                    continue

                # See if this change has occured since the last time we analyzed this page.
                updated = time.mktime(entry.updated_parsed)
                if not first_run and updated > last_checked[wiki]:
                    line = []
                    line.append('[{0}]'.format(name))
                    line.append('Edit by {0} to {1} ->'.format(
                        entry.author,
                        entry.title
                    ))
                    line.append(requests.get(
                        'http://api.mediawiki.com/api-create.php?url={0}'.format(
                            entry.link
                    )).content)

                    requests.post(publisher, data={
                        'payload': ' '.join(line)
                    })

            last_checked[wiki] = max(
                time.mktime(e.updated_parsed) for e in d.entries
            )

        first_run = False
        time.sleep(update_frequency)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

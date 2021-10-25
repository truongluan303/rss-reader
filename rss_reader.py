'''
AUTHOR: Hoang (Luan) Truong

This program will check for new content in RSS feeds and summarizes that
content to a user. It can manage multiple RSS feeds, check its current
feeds, and add or remove by command-line interaction.
'''

from subprocess import check_call
from sys import executable

try:
    import feedparser
except:
    # install feedparser in case it is not previously installed
    check_call([executable, '-m', 'pip', 'install', 'feedparser'])
    import feedparser





class Commands:
    '''
    The commands that the users can use
    '''
    ADD = 'add'
    REMOVE = 'remove'
    CHECK = 'check'
    EXIT = 'exit'





class RssReader:
    '''
    Performs the basic functions of a RSS reader including adding
    new rss feed, removing rss feed, and checking new articles in
    the available rss feeds.
    '''

    def __init__(self) -> None:
        # The managed feed is a dictionary, where:
        #       each key is the URL
        #       the value is the set of already read articles
        self.feeds = dict()




    def add_rss(self, url: str) -> None:
        '''
        Add a new rss feed to the managed feeds.
        '''
        if url not in self.feeds:
            self.feeds[url] = set()
            print('Successfully Added', url,)

        else:
            print('The given link has already existed in the managed feeds')




    def remove_rss(self, url: str) -> None:
        '''
        remove a rss feed from the managed feeds.
        '''
        if url in self.feeds:
            del self.feeds[url]
            print('Successfully Removed', url)

        else:
            print('The managed feeds contain no RSS feed with the given link')




    def check_rss(self) -> None:
        '''
        Check for new articles in the managed feeds and print all the 
        new articles to the console output.
        '''

        if not self.feeds:
            print('There is no RSS feed available in the managed feeds')
            return

        displayed_count = 0     # number of new article displayed

        # loop through each rss feed
        for url in self.feeds.keys():

            # get the articles in the rss feed
            articles = feedparser.parse(url).entries
            displayed = False

            for article in articles:
                id = article['id']
                
                # check if there is any new article
                # if a new article is found, display it and add it to the set
                # else, moving on to the next article

                if id in self.feeds[url]:
                    continue

                title = article['title']
                description = article['description']
                link = article['link']

                if not displayed:
                    print('\nFeed URL:', url)
                    displayed = True

                print('\nArticle Title:', title)
                print('Description:', description)
                print('Link:', link)

                self.feeds[url].add(id)
                displayed_count += 1

                # the max number of articles to be displayed each time is 3
                if displayed_count == 3:
                    return

                



def main() -> None:

    rss_reader = RssReader()
    print('Welcome to RSS reader!\n')


    # Keep reading commands from the terminal input until the user exits.
    while True:

        print('\nPlease enter a command:')
        usr_input = input('> ').strip().lower().split()
        print()


        if len(usr_input) > 2:
            # there's no command with more than 1 argument
            print('Invalid Command!')


        elif len(usr_input) > 1:
            cmd, url = usr_input
            # if a command has 1 argument,
            # then it is either ADD or REMOVE

            if cmd == Commands.ADD:
                rss_reader.add_rss(url)

            elif cmd == Commands.REMOVE:
                rss_reader.remove_rss(url)

            else:
                print('Invalid Command!')


        elif len(usr_input) > 0:
            cmd = usr_input[0]
            # if the command has no argument,
            # then it is either CHECK or EXIT

            if cmd == Commands.CHECK:
                rss_reader.check_rss()

            elif cmd == Commands.EXIT:
                break

            else:
                print('Invalid Command')




if __name__ == '__main__':
    main()
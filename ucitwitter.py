#Kevin Pham
#FALL 2018 UCI CS
#ICS32A HERMANS
#PROJECT 3

from twitter import *
import geocoder

MY_KEY = 'KEY'
CONSUMER_KEY = 'KEY'
CONSUMER_SECRET = 'KEY'
ACCESS_TOKEN_KEY= 'KEY'
ACCESS_TOKEN_SECRET = 'KEY'
LOCATION = "33.645329,-117.840446,5mi"
LINK = 'https'
USER = '@'
api = Api(consumer_key=CONSUMER_KEY,
          consumer_secret=CONSUMER_SECRET,
          access_token_key=ACCESS_TOKEN_KEY,
          access_token_secret=ACCESS_TOKEN_SECRET,
          tweet_mode='extended')

def filterTimeline(keyword: str):
    """filter your home timeline (tweets from people you follow) to avoid any tweets that contain keyword."""

    home_list = []

    timeline = api.GetHomeTimeline(count=200,
                                   since_id=None,
                                   max_id=None,
                                   contributor_details=False)
    home_list.extend(timeline)

    for keywords in home_list:
        if keyword.lower() not in keywords.full_text.lower():
            if 'RT' not in keywords.full_text:
                print(keywords.full_text)

def commonWord(username: str):
    """
    return the most frequent word used by a Twitter user. Get the most recent 2,000 tweets from that user.
    Split the tweets into individual words (blank delimited) and store the word.
    Remove extraneous punctuation characters from words.
    Remove common and uninteresting words such as “the”, “a”, & “and”. Find the word that occurs most often.
    """
    list_id = []
    full_list = []
    counting = {}
    unwanted = []
    del_punc = ['.', ',', ':', '*', '!', "'", '-', '…', '/', ')', '(', '|', '"', '&', '?', ';', '#', '$', '%', '^']


    try:    
        search_user = api.GetUserTimeline(screen_name=username, count=200, include_rts=False)

        for x in search_user:
            full_list.append(x.full_text)

        while len(full_list) <= 2000:
            if len(search_user) == 0:
                break
            else:            
                search_user = api.GetUserTimeline(screen_name=username, count=200, max_id = search_user[-1].id - 1, include_rts=False)

            for o in search_user:
                full_list.append(o.full_text)
        
        with open('count_words.txt', 'w') as outfile:
            for tweets in full_list:
                outfile.write(tweets.lower() + "\n")

        with open('count_words.txt', 'r') as f:
            for word in f.read().split():
                word = word.replace('"','')
                for item in del_punc:
                    if item in word:
                        word = word.replace(item, '')
                if word.lower() not in counting:
                    counting[word] = 1
                else:
                    counting[word] += 1

        with open('uninteresting.txt', 'r') as z:
            for line in z.read().split():
                unwanted.append(line.lower())

        for words in unwanted:
            if words.lower() in counting:
                del counting[words]

        for val in list(counting):
            if LINK in val:
                del counting[val]
            elif USER in val:
                del counting[val]

        most_used = sorted(counting, key=(lambda key: counting[key]), reverse=True)
        print("Gathered tweets: " , len(full_list), ". The most used word for", username, "is", most_used[0])
        #print(sorted(counting, key=(lambda key: counting[key]), reverse=True))
        # for k, v in counting.items():
        #     print(k, ':', v)

    except Exception as e:
        print(e)

def getLocation(place: str) -> list:
    """Gets location of lat/long based on input"""
    area = []
    g = geocoder.mapquest(location=place, key='KEY')
    destination = g.latlng

    for items in destination:
        area.append(items)
    area.append('5mi')

    return area

def searchArea(area: list, keyword: str):
    """
    count the number of tweets originating from 5 miles of your location containing the keyword in the last 7 days.
    Location can be specified, if not, use your location as the default.
    """
    statuses = []
    count = 0
    location = api.GetSearch(term=keyword.lower(),
                             geocode=area,
                             since='2018-11-20',
                             return_json=False,
                             count=100,
                             result_type='recent')
    statuses.extend(location)

    while len(location) > 0:
        location = api.GetSearch(term=keyword.lower(),
                                 geocode=area,
                                 since='2018-11-20',
                                 return_json=False,
                                 count=100,
                                 max_id = location[-1].id - 1,
                                 result_type='recent')
        statuses.extend(location)

    x = list(set(statuses)) #remove duplicates
    
    for items in x:
        if 'RT' not in items.full_text:
            count += 1
    print(count, "tweets in your area!")

def main():

    choice = ''
    print('\nWelcome to UCITwitter API. Choose from the following choices.')
    print('1. Filter out your home timeline to not contain keyword inputted. (ENTER 1)')
    print('2. Search a user and see what their most used word is. (ENTER 2)')
    print('3. Enter a location and see how many tweets are within 5 miles with the given keyword. (ENTER 3)')
    print('4. EXIT (ENTER 4)')
    while choice != '4':
        choice = input('What would you like to do? : ')

        if choice == '1':
            keyword = input('Enter a keyword: ')
            filterTimeline(keyword)
        elif choice == '2':
            username = input('Enter a username, Example: kanyewest: ')
            commonWord(username)
        elif choice == '3':
            place = input('Enter a location, Example: Irvine, CA: ')
            keyword = input('Enter a keyword: ')
            area = getLocation(place)
            searchArea(area, keyword)
        elif choice == '4':
            exit()
        else:
            print('Invalid choice.')


if __name__ == "__main__":
    main()

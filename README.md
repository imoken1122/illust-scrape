# illust-scrape
Collect illustrations of your favorite illustrators and characters on Pixiv.  
(Please set a sufficient waiting time so as not to bother the server)

## Prerequisites
- Python==3.7
- selenium==3.141.0
- chromedriver-binary==90.0.4430.24.0
- beautifulsoup4==4.8.0
- tqdm


## Usage

### 0. Package install

Note: Match your chromedriver version to your chrome version.(Edit requirements.txt
```
$ pip install -r requirements.txt
```


### 1. Setting parameters

set the parameters your `id`, `passward` on Pixiv,` useragent`, `profile_path` in __setting.json__.  
(For `useragent`, copy the result of searching for "my user agent" in Google Chrome. Any name can be used for `profile_path` )  
Also, set `illustrator_id` to a list of illustrator numbers on pixiv, or `tag_word` is a list of characters you want to collect.



### 2. Login Process
To login to pixiv, do the following: your user information will be created in the `profile_path` folder and you will not need to login again to see the information from there.

```
$ python -c "import scraper ; scraper.login()"
```

### 3. Let's collect images
Decide whether you want to specify a user or a tag and do the following:

For user,
```
$ python scraper.py user
```

For tag,
```
$ python scraper.py tag 
```

After execution, the images will be saved in the __images__ folder sequentially.
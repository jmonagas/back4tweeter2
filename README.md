# back4tweeter2

This is the back code for the tweeter project part two

Tweeter Pt 2
Submit Assignment
Due Nov 28 by 11:59pm
Points 1,750
Submitting a website url

Available Nov 16 at 12am - Dec 22 at 11:59pm about 1 month
Our goal for this project is to start using our own backend instead of the provided API (tweeterest.ml). To do this we will need two things:

1. Our own database
2. Our own Python API

Database
You must implement the following tables:
• user
• user_session
• tweet
• tweet_like
• comment
• comment_like
• follow

RELATIONSHIP PICTURE
Which columns and foreign keys belong in each table is up to you. The API docs will give you hints (the data that is returned is a pretty good match for what columns need to match)
Remember the foreign keys need to represent relationships, so try to figure out what relationships you need between tables and add keys accordingly.

API
You must implement (at a minimum) an API that mimics the tweeterest.ml API. You require the following end points and HTTP request type support
• /api/users
o GET, POST, DELETE, PATCH
• /api/login
o POST, DELETE
• /api/follows
o GET, POST, DELETE
• /api/followers
o GET
• /api/tweets
o GET, POST, DELETE, PATCH
• /api/tweet-likes
o GET, POST, DELETE
• /api/comments
o GET, POST, DELETE, PATCH
• /api/comment-likes
o GET, POST, DELETE
The goal of the API at first should be to behave exactly like tweeterest.ml in terms of the required values and return values. This will ensure you don't have to change your vue project at all. If you finish the mimic, make sure you have a git commit / push at that point. You can then add extra features or try to change things if you want different functionality. Make sure you document these changes with comments in the API!
Bonus Tweeter ideas
(5% each unless otherwise indicated):
• Nested comments
o User can reply directly to another users comment
o You only need to go "1 level deep". Like Facebook comments!
• Share URL's (with preview)
o Example: url-preview-example.PNG
• Show a "profile card" when hovering a username
o Utilize AJAX to pull profile information from the database
o Display that information (name, profile, etc...)
o See Facebook & Twitter for examples of this
• Search (10%, 5% for each)
o Search by username and/or email
o Search by hashtags (only if implementing hashtags too)
• Infinite scroll
o Use AJAX to continuously load Tweets when the user scrolls down
o Example: www.facebook.com
• Re-tweeting
o If you re-tweet something, you must give attribution to the author
o Link back to the original tweet
• Notification system (10%)
o Someone likes your tweet
o Someone follows you
o Someone comments on your Tweet
o Someone replies to your comment
• Hashtagging (10%)
o What's trending
o Hashtags in Tweets must be clickable, and show a list of related Tweets
• Private messaging (10%)
o One to one private messages
o Maintain an "inbox" of messages
• Tweet using an uploaded photo (5%)
• Comment using an uploaded photo (5%)
• Login with Socialite (10%)
o See: https://developers.facebook.com/docs/facebook-login/

Budget your time accordingly. Don't forget to use Git workflow to develop new features!
The website must be published on your web server. Please submit the URL for your site and please comment the GitHub link after submission.

import praw
import pandas as pd
import plotly.express as px

data = {'upvotes': [], 'comments': [], 'title': []}

# Authenticate
reddit = praw.Reddit(
    "topComments"   # This pulls authentication from a praw.ini file in the local directory
)

subreddit_name = input("Please enter the name of the desired subreddit: ")

# Fetch top posts from r/Python
subreddit = reddit.subreddit(subreddit_name)

# .hot() returns a ListGenerator, so neeed to convert to a list
hot_posts = list(subreddit.hot(limit=25))

# Sort the list
hot_posts.sort(key=lambda post: post.score)

hot_post_number = 1
for post in hot_posts:
    # print(f"Post {hot_post_number}:\nTitle: {post.title}\nUpvotes: {post.score}\nComments: {post.num_comments}\nLink: {post.url}\n")
    data['upvotes'].append(post.score)
    data['comments'].append(post.num_comments)
    data['title'].append(post.title)
    hot_post_number += 1


df = pd.DataFrame(data)

# Create scatter plot with hover text
fig = px.scatter(df, x="upvotes", y="comments", hover_name="title",
                 hover_data=["upvotes", "comments"],
                 title=f"Reddit Top Posts: Upvotes vs Comments ({subreddit_name})")

# Update axis labels to be uppercase
fig.update_layout(
    xaxis_title="Upvotes",  # Uppercase x-axis label
    yaxis_title="Comments",  # Uppercase y-axis label
)

# Show the plot
fig.show()
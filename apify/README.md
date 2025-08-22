# Instagram Scraper Actor

This Apify actor scrapes Instagram posts and comments for audience analysis.

## Features

- Scrapes Instagram profile information
- Extracts posts with captions and like counts
- Collects comments with commenter usernames and profile pictures
- Configurable limits for posts and comments per post

## Input Parameters

```json
{
    "username": "target_instagram_username",
    "maxPosts": 10,
    "includeComments": true,
    "maxCommentsPerPost": 50
}
```

## Output

The actor outputs data in the following format:

```json
{
    "username": "target_username",
    "profileInfo": {
        "followers": "1000",
        "following": "500",
        "posts": "100"
    },
    "posts": [
        {
            "url": "https://instagram.com/p/post_id/",
            "caption": "Post caption text",
            "likes": 150,
            "comments": [
                {
                    "username": "commenter_username",
                    "text": "Comment text",
                    "profilePic": "https://profile-pic-url"
                }
            ]
        }
    ],
    "scrapedAt": "2024-01-01T00:00:00.000Z"
}
```

## Usage

1. Deploy this actor to Apify
2. Run with appropriate input parameters
3. Access results via Apify API
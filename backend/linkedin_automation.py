# linkedin_automation.py
import re
import requests
import json
import os

# Retrieve LinkedIn access token from environment variable
access_token = os.environ.get("LINKEDIN_ACCESS_KEY")

class LinkedinAutomate:
    def __init__(self, yt_url, title, description):
        self.yt_url = yt_url
        self.title = title
        self.description = description
        self.python_group_list = [102168168]
        self.headers = {
            'Authorization': f'Bearer {access_token}'
        }

    def common_api_call_part(self, feed_type="feed", group_id=None):
        payload_dict = {
            "author": f"urn:li:person:{self.user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": self.description
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": self.description
                            },
                            "originalUrl": self.yt_url,
                            "title": {
                                "text": self.title
                            },
                            "thumbnails": [
                                {
                                    "url": self.extract_thumbnail_url_from_YT_video_url()
                                }
                            ]
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" if feed_type == "feed" else "CONTAINER"
            }
        }
        if feed_type == "group":
            payload_dict["containerEntity"] = f"urn:li:group:{group_id}"

        return json.dumps(payload_dict)

    def extract_thumbnail_url_from_YT_video_url(self):
        exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
        s = re.findall(exp, self.yt_url)[0][-1]
        return f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"

    def get_user_id(self):
        url = "https://api.linkedin.com/v2/me"
        response = requests.request("GET", url, headers=self.headers)
        jsonData = json.loads(response.text)
        return jsonData["id"]

    def feed_post(self, generated_text):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self.common_api_call_part()
        payload_dict = json.loads(payload)
        payload_dict["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"] = generated_text
        payload = json.dumps(payload_dict)

        return requests.request("POST", url, headers=self.headers, data=payload)

    def group_post(self, group_id, generated_text):
        url = "https://api.linkedin.com/v2/ugcPosts"
        payload = self.common_api_call_part(feed_type="group", group_id=group_id)
        payload_dict = json.loads(payload)
        payload_dict["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"] = generated_text
        payload = json.dumps(payload_dict)

        return requests.request("POST", url, headers=self.headers, data=payload)

    def main_func(self, generated_text):
        self.user_id = self.get_user_id()

        # Post to the user's feed
        feed_post = self.feed_post(generated_text)
        print(feed_post)

        # Optionally, post to groups
        for group_id in self.python_group_list:
            print(group_id)
            group_post = self.group_post(group_id, generated_text)
            print(group_post)

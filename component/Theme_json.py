import json
from datetime import datetime

class ThemeInfo:
    def __init__(self, feed_Id, Theme_Id, Theme_title, Theme_Req, tags, web_site, date):
        self.feed_Id = feed_Id
        self.Theme_Id = Theme_Id
        self.Theme_title = Theme_title
        self.Theme_Req = Theme_Req
        self.tags = tags
        self.web_site = web_site
        self.date = date

def get_multiple_feed_for_theme(themes_list):
    result_dict = {}

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    for theme in themes_list:
        # Check if the Theme_Id is already in the result_dict
        if theme.Theme_Id not in result_dict:
            result_dict[theme.Theme_Id] = {}

        # Check if the feed_Id is already in the result_dict for the specific Theme_Id
        if theme.feed_Id not in result_dict[theme.Theme_Id]:
            result_dict[theme.Theme_Id][theme.feed_Id] = {
                "Theme_Title": theme.Theme_title,
                "Theme_Req": theme.Theme_Req,
                "tag": theme.tags,
                "web_site": theme.web_site
            }

    # Create the final result with the current date
    final_result = {current_date: result_dict}
    return json.dumps(final_result, indent=2)

# Example usage
themes_data = [
    ThemeInfo("Feed1", "Theme1", "Title1", "Req1", "Tag1", "Website1", "2022-01-01"),
    ThemeInfo("Feed2", "Theme1", "Title2", "Req2", "Tag2", "Website2", "2022-01-02"),
    ThemeInfo("Feed3", "Theme2", "Title3", "Req3", "Tag3", "Website3", "2022-01-03"),
    ThemeInfo("Feed4", "Theme2", "Title4", "Req4", "Tag4", "Website4", "2022-01-04"),
    ThemeInfo("Feed5", "Theme2", "Title5", "Req5", "Tag5", "Website5", "2022-01-05"),
]

result_json = get_multiple_feed_for_theme(themes_data)
print(result_json)

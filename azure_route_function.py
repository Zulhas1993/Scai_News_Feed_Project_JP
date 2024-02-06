import azure.functions as func
import json
from scenario.test_scenario import test_scenario
from scenario.ai_news_analysis_and_recommendation import ai_news_analysis_and_recommendation
from component.Details_News import get_news_details_list,generate_news_feed_list,generate_date_wise_news_feed_list
from component.Open_AI_Article_Create_Chat_API import get_articles_list
from component.User_Article_Json import get_User_articles
from component.QuestionList import GetquestionnaireList
from Models.Tag import Tags
from component.TagInfo import add_tags,update_tags,delete_tags



app = func.FunctionApp()

# Get News Details List
@app.route(route="GetNewsDetailsList", auth_level=func.AuthLevel.FUNCTION)
def get_news_details_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Call the function to get news details list
        news_details_list = get_news_details_list()

        if news_details_list is not None:
            # Convert the list to JSON and return as an HTTP response
            return func.HttpResponse(
                json.dumps(news_details_list),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse("An error occurred during news details retrieval.", status_code=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)

# Generate News Feed List all object are exist here
@app.route(route="GenerateNewsFeedList", auth_level=func.AuthLevel.FUNCTION)
def generate_news_feed_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Call the function to generate news feed list
        generated_news_feed_json = generate_news_feed_list()

        if generated_news_feed_json is not None:
            # Return the generated news feed as an HTTP response
            return func.HttpResponse(
                generated_news_feed_json,
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse("An error occurred during news feed generation.", status_code=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)

# ******************* Generate Date wise News Feed List***********************************
# ***Azure Functions HTTP-triggered endpoint ***
@app.route(route="GenerateDateWiseNewsFeedList", auth_level=func.AuthLevel.FUNCTION)
def generate_date_wise_news_feed_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Call the function to generate date-wise news feed list
        date_wise_news_feed_json = generate_date_wise_news_feed_list()

        if date_wise_news_feed_json is not None:
            # Return the generated date-wise news feed as an HTTP response
            return func.HttpResponse(
                date_wise_news_feed_json,
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse("An error occurred during date-wise news feed generation.", status_code=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
    


#*********************** Get article list ******************************
    # ***Azure Functions HTTP-triggered endpoint ***
@app.route(route="GetArticlesList", auth_level=func.AuthLevel.FUNCTION)
def get_articles_list_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Call the function to get articles list
        articles_list = get_articles_list()

        if articles_list is not None:
            # Convert the list to JSON and return as an HTTP response
            return func.HttpResponse(
                json.dumps(articles_list, ensure_ascii=False, indent=2),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse("An error occurred during articles list generation.", status_code=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)


# ************************** Get User article **********************************
# ***Azure Functions HTTP-triggered endpoint ***
@app.route(route="GetUserArticles", auth_level=func.AuthLevel.FUNCTION)
def get_formatted_user_articles_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Call the function to get articles list
        articles_list = get_articles_list()

        if articles_list is not None:
            # Call the function to format user articles
            formatted_user_articles = get_User_articles(articles_list)

            # Convert the formatted user articles to JSON and return as an HTTP response
            return func.HttpResponse(
                json.dumps(formatted_user_articles, ensure_ascii=False, indent=2),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse("An error occurred during articles list generation.", status_code=500)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
#***************Get questionnaire List *********************************
# Azure Functions HTTP-triggered endpoint
@app.route(route="GetquestionnaireList", auth_level=func.AuthLevel.FUNCTION)
def GetquestionnaireList_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Call the function to generate the response JSON
        response_json = GetquestionnaireList()

        # Return the JSON response as an HTTP response
        return func.HttpResponse(
            response_json,
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
    

#************************* Tags Route *****************************
# Azure Functions HTTP-triggered endpoint
@app.route(route="AddTags", auth_level=func.AuthLevel.FUNCTION)
def add_tags_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the request body to get the Tags object
        request_data = req.get_json()
        tags_object = Tags(
            id=request_data.get('id', ''),
            tag_name=request_data.get('tag_name', []),
            created_at=request_data.get('created_at', ''),
            deleted_at=request_data.get('deleted_at', ''),
            updated_at=request_data.get('updated_at', '')
        )

        # Call the function to add tags
        response_message = add_tags(tags_object)

        # Return the response as an HTTP response
        return func.HttpResponse(
            response_message,
            status_code=200 if "successfully" in response_message.lower() else 500,
            mimetype="application/json"
        )

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)



# Azure Functions HTTP-triggered endpoint
@app.route(route="UpdateTags", auth_level=func.AuthLevel.FUNCTION)
def update_tags_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the request body to get the update information
        request_data = req.get_json()
        tag_id = request_data.get('tag_id', '')
        updated_tags = request_data.get('updated_tags', [])

        # Call the function to update tags
        response_message = update_tags(tag_id, updated_tags)

        # Return the response as an HTTP response
        return func.HttpResponse(
            response_message,
            status_code=200 if "successfully" in response_message.lower() else 500,
            mimetype="application/json"
        )

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)



# Azure Functions HTTP-triggered endpoint
@app.route(route="DeleteTags", auth_level=func.AuthLevel.FUNCTION)
def delete_tags_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse the request body to get the deletion information
        request_data = req.get_json()
        tag_id = request_data.get('tag_id', '')
        tags_to_delete = request_data.get('tags_to_delete', [])

        # Call the function to delete tags
        response_message = delete_tags(tag_id, tags_to_delete)

        # Return the response as an HTTP response
        return func.HttpResponse(
            response_message,
            status_code=200 if "successfully" in response_message.lower() else 500,
            mimetype="application/json"
        )

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)



@app.route(route="News", auth_level=func.AuthLevel.FUNCTION)
def News(req: func.HttpRequest) -> func.HttpResponse:

    # AIを使ったニュースの分析とレコメンド生成
    results = ai_news_analysis_and_recommendation()
    return func.HttpResponse(
        json.dumps([result.__dict__ for result in results]),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="Test", auth_level=func.AuthLevel.FUNCTION)
def Test(req: func.HttpRequest) -> func.HttpResponse:
    test_scenario()
    return func.HttpResponse(
        "Test Succeed.",
        status_code=200
    )
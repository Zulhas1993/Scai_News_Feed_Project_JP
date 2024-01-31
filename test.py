def sample_abstractive_summarization() -> None:
    # [START abstract_summary]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = "https://laboblogtextanalytics.cognitiveservices.azure.com/"
    key = "09b7c88cfff44bac95c83a2256f31907"

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    document = [
        "Othello is not a game that originated in Japan | Koryu Kato @Kanare_Abstract Login Register Othello is not a game that originated in Japan No. 304\nKoryu Kato@Kanare_Abstract January 11, 2024 08:01 At the end of last year, I posted the following entry related to the news of the Othello solution. \nIn terms of content is a light essay, but when I searched online for materials related to Othello in order to write this, I found things like ``Othello is a game that originated in Japan'' and ``Othello is a thorny game.'' I noticed that I frequently came across posts and pages that said things like 'a game that originated in Mito City, Castle Prefecture,' and I started to feel a little confused. Briefly, because it's wrong. The origin of Othello is written in great detail on Wikipedia, which everyone should check first, with numerous sources.\n. \nOthello (board game) - Wikipedia ja.wikipedia.Inquiries to creators Feedback Recommendations from creators",
    ]

    poller = text_analytics_client.begin_abstract_summary(document)
    abstract_summary_results = poller.result()
    for result in abstract_summary_results:
        if result.kind == "AbstractiveSummarization":
            print("Summaries abstracted:")
            [print(f"{summary.text}\n") for summary in result.summaries]
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))
    # [END abstract_summary]


if __name__ == "__main__":
    sample_abstractive_summarization()

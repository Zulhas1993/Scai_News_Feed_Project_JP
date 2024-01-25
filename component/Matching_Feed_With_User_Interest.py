import os
from langchain.callbacks.manager import get_openai_callback
from langchain.chat_models.azure_openai import AzureChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from Details_News import generate_news_feed_list



os.environ["AZURE_OPENAI_API_KEY"] = "5e1835fa2e784d549bb1b2f6bd6ed69f" # シークレット情報の扱いを考える
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://labo-azure-openai-swedencentral.openai.azure.com/"

def __call_chat_api(messages: list) -> AzureChatOpenAI:
    model = AzureChatOpenAI(
        openai_api_version="2023-05-15",
        azure_deployment="labo-azure-openai-gpt-4-turbo",
    )
    with get_openai_callback():
        return model(messages)
    
def analysis_and_recommendation():
    request_messages = [
        SystemMessage(content="Please answer in English"),
    ]

    # personal_information="I am adnan. I am 29 years old. I am muslim. I ahve completed my graduation from CUET in 2017. I have 4 members in my family. I live in Dhaka, Bangladesh. I am working for a prvt software company as Senior Software Engineer."

    personal_information = {
        "name" : "adnan",
        "age" : 29,
        "religion" : "muslim",
        "education" : "graduate from CUET in 2017",
        "family-member" : 4,
        "home-town" : "Dhaka-Bangladesh",
        "occupation" : "software engineer",
        "company" : "private ltd",
        "designation" : "senior software engineer"
    }

    personal_interest = {
        "trip" : {
            "What is the primary purpose of your trip?" : {"Leisure/Vacation","Visiting Family or Friends"},
            "What type of accommodation do you prefer?" : {"Hotel","Vacation Rental"},
            "Which of the following travel apps do you plan to use?" : {"Navigation (e.g., Google Maps)"},
            "How do you intend to manage your finances while traveling?" : {"Using credit/debit cards"},
        },
        "sports" : {
            "what type of sports do you like most?" : {"Indoor", "Outdoor"},
            "what sports do you prefer to play?" : {"cricket", "table-tennis", "volley-ball"},
            "how often you play outfield sports" : {"daily"},
            "Who is your favorite player in all sports?" : {"Tamim Iqbal"}
        }
    }

    details_feed = {
        "Feed-01" : "Tamim Iqbal Khan, popularly known as Tamim Iqbal, is a Bangladeshi cricketer from Chittagong. He was the captain of the national team in ODI matches from 2020 to 2023. Tamim is considered as the greatest Bangladeshi batsman and the first Bangladeshi to score a century in the ICC Men’s T20 World Cup, making 103 not out against Oman in the 2016 tournament. His 103 not out is the highest score made by a Bangladeshi at any T20 World Cup tournaments. Tamim’s 128 which he made against England in the 2017 ICC Champions Trophy is also the highest score made by a Bangladeshi at any tournaments. He is Bangladesh’s highest century maker in international matches with 25 centuries, combining all forms of cricket. Tamim made his ODI debut in 2007 and played his first Test match the following year. He scored his first century against Ireland. In March 2021, Tamim became the first Bangladeshi player to score 50 ODI half-centuries. Tamim has been on a golden run in the last two years of his ODI career. In his last 24 innings, he has scored 3 hundreds (all away) and 10 fifties with an average of close to 60",
        "Feed-02" : "Japan is a country with a rich culture and history, and there are many things to see and do. The best time to visit Japan is during the spring and autumn seasons, when the weather is mild and the cherry blossoms are in full bloom. If you’re planning a trip to Japan, you should start by deciding which cities you want to visit. Tokyo, Kyoto, and Osaka are some of the most popular destinations in Japan. You can use online trip planners like Triptile or Wanderlog to create your itinerary and map out your trip. Once you’ve decided on your destinations, you can start looking for flights. Japan has several international airports, including Narita International Airport and Kansai International Airport. You can also travel around Japan by train using the Japan Rail Pass. The pass allows you to travel on most trains in Japan, including the Shinkansen bullet train. You can also use the pass to travel on local trains and buses. When it comes to accommodation, Japan has a wide range of options, from traditional ryokans to modern hotels. You can use websites like Booking.com or Airbnb to find the best deals on accommodation. Finally, don’t forget to try the local cuisine, which includes sushi, ramen, and tempura, among other delicious dishes",
        "Feed-03" : "Lionel Messi, born on June 24, 1987, is an Argentine professional footballer who plays as a forward for and captains both Major League Soccer club Inter Miami and the Argentina national team 1. Messi started playing football as a boy and in 1995 joined the youth team of Newell’s Old Boys (a Rosario-based top-division football club) 2. Messi’s phenomenal skills garnered the attention of prestigious clubs on both sides of the Atlantic. At age 13 Messi and his family relocated to Barcelona, and he began playing for FC Barcelona’s under-14 team. He scored 21 goals in 14 games for the junior team, and he quickly graduated through the higher-level teams until at age 16 he was given his informal debut with FC Barcelona in a friendly match 23. Messi is widely regarded as one of the greatest players of all time, having received a total of eight Ballon d’Or awards and three The Best FIFA Men’s Player awards, the most for any player 4. Messi has won numerous titles and achievements throughout his career, including Olympic Games, La Liga title, Champions League title, and many more 245. Messi’s Barcelona career timeline is a nearly two-decade run with superstar planning exit",
        "Feed-04" : "Dhaka Metro Rail is a mass rapid transit system serving Dhaka, the capital city of Bangladesh. It is owned and operated by the Dhaka Mass Transit Company Limited (DMTCL) 1. The metro rail network has five planned lines which are the MRT Line 6, the only operational line, MRT Line 1 and 5, which are under construction, and MRT Line 2 and MRT Line 4, which are in the planning stages 2. The MRT Line 6 is 20.1 km long and has 16 operational stations 2. The metro rail system is part of the Strategic Transport Plan outlined by the Dhaka Transport Coordination Authority (DTCA) 2. The metro rail system is expected to reduce traffic congestion in the city and provide a faster and more efficient mode of transportation for commuters 3. The metro rail system is also expected to have a positive impact on the environment by reducing air pollution and greenhouse gas emissions 3. The metro rail system is equipped with modern facilities such as air conditioning, CCTV cameras, and Wi-Fi connectivity 1. The metro rail system is expected to be a game-changer for the city of Dhaka, providing a much-needed solution to the city’s traffic problems",
        "Feed-05" : "The world economy refers to the global economic system, which includes all economic activities conducted both within and between nations, including production, consumption, economic management, work in general, exchange of financial values and trade of goods and services 1. The world economy is a complex and dynamic system that is influenced by a wide range of factors, including political events, technological advancements, and natural disasters. According to the International Monetary Fund (IMF), the global economy is experiencing a broad-based and sharper-than-expected slowdown, with inflation higher than seen in several decades 2. The cost-of-living crisis, tightening financial conditions in most regions, Russia’s invasion of Ukraine, and the lingering COVID-19 pandemic all weigh heavily on the outlook 2. The baseline forecast is for global growth to slow from 3.5 percent in 2022 to 3.0 percent in both 2023 and 2024, well below the historical (2000–19) average of 3.8 percent 3. The world economy can be evaluated and expressed in many ways, and it is inseparable from the geography and ecology of planet Earth 1. It is important to note that the world economy is typically judged in monetary terms, even in cases in which there is no efficient market to help valuate certain goods or services",
        "Feed-06" : "Artificial Intelligence (AI) is being increasingly used in cybersecurity to identify and prevent cyber threats. AI-powered solutions can help security teams detect and respond to threats more quickly and accurately, while also reducing the risk of human error. AI can be used to monitor network traffic and identify patterns that may indicate a cyber attack. It can also be used to analyze user behavior and detect anomalies that may indicate a security breach. AI can help automate incident response, reducing the time it takes to detect and remediate security issues. AI can also be used to identify vulnerabilities in software and hardware, and to develop more effective security protocols. However, AI technology is not without its risks. Hackers can use AI to develop more sophisticated attacks, and AI systems can be vulnerable to cyber attacks themselves. It is important for organizations to implement strong security measures to protect their AI systems, including encryption, access controls, and regular security audits. Organizations should also ensure that their employees are trained in cybersecurity best practices to reduce the risk of human error",
        "Feed-07" : "The next parliamentary election in Bangladesh is scheduled to take place on January 7, 2024 1. The election will be held to elect all 300 members of the Jatiya Sangsad, the unicameral national legislature of Bangladesh 2. The current ruling party, the Awami League, led by Sheikh Hasina, won the previous election in 2018 with a landslide victory 1. The party has been in power since 2009 and is seeking a fourth consecutive term in office 3. The opposition parties have accused the government of suppressing dissent and rigging the election in their favor 3. The election has been described as a “sham” by some observers, and the opposition parties have called for a boycott of the election 3. The election is expected to be closely watched by international observers, who will be monitoring the fairness and transparency of the electoral process 1. The outcome of the election will have significant implications for the future of Bangladesh, both domestically and internationally",
    }
    details_feed_list=generate_news_feed_list()

    # personal_interest="""
    #     ("Relaxation and adventure motivate me to travel, adventure and budget traveller, beaches and mountains are my travel destinations, travel agent will plan for my travel, planning for international travel",
    #     "Artificial Inteligence. Recent news for AI. AI documentations. AI machines. Microsoft AI services")
    # """

    # 記事の要約
    request_messages.extend([
        HumanMessage(content=
        f"""
        Consider yourself as a human nature analyzer.Now analyze this user interest and make a list of his human nature:
        User personal information: {personal_information}
        User interests: {personal_interest}
        """)
    ])
    content_from_api = __call_chat_api(request_messages).content

    # details_feed = """
    #     ("Historic books are portals to bygone eras, preserving the collective wisdom and tales of civilizations past. Through the weathered pages, one glimpses the evolution of ideas, cultures, and societies. These literary treasures bridge the gap between epochs, offering timeless insights that illuminate the rich tapestry of human history.",
    #     "Mobile phones have evolved from communication tools to indispensable companions. These pocket-sized marvels connect the world, offering instant communication, entertainment, and productivity. With sleek designs and powerful capabilities, they redefine daily life, providing access to information and connecting people across the globe in the palm of our hands.",
    #     "Web development is the art of crafting digital experiences, seamlessly blending creativity and technology. It encompasses designing and coding websites, ensuring functionality and aesthetic appeal. From front-end interfaces to back-end databases, web developers navigate the ever-evolving landscape of programming languages and frameworks, shaping the online world's dynamic presence.")
    # """

    # request_messages.extend([
    #     HumanMessage(content=
    #     f"""
    #     If you are looking for information about a trip, please list 20 things you need
    #     """             
    #     )
    # ])

    

    # content_from_api = __call_chat_api(request_messages)

    # request_messages.extend([
    #     AIMessage(content="""
    #               {content_from_api}
    #               """),
    #     HumanMessage(content=f"""
    #                  Match this below paragraph list according to the above user interest and categorized this list to best match, average match and no match:
    #                  {details_feed}
    #                  Also exclude the paragragph which is not directly related to user interest  and return only the id of the list.
    #                  """)
    # ])


    request_messages.extend([
        AIMessage(content="""
                  {content_from_api}
                  """),
        HumanMessage(content=f"""
                     Match this below paragraph list according to the above user interest and categorized this list to best match, average match and no match:
                     {details_feed_list}
                     Also exclude the paragragph which is not directly related to user interest  and return only the id of the list.
                     """)
    ])
    response = __call_chat_api(request_messages).content



    # request_messages.extend([
    #     AIMessage(content="""
    #               {content_from_api}
    #               """),
    #     HumanMessage(content=f"""
    #                  Make a questionnaire on the basis of above things with 4 options. Return the questionnaire in JSON format where key will be the questions and the value will the options.
    #                  """)
    # ])

    # response = __call_chat_api(request_messages).content

    print(response)

analysis_and_recommendation()
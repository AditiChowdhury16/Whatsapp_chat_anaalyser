# import streamlit as st
# import preprocessor
# import helper
# import matplotlib.pyplot as plt
#
# st.sidebar.title("Whatsapp Chat Analyzer")
#
# uploaded_file=st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#  bytes_data = uploaded_file.getvalue()
#  data=bytes_data.decode("utf-8")
#
#  df=preprocessor.preprocess(data)
#  st.dataframe(df)
#
#  #fetch unique users
#  user_list=df['user'].unique().tolist()
#  user_list.remove('group_notification')
#  user_list.sort()
#  user_list.insert(0,"overall")
#
#  selected_user=st.sidebar.selectbox("show analysis wrt",user_list)
#
#  if st.sidebar.button("show Analysis"):
#   num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
#   col1,col2,col3,col4= st.columns(4)
#
#   with col1:
#    st.header("Total Messages")
#    st.title(num_messages)
#
#   with col2:
#    st.header("Total Words")
#    st.title(words)
#
#   with col3:
#    st.header("Media Shared")
#    st.title(num_media_messages)
#
#   with col4:
#    st.header("links Shared")
#    st.title(num_links)
#
#
#    #finding the busiest user
#    if selected_user=='overall':
#     st.title('Most Busy Users')
#     x,new_df=helper.most_busy_users(df)
#     fig,ax=plt.subplots(figsize=(20, 15))
#
#     col1,col2=st.columns([2, 1])
#
#     with col1:
#      ax.bar(x.index, x.values,color='red')
#      plt.xticks(rotation='vertical')
#      st.pyplot(fig)
#     with col2:
#      st.dataframe(new_df,height=300)

import streamlit as st
from click import help_option

import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")  # Make full-width layout

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):


        # Fetch stats
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown("Total Messages")
            st.markdown(f"<h2 style='color: white;'>{num_messages}</h2>", unsafe_allow_html=True)

        with col2:
            st.markdown("Total Words")
            st.markdown(f"<h2 style='color: white;'>{words}</h2>", unsafe_allow_html=True)

        with col3:
            st.markdown("Media Shared")
            st.markdown(f"<h2 style='color: white;'>{num_media_messages}</h2>", unsafe_allow_html=True)

        with col4:
            st.markdown("Links Shared")
            st.markdown(f"<h2 style='color: white;'>{num_links}</h2>", unsafe_allow_html=True)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()

        ax.plot(timeline['time'], timeline['message'],color="red")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()

        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

       #activity map(active days in a week)
        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #heatmap
        st.title('Weekly Activity map')
        user_heatmap=helper.activity_heatmap(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # Most Busy Users
        if selected_user == 'overall':
            st.markdown("## Most Busy Users")

            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            plt.tight_layout()

            col1, col2 = st.columns([2, 1])

            with col1:
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df, height=300)

        #wordcloud
        st.title("wordcloud")
        df_wc=helper.create_wordcloud(selected_user, df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)

        st.pyplot(fig)

        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most common word')
        st.pyplot(fig)

        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)






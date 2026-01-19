import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

sns.set_style("whitegrid")
sns.set_palette("Set2")

st.sidebar.markdown(
    """
    <h2 style='text-align:center;color:#25D366;'>💬 WhatsApp Chat Analyzer</h2>
    <hr>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader("📂 Upload WhatsApp Chat File")

def stat_card(label, value, emoji):
    st.markdown("""
    <style>
    .stat-card {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.08);
        text-align: center;
    }
    .stat-title {
        color: #075E54 !important;
        font-size: 16px;
        font-weight: 600;
    }
    .stat-value {
        color: #25D366 !important;
        font-size: 32px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.markdown("## 📄 Chat Preview")
    st.dataframe(df, use_container_width=True)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Show analysis for", user_list)

    if st.sidebar.button("🚀 Show Analysis"):

        num_messages, words, media, links = helper.fetch_stats(selected_user, df)

        st.title("📊 Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Total Messages</div>
                <div class="stat-value">{num_messages}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Total Words</div>
                <div class="stat-value">{words}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Media Shared</div>
                <div class="stat-value">{media}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-title">Links Shared</div>
                <div class="stat-value">{links}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 🗓 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(timeline['time'], timeline['message'], linewidth=3, color='#25D366')
        ax.set_xlabel("Month")
        ax.set_ylabel("Messages")
        ax.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # ------------------ DAILY TIMELINE ------------------
        st.markdown("## 📆 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        ax.set_xlabel("Date")
        ax.set_ylabel("Messages")
        ax.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # ------------------ ACTIVITY MAP ------------------
        st.markdown("## 🔥 Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📅 Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(busy_day.index, busy_day.values, color='#128C7E')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.markdown("### 🗓 Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(busy_month.index, busy_month.values, color='#075E54')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.markdown("## 🧭 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots(figsize=(10,6))
        sns.heatmap(user_heatmap, cmap="YlGnBu", linewidths=0.5)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.markdown("## 🏆 Most Busy Users")
            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(6,4))
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df, use_container_width=True)

        st.markdown("## ☁ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(8,4))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        st.markdown("## 🗣 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(6,4))
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation=0)
        st.pyplot(fig)

        st.markdown("## 😄 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 Emoji Frequency")
            st.dataframe(emoji_df, use_container_width=True)

        with col2:
            fig, ax = plt.subplots(figsize=(6,6))
            ax.pie(
                emoji_df[1],
                labels=emoji_df[0],
                autopct='%0.1f%%',
                startangle=90,
                textprops={'fontsize': 14}
            )
            ax.set_title("Top Emojis Used", fontsize=16)
            st.pyplot(fig)

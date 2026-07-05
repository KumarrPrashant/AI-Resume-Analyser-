# Originally developed by dnoobnerd [https://dnoobnerd.netlify.app]  ·  Made with Streamlit
# Galaxy / Cosmos UI redesign


###### Packages Used ######
import streamlit as st  # core package used in this project
import pandas as pd
import base64, random
import time, datetime
import pymysql
import os
import socket
import platform
import secrets
import io, random
import plotly.express as px  # to create visualisations at the admin session
import plotly.graph_objects as go

# pre stored data for prediction purposes
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos

# ---- Galaxy theme engine ----
from theme import (
    inject_theme, hero, section_header, cosmic_success, cosmic_warning,
    cosmic_error, cosmic_info, cosmic_tip, info_chips, score_orb, badge,
    course_list_html, footer,
)

# Optional / best-effort imports — the app should still run (and still look great)
# even when these heavier / network-dependent dependencies aren't available.
try:
    import geocoder
    HAS_GEOCODER = True
except Exception:
    HAS_GEOCODER = False

try:
    from geopy.geocoders import Nominatim
    HAS_GEOPY = True
except Exception:
    HAS_GEOPY = False

try:
    from pyresparser import ResumeParser
    HAS_RESUME_PARSER = True
except Exception:
    HAS_RESUME_PARSER = False

try:
    from pdfminer3.layout import LAParams
    from pdfminer3.pdfpage import PDFPage
    from pdfminer3.pdfinterp import PDFResourceManager
    from pdfminer3.pdfinterp import PDFPageInterpreter
    from pdfminer3.converter import TextConverter
    HAS_PDFMINER = True
except Exception:
    HAS_PDFMINER = False

try:
    from streamlit_tags import st_tags
    HAS_ST_TAGS = True
except Exception:
    HAS_ST_TAGS = False

    def st_tags(label='', text='', value=None, key=None):
        """Graceful fallback for streamlit_tags when the package is unavailable."""
        st.markdown(f"**{label}**")
        st.write(", ".join(value or []))
        st.caption(text)
        return value or []

from PIL import Image

try:
    import nltk
    nltk.download('stopwords', quiet=True)
except Exception:
    pass


###### Preprocessing functions ######


# Generates a link allowing the data in a given panda dataframe to be downloaded in csv format
def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    ## bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


# Reads Pdf file and check_extractable
def pdf_reader(file):
    if not HAS_PDFMINER:
        return ""
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    ## close open handles
    converter.close()
    fake_file_handle.close()
    return text


# show uploaded file path to view pdf_display
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = (
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
        f'width="100%" height="700" '
        f'style="border-radius:16px;border:1px solid rgba(255,255,255,0.14);" '
        f'type="application/pdf"></iframe>'
    )
    st.markdown(pdf_display, unsafe_allow_html=True)


# course recommendations which has data already loaded from Courses.py
def course_recommender(course_list):
    section_header("Courses &amp; Certificates Recommendations 🎓")
    c = 0
    rec_course = []
    ## slider to choose from range 1-10
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    picked = []
    for c_name, c_link in course_list:
        c += 1
        picked.append((c_name, c_link))
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    course_list_html(picked)
    return rec_course


###### Database Stuffs ######


# sql connector — resilient: the app must stay usable (and look professional)
# even when no local MySQL server is available, e.g. for a quick demo/preview.
DB_AVAILABLE = False
connection = None
cursor = None
try:
    connection = pymysql.connect(host='localhost', user='root', password='root@MySQL4admin', db='cv')
    cursor = connection.cursor()
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False


# inserting miscellaneous data, fetched results, prediction and recommendation into user_data table
def insert_data(sec_token, ip_add, host_name, dev_user, os_name_ver, latlong, city, state, country, act_name,
                 act_mail, act_mob, name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills,
                 recommended_skills, courses, pdf_name):
    if not DB_AVAILABLE:
        return
    try:
        DB_table_name = 'user_data'
        insert_sql = "insert into " + DB_table_name + """
        values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        rec_values = (
            str(sec_token), str(ip_add), host_name, dev_user, os_name_ver, str(latlong), city, state, country,
            act_name, act_mail, act_mob, name, email, str(res_score), timestamp, str(no_of_pages), reco_field,
            cand_level, skills, recommended_skills, courses, pdf_name)
        cursor.execute(insert_sql, rec_values)
        connection.commit()
    except Exception:
        pass


# inserting feedback data into user_feedback table
def insertf_data(feed_name, feed_email, feed_score, comments, Timestamp):
    if not DB_AVAILABLE:
        return
    try:
        DBf_table_name = 'user_feedback'
        insertfeed_sql = "insert into " + DBf_table_name + """
        values (0,%s,%s,%s,%s,%s)"""
        rec_values = (feed_name, feed_email, feed_score, comments, Timestamp)
        cursor.execute(insertfeed_sql, rec_values)
        connection.commit()
    except Exception:
        pass


###### Setting Page Configuration (favicon, Logo, Title) ######

st.set_page_config(
    page_title="AI Resume Analyzer · Galaxy Edition",
    page_icon='./Logo/recommend.png',
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cosmic colour template for every Plotly chart in the app
px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#8b5cf6", "#3a86ff", "#f72585", "#06ffa5", "#ffd166", "#a855f7"]


def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#eef0fb",
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=60, b=20, l=10, r=10),
    )
    return fig


###### Main function run() ######


def run():

    inject_theme()
    hero(
        title_main="AI RESUME",
        title_grad="ANALYZER",
        subtitle="Navigate your career through the cosmos — parsed by AI, guided by the stars. "
                  "Upload your resume and let mission control chart your next move. 🌌",
    )

    # (Sidebar navigation)
    st.sidebar.markdown('<div class="sidebar-title">🛰️ MISSION CONTROL</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-caption">Choose your destination in the galaxy</div>',
                         unsafe_allow_html=True)
    activities = ["User", "Feedback", "About", "Admin"]
    icons_map = {"User": "🚀 User", "Feedback": "📡 Feedback", "About": "🌠 About", "Admin": "🔐 Admin"}
    choice_display = st.sidebar.selectbox(
        "Navigate to:", [icons_map[a] for a in activities]
    )
    choice = activities[[icons_map[a] for a in activities].index(choice_display)]

    if not DB_AVAILABLE:
        st.sidebar.markdown(
            '<div class="cosmic-alert alert-warning" style="font-size:.78rem;">'
            '🛰️ Database offline — running in local preview mode.</div>',
            unsafe_allow_html=True,
        )

    link = ('<div class="sidebar-foot">Built with 🤍 by '
            '<a href="https://dnoobnerd.netlify.app/" style="color:#a855f7;text-decoration:none;">'
            'Deepak Padhi</a></div>')
    st.sidebar.markdown(link, unsafe_allow_html=True)

    ###### Creating Database and Table ######

    if DB_AVAILABLE:
        try:
            # Create the DB
            db_sql = """CREATE DATABASE IF NOT EXISTS CV;"""
            cursor.execute(db_sql)

            # Create table user_data and user_feedback
            DB_table_name = 'user_data'
            table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                            (ID INT NOT NULL AUTO_INCREMENT,
                            sec_token varchar(20) NOT NULL,
                            ip_add varchar(50) NULL,
                            host_name varchar(50) NULL,
                            dev_user varchar(50) NULL,
                            os_name_ver varchar(50) NULL,
                            latlong varchar(50) NULL,
                            city varchar(50) NULL,
                            state varchar(50) NULL,
                            country varchar(50) NULL,
                            act_name varchar(50) NOT NULL,
                            act_mail varchar(50) NOT NULL,
                            act_mob varchar(20) NOT NULL,
                            Name varchar(500) NOT NULL,
                            Email_ID VARCHAR(500) NOT NULL,
                            resume_score VARCHAR(8) NOT NULL,
                            Timestamp VARCHAR(50) NOT NULL,
                            Page_no VARCHAR(5) NOT NULL,
                            Predicted_Field BLOB NOT NULL,
                            User_level BLOB NOT NULL,
                            Actual_skills BLOB NOT NULL,
                            Recommended_skills BLOB NOT NULL,
                            Recommended_courses BLOB NOT NULL,
                            pdf_name varchar(50) NOT NULL,
                            PRIMARY KEY (ID)
                            );
                        """
            cursor.execute(table_sql)

            DBf_table_name = 'user_feedback'
            tablef_sql = "CREATE TABLE IF NOT EXISTS " + DBf_table_name + """
                            (ID INT NOT NULL AUTO_INCREMENT,
                                feed_name varchar(50) NOT NULL,
                                feed_email VARCHAR(50) NOT NULL,
                                feed_score varchar(5) NOT NULL,
                                comments VARCHAR(100) NULL,
                                Timestamp VARCHAR(50) NOT NULL,
                                PRIMARY KEY (ID)
                            );
                        """
            cursor.execute(tablef_sql)
        except Exception:
            pass

    ###### CODE FOR CLIENT SIDE (USER) ######

    if choice == 'User':

        section_header("Tell Us About Yourself 👤")
        col1, col2, col3 = st.columns(3)
        with col1:
            act_name = st.text_input('Name*')
        with col2:
            act_mail = st.text_input('Mail*')
        with col3:
            act_mob = st.text_input('Mobile Number*')

        sec_token = secrets.token_urlsafe(12)
        try:
            host_name = socket.gethostname()
        except Exception:
            host_name = "unknown-host"
        try:
            ip_add = socket.gethostbyname(host_name)
        except Exception:
            ip_add = "0.0.0.0"
        try:
            dev_user = os.getlogin()
        except Exception:
            dev_user = os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
        os_name_ver = platform.system() + " " + platform.release()

        latlong = None
        city = state = country = ""
        if HAS_GEOCODER:
            try:
                g = geocoder.ip('me')
                latlong = g.latlng
                if HAS_GEOPY and latlong:
                    geolocator = Nominatim(user_agent="http")
                    location = geolocator.reverse(latlong, language='en')
                    address = location.raw['address']
                    city = address.get('city', '')
                    state = address.get('state', '')
                    country = address.get('country', '')
            except Exception:
                pass

        # Upload Resume
        section_header("Upload Your Resume", "And get smart, AI-powered recommendations")

        ## file upload in pdf format
        pdf_file = st.file_uploader("Choose your Resume (PDF)", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Launching your resume into orbit for analysis... 🚀'):
                time.sleep(2)

            ### saving the uploaded resume to folder
            os.makedirs('./Uploaded_Resumes/', exist_ok=True)
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            pdf_name = pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            with st.expander("📄 Preview your uploaded resume", expanded=False):
                show_pdf(save_image_path)

            ### parsing and extracting whole resume
            resume_data = None
            if HAS_RESUME_PARSER:
                try:
                    resume_data = ResumeParser(save_image_path).get_extracted_data()
                except Exception:
                    resume_data = None

            if not HAS_RESUME_PARSER:
                cosmic_error(
                    "The resume-parsing engine (pyresparser) isn't installed in this environment, "
                    "so we can't extract structured data right now. Install the dependencies from "
                    "requirements.txt to enable full analysis."
                )
            elif resume_data:

                ## Get the whole resume data into resume_text
                resume_text = pdf_reader(save_image_path)

                ## Showing Analyzed data from (resume_data)
                section_header("Resume Analysis 🛰️")
                cosmic_success("Hello " + str(resume_data.get('name', 'Explorer')) + "! Your resume has landed safely.")

                section_header("Your Basic Info 👀")
                info_chips([
                    ("Name", resume_data.get('name', 'N/A')),
                    ("Email", resume_data.get('email', 'N/A')),
                    ("Contact", resume_data.get('mobile_number', 'N/A')),
                    ("Degree", str(resume_data.get('degree', 'N/A'))),
                    ("Resume Pages", str(resume_data.get('no_of_pages', 'N/A'))),
                ])

                ## Predicting Candidate Experience Level

                ### Trying with different possibilities
                cand_level = ''
                no_of_pages = resume_data.get('no_of_pages', 0) or 0
                if no_of_pages < 1:
                    cand_level = "NA"
                    badge("🌱 Fresher Level")
                elif any(k in resume_text for k in ['INTERNSHIP', 'INTERNSHIPS', 'Internship', 'Internships']):
                    cand_level = "Intermediate"
                    badge("🛰️ Intermediate Level")
                elif any(k in resume_text for k in ['EXPERIENCE', 'WORK EXPERIENCE', 'Experience', 'Work Experience']):
                    cand_level = "Experienced"
                    badge("🪐 Experienced Level")
                else:
                    cand_level = "Fresher"
                    badge("🌱 Fresher Level")

                ## Skills Analyzing and Recommendation
                section_header("Skills Recommendation 💡")

                ### Current Analyzed Skills
                keywords = st_tags(label='Your Current Skills',
                                    text='See our skills recommendation below', value=resume_data.get('skills', []),
                                    key='1')

                ### Keywords for Recommendations
                ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit']
                web_keyword = ['react', 'django', 'node js', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                                'javascript', 'angular js', 'c#', 'asp.net', 'flask']
                android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
                ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
                uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes',
                                 'storyframes', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator',
                                 'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro',
                                 'premier pro', 'adobe indesign', 'indesign', 'wireframe', 'solid', 'grasp',
                                 'user research', 'user experience']
                n_any = ['english', 'communication', 'writing', 'microsoft office', 'leadership',
                         'customer management', 'social media']

                ### Skill Recommendations Starts
                recommended_skills = []
                reco_field = ''
                rec_course = ''

                ### condition starts to check skills from keywords and predict field
                for i in resume_data.get('skills', []):

                    #### Data science recommendation
                    if i.lower() in ds_keyword:
                        reco_field = 'Data Science'
                        cosmic_success("Our analysis says you are aiming for Data Science orbit. 🛰️")
                        recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling',
                                               'Data Mining', 'Clustering & Classification', 'Data Analytics',
                                               'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
                                               'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', 'Flask',
                                               'Streamlit']
                        st_tags(label='Recommended skills for you', text='Generated by our AI engine',
                                value=recommended_skills, key='2')
                        cosmic_tip("Adding these skills to your resume will boost 🚀 your chances of getting a job.")
                        rec_course = course_recommender(ds_course)
                        break

                    #### Web development recommendation
                    elif i.lower() in web_keyword:
                        reco_field = 'Web Development'
                        cosmic_success("Our analysis says you are aiming for Web Development orbit. 🛰️")
                        recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                               'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                        st_tags(label='Recommended skills for you', text='Generated by our AI engine',
                                value=recommended_skills, key='3')
                        cosmic_tip("Adding these skills to your resume will boost 🚀 your chances of getting a job.")
                        rec_course = course_recommender(web_course)
                        break

                    #### Android App Development
                    elif i.lower() in android_keyword:
                        reco_field = 'Android Development'
                        cosmic_success("Our analysis says you are aiming for Android Development orbit. 🛰️")
                        recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java',
                                               'Kivy', 'GIT', 'SDK', 'SQLite']
                        st_tags(label='Recommended skills for you', text='Generated by our AI engine',
                                value=recommended_skills, key='4')
                        cosmic_tip("Adding these skills to your resume will boost 🚀 your chances of getting a job.")
                        rec_course = course_recommender(android_course)
                        break

                    #### IOS App Development
                    elif i.lower() in ios_keyword:
                        reco_field = 'IOS Development'
                        cosmic_success("Our analysis says you are aiming for iOS Development orbit. 🛰️")
                        recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                               'Objective-C', 'SQLite', 'Plist', 'StoreKit', 'UI-Kit',
                                               'AV Foundation', 'Auto-Layout']
                        st_tags(label='Recommended skills for you', text='Generated by our AI engine',
                                value=recommended_skills, key='5')
                        cosmic_tip("Adding these skills to your resume will boost 🚀 your chances of getting a job.")
                        rec_course = course_recommender(ios_course)
                        break

                    #### Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        reco_field = 'UI-UX Development'
                        cosmic_success("Our analysis says you are aiming for UI/UX Development orbit. 🛰️")
                        recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                               'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop',
                                               'Editing', 'Illustrator', 'After Effects', 'Premier Pro', 'Indesign',
                                               'Wireframe', 'Solid', 'Grasp', 'User Research']
                        st_tags(label='Recommended skills for you', text='Generated by our AI engine',
                                value=recommended_skills, key='6')
                        cosmic_tip("Adding these skills to your resume will boost 🚀 your chances of getting a job.")
                        rec_course = course_recommender(uiux_course)
                        break

                    #### For Not Any Recommendations
                    elif i.lower() in n_any:
                        reco_field = 'NA'
                        cosmic_warning("Currently our tool only predicts and recommends for Data Science, Web, "
                                        "Android, iOS and UI/UX Development.")
                        recommended_skills = ['No Recommendations']
                        st_tags(label='Recommended skills for you', text='Currently no recommendations',
                                value=recommended_skills, key='6')
                        cosmic_info("Maybe available in future updates. 🌠")
                        rec_course = "Sorry! Not Available for this Field"
                        break

                ## Resume Scorer & Resume Writing Tips
                section_header("Resume Tips &amp; Ideas 🥂")
                resume_score = 0

                ### Predicting Whether these key points are added to the resume
                if 'Objective' in resume_text or 'Summary' in resume_text:
                    resume_score += 6
                    cosmic_success("[+] Awesome! You have added an Objective/Summary")
                else:
                    cosmic_tip("[-] Please add your career objective — it signals your career intent to recruiters.")

                if 'Education' in resume_text or 'School' in resume_text or 'College' in resume_text:
                    resume_score += 12
                    cosmic_success("[+] Awesome! You have added Education Details")
                else:
                    cosmic_tip("[-] Please add Education. It shows your qualification level to the recruiter.")

                if 'EXPERIENCE' in resume_text or 'Experience' in resume_text:
                    resume_score += 16
                    cosmic_success("[+] Awesome! You have added Experience")
                else:
                    cosmic_tip("[-] Please add Experience. It will help you stand out from the crowd.")

                if any(k in resume_text for k in ['INTERNSHIPS', 'INTERNSHIP', 'Internships', 'Internship']):
                    resume_score += 6
                    cosmic_success("[+] Awesome! You have added Internships")
                else:
                    cosmic_tip("[-] Please add Internships. It will help you stand out from the crowd.")

                if any(k in resume_text for k in ['SKILLS', 'SKILL', 'Skills', 'Skill']):
                    resume_score += 7
                    cosmic_success("[+] Awesome! You have added Skills")
                else:
                    cosmic_tip("[-] Please add Skills. It will help you a lot.")

                if 'HOBBIES' in resume_text or 'Hobbies' in resume_text:
                    resume_score += 4
                    cosmic_success("[+] Awesome! You have added your Hobbies")
                else:
                    cosmic_tip("[-] Please add Hobbies. It shows your personality to recruiters.")

                if 'INTERESTS' in resume_text or 'Interests' in resume_text:
                    resume_score += 5
                    cosmic_success("[+] Awesome! You have added your Interests")
                else:
                    cosmic_tip("[-] Please add Interests. It shows interests beyond the job.")

                if 'ACHIEVEMENTS' in resume_text or 'Achievements' in resume_text:
                    resume_score += 13
                    cosmic_success("[+] Awesome! You have added your Achievements")
                else:
                    cosmic_tip("[-] Please add Achievements. It shows you're capable for the role.")

                if any(k in resume_text for k in ['CERTIFICATIONS', 'Certifications', 'Certification']):
                    resume_score += 12
                    cosmic_success("[+] Awesome! You have added your Certifications")
                else:
                    cosmic_tip("[-] Please add Certifications. It shows specialization for the role.")

                if any(k in resume_text for k in ['PROJECTS', 'PROJECT', 'Projects', 'Project']):
                    resume_score += 19
                    cosmic_success("[+] Awesome! You have added your Projects")
                else:
                    cosmic_tip("[-] Please add Projects. It shows hands-on work related to the role.")

                section_header("Resume Score 📝")

                ### Score Bar
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(min(resume_score, 100)):
                    score += 1
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)

                ### Score
                score_orb(score)
                cosmic_warning("Note: this score is calculated based on the sections detected in your resume.")

                ### Getting Current Date and Time
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date + '_' + cur_time)

                ## Calling insert_data to add all the data into user_data
                insert_data(str(sec_token), str(ip_add), host_name, dev_user, os_name_ver, latlong, city, state,
                            country, act_name, act_mail, act_mob, resume_data.get('name', ''),
                            resume_data.get('email', ''), str(resume_score), timestamp,
                            str(resume_data.get('no_of_pages', '')), reco_field, cand_level,
                            str(resume_data.get('skills', [])), str(recommended_skills), str(rec_course), pdf_name)

                ## Recommending Resume Writing Video
                section_header("Bonus Video: Resume Writing Tips 💡")
                resume_vid = random.choice(resume_videos)
                st.video(resume_vid)

                ## Recommending Interview Preparation Video
                section_header("Bonus Video: Interview Tips 💡")
                interview_vid = random.choice(interview_videos)
                st.video(interview_vid)

                ## On Successful Result
                st.balloons()

            else:
                cosmic_error('Something went wrong while analyzing your resume. Please try another PDF.')

    ###### CODE FOR FEEDBACK SIDE ######
    elif choice == 'Feedback':

        # timestamp
        ts = time.time()
        cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(cur_date + '_' + cur_time)

        section_header("Send Us a Transmission 📡", "We'd love your feedback")

        # Feedback Form
        with st.form("my_form"):
            feed_name = st.text_input('Name')
            feed_email = st.text_input('Email')
            feed_score = st.slider('Rate Us From 1 - 5', 1, 5)
            comments = st.text_input('Comments')
            Timestamp = timestamp
            submitted = st.form_submit_button("Transmit Feedback 🚀")
            if submitted:
                ## Calling insertf_data to add dat into user feedback
                insertf_data(feed_name, feed_email, feed_score, comments, Timestamp)
                ## Success Message
                cosmic_success("Thanks! Your feedback has been received by mission control.")
                ## On Successful Submit
                st.balloons()

        if DB_AVAILABLE:
            try:
                # query to fetch data from user feedback table
                query = 'select * from user_feedback'
                plotfeed_data = pd.read_sql(query, connection)

                # fetching feed_score from the query and getting the unique values and total value count
                labels = plotfeed_data.feed_score.unique()
                values = plotfeed_data.feed_score.value_counts()

                # plotting pie chart for user ratings
                section_header("Past User Ratings ⭐")
                fig = px.pie(values=values, names=labels, title="Chart of User Rating Score From 1 - 5", hole=0.4)
                st.plotly_chart(style_fig(fig), use_container_width=True)

                #  Fetching Comment History
                cursor.execute('select feed_name, comments from user_feedback')
                plfeed_cmt_data = cursor.fetchall()

                section_header("User Comments 💬")
                dff = pd.DataFrame(plfeed_cmt_data, columns=['User', 'Comment'])
                st.dataframe(dff, width=1000)
            except Exception:
                cosmic_info("No feedback analytics available yet.")
        else:
            cosmic_info("Feedback analytics require a database connection, which isn't available in this preview.")

    ###### CODE FOR ABOUT PAGE ######
    elif choice == 'About':

        section_header("About This Tool 🌌", "AI Resume Analyzer — Galaxy Edition")

        st.markdown(
            """
            <div class="glass-card">
                A tool which parses information from a resume using natural language processing,
                clusters keywords into career sectors, and shows AI-powered recommendations,
                predictions and analytics to the applicant based on keyword matching.
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                """
                <div class="glass-card">
                    <b>🚀 User</b><br/><br/>
                    In the sidebar, choose <i>User</i>, fill in the required fields, and upload your resume
                    as a PDF. Sit back — the AI does the rest.
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """
                <div class="glass-card">
                    <b>📡 Feedback</b><br/><br/>
                    A place where you can transmit feedback and suggestions about the tool back to
                    mission control.
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                """
                <div class="glass-card">
                    <b>🔐 Admin</b><br/><br/>
                    Login with <code>admin</code> / <code>admin@resume-analyzer</code> to view all
                    analytics gathered across the galaxy.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="cosmic-footer" style="margin-top:1.6rem;">
                Built with 🤍 by
                <a href="https://dnoobnerd.netlify.app/">Deepak Padhi</a> through
                <a href="https://www.linkedin.com/in/mrbriit/">Dr Bright — (Data Scientist)</a>
                &nbsp;·&nbsp; Galaxy UI redesign ✨
            </div>
            """,
            unsafe_allow_html=True,
        )

    ###### CODE FOR ADMIN SIDE (ADMIN) ######
    else:
        section_header("Mission Control Access 🔐", "Admin sign-in required")

        col_a, col_b = st.columns(2)
        with col_a:
            ad_user = st.text_input("Username")
        with col_b:
            ad_password = st.text_input("Password", type='password')

        if st.button('Login 🚀'):

            ## Credentials
            if ad_user == 'admin' and ad_password == 'admin@resume-analyzer':

                if not DB_AVAILABLE:
                    cosmic_warning("Welcome, Admin! However no database connection is available in this "
                                    "preview environment, so live analytics can't be displayed.")
                else:
                    try:
                        ### Fetch miscellaneous data from user_data(table) and convert it into dataframe
                        cursor.execute(
                            '''SELECT ID, ip_add, resume_score, convert(Predicted_Field using utf8),
                               convert(User_level using utf8), city, state, country from user_data''')
                        datanalys = cursor.fetchall()
                        plot_data = pd.DataFrame(datanalys, columns=['Idt', 'IP_add', 'resume_score',
                                                                      'Predicted_Field', 'User_Level', 'City',
                                                                      'State', 'Country'])

                        ### Total Users Count with a Welcome Message
                        values = plot_data.Idt.count()
                        cosmic_success(f"Welcome back, Commander! {values} explorers have used our tool so far.")

                        ### Fetch user data from user_data(table) and convert it into dataframe
                        cursor.execute(
                            '''SELECT ID, sec_token, ip_add, act_name, act_mail, act_mob,
                               convert(Predicted_Field using utf8), Timestamp, Name, Email_ID, resume_score,
                               Page_no, pdf_name, convert(User_level using utf8), convert(Actual_skills using utf8),
                               convert(Recommended_skills using utf8), convert(Recommended_courses using utf8),
                               city, state, country, latlong, os_name_ver, host_name, dev_user from user_data''')
                        data = cursor.fetchall()

                        section_header("User's Data 📊")
                        df = pd.DataFrame(data, columns=[
                            'ID', 'Token', 'IP Address', 'Name', 'Mail', 'Mobile Number', 'Predicted Field',
                            'Timestamp', 'Predicted Name', 'Predicted Mail', 'Resume Score', 'Total Page',
                            'File Name', 'User Level', 'Actual Skills', 'Recommended Skills', 'Recommended Course',
                            'City', 'State', 'Country', 'Lat Long', 'Server OS', 'Server Name', 'Server User'])

                        st.dataframe(df)
                        st.markdown(get_csv_download_link(df, 'User_Data.csv', '⬇️ Download Report'),
                                    unsafe_allow_html=True)

                        ### Fetch feedback data from user_feedback(table)
                        cursor.execute('''SELECT * from user_feedback''')
                        data = cursor.fetchall()

                        section_header("User's Feedback Data 💬")
                        df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Feedback Score', 'Comments',
                                                          'Timestamp'])
                        st.dataframe(df)

                        query = 'select * from user_feedback'
                        plotfeed_data = pd.read_sql(query, connection)

                        ### Analyzing All the Data's in pie charts
                        section_header("Galaxy Analytics 🌌")

                        cA, cB = st.columns(2)
                        with cA:
                            labels = plotfeed_data.feed_score.unique()
                            values = plotfeed_data.feed_score.value_counts()
                            fig = px.pie(values=values, names=labels, title="User Rating Score (1-5)", hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                        with cB:
                            labels = plot_data.Predicted_Field.unique()
                            values = plot_data.Predicted_Field.value_counts()
                            fig = px.pie(values=values, names=labels, title='Predicted Field by Skills', hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                        cC, cD = st.columns(2)
                        with cC:
                            labels = plot_data.User_Level.unique()
                            values = plot_data.User_Level.value_counts()
                            fig = px.pie(values=values, names=labels, title="User Experience Level", hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                        with cD:
                            labels = plot_data.resume_score.unique()
                            values = plot_data.resume_score.value_counts()
                            fig = px.pie(values=values, names=labels, title='Resume Score Distribution', hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                        cE, cF = st.columns(2)
                        with cE:
                            labels = plot_data.IP_add.unique()
                            values = plot_data.IP_add.value_counts()
                            fig = px.pie(values=values, names=labels, title='Usage by IP Address', hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                        with cF:
                            labels = plot_data.City.unique()
                            values = plot_data.City.value_counts()
                            fig = px.pie(values=values, names=labels, title='Usage by City', hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                        cG, cH = st.columns(2)
                        with cG:
                            labels = plot_data.State.unique()
                            values = plot_data.State.value_counts()
                            fig = px.pie(values=values, names=labels, title='Usage by State', hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                        with cH:
                            labels = plot_data.Country.unique()
                            values = plot_data.Country.value_counts()
                            fig = px.pie(values=values, names=labels, title='Usage by Country', hole=0.4)
                            st.plotly_chart(style_fig(fig), use_container_width=True)

                    except Exception as e:
                        cosmic_error(f"Couldn't load analytics: {e}")

            ## For Wrong Credentials
            else:
                cosmic_error("Wrong ID & Password provided. Access denied by mission control.")

    footer()


# Calling the main (run()) function to make the whole process run
run()

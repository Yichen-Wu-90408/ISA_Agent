### [ Practice Module ] ISA-PM-IPA-2021-09-01-ISY5005-GRP-AgentSG-Multi_Agent_System

---

### <<<<<<<<<<<<<<<<<<<< Start of Project >>>>>>>>>>>>>>>>>>>>

---

## SECTION 1 : Movie Recommendation System
<img src="P1.png"
     style="float: left; margin-right: 0px;" />


---

## SECTION 2 : EXECUTIVE SUMMARY 
This robot is mainly to obtain the fundraising data of each blockchain project on the Icodrops website through the crawler, and then integrate the useful data through data analysis, process and extract the key information that is helpful for investment, thereby greatly saving researchers’ time in the digital currency industry, who used to spend a lot of time writing reports every day to assist in investment decisions.


---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| Ni Yongxin(leader) | A0231559B | crawler agent | e0703591@u.nus.edu |
| Peng Junhao | A0231329L | PDF agent | e0703361@u.nus.edu |
| Wu Yichen | A0231544M | excel agent | e0703576@u.nus.edu |
| Zeng Zijing | A0231548E | email agent | zengzijing1@163.com |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO
<img src="P2.png"
     style="float: left; margin-right: 0px;" />

`Refer to project report at Github Folder: video` 


---

## SECTION 5 : USER GUIDE

### [ 1 ] Install project dependencies:

> **In order to ensure the stable operation of the system, the following dependencies are all used stable versions.**
>
> **(1) Python 3.6+**
>
> **Library requirements: smtplib, email, matplotlib.
>
> **Environment requirement: install texlive locally and add the environment variables to the path
> 
> **Receive emails: the receivers are set in row 32 of “email_agent.py”, you can change the value to your own email, e.g., recipientAddrs = ‘email1;email2;email3’.
> 
### [ 2 ] To run our multi agent system:
> **(1) Run “Git clone https://github.com/Yichen-Wu-90408/ISA_Agent.git” to download the project and unzip it, then change the directory to the root of our project folder.
> 
> **(2) Run the command “python crwaler_agent.py” to start the crawler and upload the data to the database (it will link to our established database). 
Library requirements: selenium, bs4, pymysql, requests, lxml, cfscrape.
You can set it to run regularly, e.g., once an hour.
>
> **(3) Run the command “python email.agent.py”. It will start the “pdf_agent.py” to generate an industry report based on the crawler data and the latex template, then the “email_agent.py” would send the pdf file to users through email.
> 


## SECTION 6 : PROJECT REPORT 

`Refer to project report at Github Folder: ProjectReport`

**Recommended Sections for Project Report:**

- Background
- Research on Existing Recommender System
- Analysis of Problems in China’s Movie Recommendation System
- Commercial Value of the Project
- System Design
- Operating Environment
- User Guide



---

### <<<<<<<<<<<<<<<<<<<< End of Project >>>>>>>>>>>>>>>>>>>>

---


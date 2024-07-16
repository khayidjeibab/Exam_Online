from flask import Flask, request, jsonify, render_template, redirect, url_for
import random
import requests
import configparser
import time

app = Flask(__name__)

# Ajouter enumerate à l'environnement Jinja2
app.jinja_env.globals.update(enumerate=enumerate)



# Questions et réponses fournies
questions_true_false = [
    ("DRIS stands for Driver Road Infrastructure Service.", False),
    ("It is not necessary in an ICT-based production system of smart manufacturing to include intelligent sensing technologies.", False),
    ("In 5IABCDE, E stands for Encryption.", False),
    ("5IABCDE includes five emerging technologies.", False),
    ("Blockchain is included in 5IABCDE.", True),
    ("AIoT stands for Advanced Internet of Things.", False),
    ("The Trojan room coffee pot of the computer laboratory in Cambridge University is an example of an IoT solution.", False),
    ("ITU referred to the IoT concept at the world summit on the information society in 2005.", True),
    ("NB-IoT is developed for 5G technologies.", False),
    ("The first 3GPP standard for the 5G is Release-16.", True),
    ("VR glasses, body fat scales, smart locks, and smart speakers are examples of industry-related IoT products.", False),
    ("Smart agriculture is an example of industry-related IoT products.", True),
    ("IoT is an Internet where all things are interconnected.", True),
    ("IoT requires moving from the internet of things to the internet of people.", False),
    ("IoT model includes 4 layers.", True),
    ("In the IoT model, the platform layer collects Information and process signals.", False),
    ("Huawei IoT solution architecture is 1+2+1.", True),
    ("Huawei cloud IoT platform is open, pre-integrated and access-dependent.", False),
    ("Bluetooth is an example of communication protocols used by IoT applications.", False),
    ("Fully open smart ONT requires a bit rate up to 1 Gbit/s.", True),
    ("In the IoT model, device management and security maintenance are performed by the platform.", True),
    ("Huawei IoT Solution Architecture is 1+2+1 means: one IoT access method, two platforms, and one IoT operating system.", False),
    ("Huawei LiteOS features low power consumption, small size, and quick response.", True),
    ("NB-IoT stands for NearBand Internet of Things.", False),
    ("Huawei LiteOS features basic kernel size less than 20 kB.", False),
    ("5G Architecture supports both NFV and SDN.", True),
    ("Traffic management is a common problem in modern cities.", True),
    ("Environmental sanitation is not included in the city management scenario.", False),
    ("Device management in the smart city solution includes: 2G/3G/4G, fixed and NB-IoT accesses.", True),
    ("Smart streetlamp services do not include charging piles.", False),
    ("Smart manhole cover solution can provide real-time monitoring.", True),
    ("Security management is a common problem in campus management.", True),

]

questions_single_choice = [
    ("Which of the following is considered the oldest known mention of IoT:",
     ["Bill Gates Book (the road ahead)", "ITU internet reports.", "Trojan room coffee pot", "Hannover messe"], "Trojan room coffee pot"),
    ("In which release of the 3GPP the NB-IoT standard was frozen?",
     ["13", "14", "15", "16"], "13"),
    ("Which of the following Chinese mobile operator(s) was(were) the first 5G network(s) commercially used?",
     ["China Telecom", "China Mobile", "China Unicom", "All of them"], "All of them"),
    ("In which quarter of 2019 the 5G networks were employed in China for public commercial use?",
     ["First", "Second", "Third", "Fourth"], "Fourth"),
    ("Development of IoT industry is driven by:",
     ["Consumers", "Policies", "Industry", "All of them"], "All of them"),
    ("One of the following is not a policy-driven application of the IoT industry:",
     ["Firefighting", "Smart agriculture", "Parking", "Streetlighting"], "Smart agriculture"),
    ("One of the following is consumption-driven application of the IoT industry:",
     ["Smart speaker", "Public utilities", "Security system integration", "Internet of Vehicles"], "Smart speaker"),
    ("Which of the following is industry-driven application of the IoT industry?",
     ["Smart agriculture", "Smart logistics", "IoV", "All of them"], "All of them"),
    ("From 1999 to 2013, the term “connected objects” was used to describe:",
     ["Smart wearable devices", "Smart home utilities", "Things in the radio frequency domain", "Industrial devices and applications"], "Things in the radio frequency domain"),
    ("How many layers are there in the IoT model?",
     ["2", "3", "4", "5"], "4"),
    ("Which of the following layer of the IoT model provide data presentation and customer interaction services?",
     ["Application layer", "Platform layer", "Network layer", "Device layer"], "Application layer"),
    ("One of the following is not a component of the platform layer in the IoT model:",
     ["Cloud data center", "Operations platform", "IoT gateways", "Security maintenance"], "IoT gateways"),
    ("Which of the following is a network layer technology in the IoT model?",
     ["GPRS", "NB-IoT", "4G", "All of them"], "All of them"),
    ("One of the following is not an example of an IoT application:",
     ["Smart home", "Huawei LiteOS", "Safe city", "IoV"], "Huawei LiteOS"),
    ("Which of the following solutions for the IoT model architecture are proposed by Huawei?",
     ["1+2+1", "2+1+1", "2+1+2", "1+1+2"], "1+2+1"),
    ("The adapted Huawei IoT architecture includes:",
     ["Two IoT platforms, two access methods and one IoT operating system", "One IoT platform, two access methods and one IoT operating system", "One IoT platform, two access methods and two IoT operating systems", "None of them"], "One IoT platform, two access methods and one IoT operating system"),
    ("One of the following is not an example of protocols used in the NB-IoT end-to-end solution:",
     ["HTTP", "MQTT", "ICMP", "CoAP"], "ICMP"),
    ("One of the following is not an example of devices used in the NB-IoT end-to-end solution:",
     ["MCUs", "Modules", "NB-IoT chipsets", "HTTP"], "HTTP"),
    ("Which of the following connectivity is required in a smart home using ONT technology?",
     ["1 Mbit/s", "1 Gbit/s", "1 Tbit/s", "None of them"], "1 Gbit/s"),
    ("Huawei cloud IoT platform is:",
     ["Open", "Pre-integrated", "Service-oriented", "All of them"], "All of them"),
    ("One of the following is not a common problem in modern cities:",
     ["Visitor management", "Parking management", "Street lamp management", "Manhole cover management"], "Visitor management"),
    ("Smart city solution includes:",
     ["2G/3G/4G and fixed access", "NB-IoT access", "None of them", "Both of them"], "Both of them"),
    ("One of the following is not in the application layer for smart firefighter solution:",
     ["Alarm handling", "Remote muting", "Traffic broadcast", "Device self-check"], "Traffic broadcast"),

]

questions_multiple_choice = [
    ("Which of the followings are considered as IoT application classes?",
     ["Policy-driven", "Agriculture-driven", "Industry-driven", "Application-driven"], ["Policy-driven", "Industry-driven"]),
    ("Which of the followings are included in the Huawei IoT solution architecture?",
     ["IoT platform", "IoT access", "OS", "Cloud"], ["IoT platform", "IoT access", "OS"]),
    ("Which of the followings are Huawei LiteOS features?",
     ["Open source", "Quick response", "Low power consumption", "Highly secure"], ["Open source", "Quick response", "Low power consumption"]),
    ("Which of the followings are protocols used in the NB-IoT end-to-end solution?",
     ["HTTP", "CoAP", "MQTT", "LwM2M"], ["HTTP", "CoAP", "MQTT", "LwM2M"]),
    ("Which of the followings are technologies included in the 5IABCDE smart manufacturing?",
     ["AI", "Big Data", "Edge computing", "Blockchain"], ["AI", "Big Data", "Edge computing", "Blockchain"]),
]

# Define exam duration (30 minutes)
exam_duration = 30 * 60  # in seconds

@app.route('/')
def debut():
    return render_template('debut.html')

@app.route('/index')
def index():
    return render_template('index.html', questions_true_false=questions_true_false,
                           questions_single_choice=questions_single_choice,
                           questions_multiple_choice=questions_multiple_choice)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    score = 0
    total_questions = len(questions_true_false) + len(questions_single_choice) + len(questions_multiple_choice)

    # Check True/False answers
    for i, question in enumerate(questions_true_false):
        user_answer = data.get(f"true-false-{i+1}")
        correct_answer = question[1]
        if user_answer and user_answer.lower() == str(correct_answer).lower():
            score += 1

    # Check Single Choice answers
    for i, question in enumerate(questions_single_choice):
        user_answer = data.get(f"single-choice-{len(questions_true_false) + i + 1}")
        correct_answer = question[2]
        if user_answer and user_answer == correct_answer:
            score += 1

    # Check Multiple Choice answers
    for i, question in enumerate(questions_multiple_choice):
        user_answers = data.getlist(f"multiple-choice-{len(questions_true_false) + len(questions_single_choice) + i + 1}")
        correct_answers = question[2]
        if set(user_answers) == set(correct_answers):
            score += 1

    # Redirect to result page with score and total questions
    return redirect(url_for('result', score=score, total=total_questions))

@app.route('/result')
def result():
    score = request.args.get('score', type=int)
    total = request.args.get('total', type=int)
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
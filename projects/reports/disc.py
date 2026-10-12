# DISC Personality Assessment sample report, Elevatus edition.
# Same content and the same elements as the source report: nothing added, only restyled. The cover is the Elevatus cover template.
import sys, math, os
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUTPUT, 'Elevatus - DISC Personality Assessment Sample Report.pdf')
R = Report('Omar Al-Khatib', 'Sep 11 2026', 'DISC - Personality Assessment test', '2026', 'Elevatus - DISC Personality Assessment Sample Report')

# one tonal step of the Vivid Blue scale per type: (fill, text on fill)
TYPES = {'D': ('Decisiveness', C['logo'], C['white']), 'I': ('Impact', C['vivid'], C['white']),
         'S': ('Support', C['s400'], C['s900']), 'C': ('Certainty', C['s200'], C['s900'])}
SCORES = {'D': 79, 'I': 79, 'S': 78, 'C': 76}
BODY = dict(size=9.3, lead=14.4, color=C['slate'])

# ================================================================ first page: the DISC circle and the table of contents
p = R.p
cx, rad, g = W / 2, 150, 3.5
cy = R.y + 8 + rad
quad = {'D': (180, 270, -1, -1), 'I': (270, 360, 1, -1), 'S': (90, 180, -1, 1), 'C': (0, 90, 1, 1)}
for k, (a0, a1, sx, sy) in quad.items():
    name, fill, ink = TYPES[k]
    c = (cx + sx * g, cy + sy * g)
    pts = [c] + [(c[0] + rad * math.cos(math.radians(a)), c[1] + rad * math.sin(math.radians(a))) for a in range(a0, a1 + 1, 2)]
    poly(p, pts, fill=fill)
    text(p, c[0] + sx * rad * 0.42, c[1] + sy * rad * 0.40 + 5, name, 'S', 14, ink, 'center')
circle(p, (cx, cy), 20, fill=C['white'])
R.y = cy + rad + 34
R.h2('Table of contents', size=13)
R.space(4)
for head, subs in [('Introduction to DISC personality type: online report', ['How to read and use this report']),
                   ('Section 1: Understanding DISC, in general,', ['Behavioral type overview', 'Importance of each type']),
                   ('Section 2: Understanding your DISC type', ['Your type of overview', 'Your behavioral pattern according to the type', 'Your motivating factors',
                                                               'Potential areas of improvement', 'A list of Job families that suit your type', 'Summary of your type'])]:
    R.h3(head, size=10.2, f='M')
    R.bullets(subs, size=9, lead=13.6, color=C['slate'], gap=3, after=10)

# ================================================================ introduction
R.new_page()
R.h1('Introduction')
for s in ["Welcome to DISC Personality Assessment - a powerful tool that provides both recruiters and candidates with valuable insights into behavioral preferences and individual patterns. Whether you're a recruiter seeking to make informed hiring decisions or a candidate looking to understand yourself better, this report offers valuable information to aid your journey.",
          "The DISC model is a simple and universally applicable framework that focuses on observable behaviors, categorizing them into four styles: Drive, Influence, Support, and Clarity. This assessment will help you recognize your dominant style and gain a deeper understanding of your strengths and potential areas for growth.",
          "The team conducted a thorough research journey to develop a robust and reliable DISC assessment. We explored a range of reputable sources, academic literature, and assessment portals to comprehensively understand the DISC model, its historical context, and its application in contemporary assessments. The research process involved reviewing relevant research articles, publications, and assessment materials from respected publishers in the field.",
          "Throughout our research, we focused on understanding the origins of the DISC model, its evolution over time, and the different approaches and terminologies used by various publishers. One key figure in developing the DISC model was William Moulton Marston, an American psychologist known as the father of DISC. We studied Marston's original model and the subsequent work of Walter Clarke, who created the first DISC assessment in 1956.",
          "Drawing from various research sources and expert knowledge, we have developed a comprehensive understanding of the DISC model and its practical application in assessments."]:
    R.para(s, after=4, size=8.8, lead=12.9, color=C['slate'])
R.space(4)
R.h1('How to read this report', size=15)
P2 = dict(after=4, size=8.8, lead=12.9, color=C['slate'])
R.para("This report is divided into two parts, each providing unique insights to cater to both recruiters and candidates:", **P2)
R.space(2)
R.h3('Part I: Understanding the DISC Styles', color=C['logo'])
R.para("This section introduces each of the four DISC styles, providing an overview of their behavioral tendencies. Recruiters can leverage this information to assess candidates' potential fit within specific roles and team dynamics. At the same time, candidates can gain valuable self-awareness and an understanding of their natural behavioral inclinations.", **P2)
R.space(2)
R.h3('Part II: Understanding Yourself', color=C['logo'])
for s in ["Part II is all about you! We delve into your unique DISC style, revealing how it influences your communication style, decision-making, and approach to tasks. This section empowers recruiters and candidates to understand individual behavioral traits better.",
          "As you explore this personalized report, you'll discover the power of self-awareness and gain valuable insights into your behavioral preferences. For recruiters, this report facilitates more informed hiring decisions, leading to the formation of cohesive and high-performing teams. Candidates can harness this knowledge to make career choices aligned with their natural strengths.",
          "**Please Note:** The behavioral descriptions mentioned in this report are tendencies for each style group and may or may not specifically apply to individuals personally. As a tool for self-awareness and decision-making, this assessment offers valuable insights that can be applied in various aspects of personal and professional life.",
          "Now, let's embark on this journey together as we explore the two parts of the report to understand behavioral patterns better and unleash each individual's potential. With DISC Personality Assessment, you'll gain the knowledge to make purposeful choices and foster meaningful connections in your personal and professional spheres"]:
    R.para(s, **P2)

# ================================================================ section 1
def type_cards(data, size=8.9, lead=13.2, rich_items=False):
    """2 x 2 grid of type cards; data = {key: [items]}."""
    gap = 12; cw = (CW - gap) / 2; pad = 12
    for row in (('D', 'I'), ('S', 'C')):
        h = max(bullets_h(data[k], size, lead, cw - 2 * pad, gap=4) for k in row) + 2 * pad + 32
        R.ensure(h)
        for i, k in enumerate(row):
            x = MX + i * (cw + gap); name, fill, ink = TYPES[k]
            rrect(R.p, (x, R.y, x + cw, R.y + h), 10, fill=C['white'], color=C['line'], width=1)
            rrect(R.p, (x + 6, R.y + 6, x + cw - 6, R.y + 30), 6, fill=fill)
            text(R.p, x + cw / 2, R.y + 22, f'{name} ({k})', 'S', 10.5, ink, 'center')
            bullets(R.p, x + pad, R.y + 40, data[k], size, lead, cw - 2 * pad, C['slate'], dot=C['vivid'], gap=4, bold_color=C['ink'])
        R.y += h + gap
    R.y -= gap

R.new_page()
R.h1('Section 1: Understanding DISC in General')
R.h3('Behavioral Type Overview:', color=C['logo'])
R.para("The DISC Personality Assessment Test is a tool that reveals behavioral tendencies and communication styles. It categorizes personalities into four types: Decisiveness, Impact, Support, and Certainty.", **BODY)
R.space(2)
R.h3('Behavioral Types:', color=C['logo'])
R.space(2)
type_cards({'D': ['Assertive, goal-oriented', 'Leaders, risk-takers.', 'Direct communication, results-focused.', 'Impatient may need to pay more attention to details.'],
            'I': ['Outgoing, persuasive.', 'Social, relationship builders.', 'Effective communicators are motivators.', 'Easily distracted, seeks recognition.'],
            'S': ['Cooperative, empathetic.', 'Team players, listeners.', 'Values harmony reliable.', 'They avoid confrontation and may not assert themselves.'],
            'C': ['Cooperative, empathetic.', 'Team players, listeners.', 'Values harmony reliable.', 'They avoid confrontation and may not assert themselves.']})
R.space(14)
R.para("In summary, DISC's four personality types provide insights into behavior. People are a mix of these types, influencing their interactions and teamwork. Recognizing these types enhances communication and collaboration.", **BODY)

R.new_page()
R.h1('Importance of Each Type:')
R.h3('Recognizing the Value of Each DISC Type:', color=C['logo'])
R.para("Each of the four DISC personality types brings unique strengths and attributes to team dynamics, communication styles, and work environments. Understanding the significance of each class is crucial for fostering effective collaboration and maximizing individual and collective potential.", **BODY)
R.space(4)
type_cards({'D': ["**Leadership and Drive**: Individuals with a Decisiveness type are natural leaders who drive projects forward with determination and assertiveness.",
                  "**Initiative**: They lead in challenging situations and readily make decisions, enhancing team progress.",
                  "**Results-Oriented**: Their focus on outcomes boosts productivity and efficiency within the team.",
                  "**Action**: They infuse a sense of urgency into tasks, motivating the team to achieve goals"],
            'I': ["**Communication**: Impact-oriented individuals excel in connecting with others and conveying ideas persuasively.",
                  "**Relationship Building**: They create positive and engaging environments, fostering strong team cohesion.",
                  "**Motivation**: Their enthusiasm and energy uplift team morale and inspire colleagues to perform their best.",
                  "**Adaptability**: They inject creativity and flexibility into the team, making it adaptable to various situations."],
            'S': ["**Collaboration**: Support-focused individuals are excellent team players who value cooperation and harmony.",
                  "**Empathy**: Their understanding and empathy enhance communication, resolving conflicts smoothly.",
                  "**Reliability**: They provide stability to the team, consistently delivering and fulfilling commitments",
                  "**Listener**: Their active listening skills promote effective communication and understanding among team members."],
            'C': ["**Detail-Oriented**: Certainty types ensure accuracy and precision in tasks, minimizing errors.",
                  "**Organization**: They bring structure to the team, aiding in efficient planning and execution.",
                  "**Problem Solving**: Their analytical approach helps identify and resolve",
                  "**Quality**: Their pursuit of excellence elevates the overall quality of work produced by the team."]})

# ================================================================ summary: legend + pie, as in the source
R.new_page()
R.h1('Disc - Personality Summary')
p = R.p
lx = MX + 6
for k in 'DISC':
    name, fill, ink = TYPES[k]
    rrect(p, (lx, R.y + 4, lx + 22, R.y + 13), 2, fill=fill)
    lab = f'{name}: {SCORES[k]}%'
    text(p, lx + 29, R.y + 12.4, lab, 'R', 10, C['ink'])
    lx += 29 + tw(lab, 'R', 10) + 22
R.y += 34
pr = 205; pc = (W / 2, R.y + pr)
tot = sum(SCORES.values()); a = 0
for k in 'DISC':
    sweep = 360 * SCORES[k] / tot
    ring_segment(p, pc, 0, pr, a, a + sweep, TYPES[k][1])
    a += sweep
a = 0
for k in 'DISC':  # thin white separators between the slices
    t = math.radians(a - 90)
    line(p, pc, (pc[0] + pr * math.cos(t), pc[1] + pr * math.sin(t)), C['white'], 2.2)
    a += 360 * SCORES[k] / tot
R.y = pc[1] + pr + 20

# ================================================================ type pages
def type_page(n, k, intro, sliders, cards, interps, first=False):
    R.new_page()
    p = R.p
    if first: R.h2('Personality type and Attributes', size=13); R.space(4)
    name, fill, ink = TYPES[k]
    y = R.y + 4
    head = f'{n}. {name}'
    text(p, MX, y + 18, head, 'S', 16, C['logo'])
    text(p, MX + tw(head + ' ', 'S', 16), y + 18, f'{SCORES[k]}%', 'S', 16, C['vivid'])
    R.y = y + 36
    R.para(intro, **BODY)
    # sliders
    R.space(6)
    tx0, tx1 = MX + 150, W - MX
    for lab, al, x in (('LOW', 'left', tx0), ('MEDIUM', 'center', (tx0 + tx1) / 2), ('HIGH', 'right', tx1)):
        text(p, x, R.y + 6, lab, 'M', 6.5, C['slate'], al)
    R.y += 18
    for lab, v in sliders:
        text(p, MX, R.y + 6.5, lab, 'R', 9.3, C['ink'])
        rrect(p, (tx0, R.y + 1.5, tx1, R.y + 5.5), 2, fill=C['s100'])
        xe = tx0 + (tx1 - tx0) * v
        rrect(p, (tx0, R.y + 1.5, xe, R.y + 5.5), 2, fill=C['vivid'])
        circle(p, (xe, R.y + 3.5), 4.6, fill=C['apricot'], color=C['white'], width=1.4)
        R.y += 20
    R.space(8)
    # three cards
    gap = 12; cw = (CW - 2 * gap) / 3; pad = 12; sz, ld = 8.5, 12.3
    heads = ['Motivating Factors', 'Potential areas of improvements', 'Job families that suit according to the level achieved by the personality type']
    hh = max(rich_h(t, 8.8, 12, cw - 2 * pad, f='S') for t in heads)
    h = hh + 8 + max(bullets_h(c, sz, ld, cw - 2 * pad, gap=5, indent=10) for c in cards) + 2 * pad
    for i, (t, items) in enumerate(zip(heads, cards)):
        x = MX + i * (cw + gap)
        rrect(p, (x, R.y, x + cw, R.y + h), 10, fill=C['paper'])
        rich(p, x + pad, R.y + pad, t, 8.8, 12, cw - 2 * pad, C['logo'], f='S')
        bullets(p, x + pad, R.y + pad + hh + 8, items, sz, ld, cw - 2 * pad, C['slate'], gap=5, indent=10)
    R.y += h + 16
    for t, s in interps:
        R.h3(f'Interpretation of {t}', color=C['logo'])
        R.para(s, **BODY)
        R.space(2)

type_page(1, 'D', "Congratulations! Your high Drive score indicates you're assertive, determined, and results-oriented. You exude confidence and take charge of situations. You're a natural leader who takes control of situations. You're committed and focused on outcomes. Embrace your drive and lead with confidence!",
          [('Assertiveness', 0.794), ('Determination', 0.843), ('Results-oriented', 0.696)],
          [['Seeking opportunities for leadership and decision-making roles.', 'Pursuing challenging tasks and goals to achieve tangible outcomes.', 'Thriving in competitive environments and achieving recognition for accomplishments.'],
           ["Balancing assertiveness with active listening and openness to others' perspectives.", "Be mindful of solid determination's impact on collaboration and team dynamics.", 'Learning to delegate and share responsibilities to avoid feeling overwhelmed.'],
           ['Leadership roles such as Managers, Directors, and Executives.', 'Sales and Marketing positions that require assertiveness and goal-oriented approaches.', 'Project Management roles where determination and results-driven mindset are essential.']],
          [('Assertiveness', 'You are assertive and confident in expressing your opinions and making decisions. Your strong sense of self-assuredness allows you to take charge and lead effectively.'),
           ('Determination', 'Your determination and resilience enable you to overcome challenges, and stay focused on achieving your goals. You are persistent and unwavering in your pursuit of success.'),
           ('Results-oriented', 'You maintain a balance between process, and results. While you aim for achievements, you also value the journey and collaborative efforts.')], first=True)

type_page(2, 'I', "Well done! Your high Influence score reflects your outgoing, social, and persuasive nature. You excel in connecting with others and thrive in social settings. Your charisma and persuasion skills make you an effective influencer, inspiring others to follow your lead. Embrace your ability to engage and inspire, and use your influence to impact those around you positively.",
          [('Social', 0.746), ('Outgoing', 0.794), ('Persuasiveness', 0.794)],
          [['Relishing opportunities for social interactions and networking.', 'Being motivated by positive feedback and appreciation from others.', 'Enjoying roles that involve public speaking, presenting, or leading group activities.'],
           ['Balancing social interactions with moments of introspection for personal well-being.', "Being mindful of the impact of persuasive abilities on others' decision-making.", 'Recognizing when to step back and allow others to take the lead in social situations.'],
           ['Public Relations and Media roles that involve social engagement and persuasion.', 'Sales and Customer Success positions where building rapport is crucial.', 'Leadership roles in Marketing or Event Management.']],
          [('Social', 'You thrive in social interactions and enjoy connecting with others. Your outgoing nature makes you approachable and empathetic, building strong relationships effortlessly.'),
           ('Outgoing', 'Your outgoing nature allows you to take the initiative and engage confidently in social situations. You radiate positive energy and enthusiasm, making you a natural people-person.'),
           ('Persuasiveness', "You have the ability to influence other people's thoughts and opinions using convincing arguments and facts. Your words have a powerful impact, inspiring others to follow your lead.")])

type_page(3, 'S', "Bravo! Your high Support score showcases your cooperative, patient, and team-oriented nature. You excel in collaborating with others and prioritize the success of the team. Your patience and level-headedness contribute to a supportive and harmonious team environment. Embrace your team-oriented mindset and use your support to foster collaboration and a positive team spirit.",
          [('Cooperativeness', 0.794), ('Patience', 0.647), ('Team-oriented', 0.843)],
          [["Finding purpose in being a reliable team player and contributing to the team's success.", 'Being motivated by collaborative and cooperative work environments.', 'Valuing harmony and open communication within the team.'],
           ['Balancing supportiveness with assertiveness in expressing individual needs and ideas.', "Be mindful of patience's impact on decision-making and task completion timelines.", 'Recognizing when assertiveness is necessary to address conflicts constructively.'],
           ['Team-based roles in Healthcare or Nursing.', 'Customer Service or Call Center positions where patience and empathy are essential.', 'Supportive roles in Community Services or Social Work.']],
          [('Cooperativeness', 'You excel in collaborating and working harmoniously with others. Your cooperative nature fosters a strong sense of teamwork, making you an invaluable asset to any group.'),
           ('Patience', 'You demonstrate patience but are also capable of addressing urgent matters promptly.'),
           ('Team-oriented', "You prioritize the success of the team and work diligently to ensure everyone's contributions are valued. Your dedication to teamwork fosters a collaborative and supportive environment.")])

type_page(4, 'C', "Fantastic! Your high Clarity score reflects your analytical, detail-oriented, and systematic approach. You pay attention to detail, analyze situations thoroughly, and ensure precision in your work. Your methodical thinking provides efficient decision-making and organization. Embrace your analytical mindset, use your clarity to make well-informed decisions, and create structured and organized approaches to your tasks and goals.",
          [('Analytical', 0.696), ('Detail-oriented', 0.746), ('Systematic', 0.794)],
          [['Thriving in organized and structured environments.', 'Being motivated by accuracy, precision, and attention to detail.', 'Finding fulfillment in analytical and problem-solving tasks.'],
           ['Balancing attention to detail efficiently to avoid getting lost in minutiae.', 'Being open to creative and intuitive approaches in addition to systematic thinking.', 'Recognizing when adaptability is necessary to respond to dynamic situations.'],
           ['Analytical roles in Finance or Data Science.', 'Engineering or Computer Programming positions where precision is crucial.', 'Quality Control and Compliance roles that require attention to detail.']],
          [('Analytical', 'You balance analytical thinking with intuition, considering both detailed analysis and broader perspectives.'),
           ('Detail-oriented', 'Your attention to detail ensures accuracy and precision in your work. You excel in tasks that require meticulousness and thoroughness.'),
           ('Systematic', 'Your systematic approach allows you to organize and structure processes effectively. Your methodical nature ensures efficiency and clarity in your work.')])

# ================================================================ disclaimer
R.new_page()
R.h1('Disclaimer and Further Information:')
for t, paras in [('Understanding the DISC Personality Assessment', ["The DISC Personality Assessment is a valuable tool for gaining insights into behavioral patterns and preferences. However, it's important to note that the assessment does not provide an absolute measure of personality or abilities. Instead, it offers a nuanced perspective on your behavioral tendencies based on your responses."]),
                 ('Navigating the Information in this Report', ["The information presented in this report reflects your unique responses during the assessment. It's intended to assist you in your personal development journey and enhance your self-awareness. This report should not be considered an all-encompassing representation of your entire personality or skill set."]),
                 ('Harnessing the Power of Self-Development', ["Embracing your DISC assessment results can empower you to make informed decisions about your interactions, communication style, and personal growth. By recognizing your behavioral inclinations, you can work towards refining your strengths and addressing areas that might benefit from further development."]),
                 ('Seeking Further Guidance', ["For a more comprehensive understanding of your DISC type and how to effectively utilize the insights from this report, we encourage you to reach out to our dedicated assessment team. They are available to provide additional information, answer your questions, and guide you in leveraging your assessment outcomes to your advantage.",
                                               "Remember, the DISC Personality Assessment is a valuable resource on your journey towards self-improvement, and our team is here to support you every step of the way."])]:
    R.h3(t, color=C['logo'], size=11)
    for s in paras: R.para(s, **BODY)
    R.space(6)

R.cover('DISC Personality Assessment', 'A clear view of behavioral style across four dimensions: Decisiveness, Impact, Support and Certainty.',
        'Behavioral\nAssessment', 'Sample Report')
print(R.save(OUT), 'pages ->', OUT)

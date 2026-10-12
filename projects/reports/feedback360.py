# 360 Feedback sample report (source: Central Test), Elevatus edition.
# Same content and the same elements as the source report: nothing added, only restyled. The cover is the Elevatus cover template.
# Tables come from feedback360_data.json (parsed from the source PDF, so no retyping errors).
import sys, math, os, json
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUTPUT, 'Elevatus - 360 Feedback Sample Report.pdf')
NAME = 'Nour Haddad'
R = Report(NAME, 'May 13 2026', '360 Feedback', '2026', 'Elevatus - 360 Feedback Sample Report')
DATA = json.load(open(os.path.join(HERE, 'feedback360_data.json')))

# rating levels, low to high: (label, fill, text colour on that fill)
DEEP = rgb('C96A1B')
LEVELS = [('not observed', C['mist'], C['ink']), ('very unsatisfactory', DEEP, C['white']), ('slightly unsatisfactory', C['apricot'], C['ink']),
          ('average', C['s200'], C['s900']), ('good', C['s400'], C['white']), ('excellent', C['vivid'], C['white'])]
LEVEL_OF = {'-': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
SERIES = [('manager', C['logo']), ('coworker', C['s400']), ('self', C['apricot'])]
BODY = dict(size=9.2, lead=14)
SCALE = ["– = Not observed (reviewer hasn’t observed them exhibit this behaviour)",
         "1 = very unsatisfactory (the reviewer believes there needs to be significant improvement in this area)",
         "2 = slightly unsatisfactory (the reviewer believes there needs to be some improvement in this area)",
         "3 = average (the reviewer believes the performance is ok, but there could be improvement in this area)",
         "4 = good (the reviewer believes that this is a strength)",
         "5 = excellent (the reviewer believes that this is an outstanding strength)"]

# ---------------------------------------------------------------- shared pieces
def chip_draw(p, x, y, w, v, h):
    _, fill, ink = LEVELS[LEVEL_OF[v]]
    cw, ch = 30, 14
    rrect(p, (x + (w - cw) / 2, y, x + (w + cw) / 2, y + ch), 3, fill=fill)
    text(p, x + w / 2, y + 10.3, v, 'S', 8.6, ink, 'center')
def chip_h(v, w): return 14
def name_draw(p, x, y, w, v, h): rich(p, x, y, v, 8.4, 12.2, w, C['ink'], f='S')
def name_h(v, w): return rich_h(v, 8.4, 12.2, w, f='S')

def score_table(rows, pad=(8, 6.5)):
    R.table([122, CW - 122 - 3 * 58, 58, 58, 58], ['Competency', 'Description', 'manager', 'coworker', 'self'], rows,
            size=8.4, lead=12.2, pad=pad, renderers={0: (name_draw, name_h), 2: (chip_draw, chip_h), 3: (chip_draw, chip_h), 4: (chip_draw, chip_h)},
            color=C['slate'])

def scale_block():
    R.para('These ratings are on a scale of:', **BODY)
    for s in SCALE: R.para(s, size=9.2, lead=13.4, after=0)
    R.space(10)

def donut(p, c, shares, label, r1=62, r0=42):
    a = 0
    for (name, fill, _), share in zip(LEVELS, shares):
        if share > 0: ring_segment(p, c, r0, r1, a, a + 360 * share, fill)
        a += 360 * share
    text(p, c[0], c[1] + 3.5, label, 'R', 10, C['ink'], 'center')
    lx, ly = c[0] + r1 + 26, c[1] - 30
    for i, (name, fill, _) in enumerate(LEVELS):
        rrect(p, (lx, ly + i * 11, lx + 3, ly + i * 11 + 9), 0, fill=fill)
        text(p, lx + 8, ly + i * 11 + 7.4, name, 'R', 7.2, C['ink'])

def radar(p, c, rad, labels, series):
    """Polygon grid; the inner ring is 'Not Observed', then 1 to 5. Axes run counter-clockwise from the top, as in the source."""
    n = len(labels)
    def pt(i, v): t = math.radians(-90 - i * 360 / n); return (c[0] + rad * v / 6 * math.cos(t), c[1] + rad * v / 6 * math.sin(t))
    for k in range(1, 7): poly(p, [pt(i, k) for i in range(n)], color=C['mist'], width=0.6)
    for i in range(n): line(p, c, pt(i, 6), C['mist'], 0.6)
    for (name, col), vals in zip(SERIES, series):
        pts = [pt(i, v + 1) for i, v in enumerate(vals)]
        poly(p, pts, fill=col, color=col, width=1.6, opacity=0.14, stroke_opacity=1)
        for q in pts: circle(p, q, 2.4, fill=col)
    text(p, c[0], c[1] - rad / 6 - 3 + 14, 'Not Observed', 'R', 6.6, C['slate'], 'center')
    for k in range(1, 6): text(p, c[0] - 5, c[1] - rad * (k + 1) / 6 + 2.6, str(k), 'R', 7, C['ink'], 'right')
    for i, lab in enumerate(labels):
        q = pt(i, 6.75); ang = (-90 - i * 360 / n) % 360
        al = 'center' if abs(math.cos(math.radians(ang))) < 0.2 else ('left' if math.cos(math.radians(ang)) > 0 else 'right')
        text(p, q[0], q[1] + (3 if al != 'center' else (0 if math.sin(math.radians(ang)) < 0 else 8)), lab, 'R', 8.2, C['ink'], al)
    lx, ly = c[0] + rad * 0.62, c[1] - rad - 26
    for i, (name, col) in enumerate(SERIES):
        circle(p, (lx, ly + i * 12), 3.4, fill=col); text(p, lx + 9, ly + i * 12 + 3, name, 'R', 8.6, C['ink'])

def word_cloud(p, box, weights):
    """Words sized by how often and how high they were ranked; placed on a spiral from the centre, largest first."""
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    top = max(weights.values()); placed = []
    shades = [C['vivid'], C['logo'], C['s400'], C['slate'], C['electric']]
    for k, (w, wt) in enumerate(sorted(weights.items(), key=lambda kv: (-kv[1], kv[0]))):
        size = 8.5 + 13 * wt / top; f = 'S' if wt >= top * 0.7 else 'M'
        ww, hh = tw(w, f, size), size * 1.12
        for step in range(4000):
            t = step * 0.31; rr = 1.15 * t
            x, y = cx + rr * math.cos(t) * 1.7 - ww / 2, cy + rr * math.sin(t) - hh / 2
            if x < x0 or y < y0 or x + ww > x1 or y + hh > y1: continue
            if all(x + ww + 5 < a or a + c + 5 < x or y + hh + 2 < b or b + d + 2 < y for a, b, c, d in placed):
                placed.append((x, y, ww, hh)); text(p, x, y + size * 0.86, w, f, size, shades[k % len(shades)]); break

def ranked(lists):
    """lists: {reviewer: [rank-1 names, rank-2 names, rank-3 names]} → weight per competency (3 points for rank 1, 2, 1)."""
    out = {}
    for ranks in lists.values():
        for i, names in enumerate(ranks):
            for nm in names.split(', '): out[nm] = out.get(nm, 0) + 3 - i
    return out

def reviewer_lists(lists):
    for who, ranks in lists.items():
        R.h3(f'{who}:', size=9.6)
        for i, names in enumerate(ranks):
            R.para(f'{i + 1}. {names}', size=9.2, lead=14, after=3, x=MX + 10)
        R.space(6)

def open_text(title, lead, answers):
    R.new_page()
    R.h2(title, size=12.5)
    R.para(f'**{lead}**', **BODY, after=16)
    for who, items in answers:
        R.h3(f'{who}:', size=9.6)
        R.bullets(items, size=9.2, lead=14, gap=6, after=10)

# ================================================================ introduction
R.h1('Introduction')
R.para("**This report presents an analysis of the results obtained in Elevatus’s 360 Feedback. This evaluation tool is designed to analyze the professional competencies of individuals, based on multi-source feedback.**", **BODY, after=14)
R.h3('Benefits of using a 360°Feeback')
R.bullets([f"To create awareness on how {NAME}’s professional competencies are perceived by others.",
           f"To provide information on {NAME}’s strengths and how to build upon those.",
           f"To find out about areas {NAME} may need to improve on in order to become more effective.",
           "To establish a personal development plan according to the needs identified."], **BODY, after=14)
R.h3('How to use this 360 report')
R.para(f"The 360 test report is a support for reflection and communication. It should be part of an active exchange with {NAME}.", **BODY, after=18)
R.h3('Some precautions to be taken when reading this report:')
R.bullets(["Remember, not all reviewers who have given their rating for this 360 feedback are trained for this type of exercise. Thus, it is advisable not to give too much importance to each score independently, but rather to study the consensus between reviewers.",
           "Use of this report requires a complete understanding of the objectives of the evaluation and of the precise meanings of the competencies measured, in order to interpret the results accurately.",
           "The results must be analyzed in accordance with the requirements of the job position and the working environment in which the person will evolve.",
           "It is advisable to complete this evaluation by using other tests as well (for example, a reasoning or personality questionnaire), in order to have an overall overview of the candidate’s potentialities.",
           "This report is confidential and is intended for use by professionals who have sufficient knowledge of psychometric testing. The report should not be released to a third party without the explicit consent of the person being evaluated."], **BODY)

# ================================================================ summary page
R.new_page()
R.h1('Summary Page')
R.para(f"**This section provides you with a quick general summary of how {NAME} was rated by the different reviewers. Below you can see how often (in percent) she was evaluated for each category, across all six rating levels. You can use this page to see at a glance how the various reviewers responded.**", **BODY, after=20)
# shares measured from the source charts, in the order of LEVELS (manager and self are exact counts out of 46 competencies)
SHARES = [('manager', [14 / 46, 0, 0, 1 / 46, 3 / 46, 28 / 46]),
          ('coworker', [0.203, 0, 0.022, 0.032, 0.192, 0.551]),
          ('self', [0, 0, 5 / 46, 15 / 46, 16 / 46, 10 / 46])]
for label, shares in SHARES:
    donut(R.p, (W / 2 - 40, R.y + 70), shares, label)
    R.y += 168

# ================================================================ general performance
R.new_page()
R.h1('Analysis of General Performance')
R.para(f"**This section brings together all ratings, showing the average score on each of the competency groups, and their general performance rating. This can be used to identify which broad areas {NAME} excels in, and which areas may need further development. See the analysis by competency group section for more detailed results.**", **BODY, after=12)
scale_block()
R.para("For categories where there are multiple reviewer (such as co-workers or direct reports), the ratings are averaged across the group, and not observed scores are only shown if the entire group chooses not observed.)", **BODY, after=12)
score_table(DATA['general'], pad=(8, 3.2))

# ================================================================ by competency group
R.new_page()
R.h1('Analysis by competency group')
R.para("**This section of the report gives a more in-depth analysis of each competency group, to enable a more comprehensive discussion of an individual’s performance.**", **BODY, after=12)
scale_block()
R.para("For categories where there are multiple reviewers (such as co-workers or direct reports), the ratings are averaged across the group, and not observed scores are only shown if the entire group chooses not observed.", **BODY, after=14)
R.h3('How to interpret this section / advice')
R.bullets([f"It is important to note that if a competency is rated as ‘not observed,’ it does not necessarily mean that {NAME} is lacking in this competency. It may mean that she did not have the opportunity to demonstrate her skill in this area.",
           f"It is also important to highlight competencies where there are differences between the reviewers. For example, {NAME} may believe her presentation skills to be lacking, yet her colleagues may believe she has excellent presentation skills; it could be beneficial to discuss this.",
           f"If {NAME} has been rated as low on a competency, it would be advisable to help her understand why she has been rated this way, and to develop a personal development plan with her on how to improve in this area."], **BODY)

for g in DATA['groups']:
    R.new_page()
    R.h2(g['title'], size=12.5)
    R.para(f"**{g['intro']}**", **BODY, after=10)
    rad = 104; c = (W / 2 - 14, R.y + 42 + rad)
    radar(R.p, c, rad, [r[0] for r in g['rows']], [[LEVEL_OF[r[2 + k]] for r in g['rows']] for k in range(3)])
    R.y = c[1] + rad + 44
    score_table(g['rows'])

# ================================================================ key competencies and open text
R.new_page()
R.h1('Key Competencies and Open Text Feedback')
R.space(6)
R.h3('Key Strengths and Areas for Improvement')
R.para(f"Reviewers were asked to state what they believe to be {NAME}’s top three strengths and top three areas for improvement, from the complete list of evaluated competencies, in the previous section.", **BODY)
R.para("In relation to ratings that have been given by multiple reviewers (such as coworkers or direct reports), the consensual key strengths and areas for improvement are given. That is, those that are ranked the most consistently as the top three.", **BODY, after=20)
R.h3('Open Text Feedback')
R.para("This section presents the open text feedback provided by all reviewers. These comments can be useful for understanding the results in more depth, and allowing the reviewers to express their feedback without being restrained to a rating scale.", **BODY)
R.para("The comments are displayed in the way that they were entered by the participants. The order does not reflect their importance. To get the most out of the information provided, it should be considered alongside the ratings that have been provided in the previous report sections.", **BODY)

STRENGTHS = {'manager': ['Adaptation to Change', 'Listening skills', 'Analytical Thinking'],
             'coworker': ['Knowledge Management, Presentation skills, Organisational Skills, Quality Orientation, Involvement',
                          'Organisational Skills, Strategic communication, Involvement, Respecting Instructions, Taking Responsibility, Analytical Thinking',
                          'Sense of Duty, Knowledge Sharing, Availability, Modesty'],
             'self': ['Availability', 'Striving', 'Self-appraisal']}
IMPROVE = {'manager': ['Managerial Courage', 'Influencing Skills', 'Delegation'],
           'coworker': ['Decision-making, Innovation - Creativity, Delegation, Self-affirmation, Influencing Skills',
                        'Influencing Skills, Analytical Thinking, Knowledge Management, Team Motivation, Promoting Change, Self-affirmation',
                        'Openness to Diversity, Learning Agility, Promoting Change, Strategic Planning, Global vision'],
           'self': ['Perspective taking', 'Respect', 'Team Motivation']}
for title, lead, lists in (('Key Strengths', f"This section provides a summary of what {NAME}’s colleagues believe her key strengths are.", STRENGTHS),
                           ('Key Areas for Improvement', f"This section provides a summary of what {NAME}’s colleagues believe her key areas of improvement are.", IMPROVE)):
    R.new_page()
    R.h2(title, size=12.5)
    R.para(f'**{lead}**', **BODY, after=10)
    word_cloud(R.p, (MX, R.y, MX + 330, R.y + 170), ranked(lists))
    R.y += 190
    reviewer_lists(lists)

NONE = ['No Response given']
open_text('Positive Open Text Feedback', f"This section provides a summary of the positive open text feedback that {NAME}’s colleagues have provided.",
          [('manager', NONE),
           ('coworker', ["Nour is a very positive-minded person. A great co-worker. Feels happy to motivated to work along with her for our common goals in striving the organization forward.",
                         "Incredibly organised & strategic, on the ball and on top of everything, nothing ever gets missed. Always working to the best standards possible. Very conscientious and always available to help.",
                         "Nour is a very supportive person and has a really high knowledge of her area of work. It is really nice to work with Nour.",
                         "Nour is a great coworker, she is always available, patient and supportive. She is excellent at mentoring and leading project. Meticulous, the quality of her job and her implication is an inspiration and transmit motivation and will to surpass oneself when working on the projects she conduct."]),
           ('self', NONE)])
open_text('Negative Open Text Feedback', f"This section provides a summary of the negative open text feedback that {NAME}’s colleagues have provided.",
          [('manager', NONE),
           ('coworker', ["n/a",
                         "Difficult to think of anything. At a stretch (!!!) it could be remaining flexible to others’ working styles and project manage some elements on a more macro level",
                         "It is difficult to assess some competences due that we have always worked online, without the benefit of an in person relation (this is important as it might be the reason behind my comment here ). In my opinion it might be a benefit for Nour to be aware about different styles and levels of maturity of the members of the team and organize the supervision and checks accordingly to promote the maximum level of autonomy for each team member.",
                         "Nour might sometimes lack of self-affirmation"]),
           ('self', NONE)])
open_text('Other Open Text Feedback', f"This section provides a summary of the other open text feedback that {NAME}’s colleagues have provided.",
          [('manager', NONE),
           ('coworker', [f"3 competencies that {NAME} should work on: The options I have selected in this part is not valid as I didnt have any other option to select",
                         "Wonderful to work with & the team would be lost without you"]),
           ('self', NONE)])

# ================================================================ personal development plan
def plan_form(n):
    """Empty form to fill in by hand, as in the source: a title row and four labelled boxes."""
    rows = [(f'Focus Area {n}', 26), ('Goal', 62), ('Short Term Action Plan (within the next 3 months)', 66), ('Long Term Action Plan (within one year)', 70)]
    x0, x1 = MX + 60, W - MX - 60
    total = sum(18 + h for _, h in rows)
    R.ensure(total + 20)
    p = R.p; y = R.y
    for i, (label, h) in enumerate(rows):
        rrect(p, (x0, y, x1, y + 18), 0, fill=C['logo'] if i == 0 else C['s100'])
        text(p, x0 + 8, y + 12.4, label, 'S', 8.8, C['white'] if i == 0 else C['logo'])
        y += 18 + h
    rrect(p, (x0, R.y, x1, y), 0, color=C['mist'], width=1)
    yy = R.y
    for label, h in rows[:-1]:
        yy += 18 + h; line(p, (x0, yy), (x1, yy), C['mist'], 1)
    R.y = y + 26

R.new_page()
R.h1('Personal Development Plan')
R.para("**This plan will help you to establish a clear action plan, to help you focus on any areas that need improvement.**", **BODY)
R.bullets(["Identify 3 areas that you would like to improve on. You can consult the summary page to get a better overview and look at the detailed results if needed. (Example focus area: Presentation skills)",
           "Identify the goals that you would like to reach for each area. (Example goal: Feel confident giving a presentation in front of the team)",
           "Provide a clear list of actions that will help you to reach your goals in the short-term and long-term. (Example short term action plan: Give a speech in front of your family and friends.Example long term action plan: Follow a training to improve your presentation skills)"], **BODY, after=22)
for n in (1, 2, 3): plan_form(n)

R.cover('360 Feedback', 'A clear view of professional competencies across nine groups, as rated by manager, coworkers and self.',
        'Multi-source\nFeedback', 'Sample Report')
print(R.save(OUT), 'pages ->', OUT)

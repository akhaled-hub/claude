# SMART Personality sample report, Elevatus edition.
# Same content and the same elements as the source report (Testlify): nothing added, only restyled. The cover is the Elevatus cover template.
# The source's candidate was the vendor's own account ("Testlify Support"), so a sample candidate takes its place,
# and the two ''Name'' placeholders left in the source text are filled with that candidate's name.
import sys, math, os
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUTPUT, 'Elevatus - SMART Personality Assessment Sample Report.pdf')
PERSON, FIRST, DATE = 'Sara Al-Haddad', 'Sara', 'Oct 12, 2026'
R = Report(PERSON, DATE, 'SMART - Personality', '2026', 'Elevatus - SMART Personality Assessment Sample Report')

BODY = dict(size=9.3, lead=14.4, color=C['slate'])
WARN = C['apricot_ink']

# score levels, as in the source bars (low / medium / high), one brand colour each
def level_color(v): return C['vivid'] if v >= 70 else (C['s400'] if v > 33.34 else C['apricot'])

# ================================================================ candidate information
R.h1('Candidate Information')
R.space(2)
rows = [('Name', PERSON), ('Date', DATE), ('Email', 'sara.alhaddad@example.com'), ('Phone number', 'N/A')]
rh, lw = 30, 170   # the source table has no header row: label column + value column
rrect(R.p, (MX, R.y, W - MX, R.y + rh * len(rows)), 8, color=C['line'])
rrect(R.p, (MX, R.y, MX + lw, R.y + rh * len(rows)), 8, fill=C['paper'])
R.p.draw_rect((MX + lw - 8, R.y, MX + lw, R.y + rh * len(rows)), fill=C['paper'], color=None)
for i, (k, v) in enumerate(rows):
    y = R.y + i * rh
    if i: line(R.p, (MX, y), (W - MX, y))
    text(R.p, MX + 12, y + 19, k, 'M', 9.3, C['logo'])
    text(R.p, MX + lw + 12, y + 19, v, 'R', 9.3, C['ink'])
line(R.p, (MX + lw, R.y), (MX + lw, R.y + rh * len(rows)))
R.y += rh * len(rows)

# ================================================================ table of contents
R.new_page()
R.h1('Table of contents')
R.space(2)
for head, sub, items in [('Introduction', 'Overview of the SMART Personality assessment and the Big Five framework.', None),
                         ('How to read this report', 'Guidelines for interpreting the results and understanding the scoring system.', None),
                         ('Graphical representation of SMART score', "Summary of the individual's workplace preferences and role fit.", None),
                         ('Personality dimensions and sub-traits', 'In-depth results and personalized insights for each of the five core dimensions:',
                          ['Sociability', 'Mindfulness', 'Agreeableness', 'Receptivity to new things', 'Temperamental']),
                         ('Disclaimer', 'Notes on interpretation, validity, and intended use of the assessment.', None)]:
    R.h2(head, size=12)
    R.para(sub, after=4 if items else 12, **{k: v for k, v in BODY.items()})
    if items: R.bullets(items, size=9, lead=13.6, color=C['slate'], gap=3, after=12)

# ================================================================ response overview
R.new_page()
R.h1('Response Overview')
R.para("This page reflects how the assessment was answered — response consistency and self-presentation. It is a data-quality check, not a measure of personality.", **BODY)
R.space(4)
p = R.p; pad = 14
s1 = "Responses leaned strongly toward favorable answers, which can affect some trait scores. Worth a brief check in conversation."
s2 = "Based on how this assessment was answered — not a measure of personality."
h = pad + 12 + 22 + rich_h(s1, 9.3, 14, CW - 2 * pad) + 6 + 13 + pad
rrect(p, (MX, R.y, W - MX, R.y + h), 10, fill=C['white'], color=C['line'])
y = R.y + pad
text(p, MX + pad, y + 8, 'Response Summary', 'M', 8.6, C['slate'])
text(p, MX + pad, y + 28, 'Review Flagged', 'S', 14, WARN)
y += 38
y += rich(p, MX + pad, y, s1, 9.3, 14, CW - 2 * pad, C['ink']) + 6
circle(p, (MX + pad + 3.5, y + 5.6), 3.4, color=C['slate'], width=0.7)
text(p, MX + pad + 2.6, y + 7.6, 'i', 'M', 5.5, C['slate'])
text(p, MX + pad + 11, y + 8, s2, 'R', 8.2, C['slate'])
R.y += h + 12
gap = 12; cw = (CW - gap) / 2
cards = [('Confidence Index', '64% (Moderate)', "Responses showed some inconsistency. Trait scores remain usable but should be read with mild caution, particularly borderline results."),
         ('Self-Presentation', '75% (Elevated)', "Responses leaned strongly toward favorable answers across multiple questions, which can inflate some trait scores. Interpret with caution.")]
h = pad + 38 + max(rich_h(s, 9, 13.6, cw - 2 * pad) for _, _, s in cards) + pad
for i, (t, v, s) in enumerate(cards):
    x = MX + i * (cw + gap)
    rrect(p, (x, R.y, x + cw, R.y + h), 10, fill=C['white'], color=C['line'])
    text(p, x + pad, R.y + pad + 8, t, 'M', 8.6, C['slate'])
    text(p, x + pad, R.y + pad + 27, v, 'S', 13, WARN)
    rich(p, x + pad, R.y + pad + 38, s, 9, 13.6, cw - 2 * pad, C['ink'])
R.y += h + 26
R.h2('Summary Interpretation', size=13)
R.space(2)
STATUS = {'Valid': C['vivid'], 'Usable, mild caution': C['s400'], 'Review Flagged': C['apricot'], 'Invalid – re-test advised': WARN}
def st_draw(p, x, y, w, v, h): text(p, x, y + 9.9, v, 'M', 9, STATUS[v])
def st_h(v, w): return 13.4
R.table([170, CW - 170], ['Summary', 'What it means'],
        [['Valid', 'Responses are reliable. Trait scores can be interpreted normally.'],
         ['Usable, mild caution', 'Minor inconsistencies in the responses. Trait scores remain usable; verify borderline results.'],
         ['Review Flagged', 'Response patterns warrant review before relying on the scores.'],
         ['Invalid – re-test advised', 'Response patterns are unreliable; results should not drive a decision alone.']],
        renderers={0: (st_draw, st_h)}, size=9)

# ================================================================ introduction, how to read, SMART radar
DIMS = [('Sociability', 55.56), ('Mindfulness', 79.17), ('Agreeableness', 59.72), ('Receptivity to new things', 76.39), ('Temperamental Behavior', 81.95)]

def radar(p, c, rad):
    n = len(DIMS)
    def pt(i, v): t = math.radians(-90 + i * 360 / n); return (c[0] + rad * v / 100 * math.cos(t), c[1] + rad * v / 100 * math.sin(t))
    for k in range(10, 101, 10): poly(p, [pt(i, k) for i in range(n)], color=C['line'], width=0.6)
    for i in range(n): line(p, c, pt(i, 100), C['line'], 0.6)
    pts = [pt(i, v) for i, (_, v) in enumerate(DIMS)]
    poly(p, pts, fill=C['vivid'], color=C['vivid'], width=1.8, opacity=0.12, stroke_opacity=1)
    for q in pts: circle(p, q, 2.8, fill=C['vivid'], color=C['white'], width=1.2)
    for i, (name, v) in enumerate(DIMS):
        q = pt(i, 113)
        al = 'center' if i == 0 else ('left' if i in (1, 2) else 'right')
        dy = -5 if i == 0 else (12 if i in (2, 3) else 3)
        lab = f'{name}  {v:g}%'
        text(p, q[0], q[1] + dy, lab, 'R', 9.5, C['ink'], al)

R.new_page()
R.h1('Introduction')
R.para("The Big Five Factor Theory is the basis of this SMART personality assessment. All five dimensions are preserved in order to comprehend their breadth across various human behaviours and their implications", **BODY)
R.space(8)
R.h1('How to read this report', size=15)
R.para("This personality assessment tool that we call SMART. We've based it on the widely recognized Big Five Factor Theory, which is often used in entry-level pre-hire assessments. Our team conducted a deep dive into the research to make sure we covered all sub-factors of each of the 5 dimensions, making our assessment the most comprehensive and up-to-date tool available. And we don't stop there - to ensure our assessment is accurate and relevant, we carefully crafted behavior indicators and measurements using the latest scientific knowledge. With SMART assessment, you can be confident that you're getting a thorough and accurate evaluation of individual's personality traits.", **BODY)
R.space(8)
R.h1('Graphical representation of SMART score', size=15)
panel = fitz.Rect(MX, R.y + 2, W - MX, R.y + 2 + 280)
rrect(R.p, panel, 12, fill=C['paper'])
radar(R.p, (W / 2, panel.y0 + 148), 100)
R.y = panel.y1 + 14
cards = [('Culture Alignments', 'Values and encourages emotional intelligence, empathy, and work-life balance.'),
         ('Motivating Factors', 'Supportive , Understanding, and Flexibility.'),
         ('Suitable Roles', 'Tele-caller, Support executive, Community outreach roles.')]
gap = 12; cw = (CW - 2 * gap) / 3; pad = 12
h = pad + 20 + max(rich_h(s, 8.8, 13, cw - 2 * pad) for _, s in cards) + pad
for i, (t, s) in enumerate(cards):
    x = MX + i * (cw + gap)
    rrect(R.p, (x, R.y, x + cw, R.y + h), 10, fill=C['paper'])
    text(R.p, x + pad, R.y + pad + 9, t, 'S', 9.2, C['logo'])
    rich(R.p, x + pad, R.y + pad + 20, s, 8.8, 13, cw - 2 * pad, C['slate'])
R.y += h

# ================================================================ dimension pages
def dimension(n, name, score, interp, traits, strengths, indicators, rec, first=False):
    R.new_page()
    if first: R.h1('Personality dimensions and sub-traits'); R.space(2)
    p = R.p
    head = f'{n}. {name}'
    text(p, MX, R.y + 16, head, 'S', 16, C['logo'])
    text(p, MX + tw(head + '  ', 'S', 16), R.y + 16, f'{score}%', 'S', 16, C['vivid'])
    R.y += 32
    R.h3('Interpretation', color=C['logo'])
    R.para(interp, **BODY)
    # sub-trait bars: low / medium / high scale
    R.space(4)
    tx0, tx1 = MX + 130, W - MX - 52
    for lab, al, x in (('LOW', 'left', tx0), ('MEDIUM', 'center', (tx0 + tx1) / 2), ('HIGH', 'right', tx1)):
        text(p, x, R.y + 6, lab, 'M', 6.5, C['slate'], al, track=0.08)
    R.y += 18
    for lab, v in traits:
        col = level_color(v)
        text(p, MX, R.y + 6.5, lab, 'M', 9.3, C['ink'])
        rrect(p, (tx0, R.y + 1.5, tx1, R.y + 5.5), 2, fill=C['s100'])
        xe = tx0 + (tx1 - tx0) * v / 100
        rrect(p, (tx0, R.y + 1.5, xe, R.y + 5.5), 2, fill=col)
        circle(p, (xe, R.y + 3.5), 4.6, fill=col, color=C['white'], width=1.4)
        text(p, W - MX, R.y + 6.5, f'{v:g}%', 'S', 9.3, C['ink'], 'right')
        R.y += 20
    R.space(10)
    pad = 13
    for t, items in (('Core strengths', strengths), ('Potential indicators', indicators)):
        if not items: continue
        h = pad + 18 + bullets_h(items, 8.9, 13.4, CW - 2 * pad, gap=3) + pad
        R.ensure(h)
        rrect(p, (MX, R.y, W - MX, R.y + h), 10, fill=C['paper'])
        text(p, MX + pad, R.y + pad + 9, t, 'S', 9.6, C['logo'])
        bullets(p, MX + pad, R.y + pad + 18, items, 8.9, 13.4, CW - 2 * pad, C['slate'], gap=3)
        R.y += h + 10
    R.space(6)
    R.h3('Recommendation', color=C['logo'], size=11)
    R.para(rec, **BODY)

dimension(1, 'Sociability', '55.56',
          f"{FIRST} has a tendency to be comfortable in social situations and enjoy spending time with others, but also values alone time and needs some time to recharge after socializing. {FIRST} may be more assertive and outgoing in certain situations, but also be able to adapt to more quiet settings and be comfortable being more reserved when necessary.",
          [('Being Positive', 58.33), ('Communicative', 58.33), ('Excitement Seeking', 83.33), ('Assertiveness', 91.67), ('Friendliness', 25), ('Cheerfulness', 16.67)],
          ['Is energetic, always on alert and to be busy most of the time.', 'Self-assured and confident without being aggressive.'],
          ['Is responsible and accept consequences.', 'Clearly express ideas to others in precise manner.'],
          f"Encourage {FIRST} to embrace their sociable nature while also honoring their need for downtime. Balancing social activities with personal time will help them recharge and maintain a positive outlook. Engaging in diverse social settings, both lively and calm, will enhance their adaptability and confidence. Celebrating their unique blend of assertiveness and reservation can further enrich their social experiences, allowing {FIRST} to thrive in both energetic and serene environments. This balanced approach will support their overall well-being and personal growth.",
          first=True)

dimension(2, 'Mindfulness', '79.17',
          f"{FIRST} is likely to be organized, reliable, and responsible. {FIRST} may take a thoughtful and planned approach to tasks and responsibilities and may be more inclined to follow rules and routines. {FIRST} may also be more risk-averse and less inclined to try new things without careful consideration. {FIRST} may find creative solutions to problems using the resources available to it.",
          [('Self', 58.33), ('Dutifulness', 66.67), ('Thoughtfulness', 91.67), ('Thoroughness', 75), ('Resourcefulness', 91.67), ('Persistence', 91.67)],
          ['Has a conscious awareness of the needs and feelings of others.', 'Has the ability to find quick and clever ways to overcome difficulties.', 'Ability to remain in the same state for an indefinitely long time till goal is achieved.'],
          ["Has the ability to control one's actions, impulses, or emotions and maintain composure.", 'Devoted to the task at hand and makes sure all requirements are met.', 'Is extremely cautious and pays close attention to details.'],
          f"{FIRST} has already shown a strong ability to be organized, reliable, and disciplined in their approach to tasks and responsibilities. By thoughtfully planning and following routines, they have successfully navigated challenges and maintained consistency in their endeavors. Their ability to balance structure with creative problem-solving has contributed to positive outcomes in various situations. Building on these strengths, {FIRST} can further benefit from occasionally integrating moments of spontaneity, allowing for new experiences while still relying on their well-established sense of responsibility. This balanced approach will enhance their personal growth and lead to even more fulfilling experiences.")

dimension(3, 'Agreeableness', '59.72',
          f"{FIRST} has a tendency to exhibit a balance of cooperative and competitive tendencies. {FIRST} may be open to compromise and willing to consider others' perspectives, but {FIRST} is also able to assert his or her own needs and priorities when necessary. {FIRST} may be able to navigate social situations with sensitivity and tact, but {FIRST} may also be more independent and less concerned with maintaining harmonious relationships in certain situations.",
          [('Selflessness', 66.67), ('Trustworthy', 58.33), ('Collaborative', 58.33), ('Empathetic', 66.67), ('Humbleness', 58.33), ('Helpfulness', 50)],
          None,
          ["Seeking out others' well-being over one's own in order to prioritise it.", 'Is honest who can be entrusted with anything that is very important.', 'Participates and works with others to achieve shared goals.',
           'Has the capacity for sharing the feelings of another from their perspective.', 'Being humble and not immersing oneself in the pool of self-glory.', 'Constantly willing to help others and provides assistance.'],
          f"Promoting open communication and encouraging {FIRST} to be willing to compromise will help enhance their effectiveness in social interactions. Engaging in discussions that value multiple perspectives can further strengthen their adaptability.")

dimension(4, 'Receptivity to new things', '76.39',
          f"{FIRST} is likely to be open-minded, curious, and receptive to new ideas and experiences. {FIRST} may enjoy trying new things and be more willing to take risks and try things that are outside {FIRST} comfort zone. {FIRST} may also be more creative and open to considering unconventional perspectives. {FIRST} may have a deep appreciation for the aesthetic, emotional, or intellectual qualities of art.",
          [('Creativity', 91.67), ('Unconventional', 91.67), ('Aesthetics', 91.67), ('Curiosity', 50), ('Adventurousness', 91.67), ('Insightfulness', 41.67)],
          ['Has the ability to produce ideas or things that are new, unique, and valuable.', 'Follow ideas or actions that are different from what is considered normal or traditional.', 'Shows immense passion for or fascination for everything in life.', 'Is daring and inclined or willingness to accept risks.'],
          ['Has a strong desire to know or learn something unusual or even well-known facts.', 'Shows deep understanding and intelligent application of knowledge.'],
          f"{FIRST} has already demonstrated a remarkable openness to new experiences and a strong creative ability. Their curiosity and willingness to step outside their comfort zone have led to a broader perspective and a deeper appreciation for unconventional ideas. This receptivity to new things, coupled with their artistic sensibilities, has enriched both their personal and intellectual life. By continuing to engage in creative outlets and collaborative projects, {FIRST} can further nurture this strength and explore new avenues for growth. Recognizing their ability to embrace the unknown and take risks will support their ongoing journey of exploration and self-expression, leading to even more meaningful and fulfilling experiences.")

dimension(5, 'Temperamental Behavior', '81.95',
          f"{FIRST} is more inclined to react emotionally and is prone to feeling unfavorable emotions like sadness, rage, and anxiety. {FIRST} can be more susceptible to stress and struggle to handle challenging circumstances. This does not necessarily imply that {FIRST} cannot control his or her emotions or that {FIRST} is always sad; rather, it may simply indicate that {FIRST} is more likely to experience negative emotions and may require more effort to control and manage them.",
          [('Moodiness', 91.67), ('Emotional Reactivity', 83.33), ('Dependency', 83.33), ('Timidity', 91.67), ('Oversensitivity', 66.67), ('Insecurity', 75)],
          ['Emotional stability and consistency, without frequent or intense mood swings.', 'Ability to handle change and pressure with resilience, without sudden breakdowns or drastic changes.',
           'Independent and self-sufficient, without relying on others for emotional support or care.', 'Confident and courageous, especially in social situations, without lacking self-esteem.'],
          ['Resilient and able to take criticism or negative feedback without being easily offended or hurt.', "Confident in one's own worth, abilities, and chances of success, without doubting oneself."],
          f"{FIRST} has already demonstrated resilience in managing emotional fluctuations and navigating challenging situations. Their awareness of emotional reactivity is a positive step toward developing greater emotional stability. Building on this self-awareness, {FIRST} can further strengthen their ability to manage stress and mood by continuing to adopt practices that help regulate emotions, such as cognitive-behavioral techniques, mindfulness activities like meditation or yoga, and regular physical exercise. Establishing routines and setting clear boundaries will also contribute to their emotional well-being, providing a sense of control and stability. With these strategies and the support of constructive feedback and strong relationships, {FIRST} will be well-equipped to maintain balance in the face of adversity and continue fostering personal growth.")

# ================================================================ disclaimer
R.new_page()
R.h1('Disclaimer')
R.para("This personality assessment tool that we call SMART. We've based it on the widely recognized Big Five Factor Theory, which is often used in entry-level pre-hire assessments. Our team conducted a deep dive into the research to make sure we covered all sub-factors of each of the 5 dimensions, making our assessment the most comprehensive and up-to-date tool available. And we don't stop there - to ensure our assessment is accurate and relevant, we carefully crafted behavior indicators and measurements using the latest scientific knowledge. With SMART assessment, you can be confident that you're getting a thorough and accurate evaluation of individual's personality traits.", **BODY)

R.cover('SMART Personality Assessment', 'A clear view of personality across five dimensions: Sociability, Mindfulness, Agreeableness, Receptivity to new things and Temperamental Behavior.',
        'Personality\nAssessment', 'Sample Report')
print(R.save(OUT), 'pages ->', OUT)

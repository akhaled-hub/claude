# 360 Feedback presentation (source: Central Test sales deck), Elevatus edition. 16:9, 8 slides, same order and same words.
# Left out on purpose: stock photos and the isometric illustration (not Elevatus imagery), the vendor's contact details and office map.
# The report previews on slide 6 are vector crops of the Elevatus 360 Feedback report, so build feedback360.py first.
import sys, os
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUTPUT, 'Elevatus - 360 Feedback Presentation.pdf')
REPORT = os.path.join(OUTPUT, 'Elevatus - 360 Feedback Sample Report.pdf')
SW, SH, M = 960, 540, 56
doc = fitz.open()
doc.set_metadata({'title': 'Elevatus - 360 Feedback Presentation', 'author': 'Elevatus', 'creator': 'Elevatus', 'producer': 'Elevatus'})

def slide(dark=False, title=None):
    p = doc.new_page(width=SW, height=SH); fonts(p)
    if dark:
        p.insert_image(p.rect, filename=os.path.join(ASSETS, 'cover-bg.png'), keep_proportion=False)
        wordmark(p, M, 44, 128, C['white'])
    else:
        wordmark(p, M, 34, 92, C['vivid'])
        text(p, M, SH - 24, '360 Feedback', 'R', 8, C['slate'])
        text(p, SW - M, SH - 24, str(len(doc)), 'R', 8, C['slate'], 'right')
        if title: text(p, M, 104, title, 'S', 26, C['logo'])
    return p

def pill(p, x, y, label, w=None, filled=False, size=11):
    w = w or tw(label, 'S', size) + 28
    rrect(p, (x, y, x + w, y + 24), 12, fill=C['vivid'] if filled else C['white'], color=C['vivid'], width=1.2)
    text(p, x + w / 2, y + 16, label, 'S', size, C['white'] if filled else C['vivid'], 'center')
    return w

def check(p, x, y, color=C['vivid']):
    circle(p, (x, y), 7, color=color, width=1.3)
    sh = p.new_shape(); sh.draw_polyline([(x - 3.2, y + 0.2), (x - 0.8, y + 2.6), (x + 3.4, y - 2.6)]); sh.finish(color=color, width=1.4, closePath=False, lineCap=1, lineJoin=1); sh.commit()

def dots(p, x, y, items, size, lead, maxw, color=C['slate'], dot=C['vivid'], gap=2):
    for it in items:
        circle(p, (x + 2, y + lead * 0.5), 1.5, fill=dot)
        y += rich(p, x + 11, y, it, size, lead, maxw - 11, color) + gap
    return y

# 1 ---------------------------------------------------------------- title
p = slide(dark=True)
text(p, M - 2, 232, '360 Feedback', 'L', 56, C['white'])
text(p, M, 276, 'Enhance the skills of your employees', 'R', 19, C['white'])
pix = fitz.Pixmap(os.path.join(ASSETS, 'cover-mockup.png')); iw = 560; ih = iw * pix.height / pix.width
p.insert_image(fitz.Rect(SW - iw + 40, SH - ih - 26, SW + 40, SH - 26), filename=os.path.join(ASSETS, 'cover-mockup.png'))

# 2 ---------------------------------------------------------------- the 360 feedback
p = slide(title='The 360 Feedback')
items = [('Goal', "Evaluate an individual's skills by combining their self-assessment and that of those around them"),
         ('Principle', "Evaluation sent to the candidate themselves and their professional entourage: managers, colleagues, clients, etc."),
         ('Target audience', "Any employee, individually or in a team."),
         ('Objectivity', "The multiplicity of reviewers provides a complete and objective view of the candidate.")]
cw = (SW - 2 * M - 64) / 2
for i, (label, body) in enumerate(items):
    x = M + (i % 2) * (cw + 64); y = 168 + (i // 2) * 150
    pill(p, x, y, label, w=170, size=12)
    rich(p, x, y + 42, body, 14, 21, cw - 20, C['slate'])

# 3 ---------------------------------------------------------------- advantages
p = slide(title='Advantages')
cards = [('PERSONAL DEVELOPMENT', 'Help your teams to strengthen their self-knowledge', "The comparison between the different perceptions of an employee's skills is a basis for a development plan."),
         ('SKILL DEVELOPMENT', 'Highlight the strengths and focus on the areas of development', "Identify the strengths in your company and target areas for development as well as training needs."),
         ('ANNUAL EVALUATION', 'Feedback on professional and behavioral performance', "Feedback from the managers, peers or customers helps refocus on objectives and enhance the role of an employee within the company.")]
gap = 22; cw = (SW - 2 * M - 2 * gap) / 3
for i, (cap, head, body) in enumerate(cards):
    x = M + i * (cw + gap); y = 156
    rrect(p, (x, y, x + cw, y + 300), 14, fill=C['paper'])
    text(p, x + 24, y + 40, cap, 'M', 10, C['vivid'], track=0.08)
    hh = rich(p, x + 24, y + 62, head, 17, 23, cw - 48, C['logo'], f='S')
    rich(p, x + 24, y + 62 + hh + 16, body, 12.5, 19, cw - 48, C['slate'])

# 4 ---------------------------------------------------------------- features
p = slide(title='Features of 360 Feedback')
feats = ["For reviewers: Information on the bond with the participant (no. of years of collaboration, hierarchical link, etc.)",
         "Rating of the skills to be assessed: very unsatisfactory (1); very good (5); unobserved (0)",
         "General performance assessment", "Strengths and areas for improvement", "Personalised comments"]
y = 146
for f_ in feats:
    check(p, M + 8, y + 9)
    y += rich(p, M + 30, y, f_, 12.5, 18.5, 330, C['slate']) + 12
img = os.path.join(ASSETS, 'feedback360-rating-form.png'); pix = fitz.Pixmap(img)
fw = 420; fh = fw * pix.height / pix.width; fx = SW - M - fw; fy = 140
rrect(p, (fx - 12, fy - 12, fx + fw + 12, fy + fh + 12), 14, fill=C['white'], color=C['s100'], width=1.2)
p.insert_image(fitz.Rect(fx, fy, fx + fw, fy + fh), filename=img)
facts = ['3 modules:\ngeneric, sales,\nmanagerial', '4 categories of\nreviewers\n(n, n+1, n-1, others)', 'Available in\nFrench, English\nand Spanish', 'Time:\n10-15 minutes']
fwid = (SW - 2 * M) / 4; y0 = 400
line(p, (M, y0 - 14), (SW - M, y0 - 14), C['line'], 1)
for i, f_ in enumerate(facts):
    lines_ = f_.split('\n')
    for k, ln in enumerate(lines_):
        text(p, M + i * fwid + fwid / 2, y0 + 16 + k * 17 + (3 - len(lines_)) * 8.5, ln, 'S', 12.5, C['logo'], 'center')
    if i: line(p, (M + i * fwid, y0), (M + i * fwid, y0 + 66), C['line'], 1)

# 5 ---------------------------------------------------------------- skills assessed
p = slide(title='Skills Assessed')
text(p, M, 128, '51 skills divided in 9 groups for the 3 modules (generic, sales, managerial)', 'R', 13, C['slate'])
rows = [[('Work commitment', ['Quality orientation', 'Initiative', 'Taking responsibility', 'Striving', 'Involvement', 'Availability'], False),
         ('Analysis and expertise', ['Decision making', 'Analytical thinking', 'Learning agility', 'Knowledge management', 'Perspective taking', 'Knowledge sharing'], False),
         ('Planning and vision', ['Time-management', 'Organization skills', 'Strategic planning', 'Risk management', 'Innovation-creativity', 'Global vision'], False),
         ('Leadership', ['Team motivation', 'Mentoring', 'Managerial courage', 'Change management', 'Delegation', 'Performance management'], True),
         ('Sales', ['Negotiation', 'Understanding needs', 'Closing deals', 'Identification of opportunities', 'Prospecting skills', 'Networking'], True)],
        [('Values and integrity', ['Sense of duty', 'Modesty', 'Openness to diversity', 'Discretion', 'Impartiality', 'Respect'], False),
         ('Self-knowledge and management', ['Respecting instructions', 'Adaptation to change', 'Persistence', 'Stress management', 'Self-appraisal', 'Responsiveness'], False),
         ('Communication skills', ['Influencing skills', 'Strategic communication', 'Listening skills', 'Self affirmation', 'Presentation skills'], False),
         ('Relationship management', ['Conflict resolution', 'Team cohesion', 'Interpersonal skills', 'Sympaphy'], False)]]
for r, row in enumerate(rows):
    colw = (SW - 2 * M) / len(row); y = 152 + r * 172
    for i, (name, skills, filled) in enumerate(row):
        x = M + i * colw
        pill(p, x, y, name, w=colw - 14, filled=filled, size=9.6 if len(name) > 24 else 10.5)
        dots(p, x + 8, y + 36, skills, 9.6, 14.6, colw - 22)

# 6 ---------------------------------------------------------------- advantages: highlights + report format
p = slide(title='Advantages')
rep = fitz.open(REPORT)
pg = next(i for i, q in enumerate(rep) if 'Analysis & Expertise' in q.get_text() and 'Decision-making' in q.get_text() and 'Knowledge Sharing' in q.get_text() and i > 4)
tb = rep[pg].search_for('Competency')[0]
radar_clip = fitz.Rect(MX + 60, tb.y0 - 302, W - MX - 60, tb.y0 - 18)
rh = 228; rw = rh * radar_clip.width / radar_clip.height
rrect(p, (M, 122, M + rw + 20, 122 + rh + 10), 12, fill=C['white'], color=C['s100'], width=1.2)
p.show_pdf_page(fitz.Rect(M + 10, 127, M + 10 + rw, 127 + rh), rep, pg, clip=radar_clip)
hx = M + rw + 70
pill(p, hx, 128, 'Highlights of 360 Feedback', w=250, size=12)
y = 172
for h_ in ['Global and objective assessment of performance', 'Respect for the confidentiality of reviewers',
           'Detailed report promoting the construction of a personal development plan', 'Qualitative feedback in the form of comments',
           'Easy to use, with unlimited number of reviewers']:
    check(p, hx + 8, y + 9)
    y += rich(p, hx + 30, y, h_, 13.5, 19, SW - M - hx - 30, C['ink']) + 12
band = fitz.Rect(0, 372, SW, SH)
rrect(p, band, 0, fill=C['logo'])
table_clip = fitz.Rect(MX, tb.y0 - 9, W - MX, tb.y0 + 118)
tw_ = 440; th_ = tw_ * table_clip.height / table_clip.width
rrect(p, (M, 392, M + tw_ + 16, 392 + th_ + 12), 8, fill=C['white'])
p.show_pdf_page(fitz.Rect(M + 8, 398, M + 8 + tw_, 398 + th_), rep, pg, clip=table_clip)
bx = M + tw_ + 56
text(p, bx, 412, '360 Feedback Report Format', 'S', 14, C['white'])
dots(p, bx, 424, ['Introduction & how to read the report', 'General summary of feedback by category of reviewer', 'Global performance analysis',
                 'Detailed analysis of feedback by skill group', 'Summary of key skills and areas for improvement', 'Personalised comments'],
     11.5, 16.4, SW - M - bx, C['white'], dot=C['apricot'], gap=0)
text(p, M, SH - 12, '', 'R', 8, C['white'])

# 7 ---------------------------------------------------------------- 3 steps
p = slide(title='Launch your 360 campaign in 3 steps')
steps = [('Set up your campaign', ['Define the objectives of the campaign, the desired minimum participation rate and the rights of the evaluators', 'Add people to evaluate']),
         ('Manage reviewers', ['Add reviewers who will give their feedback', 'Define the type of reviewer (managers, colleagues, etc.)']),
         ('Return the results', ['View reports as soon as the participation rate is reached', 'Organise the restitution of reports and the implementation of skills development actions'])]
gap = 30; cw = (SW - 2 * M - 2 * gap) / 3
line(p, (M + 18, 186), (SW - M - cw + 18, 186), C['s200'], 1.4)
for i, (head, pts_) in enumerate(steps):
    x = M + i * (cw + gap)
    circle(p, (x + 18, 186), 18, fill=C['vivid'])
    text(p, x + 18, 191.5, str(i + 1), 'S', 15, C['white'], 'center')
    text(p, x, 244, head, 'S', 17, C['logo'])
    dots(p, x, 264, pts_, 12.5, 19, cw - 6, gap=8)

# 8 ---------------------------------------------------------------- contact
p = slide(dark=True)
text(p, M - 2, 250, 'Contact us', 'L', 52, C['white'])
text(p, M, 292, 'Elevatus', 'S', 16, C['white'])
text(p, M, 318, 'elevatus.io', 'R', 16, C['white'])

doc.subset_fonts()
doc.save(OUT, garbage=4, deflate=True)
print(len(doc), 'slides ->', OUT)

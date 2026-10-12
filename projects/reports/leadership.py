# Leadership Style sample report, Elevatus edition.
# Same content and the same elements as the source report: nothing added, only restyled. The cover is the Elevatus cover template.
import sys, math, os
from lib import *

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUTPUT, 'Elevatus - Leadership Style Sample Report.pdf')
R = Report('Layla Mansour', 'Apr 30 2026', 'Leadership Style', '2026', 'Elevatus - Leadership Style Sample Report')

STYLES = [('Transformational', 82), ('Democratic', 92), ('Laissez Faire', 74), ('Servant', 82), ('Transactional', 87), ('Autocratic', 75)]

def level(v): return 'High' if v > 80 else ('Moderate' if v > 50 else 'Low')
LEVEL_COLOR = {'High': C['vivid'], 'Moderate': C['s400'], 'Low': C['apricot_ink']}

def radar(p, c, rad):
    n = len(STYLES)
    def pt(i, v): t = math.radians(-90 + i * 360 / n); return (c[0] + rad * v / 100 * math.cos(t), c[1] + rad * v / 100 * math.sin(t))
    for k in range(10, 101, 10): circle(p, c, rad * k / 100, color=C['line'], width=0.6)
    for i in range(n): line(p, c, pt(i, 100), C['line'], 0.6)
    pts = [pt(i, v) for i, (_, v) in enumerate(STYLES)]
    poly(p, pts, fill=C['vivid'], color=C['vivid'], width=1.8, opacity=0.12, stroke_opacity=1)
    for q in pts: circle(p, q, 2.8, fill=C['vivid'], color=C['white'], width=1.2)
    for k in range(10, 101, 10):
        t = math.radians(-60); rr = rad * k / 100
        text(p, c[0] + rr * math.cos(t), c[1] + rr * math.sin(t) - 1.5, str(k), 'R', 5, C['slate'], 'center')
    for i, (name, v) in enumerate(STYLES):
        q = pt(i, 114)
        al = 'center' if i in (0, 3) else ('left' if i in (1, 2) else 'right')
        dy = -4 if i == 0 else (12 if i == 3 else 3)
        s1 = f'{name} {v}%'
        text(p, q[0], q[1] + dy, s1, 'R', 9.5, C['ink'], al)

# ================================================================ first page
R.h2('In this Report:', size=13)
R.space(2)
R.bullets(['Introduction: Leadership Style', 'Theories of Leadership Style', 'How to read the report',
           'Executive Summary of Your Leadership Style', 'Leadership style and insights',
           'Description of the Leadership Style', 'Disclaimer'], size=10, after=22)

# ================================================================ introduction
R.h1('Introduction: Leadership Style')
R.para("Leadership is the art of motivating a group of people toward achieving a common goal. It requires a unique blend of traits, skills, and personal style. Your leadership style, which is how you communicate with, motivate, and manage your team, significantly impacts the effectiveness, productivity, and environment of your work. Recognizing and understanding your leadership style is crucial for personal development and organizational success.")
R.para("The concept of leadership style has evolved over the years, leading to the development of various theories that provide insight into different leadership dimensions. These styles range from more directive approaches that prioritize decision-making and control, to more inclusive forms that value collaboration and team input. Each style has its strengths and areas for improvement, affecting team dynamics, job satisfaction, and performance outcomes differently.")
R.para("This report dives into your individual leadership style, offering insights into how your unique traits align with broader leadership theories. It's designed to help you understand your innate leadership qualities, how you can leverage these in your professional journey, and areas where you might consider further development. By the end of this report, you'll have a clearer picture of your leadership style, equipped with the knowledge to harness your strengths and address areas for growth.")
R.space(12)
R.h1('Theories of Leadership Style')
R.para("Leadership theories have been developed to explain the impact of leadership styles on team performance and organizational success. These theories include:")
R.bullets(["**Trait Theory:** Suggests that effective leaders possess a certain set of traits or characteristics that distinguish them from non-leaders.",
           "**Behavioral Theory:** Focuses on the behaviors of leaders and categorizes them into styles such as democratic, autocratic, and laissez-faire.",
           "**Situational Leadership:** Proposes that the most effective leadership style varies depending on the situation and the development level of the followers.",
           "**Transformational and Transactional Leadership:** Transactional leadership is based on a system of rewards and punishments, while transformational leadership inspires followers to transcend their own self-interests for the good of the group or organization."])
R.para("Understanding these theories provides a framework for analyzing your leadership style and offers insights into how you can adapt and thrive in various contexts.")

# ================================================================ how to read
R.space(12)
R.h1('How to Read the Report')
R.para("This report is structured to give you a comprehensive analysis of your leadership style. Here's how to navigate it:")
R.bullets(["**Executive Summary of Your Leadership Style:** A high-level overview of your dominant leadership style and key traits.",
           "**Your Leadership Style and Insights:** Detailed insights into how your leadership style plays out in practical scenarios, including strengths and potential areas for growth.",
           "**Description of the Leadership Style:** An in-depth look at the characteristics of your primary leadership style and how it compares to other styles.",
           "**Disclaimer** Important information regarding the interpretation and use of the findings in this report."])
R.para("Read through each section to gain a full understanding of your leadership profile and how you can apply these insights in your professional journey.")

# ================================================================ executive summary
R.new_page()
R.h1('Executive Summary of Your Leadership Style')
R.para("Your leadership style embodies the unique way you inspire and guide your team toward achieving their goals. This report synthesizes your responses to provide a snapshot of your dominant leadership traits, offering a window into your natural inclinations as a leader. Whether you lean towards a transformational approach, inspiring innovation and growth, or favor a more transactional method, focusing on structure and results, this summary will highlight your foundational leadership qualities.")
panel = fitz.Rect(MX, R.y + 6, W - MX, R.y + 6 + 300)
rrect(R.p, panel, 12, fill=C['paper'])
radar(R.p, (W / 2, panel.y0 + 150), 104)
R.y = panel.y1 + 22
R.h2('Norms for Score Range (%)', size=11)
R.space(2)
def lv_draw(p, x, y, w, v, h): text(p, x, y + 9.9, v, 'M', 9, LEVEL_COLOR[v])
def lv_h(v, w): return 15
R.table([110, 90, CW - 200], ['Score Range (%)', 'Levels', 'Description'],
        [['81-100', 'High', 'Reflects a strong presence or preference for that leadership style or trait.'],
         ['51-80', 'Moderate', 'Indicates a balanced or occasional demonstration of the leadership style or trait.'],
         ['0-50', 'Low', 'Suggests minimal alignment with or use of the specific leadership style or trait.']],
        renderers={1: (lv_draw, lv_h)}, size=9)

# ================================================================ style sections
def style(name, pct, interp, traits, recs, tips):
    R.ensure(300)  # heading, interpretation and table stay together
    R.h2(f'{name}: {pct}%', size=15)
    R.h3('Interpretation:')
    R.para(interp, size=9.8, lead=14.8, after=10)
    R.table([128, 62, CW - 190], ['Traits', 'Score in %', 'Interpretation'], [[a, str(b), c] for a, b, c in traits], pad=(9, 6.5))
    R.space(14)
    R.h3('Recommendations:')
    R.bullets(recs, size=9, lead=13.4, gap=3, after=10)
    R.h3('Tips!:')
    R.bullets(tips, size=9, lead=13.4, gap=3, after=24)

R.new_page()
R.h1('Leadership Style and Insights', size=19)
R.para("In this section, we delve into the nuances of your leadership style, providing specific examples of how your traits manifest in your interactions with your team and decision-making processes. We'll explore the strengths that you bring to the table, such as your ability to motivate others, foster a positive work environment, or drive efficiency and discipline toward achieving objectives. Additionally, we'll identify areas where you might consider further development to enhance your leadership effectiveness and adaptability.", color=C['slate'], after=16)

style('Transformational', '81.5',
      "You are exceptional at inspiring your team and driving innovation. You thrive in dynamic environments and excel at encouraging creativity and growth in your team members. Continue to inspire your team by setting clear, ambitious goals that align with your vision.",
      [['Intellectual Stimulation', 100, 'You thrive on fostering innovation, encouraging your team to think creatively and challenge the status quo.'],
       ['Idealized Influence', 93, 'You build a foundation of trust and admiration within your team through your integrity and ability to act as a role model.'],
       ['Individualized Consideration', 73, 'You provide support, yet further tailoring your approach to individual needs could strengthen your leadership.'],
       ['Inspiration and Vision', 60, 'You show promise in inspiring others, and with a bit more effort to make your vision even more compelling, you could really motivate your team.']],
      ['Embrace new challenges with enthusiasm, seeing them as opportunities to grow.',
       'Become a mentor; your experience can guide future leaders.',
       'Cherish feedback as a tool for continuous improvement and a way to refine your transformative impact.'],
      ["Develop a vision that resonates with your team's goals and frequently share this to inspire and motivate them.",
       'Promote innovation by encouraging your team to challenge usual ways and come up with creative solutions.',
       "Take time to understand each team member's strengths and help them realize their potential."])

style('Democratic', '91.5',
      "You are excellent at involving your team in decision-making, which boosts innovation and engagement. Continue fostering a participative culture by regularly soliciting and acting on team feedback.",
      [['Collaborative Communication', 93, 'You excel in creating an atmosphere of open dialogue, where transparent communication builds trust and encourages collaboration.'],
       ['Empowerment and Trust', 93, 'You empower your team and instill a strong sense of ownership over their work, fostering independence.'],
       ['Participative Decision Making', 93, 'You shine in creating a collaborative environment where every voice is valued in decision-making processes.'],
       ['Consensus', 87, 'You adeptly navigate diverse opinions to build consensus, ensuring decisions are supported and enacted by the whole team.']],
      ['Prioritize creating spaces for team input, making decision-making a shared journey.',
       'Enhance your facilitation skills to navigate through diverse viewpoints effectively.',
       'Delegate tasks creatively, turning ownership into empowerment.'],
      ['Regularly ask for your team’s input on decisions and strategy, fostering an inclusive environment.',
       'Lead open discussions to consider different viewpoints and reach a group consensus.',
       'Enhance engagement and ownership among team members by letting them participate in decision-making.'])

style('Laissez Faire', '73.5',
      "You are comfortable with granting autonomy but could be more consistent. Establish clear guidelines for when and how team members should operate independently.",
      [['Flexibility', 93, 'Your flexible leadership approach allows team members to tackle tasks in ways that best suit their strengths and creativity.'],
       ['Resource Provision', 87, 'You ensure your team has all the resources they need, letting them work efficiently and independently.'],
       ['Trust and Minimal Supervision', 87, "Your trust in your team's capabilities allows them to work independently, fostering innovation and self-direction."],
       ['Autonomy and Independence', 27, 'You could stimulate creativity and independent problem-solving by increasing the autonomy you grant your team.']],
      ['Reevaluate the balance between autonomy and guidance in your leadership style.',
       'Consider situations or projects where a slightly more hands-on approach could benefit your team.',
       'Foster a culture of independence while ensuring that goals and expectations are clearly communicated and understood.'],
      ['Make sure your team is well-equipped and informed before you step back.',
       'Set clear goals and define the boundaries within which they have the freedom to operate.',
       'Keep communication lines open for support and guidance, ensuring they feel supported even with a hands-off approach.'])

style('Servant', '81.75',
      "You excel at supporting and empowering your team, focusing on their well-being and success. Continue to prioritize team development and consider implementing regular wellness checks.",
      [['Empathy and Listening', 93, 'You create a supportive and understanding environment through your empathetic approach and active listening skills.'],
       ['Humility', 87, 'Your humble approach fosters an open, learning-focused environment that encourages innovation and free idea exchange.'],
       ['Stewardship', 87, "You take responsibility for your team's welfare, fostering a deeply committed and loyal group."],
       ['Community Building', 60, 'Strengthening your community-building efforts could create a more unified team environment.']],
      ['Deepen your commitment to serving your team by regularly checking in on their aspirations and challenges.',
       'Lead by example, demonstrating the core values of empathy, listening, and support in every interaction.',
       'Foster a culture where the growth and success of each team member are celebrated as collective victories.'],
      ['Listen actively to what your team needs and respond with empathy.',
       'Set an example of service and support in every action you take.',
       'Help your team grow by providing the resources and opportunities they need to advance their skills and careers.'])

style('Transactional', '86.75',
      "You excel in structured environments and are skilled at using rewards and clear rules to achieve team goals. Maintain your structured approach but also remember to celebrate team successes to boost morale.",
      [['Contingent Reward', 93, 'You masterfully use rewards and recognition to motivate and reinforce desired outcomes, significantly impacting team performance.'],
       ['Management by Exception (Passive)', 87, 'You effectively intervene when necessary, maintaining performance standards without micromanaging.'],
       ['Noninterference', 87, 'You successfully grant your team the autonomy they need to innovate, demonstrating trust in their expertise and abilities.'],
       ['Management by Exception (Active)', 80, 'You address performance issues effectively but enhancing your proactive measures could prevent future problems.']],
      ['Tailor rewards to fit the unique drivers of each team member.',
       'Strive for a harmony between achieving targets and nurturing a thriving team atmosphere.',
       'Experiment with innovative reward systems to keep motivation high.'],
      ["Clearly outline what you expect from the team, what they will receive when they meet these expectations, and the consequences if they don't.",
       'Use clear metrics to give feedback and reward achievements promptly.',
       'Ensure you recognize both team results and individual efforts to foster a balanced work environment.'])

style('Autocratic', '75.25',
      "You can switch between decisive and open leadership styles. Leverage this adaptability by assessing situations more clearly to determine when to be more authoritative.",
      [['Immediate Decision', 87, 'You ensure swift action and effective resolution of challenges with your decisiveness in critical situations.'],
       ['Limited Empowerment', 87, 'Your close oversight ensures adherence to processes and quality, which is crucial in highly regulated environments.'],
       ['Clear Expectations', 67, "While your expectations are beneficial, more precise communication could lift your team's performance even higher."],
       ['Directive Control', 60, 'While you provide effective direction, considering more input from your team could enhance engagement and results.']],
      ['Identify situations where adopting a more collaborative approach could yield richer insights.',
       'Develop a nuanced understanding of when to assert authority and when to invite collaboration, blending the best of autocratic and democratic styles',
       'Practice transparency to build trust even when decisions are made unilaterally.'],
      ["Make informed decisions quickly but ensure you're aware of the team's needs and contexts.",
       'Explain your decisions to your team to help them understand and accept them better.',
       'Identify when to involve the team in decisions more collaboratively to improve team dynamics.'])

# ================================================================ description
R.new_page()
R.h1('Description of the Leadership Style')
R.para("Here, we offer a comprehensive description of your identified leadership style, drawing on the theoretical frameworks mentioned earlier. You'll learn about the core principles that underpin your style, how they influence your behavior and decisions, and their impact on team dynamics and performance. This section aims to provide a deeper understanding of your leadership approach and how it aligns with broader leadership models.", after=14)
def type_draw(p, x, y, w, v, h): text(p, x, y + 10, v, 'S', 9.2, C['logo'])
def type_h(v, w): return 14
R.table([112, CW - 112], ['Personality Type', 'Score Interpretation'],
        [['Transformational', "**Seek leaders who ignite change and inspire innovation.** Transformational leaders are visionaries, capable of steering teams toward groundbreaking achievements by fostering a shared vision and challenging the status quo. They excel in dynamic environments, driving growth and encouraging creativity, making them ideal for roles that require adaptability and a forward-thinking approach."],
         ['Transactional', "**Target individuals who prioritize order, structure, and clear outcomes.** Transactional leaders focus on achieving set objectives through a systematic approach of rewards and penalties. They thrive in established, process-driven settings where performance and results are closely monitored. This leadership style is pivotal for roles needing consistent execution and a high degree of reliability."],
         ['Democratic', "**Look for leaders who value collaboration, inclusivity, and team empowerment.** Democratic leaders facilitate open dialogue, ensure team participation in decision-making, and build consensus. They are best suited for roles that demand innovation and collective problem-solving, as they create environments where every voice is heard and valued. Their approach encourages team cohesion and engagement, essential for creative and flexible work cultures."],
         ['Autocratic', "**Ideal for situations requiring decisive action and strong direction.** Autocratic leaders make quick decisions with minimal consultation. They provide clear expectations and closely supervise their teams, ensuring efficient task completion. This style is effective in high-pressure environments or when working with less experienced teams needing guidance."],
         ['Servant', "**Servant leaders put their team's needs first, focusing on growth, well-being, and empowering others to succeed.** They excel in roles that require building strong community bonds, fostering an inclusive culture, and enhancing team performance through support and mentorship. This leadership is valuable in environments where trust, collaboration, and long-term development are prioritized."],
         ['Laissez-faire', "**Best for roles where innovation, creativity, and autonomy are paramount.** Laissez-faire leaders offer freedom and trust to their teams to explore and solve problems independently. This hands-off approach is effective in highly skilled environments where individuals are motivated and self-directed. It encourages ownership and accountability, making it ideal for creative industries or research-driven fields."]],
        renderers={0: (type_draw, type_h)}, size=8.7, lead=12.6, pad=(9, 7), color=C['slate'])

# ================================================================ disclaimer
R.new_page()
R.h1('Disclaimer')
for s in ["This leadership assessment report is designed as a developmental tool to aid in your understanding and growth as a leader. The insights provided are derived from your responses to the assessment and are intended to highlight predominant leadership styles and potential areas for improvement. It is important to consider these insights within the broader context of your personal experiences, professional environment, and the specific dynamics of your team.",
          "The interpretations and recommendations made in this report are suggestions based on established leadership theories and practices. They should not be viewed as definitive judgments of your capabilities or potential. Leadership effectiveness varies widely depending on numerous factors, including organizational culture, team composition, and situational challenges. As such, the effectiveness of different leadership styles can fluctuate in different settings.",
          "We encourage you to use this report as a starting point for reflection and discussion, rather than as a conclusive assessment. Leadership development is a continuous process, and growth comes from a willingness to learn, adapt, and apply new strategies in practice. Consider seeking feedback from peers, mentors, and team members to gain a fuller understanding of your leadership impact and areas for growth.",
          "Additionally, while this report aims to provide valuable insights into your leadership style, it is by no means exhaustive. Other aspects of leadership, such as emotional intelligence, strategic thinking, and resilience, also play critical roles in effective leadership but may not be fully captured within the scope of this assessment.",
          "Lastly, the confidentiality of your responses and the results of this assessment is of utmost importance. This report is intended for your personal use, and any sharing or discussion of its contents should be done at your discretion and with consideration for the privacy and respect of all individuals involved."]:
    R.para(s, lead=16, after=10)

R.cover('Leadership Style', 'A clear view of leadership style across six dimensions: Transformational, Democratic, Laissez-Faire, Servant, Transactional and Autocratic.',
        'Leadership\nAssessment', 'Sample Report')
print(R.save(OUT), 'pages ->', OUT)

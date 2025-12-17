A playbook for designing analytics dashboards that are trustworthy, instantly understandable, and visually elegant—from first sketch to partner‑ready polish.
1 · Design Philosophy
Purpose before pixels – Every view must answer a concrete business question. If you cannot finish the sentence “Stakeholders will use this view to ____,” rethink or remove it. 

Cognitive efficiency – maximize the information‑to‑ink ratio; delete anything that does not carry meaning (gridlines, drop‑shadows, decorative icons). This principle stems from Edward Tufte’s concept of chartjunk.

Hierarchical scanning – Position the most critical information in the upper‑left (Western F‑pattern) and give it visual dominance. Stakeholders decide within seconds whether to engage further.

Context + comparison – Numbers rarely speak on their own. Provide baselines, targets, or previous periods so users know whether the result is good or bad. BANs should ship with context (e.g., Δ vs LY).

Accessible, brand‑consistent aesthetics – Use a restrained, high‑contrast color palette and prefer shades of a single hue over many hues.

Text as a design element – Descriptive titles/subtitles, embedded color legends, on‑chart annotations, and micro‑copy that instruct users dramatically improve comprehension.

Important: Engage with the dashboard from the user's perspective – the tool user – not just as the developer –  the tool builder. Consider the key performance indicators (KPIs) relevant to this domain: What were the activity levels and volumes last week? How does this month compare to the previous one? Identify recent trends and changes, and understand the main drivers behind them. A well-designed dashboard should not only help users find answers to these essential business questions but also present insights in a way that is easily digestible and enjoyable to explore. 

Read this great blog that goes deeper into the difference between “Builder” vs “Enabler” mindset/approach  One Perspective That Separates Good BI Developers from Great Ones
 

image-20250912-213310.png
 

image-20250912-224322.png
2 · Process Workflow
Stage

Key Actions

Deliverables

Discover & Define

– Identify decision‑makers, their data literacy, and the core metrics/questions.

– Translate questions into concrete KPIs and user stories.

Documentation / developer understanding: 

audience / user personae

business processes / decisions being supported

list of metrics & attributes

Model & Validate

– Build metrics in dbt as fully tested, documented models.

– Profile source tables; reconcile totals against trusted systems.

Certified dataset (all dbt tests green)

(For some projects, esp. Apple) Wireframe & Prototype

– Sketch a two‑ or three‑row layout using style‑guide templates.

– Place BANs on the top row, trends in the middle, and drill‑downs at the bottom; decide required interactions. Socialize with requester / business partner for feedback. 

Low‑fidelity mock‑up (Miro, Confluence canvas, Tableau)

Develop 

– Build dashboard, making sure to periodically interact with it from the stakeholder perspective, make the UX improvements you’d want. 

Dashboard Draft / V1

Internal QA & Peer Review

– Run metric accuracy checks and cross‑filter sanity tests.

– Submit screenshots to Claude Sonnet (latest model number) in Github Copilot for feedback & recommendations

- Ask a non‑author teammate to interpret each view aloud—listen for confusion. Text boxes with guidance may be necessary.

QA checklist completed 

Stakeholder Feedback

– Share internally first; gather written feedback on relevance and usability.

– Iterate until all feedback is incorporated

Revised Draft / V2

External‑Ready

– Apply final formatting and accessibility passes.

– Publish to Tableau Cloud or MicroStrategy, test the “viewer” experience (Tableau: publish only dashboard pages, exclude the many worksheet tabs. Microstrategy: view in “presentation” mode)

– Appropriate security measures applied (row level security in Tableau)

Release notes & published URL

Data refresh job scheduled, confirmed working without error

Ship

– Share with external stakeholder!

Email url to stakeholder(s), including brief summary and invitation to hold a walkthrough call. 

3 · Visual & Interaction Design Requirements 
3.1 Layout & Hierarchy
Follow the two‑ or three‑row pattern—

BANs across the top for most dashboards (columnar to one side in some cases)

The key trends in the centre

Supporting distributions or details below.

This is a very typical pattern but not the only one. Go deeper into dashboard design patterns at https://dashboarddesignpatterns.github.io/patterns.html 

Maintain generous white‑space gutters (≥ 16 px) to avoid visual crowding.

3.2 Key Numbers (BANs)
Place KPI boxes on the top row of the screen (again, sometimes vertical on one side will better serve in some cases). 

Pair each BAN with either (a) Δ vs target, (b) Δ vs prior period, or (c) a spark‑line; aim for a three‑second read.

Detailed guides/examples: https://nastengraph.substack.com/p/anatomy-of-the-kpi-card
https://www.datarevelations.com/bans/ 

3.3 Chart & Table Patterns
Match chart type to question: line → trend, bar → ranking, heat‑map → part‑to‑whole. FT Visual Vocabulary

Generally numeric data labels should go directly on the series

For combo charts, be thoughtful & deliberate with series shape. Eg quantity should be a bar, a % rate should be a line

Detailed guides & examples:   

https://nastengraph.substack.com/p/dataviz-101-key-principles-for-crafting
|https://nastengraph.substack.com/p/bar-charts-best-practices
|https://nastengraph.substack.com/p/line-charts-best-practices
 

Optional: create a heat‑map legend into a filter beside its chart; hide the default legend to reclaim space.

Tables: use compact cell padding, banded rows, and collapsible subtotals.

3.1  Illustration:

Source: https://www.kickstarter.com/projects/643038322/dashboard-wireframe-kit-2nd-edition 

3.4 Numbers, Units & Axes
Apply number abbreviations for count/amount thousands (K), millions (M), and billions (B) 

Remove redundant axis titles (e.g., remove date axis label “Date” ).

Any axis labels should be easily readable, not truncated; clean up default derived metric/attribute names if they contain calculations 

3.5 Color & Typography
Set global font to Tableau/Arial 10 pt; section titles 14 pt bold; BAN digits 32 pt. (we should verify our standard)

Use color thoughtfully / deliberately, to aid viewer understanding. See bar chart example to the right; see more at link https://nastengraph.substack.com/p/bar-charts-best-practices
 

Additional helpful points here:   https://nastengraph.substack.com/p/dataviz-101-key-principles-for-crafting
 

3.6 Interaction & Performance
Keep essential filters visible; hide chapter‑level filters that partner users will not see. 

Test interactivity to see if the views are useful and valuable. Read and interpret the chart for yourself! 

Do the values make sense, or do they need renaming or grouping? 

If a spaghetti graph appears, due to an attribute with many values, apply some intuitive binning / categorization that reduces the number of lines on the chart. For example, breaking out spend volume by merchants should display Top 10 - 20 and group the rest into “All Other”. 

Design at the final device size to control the UX / UI 

Performance: 

https://nastengraph.substack.com/p/how-to-increase-dashboard-performance
 

Designing Efficient Production Dashboards

3.5 Illustration: use of color for distributions

4 · Quality‑Gate Checklists 
Open to suggestions / adjustments – not a locked-down list. 

A. Self-QA: ready for peer review
Layout follows the two‑/three‑row template; 

BANs (Big Ass Numbers/KPI boxes) emphasized & contextualized

Data labels directly on plot points for faster comprehension

Dashboard reflects design choices of the tool user and/or business stakeholder, eg: 

Attributes with many values binned in a helpful, intuitive way

KPIs reconcile with established reporting in prod / data sourced from tested + validated dbt models. 

B. Team QA: shippable to stakeholder
Descriptive titles, user-friendly field names and labels. No raw SQL field names or Tableau-generated derived metric names. Clean, readable, (preferably non-truncated) text in axes and elsewhere. 

Number formats consistent and match style guide 

Cleansed of Chartjunk: gridlines, labels, titles (etc etc) not actively aiding viewers' comprehension is removed.  

Filters, tooltips, and actions tested: interactions don’t create hard-to-read views. Instructions for interactivity added if necessary. 

dbt health tile & exposure configured; indicators all green, last refresh date displayed

Metric definitions available, dedicated tab or in tool tip

BI team member signs off on data accuracy and visual QA

C. Ongoing, post-launch updates informed by customer feedback 

Tooltips Summarize takeaway / insight in one sentence

Goes beyond weather reporting and actually surfaces insights about trends & drivers

Performance: initial load < 10s; interaction latency < 4s.

Potentially: Tableau Pulse KPIs configured? 

 

Inspired by Spotify’s “spicy dashboard” checklist https://storage.googleapis.com/production-eng/1/2024/08/EN221-Viz-Dashboard-Checklist-fillable.pdf

Comprehensive Guides: 

https://uxplanet.org/10-rules-for-better-dashboard-design-ef68189d734c 

https://dataschool.com/how-to-design-a-dashboard/dashboard-design-process/ 
https://uxdesign.cc/over-complicated-over-simplified-the-ux-efficient-frontier-561d7773bc6b 
https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards 

---- 

TABLEAU EXTENDED RESOURCES: 

Visual Style Best Practice:

Use descriptive titles

Data labels: place data points directly on charts – bar charts always, line chart depends on the story https://www.tableau.com/solutions/gallery/visual-vocabulary 

Format count and amount numbers using abbreviations such as K, M, and B [add source].

Include KPI boxes (referred to as BANs - Big Ass Numbers) in the top row for immediate understanding of scale.

Consult https://greendot.atlassian.net/wiki/spaces/BIA/pages/1075611076/Dashboard+Development+Playbook?atlOrigin=eyJpIjoiODE4MjMxN2I4M2NhNGE1ZmI1MGQzNjIwNWI2NzNlYmUiLCJwIjoiYyJ9 for full style guide

Functionality best practice:

Configure dbt “exposure” to recognize the tableau dashboard that the dbt pipeline powers

Add dbt health tile to dashboard

Ensure YML data definitions are populated in the Tableau Data Catalogue.

Display data pipeline health tiles on the dashboard.

DBT <> Tableau integration 

https://cloudydata.substack.com/p/tableau-and-dbt-governed-self-service

https://greendot.atlassian.net/wiki/spaces/BIA/pages/1111261658/Tableau+DBT+Data+Exchange?atlOrigin=eyJpIjoiMzQ3MDI0ZDNhYmM5NDA1N2JmODk0MTNlNjdjYjQ5YmYiLCJwIjoiYyJ9

Key Challenges/Questions to Consider:

Properly structure data and Tableau dashboards for both internal and external use. Is it feasible for one dashboard to serve both audiences with appropriate row and column security? Alternatively, should there be a dedicated internal dashboard featuring all-partner views, alongside an external dashboard tailored for displaying a single partner's data?

`

Resources

Tableau Training & Reference Docs

Trailhead Academy: Learn Tableau

https://www.tableau.com/learn/training

https://exchange.tableau.com/?reg-delay=true

https://help.tableau.com/current/pro/desktop/en-us/visual_best_practices.htm

https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm 

https://www.tableau.com/blog/tableau-iron-viz-winners

Data storytelling - concrete examples: 

https://nastengraph.substack.com/p/5-behaviors-that-kill-your-bi-credibility 

https://www.storytellingwithdata.com/blog/from-dashboard-to-story 
https://www.storytellingwithdata.com/blog/a-multi-level-makeover-simplifying-a-shrinkage-report 

More walkthroughs/demonstrations : https://www.storytellingwithdata.com/blog

Charts

https://nastengraph.substack.com/p/bar-charts-best-practices

https://nastengraph.substack.com/p/pie-charts-best-practices 

https://nastengraph.substack.com/p/dataviz-101-key-principles-for-crafting

https://nastengraph.substack.com/p/line-charts-best-practices 

How to Deal with Spaghetti Line Charts [Tableau Public]

https://www.storytellingwithdata.com/chart-guide 

FT Visual Vocabulary

KPI Boxes (BANs)

https://www.datarevelations.com/bans/ 

https://nastengraph.substack.com/p/anatomy-of-the-kpi-card 

https://public.tableau.com/app/profile/gbolahan.adebayo/viz/20waystodesignyourKPIs/Dashboard1



Colors

https://nastengraph.substack.com/p/guide-to-color-tools

https://www.datawrapper.de/blog/colors-for-data-vis-style-guides 

Even More – great visualization blogs 

https://www.flerlagetwins.com/p/tableau-essential-reading.html 
https://nightingaledvs.com/ 5

https://www.storytellingwithdata.com/makeovers

https://www.flerlagetwins.com/



Competitor Tools: 

https://www.thoughtspot.com/product/visualize

Books 

Data Visualization resources in Sharepoint – pdfs of great data viz design books, including classics from Edward Tufte and Alberto Cairo 



Videos 

https://youtu.be/f_CT-_YjUoE?si=7yBevOTOIDZ7JuUG

https://www.youtube.com/watch?v=RyWxEver8hg

https://www.youtube.com/watch?v=dnP12MtfCZU



Social

https://www.reddit.com/r/tableau/

 

Dashboard Documentation 

https://medium.com/@katerina.protivenskiy/tired-of-documenting-tableau-dashboards-these-4-tools-make-it-easier-e1ec07de56be

https://nastengraph.substack.com/p/how-to-write-dashboard-documentation

https://docs.google.com/presentation/d/1EFgl1ckByFPN-fkGpdF4wLErfBaBaHAh/edit?slide=id.p1#slide=id.p1

https://www.linkedin.com/posts/prasannprem_the-ultimate-cheatsheet-for-naming-calculated-activity-7325361188664410112-QQ5l?utm_source=share&utm_medium=member_ios&rcm=ACoAAAfI7F0BV6DMqqbXw0eiX03KPCG4tB942Pk



Advanced Tableau topics 

https://www.embedtableau.com/start/how

https://www.tableau.com/blog/visual-analytics-tableau-viz-extensions

https://www.tableau.com/data-culture



Even more tips & guides 

https://www.flerlagetwins.com/p/tableau-essential-reading.html 

Tableau's Hidden Functions (interactive report)





 Resources – recategorized

Tableau Training & Reference Docs

Trailhead Academy: Learn Tableau: Dive into an extensive platform designed to elevate your Tableau skills with structured learning paths and hands-on projects. Trailhead Academy: Learn Tableau

Tableau Training: Explore a variety of training materials and courses tailored to enhance your understanding and application of Tableau. https://www.tableau.com/learn/training

Tableau Exchange: Discover a vibrant community where users share valuable Tableau resources, fostering collaboration and innovation. https://exchange.tableau.com/?reg-delay=true

Visual Best Practices: Learn essential guidelines to create effective visualizations that communicate data insights clearly and effectively. https://help.tableau.com/current/pro/desktop/en-us/visual_best_practices.htm

Dashboards Best Practices: Gain insights into crafting dashboards that not only look good but also drive actionable insights for your audience. https://help.tableau.com/current/pro/desktop/en-us/dashboards_best_practices.htm

Iron Viz Winners: Get inspired by the creativity and innovation showcased by winners of Tableau's prestigious Iron Viz competition. https://www.tableau.com/blog/tableau-iron-viz-winners

Data Storytelling - Concrete Examples

BI Credibility: Understand the critical behaviors that can undermine your business intelligence efforts and how to maintain credibility. https://nastengraph.substack.com/p/5-behaviors-that-kill-your-bi-credibility

From Dashboard to Story: Transform your dashboards into engaging narratives that resonate with your audience and drive decision-making. https://www.storytellingwithdata.com/blog/from-dashboard-to-story

Simplifying Reports: Discover a case study that illustrates the power of simplifying complex reports for better comprehension and impact. https://www.storytellingwithdata.com/blog/a-multi-level-makeover-simplifying-a-shrinkage-report

Walkthroughs and Demonstrations: Access a wealth of resources that provide practical insights into mastering data storytelling techniques. https://www.storytellingwithdata.com/blog

Charts

Bar Charts Best Practices: Uncover the key principles that make bar charts effective tools for data presentation and analysis. https://nastengraph.substack.com/p/bar-charts-best-practices

Pie Charts Best Practices: Learn how to craft informative pie charts that effectively convey proportions and comparisons in your data. https://nastengraph.substack.com/p/pie-charts-best-practices

Data Visualization Principles: Familiarize yourself with the foundational principles that guide the creation of impactful visualizations. https://nastengraph.substack.com/p/dataviz-101-key-principles-for-crafting

Line Charts Best Practices: Discover best practices for designing line charts that clearly illustrate trends and changes over time. https://nastengraph.substack.com/p/line-charts-best-practices

Spaghetti Line Charts: Learn strategies for effectively managing and interpreting complex line charts that can overwhelm viewers. How to Deal with Spaghetti Line Charts [Tableau Public]

Chart Guide: Access a comprehensive resource that outlines various chart types and their appropriate applications in data visualization. https://www.storytellingwithdata.com/chart-guide

FT Visual Vocabulary: Enhance your understanding of visual vocabulary and its importance in effective data communication. FT Visual Vocabulary

KPI Boxes (BANs)

KPI Boxes Overview: Gain insights into the fundamental concepts of KPI boxes and their role in performance tracking. https://www.datarevelations.com/bans/

Anatomy of the KPI Card: Explore the essential elements that contribute to the design of effective KPI cards for data presentation. https://nastengraph.substack.com/p/anatomy-of-the-kpi-card

Colors

Guide to Color Tools: Discover useful resources for selecting color schemes that enhance the clarity and appeal of your visualizations. https://nastengraph.substack.com/p/guide-to-color-tools

Colors for Data Visualization Style Guides: Learn best practices for utilizing color in data visualizations to ensure consistency and effectiveness. https://www.datawrapper.de/blog/colors-for-data-vis-style-guides

Even More – Great Visualization Blogs

Essential Reading for Tableau: Explore a curated list of vital resources that every Tableau user should consider for their learning journey. https://www.flerlagetwins.com/p/tableau-essential-reading.html

Nightingale Data Visualization: Engage with a blog dedicated to the art and science of data visualization, offering fresh insights and perspectives. https://nightingaledvs.com/

Makeovers in Data Storytelling: View compelling examples of how data storytelling can be transformed for greater impact and clarity. https://www.storytellingwithdata.com/makeovers

Flerlage Twins Blog: Access a wealth of insights and tips that can enhance your data visualization skills and knowledge. https://www.flerlagetwins.com/

Competitor Tools

ThoughtSpot Visualization: Learn about the innovative visualization capabilities offered by ThoughtSpot and how they can enhance data analysis. https://www.thoughtspot.com/product/visualize

Books

Data Visualization Resources: Find a collection of highly recommended books that can deepen your understanding of data visualization design principles. Data Visualization

Videos

Data Visualization Videos: Access a selection of informative videos that provide valuable insights into the world of data visualization. Video 1 Video 2 Video 3

Social

Tableau Community on Reddit: Join the conversation and engage with fellow Tableau enthusiasts in an active online community. https://www.reddit.com/r/tableau/

Dashboard Documentation

Documenting Tableau Dashboards: Discover tools and tips that simplify the process of documenting your Tableau dashboards effectively. https://medium.com/@katerina.protivenskiy/tired-of-documenting-tableau-dashboards-these-4-tools-make-it-easier-e1ec07de56be

How to Write Dashboard Documentation: Get guidance on crafting clear and effective documentation for your dashboards. https://nastengraph.substack.com/p/how-to-write-dashboard-documentation

Dashboard Documentation Presentation: View a presentation that outlines best practices for documenting dashboards effectively. https://docs.google.com/presentation/d/1EFgl1ckByFPN-fkGpdF4wLErfBaBaHAh/edit?slide=id.p1#slide=id.p1

Cheatsheet for Naming Calculated Fields: Access a handy cheatsheet that provides naming conventions for calculated fields in Tableau. https://www.linkedin.com/posts/prasannprem_the-ultimate-cheatsheet-for-naming-calculated-activity-7325361188664410112-QQ5l?utm_source=share&utm_medium=member_ios&rcm=ACoAAAfI7F0BV6DMqqbXw0eiX03KPCG4tB942Pk

Advanced Tableau Topics

Getting Started with Tableau: Find resources tailored for advanced users looking to deepen their Tableau expertise. https://www.embedtableau.com/start/how

Visual Analytics with Tableau Extensions: Explore the enhanced visual analytics capabilities that Tableau extensions offer for deeper insights. https://www.tableau.com/blog/visual-analytics-tableau-viz-extensions

Building a Data Culture: Learn how to foster a data-driven culture within your organization for better decision-making. https://www.tableau.com/data-culture

Even More Tips & Guides

Tableau Essential Reading: Discover additional resources that are essential for anyone looking to excel with Tableau. https://www.flerlagetwins.com/p/tableau-essential-reading.html

Hidden Functions in Tableau: Engage with an interactive report that uncovers the lesser-known functions of Tableau for advanced users. Tableau's Hidden Functions (interactive report)

--- A BLOG POST: 

There is a wealth of incredible dashboards, visualizations published on tableau public. 
I’m super impressed by it. It really showcases the flexibility and sophistication that sets Tableau apart in the BI tool category. Here are some of the best examples i’ve seen. 

There’s a well-known Financial Times “visual vocabulary” infographic (linked in our Tableau guide). I found the author’s Tableau version which is excellent. Here are a few pages out of the larger guide:

a. Change over Time


b. Distribution


c. Deviation


Another user compiled a massive collection of examples of the “visual vocabulary” styles. So many that I need to rotate the screenshot sideways to fit. 


 

Bar chart design guide – a library of really cool, specialized bar chart sub-types: 


20 KPI Box Examples – functional – a good reference to have on hand for simpler KPI box styles.

Ruben Martinez’s profile features a fantastic series of ~20 “Mastering Tableau” guides, including:

a. Color encoding – effective use of color cues 


b. The KPI Lineup – a variety of visually satisfying KPI layouts  


Yet more KPI frameworks: 10 Commandments of Big Numbers 

Big Numbers framework via linkedin Post

Put into Tableau practice by a different author

The great thing about the Tableau Public Gallery is that you can make a copy of any of these expert’s workbooks, and open an editable version of your own. This enables reverse engineering these visualizations, including copying their table calculations!

 

 

Click “make a copy”
 

Directly access the formulae powering the visual elements
So many great opportunities to learn from the best visualization designers in the Tableau community. Enjoy!

 
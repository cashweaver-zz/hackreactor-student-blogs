# Organize the README file
import re
from string import Template

print '# Hack Reactor Student Blogs'
print ''
print 'Personal blogs of [Hack Reactor](http://www.hackreactor.com) students.'

blogs = {}
cur_year = ''
cur_cohort = ''
with open('README.md') as f:
    content = f.readlines()

    for line in content:
        year = re.match('^## ([0-9]+)$', line)
        cohort = re.match('^### (.+)$', line)
        blog = re.match('^- \[([^\]]+)\]\(([^\)]+)\)', line)
        if year:
            cur_year = year.group(1)
            blogs[cur_year] = {}
        elif cohort:
            cur_cohort = cohort.group(1)
            blogs[cur_year][cur_cohort] = []
        elif blog:
            blogs[cur_year][cur_cohort].append({'name': blog.group(1), 'url': blog.group(2)})

year_template = Template('\n## $year')
cohort_template = Template('\n### $cohort\n')
blog_template = Template('- [$name]($url)')
for year in blogs:
    print year_template.substitute(year=year)
    for cohort in blogs[year]:
        print cohort_template.substitute(cohort=cohort)
        for blog in sorted(blogs[year][cohort], key=lambda blog: blog['name']):
            print blog_template.substitute(name=blog['name'], url=blog['url'])

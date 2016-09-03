# Organize the README file
import re
import requests
from datetime import datetime
from string import Template

print '# Hack Reactor Student Blogs'
print ''
print 'Personal blogs of [Hack Reactor](http://www.hackreactor.com) students.'
print ''
print '|Tag | Description|'
print '|---|---|'
print "|sf | Hack Reactor's San Francisco office|"
print "|remote | Hack Reactor's remote program|"
print '|hir | Hacker in Residence|'

blogs = {}
cur_year = ''
cur_cohort = ''
with open('README.md') as f:
    content = f.readlines()

    for line in content:
        year = re.match('^## ([0-9]+)$', line)
        cohort = re.match('^### (.+)$', line)
        blog = re.match('^- \[([^\]]+)\]\(([^\)]+)\) \[([^\]]+)\]', line)
        if year:
            cur_year = year.group(1)
            blogs[cur_year] = {}
        elif cohort:
            cur_cohort = cohort.group(1)
            blogs[cur_year][cur_cohort] = []
        elif blog:
            blogs[cur_year][cur_cohort].append({'name': blog.group(1), 'url': blog.group(2), 'tags': blog.group(3)})

year_template = Template('\n## $year')
cohort_template = Template('\n### $cohort\n')
blog_template = Template('- [$name]($url) [$tags]')
for year in reversed(sorted(blogs)):
    print year_template.substitute(year=year)
    for cohort in reversed(sorted(blogs[year], key=lambda month: datetime.strptime(month, '%B'))):
        print cohort_template.substitute(cohort=cohort)
        for blog in sorted(blogs[year][cohort], key=lambda blog: blog['name']):
            # ref: http://stackoverflow.com/a/13641613
            try:
                r = requests.head(blog['url'])
                if r.status_code != 404:
                    print blog_template.substitute(name=blog['name'], url=blog['url'], tags=blog['tags'])
                # prints the int of the status code. Find more at httpstatusrappers.com :)
            except requests.ConnectionError as e:
                pass

from html.parser import HTMLParser
from urllib.request import Request,urlopen
from datetime import date,timedelta
from pathlib import Path
from xml.sax.saxutils import escape
import re
class Calendar(HTMLParser):
 def __init__(self):super().__init__();self.days={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('data-date') and a.get('data-level') is not None:
   self.days[a['data-date']]=int(a['data-level'])
def render(days,dark):
 bg,fg,mut,colors=('#12282b','#e3eee2','#acc6bb',['#203a3b','#315c49','#488b62','#6bb77d','#a4e3ac']) if dark else ('#faf8f0','#173c35','#526c65',['#e5ebe1','#c5dfbf','#8fc58e','#519d6b','#28654e'])
 dates=sorted(days);start=date.fromisoformat(dates[0]);start-=timedelta(days=(start.weekday()+1)%7)
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 260" role="img"><title>GitHub contribution activity from {dates[0]} to {dates[-1]}</title><style>text{{font-family:monospace}}@media(prefers-reduced-motion:reduce){{.sweep{{display:none}}}}</style><rect width="1000" height="260" rx="8" fill="{bg}"/><text x="24" y="33" fill="{mut}" font-size="13">FIELD NOTES / CONTRIBUTIONS</text><text x="24" y="63" fill="{fg}" font-size="24" font-weight="bold">BUILD. TEST. REPEAT.</text>']
 rects=[]
 for d,level in sorted(days.items()):
  offset=(date.fromisoformat(d)-start).days;x=24+offset//7*18;y=88+offset%7*18
  shape=f'<rect x="{x}" y="{y}" width="14" height="14" rx="2"'
  out.append(shape+f' fill="{colors[level]}"><title>{d}: activity level {level} of 4</title></rect>');rects.append(shape+'/>')
 out.append('<defs><clipPath id="cells">'+''.join(rects)+'</clipPath><linearGradient id="glow"><stop stop-color="#91ffc0" stop-opacity="0"/><stop offset=".7" stop-color="#91ffc0" stop-opacity=".65"/><stop offset="1" stop-color="#e3ffec" stop-opacity="0"/></linearGradient></defs>')
 out.append('<g clip-path="url(#cells)" class="sweep"><rect x="-140" y="85" width="140" height="132" fill="url(#glow)"><animate attributeName="x" values="-140;1000;1000" keyTimes="0;.85;1" dur="7s" repeatCount="indefinite"/></rect></g>')
 out.append(f'<text x="24" y="242" fill="{mut}" font-size="12">{dates[0]} — {dates[-1]} · GitHub activity snapshot</text></svg>')
 return ''.join(out)
def main():
 req=Request('https://github.com/users/umair-aziz025/contributions',headers={'User-Agent':'profile-contribution-panel'})
 html=urlopen(req,timeout=30).read().decode();p=Calendar();p.feed(html)
 if len(p.days)<350 or any(v not in range(5) for v in p.days.values()):raise ValueError('Incomplete contribution data; keeping previous panel')
 path=Path('assets/contributions');path.mkdir(parents=True,exist_ok=True)
 for dark in [False,True]:(path/('activity-'+('dark' if dark else 'light')+'.svg')).write_text(render(p.days,dark))
 readme=Path('README.md');md=readme.read_text();marker='<!-- contribution-panel -->'
 if marker not in md:
  md+='\n'+marker+'\n\n## Contribution activity\n\n<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/contributions/activity-dark.svg"><img src="./assets/contributions/activity-light.svg" width="100%" alt="GitHub contribution activity with a green light sweeping across the calendar."></picture>\n'
  readme.write_text(md)
 print(f'Rendered {len(p.days)} actual contribution days.')
if __name__=='__main__':main()

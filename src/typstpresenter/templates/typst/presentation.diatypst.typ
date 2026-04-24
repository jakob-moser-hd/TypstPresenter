#import "@preview/diatypst:0.9.1": *
#show: slides.with(
  title: [{{ presentation.title | express }}],
  toc: false
)

#set heading(numbering: none)

{% for slide in presentation %}
== {{ slide.title | express }}

{% for content in slide.contents %}
{{ content | express }}

{% endfor %}
{% endfor %}

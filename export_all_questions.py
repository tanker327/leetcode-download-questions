import requests
import json
from types import SimpleNamespace
from weasyprint import HTML

baseJSON = {
    "operationName": "questionData",
    "variables": {
        "titleSlug": "PLACEHOLDER"
    },
    "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    exampleTestcases\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      paidOnly\n      hasVideoSolution\n      paidOnlyVideo\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    enableDebugger\n    envInfo\n    libraryUrl\n    adminUrl\n    __typename\n  }\n}\n"
}

graphQLEndpoint = 'https://leetcode.com/graphql'

htmlstr = '<div>'
htmlstr += '<style> @page { size: letter portrait; margin: 1cm; }\n * { word-wrap: break-word; } pre { white-space: pre-wrap; } body { font-size: 12px} </style>'

def update_question_links(question_links):
  with open('top-interview-150') as f:
    links =  f.read()

  links = links.split('\n')

  for each in links:
    question_links.append(each)

def get_section(section_text):
  global htmlstr
  htmlstr += '<div>'
  htmlstr += f'<h1>{section_text[1:]}</h1>'
  htmlstr += '</div>'
  htmlstr += '<p style="page-break-before: always" ></p>'

def get_question(question_link):
  slug = question_link.split('https://leetcode.com/problems/', 1)[1]
  baseJSON['variables']['titleSlug'] = slug
  resp = requests.get(graphQLEndpoint, json=baseJSON)

  x = json.loads(resp.text, object_hook=lambda d: SimpleNamespace(**d))

  global htmlstr
  htmlstr += '<div>'
  htmlstr += f'<h2>{x.data.question.title}</h2>'
  htmlstr += x.data.question.content 
  htmlstr += '</div>'
  htmlstr += '<p style="page-break-before: always" ></p>'

def main():
  question_links = []
  update_question_links(question_links)
  for line in question_links:
    try:
      if line[0] == '~':
        get_section(line)
      else:
        get_question(line)
      
      print(line)
      print('------------------------------')

    except:
      continue
  
  global htmlstr
  htmlstr += '</div>'
  HTML(string=htmlstr).write_pdf('top-interview-150.pdf')


if __name__=='__main__':
  print('\n')
  main()
  

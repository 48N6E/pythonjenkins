# 试图相关

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2018/1/17


import jenkins

server = jenkins.Jenkins('http://192.168.30.36:8080', username="admin", password="d2e735dd39e64a4381da1d6f04795b9c")
params = {'Branch': 'oriin/master', 'host': '192.168.1.110'}

print(server.get_views())
'''
[{'_class': 'hudson.model.AllView', 'name': 'all', 'url': 'http://127.0.0.1:8080/'}, {'_class': 'hudson.model.ListView', 'name': 'myview', 'url': 'http://127.0.0.1:8080/view/myview/'}]
'''

# CURD VIEW
server.view_exists()
server.create_view('EMPTY', jenkins.EMPTY_VIEW_CONFIG_XML)
views = server.get_views()
server.delete_view('EMPTY')
server.reconfig_view('newview',jenkins.EMPTY_VIEW_CONFIG_XML)
server.get_view_name('EMPTY')
view_config = server.get_view_config('EMPTY')
# 获取试图下所有的job
print(server._get_view_jobs('myview'))

# 试图配置信息
print(server.get_view_config('myview'))
'''
<?xml version="1.0" encoding="UTF-8"?>
<hudson.model.ListView>
  <name>myview</name>
  <description>测试试图</description>
  <filterExecutors>false</filterExecutors>
  <filterQueue>false</filterQueue>
  <properties class="hudson.model.View$PropertyList"/>
  <jobNames>
    <comparator class="hudson.util.CaseInsensitiveComparator"/>
    <string>ansible-playbook</string>
    <string>my-github</string>
  </jobNames>
  <jobFilters/>
  <columns>
    <hudson.views.StatusColumn/>
    <hudson.views.WeatherColumn/>
    <hudson.views.JobColumn/>
    <hudson.views.LastSuccessColumn/>
    <hudson.views.LastDurationColumn/>
    <hudson.views.BuildButtonColumn/>
    <hudson.plugins.git.GitBranchSpecifierColumn plugin="git@3.7.0"/>
  </columns>
  <recurse>false</recurse>
</hudson.model.ListView>
'''
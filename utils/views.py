import jenkins
from utils.logger import logger
import os
from exception.playerror import DeployError

#显示多少个视图
def viewsCount(server):
    print(len(server.get_views()))

#显示试图下的job
def showView(viewname):
    print("Get Job信息: {}".format(server._get_view_jobs(viewname)))


#创建视图
def createView(sever,viewname,configxml = jenkins.EMPTY_VIEW_CONFIG_XML):
    if server.view_exists(viewname):
        logger.error("viewname %s 已经存在"% viewname)
    else:
        server.create_view(viewname, configxml)
        logger.flow("%s view 创建成功"% viewname)


#删除项目
def delView(server,viewname):
    if server.job_exists(viewname):
        server.delete_view(viewname)
        logger.success("%s view 删除成功"% viewname)
    else:
        logger.error(" %s 不存在" % viewname)


#获取试图配置信息
def readViewConfig(server,viewname):
    try:
        logger.flow(server.get_view_config(viewname))
    except Exception as e:
        logger.error("视图不存在 %s"% e )
    desktop_path = os.path.abspath(os.path.pardir) + '\\pythonjenkins\\file\\'
    full_path = desktop_path + viewname
    file = open(full_path, 'w',encoding="utf-8")
    file.write(server.get_view_config(viewname))

#往视图里添加job
def addViewJob(viewname,jobname):
    old_string = 'mparator class="hudson.util.CaseInsensitiveComparator"/>'
    new_string = ('mparator class="hudson.util.CaseInsensitiveComparator"/>' +
              '\n    ' +
              '<string>%s</string>'% jobname)

    content = server.get_view_config(viewname)
    if  jobname not in content:
        new_content = content.replace(old_string, new_string).replace('\r', '')
        with open(os.path.abspath(os.path.pardir) + '\\pythonjenkins\\file\\%s'% viewname,'w') as newfile:
            newfile.write(new_content)
    else:
        raise ("job 已经存在")

    with open(os.path.abspath(os.path.pardir) + '\\pythonjenkins\\file\\%s' % viewname, 'r') as newfile:
        new_config = newfile.read()
        server.reconfig_view(viewname, new_config)
        logger.flow("%s 已经添加到 %s " % (jobname,viewname))


#视图里删除job
def delViewJob(viewname,jobname):
    old_string = ('<string>%s</string>'% jobname)
    new_string = ''
    content = server.get_view_config(viewname)
    if jobname in content:
        new_content = content.replace(old_string, new_string).replace('\r', '')
        with open(os.path.abspath(os.path.pardir) + '\\pythonjenkins\\file\\%s' % viewname, 'w') as newfile:
            newfile.write(new_content)
    else:
        logger.error("job 不存在")

    with open(os.path.abspath(os.path.pardir) + '\\pythonjenkins\\file\\%s' % viewname, 'r') as newfile:
        new_config = newfile.read()
        server.reconfig_view(viewname, new_config)
        logger.flow("%s 已经从 %s 删除" % (jobname,viewname))

#复制视图
def copyView(viewname,newname):
    old_string = ('<name>%s</name>'% viewname)
    new_string = ('<name>%s</name>'% newname)
    content = server.get_view_config(viewname)
    if not server.view_exists(viewname):
        new_content = content.replace(old_string, new_string).replace('\r', '')
        with open(os.path.abspath(os.path.pardir) + '\\pythonjenkins\\file\\%s' % viewname, 'w') as newfile:
            newfile.write(new_content)
    else:
        logger.error("%s 不存在"% viewname)
    try:
        with open(os.path.abspath(os.path.pardir) + '\\pythonjenkins\\file\\%s' % viewname, 'r') as newfile:
            new_config = newfile.read()
            server.create_view(newname, new_config)
            logger.flow("%s 已经基于 %s copy成功" % (newname,viewname))
    except Exception as e :
        logger.error("%s 已经存在" % newname)

if __name__ == '__main__':
    server = jenkins.Jenkins('http://192.168.30.36:8080', username="ops.admin", password="11+456+")
    viewsCount(server)
    showView("all")
    #readViewConfig(server,"test")
    #reateView(server,"test")
    #delView(server,"test")
    addViewJob("test","10-nginx")
    delViewJob('test','10-nginx')
    copyView('test','test1')
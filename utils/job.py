import jenkins
from utils.logger import logger
from exception.playerror import DeployError
import os

#显示多少个项目
def showJobs(server):
    #print("job数量:%s" % server.jobs_count())
    logger.flow("job数量:%s" % server.jobs_count())
    all_jobs_li = server.get_all_jobs()
    for item in all_jobs_li:
        print('name: %s' % item['name'], 'URL: ', item['url'])


#显示项目详细信息
def showJobDetail(jobname):
    print("DEBUG Job信息: {}".format(server.debug_job_info(jobname)))

    print("Get Job信息: {}".format(server.get_job_info(jobname)))


#创建项目
def createJob(sever,jobname):
    if server.job_exists(jobname):
        logger.flow("jobname %s 已经存在"% jobname)
    else:
        server.create_job(jobname, jenkins.RECONFIG_XML)

#删除项目
def delJob(server,jobname):
    if server.job_exists(jobname):
        server.create_job(jobname, jenkins.RECONFIG_XML)
    else:
        logger.error("cbname %s 不存在" % jobname)


#复制项目
def copyJob(jobname,tocopyname):
    try:
        server.copy_job(jobname,tocopyname)
    except  Exception as e:
        logger.error("复制失败 %s"% e)

#构建项目
def buildJob(jobname,server,params):
    try:
        print(server.build_job_url(jobname))
        logger.success("构建成功 %s "% jobname )
    except Exception as e:
        logger.error("构建失败 %s"% e )

    # # 触发Job(方式二)
    server.build_job(jobname, parameters=params)

#获取项目配置信息
def readJobConfig(server,jobname):
    try:
        logger.flow(server.get_job_config(jobname))
    except Exception as e:
        logger.error("项目不存在 %s"% e )
    desktop_path = os.path.abspath(os.path.pardir) + '\\file\\'
    full_path = desktop_path + jobname
    file = open(full_path, 'w',encoding="utf-8")
    file.write(server.get_job_config(jobname))

#修改job分配的构建主机
def mdassignednodeJob(jobname,oldassignednode,newassignednode):
    old_string = '<assignedNode>%s</assignedNode>'% oldassignednode
    new_string = ('<assignedNode>%s</assignedNode>'% newassignednode)

    content = server.get_job_config(jobname)
    if  newassignednode not in content:
        new_content = content.replace(old_string, new_string).replace('\r', '')
        with open(os.path.abspath(os.path.pardir) + '\\file\\%s'% jobname,'w') as newfile:
            newfile.write(new_content)
    else:
        raise ("节点分配正确，无需更改")

    with open(os.path.abspath(os.path.pardir) + '\\file\\%s' % jobname, 'r') as newfile:
        new_config = newfile.read()
        server.reconfig_job(jobname, new_config)
        logger.flow("%s 已经分配到 %s " % (jobname,newassignednode))

#显示所有项目,按照分配节点
def showJob(assignednode):
    all_jobs_li = server.get_all_jobs()
    all_jobs = []
    assignednode_jobs = []
    for job in all_jobs_li:
        all_jobs.append(job['name'])
    oldassignednode= '<assignedNode>%s</assignedNode>' % assignednode
    for i in all_jobs:
        content = server.get_job_config(i)
        if oldassignednode in  content:
            assignednode_jobs.append(i)
    return assignednode_jobs

#显示所有项目,按照配置内容
def showcontextJob(context):
    all_jobs_li = server.get_all_jobs()
    all_jobs = []
    assignednode_jobs = []
    for job in all_jobs_li:
        all_jobs.append(job['name'])
    context= '%s' % context
    for i in all_jobs:
        content = server.get_job_config(i)
        if context in  content:
            assignednode_jobs.append(i)
    print(assignednode_jobs)



#批量修改分配主机
def allmodassignednodeJob(server,oldassignednode,newassignednode):
    old_string = '<assignedNode>%s</assignedNode>'% oldassignednode
    new_string = ('<assignedNode>%s</assignedNode>'% newassignednode)
    for jobname in showJob(oldassignednode):
        # 获取所有分配节点是jenkins-k8s的主机
        content = server.get_job_config(jobname)
        new_content = content.replace(old_string, new_string).replace('\r', '')
        with open(os.path.abspath(os.path.pardir) + '\\file\\%s' % jobname, 'w') as newfile:
            newfile.write(new_content)
            try:
                server.reconfig_job(jobname, new_content)
                logger.flow("%s 已经分配到 %s " % (jobname, newassignednode))
            except Exception as e:
                print(e)

    # for jobname in showJob(oldassignednode):
    #     with open(os.path.abspath(os.path.pardir) + '\\file\\%s' % jobname, 'r') as newfile:
    #         new_config = newfile.read()
    #         server.reconfig_job(jobname, new_config)
    #         logger.flow("%s 已经分配到 %s " % (jobname, newassignednode))

if __name__ == '__main__':
    server = jenkins.Jenkins('http://jenkins.hgj.net/', username="ops.admin", password="Yunlsp123+456+")
    #params = {'one': 'oriin/master', 'two': '192.168.30.36'}
    #showJobs(server)
    #showJobDetail('test')
    #readJobConfig(server,'python-wechat-helper')
    showcontextJob("构建前")
    #mdassignednodeJob('whale-user-demo17','jenkins-k8s','jenkins-k8s2')
    #allmodassignednodeJob(server,'jenkins-k8s','jenkins-k8s2')

    #createJob(server,'test')
    #delJob(server,'myjob')
    #copyJob('my-gi11th1ub', 'copy-my-github')
    #params = {'two': 'oriin/master', 'one': '192.168.1.110'}
   # buildJob("test",server,params)



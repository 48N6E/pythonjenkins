import jenkins
from utils.logger import logger
from exception.playerror import DeployError


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



if __name__ == '__main__':
    server = jenkins.Jenkins('http://192.168.30.36:8080', username="ops.admin", password="123+456+")
    params = {'one': 'oriin/master', 'two': '192.168.30.36'}
    showJobs(server)
    showJobDetail('test')
    createJob(server,'test')
    #delJob(server,'myjob')
    #copyJob('my-gi11th1ub', 'copy-my-github')
    #params = {'two': 'oriin/master', 'one': '192.168.1.110'}
   # buildJob("test",server,params)



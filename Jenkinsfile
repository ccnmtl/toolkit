
TAG = 'build-' + env.BUILD_NUMBER
env.TAG = TAG

// check for required parameters. assign them to the env for
// convenience and make sure that an exception is raised if any
// are missing as a side-effect

env.ENV = ENV
env.APP = APP
env.REPO = REPO
env.CONFIG_PATH = CONFIG_PATH

def server_hosts = EC2_HOSTS.split(" ")
def checkoutDir
def jobsDbHost
def jobsDbUser
def jobsDbPassword
def jobsDbDbName
def jobsDbPort
def workspaceToken

def err = null
currentBuild.result = "SUCCESS"

try {
    node {
        options {
            timeout(time:5, units: 'MINUTES')
        }
        stage 'Checkout'
        checkout scm
        checkoutDir = pwd()
        jobsDbHost = getAwsParameter("/${env.ENV}/postgresql/DATABASE_HOST")
        // jobsDbHost = 'db' // This is using docker compose for the postgres db container
        jobsDbUser = getAwsParameter("/${env.ENV}/toolkit/POSTGRES_USER")
        jobsDbPassword = getAwsParameter("/${env.ENV}/toolkit/POSTGRES_PASSWORD")
        jobsDbPort = 5432
        // jobsDbPort = 7432 // This is using docker compose for the postgres db container
        // jobsDbDbName = getAwsParameter("/${env.ENV}/toolkit/JOBS_DB_NAME")
        jobsDbDbName = 'toolkit' // This is using docker compose for the postgres db container
        SENTRY_DSN = getAwsParameter("/${env.ENV}/toolkit/SENTRY_DSN")
        SENTRY_KEY = getAwsParameter("/${env.ENV}/toolkit/SENTRY_KEY")
        stage 'Generate .env file'
        sh """
            echo TAG=${env.TAG} > .env
            echo ENV=${env.ENV} >> .env
            echo POSTGRES_USER=${jobsDbUser} >> .env
            echo POSTGRES_PASSWORD=${jobsDbPassword} >> .env
            echo POSTGRES_DB=${jobsDbDbName} >> .env
            echo JOBS_DB_HOST=${jobsDbHost} >> .env
            echo JOBS_DB_USER=${jobsDbUser} >> .env
            echo JOBS_DB_PASSWORD=${jobsDbPassword} >> .env
            echo JOBS_DB_DB_NAME=${jobsDbDbName} >> .env
            echo JOBS_DB_PORT=${jobsDbPort} >> .env
            echo CONFIG_PATH=${env.CONFIG_PATH} >> .env
            echo SENTRY_DSN=${SENTRY_DSN} >> .env
            echo SENTRY_KEY=${SENTRY_KEY} >> .env
        """
        def branches = [:]
        stage "Copy files to host"

        for (int i = 0; i < server_hosts.size(); i++) {
            branches["copy-files-to-host-${i}"] = copy_files_to_host(i, server_hosts[i], checkoutDir)
        }
        parallel branches
        stage "Restart Docker compose"
        branches = [:]
        for (int i = 0; i < server_hosts.size(); i++) {
            branches["docker-compose-${i}"] = restart_docker_compose(i, server_hosts[i])
        }
        parallel branches
    }

} catch (caughtError) {
    err = caughtError
    currentBuild.result = "FAILURE"
} finally {
    (currentBuild.result != "ABORTED") && node {
        notifyBuild(currentBuild.result)
    }

    /* Must re-throw exception to propagate error */
        if (err) {
        throw err
    }
}

// -------------------- helper functions ----------------------

def notifyBuild(String buildStatus = 'STARTED') {
    // build status of null means successful
    buildStatus =  buildStatus ?: 'SUCCESS'

    // Default values
    def colorCode = '#FF0000'
    def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
    def summary = "${subject} (${env.BUILD_URL})"
    def details = """<p>STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>"""

    // Override default values based on build status
    if (buildStatus == 'STARTED') {
        color = 'YELLOW'
        colorCode = '#FFFF00'
    } else if (buildStatus == 'SUCCESS') {
        color = 'GREEN'
        colorCode = '#36a64f'
    } else {
        color = 'RED'
        colorCode = '#FF0000'
    }

    // Send notifications
    //  slackSend (color: colorCode, message: summary)

    // step([$class: 'Mailer',
    //         notifyEveryUnstableBuild: true,
    //         recipients: ADMIN_EMAIL,
    //         sendToIndividuals: true])
}

def copy_files_to_host(int i, String host, String checkoutDir) {
    cmd = {
        node {
            sh """
            scp -r ${checkoutDir}/.env ${host}:/var/www/${APP}/.env
            scp -r ${checkoutDir}/* ${host}:/var/www/${APP}
            """
        }
    }
    return cmd
}

def restart_docker_compose(int i, String host) {
    cmd = {
        node {
            sh """
            ssh ${host} "cd /var/www/${APP} && docker compose -f toolkit-docker-${env.ENV}.yml down || true"
            ssh ${host} "cd /var/www/${APP} && docker compose -f toolkit-docker-${env.ENV}.yml up -d"
            """
        }
    }
    return cmd
}

def getAwsParameter(String name) {
    return sh(script: "aws ssm get-parameter --name ${name} --with-decryption --query \"Parameter.Value\" --output text", returnStdout: true).trim()
}

// retry with exponential backoff
def retry_backoff(int max_attempts, Closure c) {
    int n = 0
    while (n < max_attempts) {
        try {
            c()
            return
        } catch (err) {
            if ((n + 1) >= max_attempts) {
                // we're done. re-raise the exception
                throw err
            }
            sleep(2**n)
            n++
            }
    }
    return
}
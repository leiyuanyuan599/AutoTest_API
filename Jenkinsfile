pipeline {
    agent any

    environment {
        REPORT_DIR = "reports/allure-report"
        RESULTS_DIR = "reports/allure-results"
        PYTHON_ENV = "venv"

        // Jenkins凭证ID（请先在Jenkins Credential里添加）
        FEISHU_WEBHOOK = credentials('feishu_webhook')
        DING_WEBHOOK = credentials('ding_webhook')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Env') {
            steps {
                sh '''
                python3 -m venv ${PYTHON_ENV}
                . ${PYTHON_ENV}/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                sh '''
                . ${PYTHON_ENV}/bin/activate
                pytest --alluredir=${RESULTS_DIR} --maxfail=3 --disable-warnings -q
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                . ${PYTHON_ENV}/bin/activate
                allure generate ${RESULTS_DIR} -o ${REPORT_DIR} --clean
                '''
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    reportName: 'Pytest Allure Report',
                    reportDir: "${REPORT_DIR}",
                    reportFiles: 'index.html',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: false
                ])
            }
        }
    }

    post {
        success {
            script {
                def reportUrl = "${env.BUILD_URL}allure"
                def msg = """✅ Pytest自动化测试成功
项目：${env.JOB_NAME}
构建编号：#${env.BUILD_NUMBER}
报告链接：${reportUrl}
"""

                // 邮件通知
                emailext(
                    subject: "✅【成功】Pytest测试报告 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: msg,
                    to: "qa-team@yourcompany.com"
                )

                // 飞书通知
                httpRequest(
                    httpMode: 'POST',
                    contentType: 'APPLICATION_JSON',
                    requestBody: """{
                        "msg_type": "text",
                        "content": {"text": "${msg}"}
                    }""",
                    url: "${FEISHU_WEBHOOK}"
                )

                // 钉钉通知
                httpRequest(
                    httpMode: 'POST',
                    contentType: 'APPLICATION_JSON',
                    requestBody: """{
                        "msgtype": "text",
                        "text": {"content": "${msg}"}
                    }""",
                    url: "${DING_WEBHOOK}"
                )
            }
        }

        failure {
            script {
                def reportUrl = "${env.BUILD_URL}allure"
                def msg = """❌ Pytest自动化测试失败
项目：${env.JOB_NAME}
构建编号：#${env.BUILD_NUMBER}
报告链接：${reportUrl}
请检查Jenkins日志和测试报告。
"""

                emailext(
                    subject: "❌【失败】Pytest测试报告 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                    body: msg,
                    to: "qa-team@yourcompany.com"
                )

                httpRequest(
                    httpMode: 'POST',
                    contentType: 'APPLICATION_JSON',
                    requestBody: """{
                        "msg_type": "text",
                        "content": {"text": "${msg}"}
                    }""",
                    url: "${FEISHU_WEBHOOK}"
                )
            }
        }
    }
}

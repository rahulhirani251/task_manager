
def run(String cmd) {
    if (isUnix()) {
        sh cmd
    } else {
        bat cmd
    }
}

def venvPython() {
    return isUnix() ? '.venv/bin/python' : '.venv\\Scripts\\python'
}

pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        APP_ENV = 'testing'
    }

    stages {
        stage('Build') {
            options {
                timeout(time: 6, unit: 'MINUTES')
            }
            steps {
                echo 'Dependencies install ho rahi hain...'
                script {
                    if (isUnix()) {
                        run('python3 -m venv .venv')
                    } else {
                        run('python -m venv .venv')
                    }
                    // Timeout aur retries: network atke to build hamesha ke liye latki na rahe
                    run("${venvPython()} -m pip install --disable-pip-version-check --default-timeout=60 --retries 5 -r requirements.txt")
                    run("${venvPython()} -m py_compile app.py")
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Tests chal rahe hain...'
                script {
                    run("${venvPython()} -m pytest -v --junitxml=test-results.xml")
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Deploy') {
            // Sirf main branch se deploy hoga
            when {
                anyOf {
                    branch 'main'
                    expression { env.GIT_BRANCH == 'origin/main' }
                }
            }
            options {
                timeout(time: 3, unit: 'MINUTES')
            }
            steps {
                echo 'Local deploy: app production mode mein start karke check ho rahi hai...'
                script {
                    run("${venvPython()} deploy_check.py")
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful: Build, Test aur Deploy complete.'
        }
        failure {
            echo 'Pipeline fail ho gayi, console output check karo.'
        }
    }
}
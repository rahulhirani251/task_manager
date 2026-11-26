// Cross-platform: Windows (bat) aur Linux/Mac (sh) dono par chalta hai

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

    // Local Jenkins ko GitHub webhook nahi mil sakta, isliye har 2 minute mein repo check hoga
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
            steps {
                echo 'Deploy ho raha hai...'
                script {
                    try {
                        // Jenkins > Credentials mein "Secret text", ID: render-deploy-hook
                        withCredentials([string(credentialsId: 'render-deploy-hook', variable: 'DEPLOY_HOOK')]) {
                            if (isUnix()) {
                                sh 'curl -fsS -X POST "$DEPLOY_HOOK"'
                            } else {
                                bat 'curl -fsS -X POST "%DEPLOY_HOOK%"'
                            }
                        }
                    } catch (err) {
                        echo "Deploy hook available nahi ya fail hua: ${err.getMessage()}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline successful: Build, Test aur Deploy complete.'
        }
        unstable {
            echo 'Build aur Test pass, lekin Deploy complete nahi hua (deploy hook check karo).'
        }
        failure {
            echo 'Pipeline fail ho gayi, console output check karo.'
        }
    }
}
